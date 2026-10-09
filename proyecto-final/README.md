# Proyecto final: búsqueda y análisis de productos de Amazon con MCP

**Fecha límite: 26 de octubre de 2026.**

Construye un servidor MCP por HTTP local para buscar y analizar productos de
**Amazon Reviews 2023 · Electronics**, utilizando embeddings y operaciones de
**PyTorch o NumPy**. Proporcionamos una selección de **600 productos y 6 992 reseñas**,
entre 5 y 30 por producto; no necesitas preparar otra muestra ni crear un agente.

## Material proporcionado

- [Notebook](./preparacion_datos.ipynb): lectura y exploración de los datos.
- [datasets](./datasets/): los dos archivos pequeños que utilizará la aplicación.
- [Guía de desarrollo](./GUIA.md): pasos para crear tu proyecto y trabajar con embeddings.
- [config.json](./config.json): configuración del modelo para incorporar a tu aplicación.
- [Guía HTTP y snippets de `client.py` y `main.py`](./MCP_HTTP.md): conexión y demostración.
- [Dataset](./DATASET.md): campos, diversidad, selección y fuentes.

## Qué implementar

Crea tu proyecto con **`uv`** y trabaja con los dos archivos de la selección proporcionada
en `datasets/`. Implementa `support/data.py` para leer y preparar los datos,
`support/settings.py` para cargar y validar la configuración y `support/encoder.py`
para codificar textos con `sentence-transformers/all-MiniLM-L6-v2`. La notebook
sirve como referencia; la aplicación debe ejecutarse sin correrla previamente.
Consulta la [estructura del proyecto](./GUIA.md#estructura-del-proyecto).

Modularizar significa separar las funciones en archivos Python e importarlas,
como en las notebooks y el proyecto `uv` de U1S4. El archivo `support/__init__.py`
puede quedar vacío.

Combina el embedding del catálogo con el promedio normalizado de los embeddings
de sus reseñas: **50 % de cada fuente**, seguido de normalización. Usa el mismo
modelo para catálogo, reseñas y consultas; prepara los vectores una vez al iniciar
el servidor. La [guía](./GUIA.md#3-generar-los-embeddings-para-la-búsqueda) explica
las operaciones con ejemplos.

Implementa estas tres herramientas:

| Herramienta | Operación | Resultado esperado |
|---|---|---|
| `search_products(query, top_k=5)` | Buscar productos por similitud coseno, combinando catálogo y reseñas. | ID de producto, título, similitud y cantidad de reseñas seleccionadas, en orden descendente. |
| `analyze_product(product_id)` | Resumir las valoraciones de un producto. | Cantidad de reseñas, conteos y proporciones de 1 a 5 estrellas, media y mediana. |
| `compare_products(product_ids)` | Comparar al menos dos productos distintos. | Resumen de cada producto y diferencias de media respecto al primero. |

Calcula las similitudes y estadísticas con NumPy o PyTorch y devuelve valores de
Python serializables. Puedes usar pandas para explorar los datos. Las herramientas
de `server.py` deben utilizar los módulos de `support/`.

Las estadísticas describen **las reseñas seleccionadas**, no todas las valoraciones
de Amazon. No se evalúan la regeneración ni las gráficas de la notebook.

## Ejecución y comportamiento

El servidor utiliza **Streamable HTTP** en **`http://127.0.0.1:8000/mcp`**.
El cliente debe descubrir e invocar las tres herramientas.

- `top_k`: entero entre 1 y 20; devuelve como máximo esa cantidad de coincidencias.
- Consulta o ID en blanco: error claro. En una comparación, los IDs deben ser distintos.
- Producto desconocido: análisis con conteo cero, conteos y proporciones en cero y
  media/mediana `null`. Si falta una media, la diferencia correspondiente también es `null`.
- Una llamada inválida no debe impedir una llamada válida posterior.

La búsqueda semántica devuelve los productos más cercanos incluso si la consulta
es poco relevante. Su puntuación no es una probabilidad ni mide la calidad del producto.

Usa **anotaciones de tipo** y comprueba **`mypy --strict`** sobre los archivos Python
de tu aplicación, incluidos todos los módulos de `support/`; el análisis debe
finalizar sin errores. **Ruff es opcional.**

## Entregables

Sube el proyecto en un **archivo comprimido (.zip)** mediante el
[formulario de entrega](https://docs.google.com/forms/d/e/1FAIpQLSew4UpE94kmWvK5M54-ubF1aeTqbk5SMOQ1IfDjdBiingDWFw/viewform?usp=publish-editor),
a más tardar el **26 de octubre de 2026**.

- Carpeta del proyecto con código, `config.json`, `pyproject.toml`, `uv.lock`,
  `.python-version` y `datasets/`. Omite `.venv`, cachés y pesos del modelo.
- README breve con comandos para iniciar el servidor, ejecutar el cliente y
  comprobar los tipos. Si guardas vectores, explica cómo regenerarlos.
- Dos ejemplos de consultas de dominio con una interpretación breve de sus
  resultados y una limitación. Puedes incluirlos en el mismo README.

## Evaluación

| Criterio | Puntos |
|---|---:|
| Ejecución reproducible con `uv`, modularización y configuración del modelo | 15 |
| Tres herramientas MCP y demostración HTTP | 25 |
| Embeddings, búsqueda vectorizada y estadísticas correctas | 40 |
| Interpretación de resultados y alcance de los datos | 10 |
| Entradas inválidas y recuperación del servidor | 5 |
| Anotaciones y `mypy --strict` | 5 |
| **Total** | **100** |

Se revisarán la correspondencia vector–producto, la combinación de ambas fuentes,
el orden de búsqueda y las estadísticas. Las ampliaciones opcionales no afectan la calificación.

## Ampliaciones opcionales

Puedes añadir `keywords` para filtrar por palabras normalizadas antes de ordenar
por similitud; describe cómo combinas esas palabras.

También puedes explorar clasificación o estimación de valoraciones mediante
vecinos similares, usando registros separados del índice para evaluar. Las
estrellas no equivalen a etiquetas de sentimiento verificadas.

## Referencias

- [Amazon Reviews 2023](https://amazon-reviews-2023.github.io/).
- [Modelo all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).
- [Sentence Transformers](https://www.sbert.net/docs/package_reference/sentence_transformer/SentenceTransformer.html).
- [SDK oficial de MCP para Python](https://py.sdk.modelcontextprotocol.io/).
