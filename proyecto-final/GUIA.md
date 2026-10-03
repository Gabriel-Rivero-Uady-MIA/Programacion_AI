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
con los de las reseñas para recuperar textos de significado parecido.

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

### Pasar de tres textos al dataset

Sustituye `example_texts` por `texts` y utiliza el tamaño de lote de la configuración.
Con los archivos de esta categoría obtendrás **16 205 filas y 384 columnas**:
una fila por reseña con texto. Cada fila conserva su posición en `review_ids`.

Haz esta preparación una vez, antes de atender consultas. Puedes mantener modelo,
matriz y registros en memoria; guardarlos en disco es opcional. Cambiar `top_k`
o recibir otra consulta no requiere volver a codificar todas las reseñas.

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
con todas las filas de la matriz. La consulta se codifica en cada llamada; las
reseñas se reutilizan. Si trabajas con NumPy, puedes convertir los tensores de CPU
con `.cpu().numpy()` y continuar allí.

## 4. Implementar búsqueda y análisis

Dentro de `search_reviews`, sigue este recorrido:

1. Valida la consulta y `top_k` según el enunciado.
2. Codifica la consulta con el modelo ya cargado.
3. Calcula un puntaje por reseña: el producto de la matriz normalizada por el
   vector normalizado de la consulta. Para el dataset, `(16205, 384) @ (384,)`
   produce `(16205,)`. Evita comparar todas las reseñas entre sí.
4. Selecciona las posiciones con mayor puntaje usando `torch.topk` o
   `np.argsort` en orden descendente. Limita la cantidad al número de candidatos.
5. Recupera las reseñas originales mediante esas posiciones e IDs y devuelve
   ID, texto, producto, valoración y similitud como valores de Python.

En el ejemplo de tres textos, una consulta sobre retrasos de entrega debería
recuperar primero el texto del paquete. Observa las posiciones, además de los
puntajes, para reconocer cómo se recupera el registro correcto. La puntuación
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
