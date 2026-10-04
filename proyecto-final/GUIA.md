# Guía de desarrollo

Consulta el [README](./README.md) para el alcance y los entregables.

## 1. Crear el entorno y explorar los datos

Crea una carpeta propia y ejecuta:

```bash
uv init
uv add numpy torch sentence-transformers "mcp>=2,<3"
uv add --dev mypy pandas matplotlib ipykernel
```

Copia la [notebook](./preparacion_datos.ipynb) y [config.json](./config.json) a tu
proyecto. Abre la notebook en VS Code o PyCharm con el intérprete de `.venv` y
ejecútala en orden. Reconoce IDs, valoraciones, textos vacíos y tamaños de muestra.

## 2. Preparar los datos y el modelo

Adapta las funciones de lectura de la notebook y conserva sus IDs de reseña.
Carga los valores de `config.json`: modelo, tamaño del lote y dispositivo.
Comprueba que el nombre no esté vacío y que el tamaño de lote sea un entero positivo.
Puedes usar un modelo Pydantic para validar esta configuración.

Como organización posible, `support/data.py` puede reunir lectura,
`support/settings.py` configuración y `support/encoder.py` codificación. También
puedes concentrar el código en `server.py`.

## 3. Generar los embeddings para la búsqueda

Un embedding es un vector que representa un texto. Con este modelo, cada reseña
produce **384 números**. La consulta se convierte en otro vector y se compara
con una representación de cada producto. Combinaremos lo que ofrece el catálogo
con lo que cuentan sus clientes.

### Seleccionar los textos y conservar su orden

Retoma `texts`, `review_ids` y `searchable_reviews` de la última sección de la
[notebook de preparación](./preparacion_datos.ipynb). Los textos sin contenido se
excluyen de la búsqueda; conserva todas las reseñas para las estadísticas.

| Posición | ID de reseña | Texto | Vector |
|---|---|---|---|
| 0 | Primer ID de `review_ids` | `texts[0]` | Primera fila de la matriz |
| 1 | Segundo ID de `review_ids` | `texts[1]` | Segunda fila de la matriz |

No ordenes ni filtres una de estas listas por separado después de generar los
vectores. Cuando recuperes una posición, úsala para encontrar el ID y el registro
de esa misma reseña. No asumas que corresponde a la lista de todas las reseñas,
porque esa lista también incluye textos vacíos. Si conservas la selección como
DataFrame, recupera por posición con `.iloc[position]`; `.loc` busca por etiqueta
de índice y el filtrado puede haber dejado saltos en esas etiquetas.

### Empezar con tres textos

Este ejemplo aislado muestra la carga y la codificación. En tu aplicación,
obtén el nombre del modelo, dispositivo y tamaño del lote de `config.json`.

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2", device="cpu"
)
example_texts = [
    "The package arrived two weeks late.",
    "The coffee tastes fresh and delicious.",
    "Customer support answered my question quickly.",
]
review_vectors = model.encode(
    example_texts,
    batch_size=2,
    convert_to_tensor=True,
    normalize_embeddings=True,
)
print("Shape:", review_vectors.shape)  # torch.Size([3, 384])
```

`batch_size=2` procesa hasta dos textos por lote; el resultado contiene los tres,
en su orden original. `convert_to_tensor=True` devuelve un tensor PyTorch.
`normalize_embeddings=True` ajusta cada vector a longitud uno, lo que permite
calcular similitud coseno mediante producto escalar. Puedes normalizar los vectores
con PyTorch o NumPy por separado si prefieres seguir el ejemplo de clase.

La primera carga descarga el modelo. Las siguientes aprovechan su caché local.
Este modelo está orientado a inglés y trunca textos mayores de 256 tokens de su
tokenizador: utiliza consultas en inglés y menciona esta limitación en tu interpretación.

### Representar cada producto con catálogo y reseñas

El catálogo aporta `title` y una lista `features`. En estos archivos `description`
está vacío: utiliza **título + características** como texto de catálogo. Puedes
unir las características con `" ".join(features)` y añadir el título.

Prepara estas dos fuentes con el mismo modelo y `normalize_embeddings=True`:

| Fuente | Qué codificar | Qué conservar |
|---|---|---|
| Catálogo | Un texto de título y características por producto con texto. | ID del producto asociado a cada vector. |
| Reseñas | Cada reseña con texto, por separado. | ID de reseña e ID del producto asociado a cada fila. |

No concatenes todas las reseñas de un producto: el modelo truncaría el texto.
**Promedia sus vectores**, agrupando por `product_id`. Para un producto con tres
reseñas, la selección tiene forma `(3, 384)` y `mean(dim=0)` produce `(384,)`.
Este promedio resume temas de las opiniones; no calcula la valoración del producto.

El cálculo tiene tres pasos:

1. Obtén el vector normalizado del catálogo.
2. Promedia los vectores de las reseñas con texto de ese producto y normaliza el promedio.
3. Combina ambos con **50 % de cada fuente** y normaliza el resultado.

Ejemplo numérico aislado para comprender las operaciones:

```python
import torch
import torch.nn.functional as F

