# Proyecto final: búsqueda y análisis de reseñas de Amazon con MCP

**Fecha límite: 19 de octubre de 2026.**

Construye un servidor MCP local para buscar reseñas y analizar productos de
**Amazon Reviews 2023, categoría Subscription Boxes**. Sus herramientas permitirán
consultar experiencias sobre entregas, contenido de las cajas y atención al cliente,
y comparar las valoraciones de los productos.

Utilizarás embeddings y operaciones vectorizadas con **PyTorch o NumPy**.
La demostración se realiza con un cliente Python por HTTP; **no necesitas crear
ni conectar un agente para probar o entregar el proyecto**.

## Material proporcionado

- [Notebook de preparación y exploración](./preparacion_datos.ipynb): descarga,
  lectura de JSONL y ejemplos con pandas y Matplotlib.
- [Guía de desarrollo](./GUIA.md): pasos para crear tu proyecto y trabajar con embeddings.
- [config.json](./config.json): configuración del modelo para incorporar a tu aplicación.
- [Guía HTTP y snippets de `client.py` y `main.py`](./MCP_HTTP.md): conexión y demostración.
- [Dataset](./DATASET.md): archivos oficiales, campos y alcance.

## Qué implementar

Crea tu proyecto con **`uv`** y trabaja con los archivos completos de reseñas y
metadatos. Adapta la lectura de la notebook, carga la configuración e implementa
la codificación de textos con `sentence-transformers/all-MiniLM-L6-v2`.

Genera los embeddings por lotes y conserva la correspondencia entre vectores e IDs
de reseña. Prepara los vectores una vez y reutilízalos en las consultas. Puedes
mantenerlos en memoria al iniciar el servidor o guardarlos para cargarlos después.
Utiliza el mismo modelo para las reseñas y las consultas; no necesitas entrenarlo.
La [guía de embeddings](./GUIA.md#3-generar-los-embeddings-para-la-búsqueda) explica
la selección de textos, las formas de los tensores y el recorrido de una consulta.

Implementa estas tres herramientas:

| Herramienta | Operación | Resultado esperado |
|---|---|---|
| `search_reviews(query, top_k=5)` | Buscar los textos más similares a una consulta mediante similitud coseno. | ID de reseña, texto, producto, valoración y similitud, en orden descendente. |
| `analyze_product(product_id)` | Resumir las valoraciones de un producto. | Cantidad de reseñas, conteos y proporciones de 1 a 5 estrellas, media y mediana. |
| `compare_products(product_ids)` | Comparar al menos dos productos distintos. | Resumen de cada producto y diferencias de media respecto al primero. |

Calcula similitudes y estadísticas con arreglos de NumPy o tensores de PyTorch.
Puedes usar pandas para explorar o relacionar los metadatos por `parent_asin`.
Conserva las reseñas sin texto para las estadísticas, aunque no tengan embedding.
Indica el tamaño de muestra y devuelve datos serializables por el cliente MCP.

Puedes implementar las herramientas directamente en `server.py` o separarlas en
módulos. La guía propone `support` como una forma de organizar el código, sin
exigir una arquitectura particular.

## Ejecución y comportamiento

El servidor utiliza **Streamable HTTP** en **`http://127.0.0.1:8000/mcp`**.
El cliente debe descubrir e invocar las tres herramientas.

- `top_k`: entero entre 1 y 20; devuelve como máximo esa cantidad de coincidencias.
- Consulta o ID en blanco: error claro. En una comparación, los IDs deben ser distintos.
- Producto desconocido: análisis con conteo cero, conteos y proporciones en cero y
  media/mediana `null`. Si falta una media, la diferencia correspondiente también es `null`.
- Una llamada inválida no debe impedir una llamada válida posterior.

La búsqueda semántica devuelve los textos más cercanos incluso si la consulta
es poco relevante. Su puntuación no es una probabilidad ni mide la calidad del producto.

Usa **anotaciones de tipo** y comprueba **`mypy --strict`** sobre los archivos Python
de tu aplicación. **Ruff es opcional.**

## Entregables

- Carpeta del proyecto con código, `config.json`, `pyproject.toml`, `uv.lock` y
  `.python-version`. Omite `.venv`, cachés y pesos del modelo.
- README breve con comandos para obtener los datos, iniciar el servidor, ejecutar
  el cliente y comprobar los tipos. Si guardas vectores, explica cómo regenerarlos.
- Capturas o salida de la demostración: búsqueda, análisis, comparación, producto
  desconocido y llamada inválida seguida de una válida; incluye la salida de mypy.
- Dos ejemplos de consultas de dominio con una interpretación breve de sus
  resultados y una limitación. Puedes incluirlos en el mismo README.

## Evaluación

| Criterio | Puntos |
|---|---:|
| Ejecución reproducible con `uv` y configuración del modelo | 15 |
| Tres herramientas MCP y demostración HTTP | 25 |
| Embeddings, búsqueda vectorizada y estadísticas correctas | 40 |
| Interpretación de resultados y alcance de los datos | 10 |
| Entradas inválidas y recuperación del servidor | 5 |
| Anotaciones y `mypy --strict` | 5 |
| **Total** | **100** |

Se revisarán la correspondencia vector–reseña, el uso del mismo modelo, el orden
de búsqueda y las estadísticas de las reseñas correctas. La organización interna
y las herramientas opcionales no añaden ni restan puntos.

## Ampliaciones opcionales

Puedes añadir `keywords` a la búsqueda para filtrar por palabras normalizadas
antes de ordenar por similitud. Es una ampliación opcional, no un requisito para
obtener los 100 puntos. Describe cómo combinas las palabras si la implementas.

También puedes explorar clasificación o estimación de valoraciones mediante
vecinos similares, usando registros separados del índice para evaluar. Las
estrellas no equivalen a etiquetas de sentimiento verificadas.

## Referencias

- [Amazon Reviews 2023](https://amazon-reviews-2023.github.io/).
- [Modelo all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).
- [Sentence Transformers](https://www.sbert.net/docs/package_reference/sentence_transformer/SentenceTransformer.html).
- [SDK oficial de MCP para Python](https://py.sdk.modelcontextprotocol.io/).