catalog_vector = F.normalize(torch.tensor([1.0, 0.0]), dim=0)
review_vectors_for_product = torch.tensor([[0.0, 1.0], [1.0, 0.0]])
review_average = review_vectors_for_product.mean(dim=0)
review_summary = F.normalize(review_average, dim=0)
product_vector = F.normalize(0.5 * catalog_vector + 0.5 * review_summary, dim=0)
print("Product vector:", product_vector)
```

Aquí usamos dos componentes para leer los números; los vectores reales tienen
384. Normalizar el promedio antes de combinar da el mismo peso a ambas fuentes,
independientemente de la longitud de ese promedio. Cada reseña aporta lo mismo;
no ponderes por estrellas ni por cantidad total de reseñas de otros productos.

Puedes recorrer los IDs de producto con un `for`, seleccionar las posiciones de
sus reseñas y calcular `mean(dim=0)`. Al terminar, reúne los vectores con
`torch.stack`. En NumPy, las operaciones equivalentes son `mean(axis=0)`,
normalización por longitud y `np.stack`.

**Si falta una fuente**, utiliza y normaliza la disponible. Un producto sin
catálogo puede usar sus reseñas; uno sin reseñas con texto puede usar el catálogo.
Si no hay texto en ninguna fuente, exclúyelo de la búsqueda, pero conserva sus
valoraciones para análisis.

Obtendrás una matriz final de **`(641, 384)`** y una lista `product_ids` en el
mismo orden. Estos archivos tienen 640 productos con texto de catálogo; el restante
se representa mediante sus reseñas. Conserva también el conteo total de reseñas
por producto, incluidas las que no tienen texto, para mostrarlo en los resultados.

Prepara esta matriz una vez al iniciar el servidor. Las reseñas y el catálogo se
codifican por lotes; la búsqueda compara solo los 641 vectores finales. Mantén
modelo, matriz y registros en memoria; guardarlos en disco es opcional.

### Codificar una consulta

Utiliza el mismo objeto `model` y la misma normalización:

```python
query = "My delivery arrived late."
query_vectors = model.encode(
    [query], convert_to_tensor=True, normalize_embeddings=True
)
query_vector = query_vectors[0]
print("Query shape:", query_vectors.shape)  # torch.Size([1, 384])
print("Vector shape:", query_vector.shape)  # torch.Size([384])
```

La lista `[query]` contiene un solo texto. `[0]` obtiene su vector para compararlo
con todas las filas de la matriz de productos. La consulta se codifica en cada
llamada; los vectores de productos se reutilizan. Si trabajas con NumPy, puedes convertir los tensores de CPU
con `.cpu().numpy()` y continuar allí.

## 4. Implementar búsqueda y análisis

Dentro de `search_products`, sigue este recorrido:

1. Valida la consulta y `top_k` según el enunciado.
2. Codifica la consulta con el modelo ya cargado.
3. Calcula un puntaje por producto: el producto de la matriz normalizada por el
   vector normalizado de la consulta. Para el dataset, `(641, 384) @ (384,)`
   produce `(641,)`.
4. Selecciona las posiciones con mayor puntaje usando `torch.topk` o
   `np.argsort` en orden descendente. Limita la cantidad al número de candidatos.
5. Recupera los productos mediante esas posiciones en `product_ids` y devuelve
   ID, título, similitud y conteo total de reseñas como valores de Python.

Prueba consultas de catálogo, como `"A box with games for couples"`, y consultas
de experiencias, como `"Problems with delivery and customer service"`. Revisa
los títulos de los productos recuperados y sus tamaños de muestra. La puntuación
mide similitud; no representa una probabilidad ni garantiza relevancia.

Para el análisis, selecciona las valoraciones del producto y calcula conteos,
proporciones, media y mediana. Incluye las reseñas sin texto. La comparación
reutiliza estos cálculos para los productos solicitados.

## 5. Conectar y demostrar

Sigue [MCP_HTTP.md](./MCP_HTTP.md) para registrar las herramientas y utilizar los
snippets de `client.py` y `main.py`. Prepara los datos antes de atender consultas,
sin volver a codificar todas las reseñas en cada llamada.

Ejecuta el servidor en una terminal y el cliente en otra. Revisa búsqueda, análisis,
comparación, producto desconocido y recuperación tras una entrada inválida.

## 6. Comprobar y entregar

Si toda tu implementación está en `server.py`:

```bash
uv run --locked mypy --strict server.py client.py main.py
```

Añade al comando cualquier otro archivo o módulo Python de la aplicación que
hayas creado. Conserva `uv.lock` y verifica `uv sync --locked` desde una copia
sin `.venv`. Documenta tus comandos y entrega únicamente los archivos necesarios
para ejecutar el trabajo, junto con la evidencia y explicación de resultados.

## Referencias para embeddings

- [Modelo y dimensiones](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).
- [Codificación y similitud de textos](https://www.sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html).
- [Parámetros de `encode`](https://www.sbert.net/docs/package_reference/sentence_transformer/SentenceTransformer.html).
