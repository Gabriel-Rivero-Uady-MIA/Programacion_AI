# Dataset: Amazon Reviews 2023 · Subscription Boxes

Trabajaremos con la categoría **Subscription Boxes** de Amazon Reviews 2023. El dataset incluye reseñas con texto, estrellas e identificadores y
metadatos con títulos y descripciones de productos. Los archivos se relacionan
mediante `parent_asin`; algunos productos pueden no tener metadatos.

La categoría tiene aproximadamente **16 200 reseñas y 641 productos asociados a
las reseñas**. Sus archivos comprimidos son pequeños:

- [Reseñas: Subscription_Boxes.jsonl.gz](https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/review_categories/Subscription_Boxes.jsonl.gz), aproximadamente 2,7 MB.
- [Metadatos: meta_Subscription_Boxes.jsonl.gz](https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/meta_categories/meta_Subscription_Boxes.jsonl.gz), aproximadamente 0,28 MB.

La [notebook de preparación](./preparacion_datos.ipynb) muestra cómo descargar y
leer ambos archivos. Guárdalos en `data/` como `reviews.jsonl.gz` y
`products.jsonl.gz`. Los tamaños corresponden a los archivos comprimidos;
el modelo de embeddings se descarga por separado.

## Qué es JSONL

En un archivo JSONL, cada línea es un objeto JSON independiente. Por ejemplo:

```jsonl
{"parent_asin": "PRODUCT_A", "text": "Good selection of items.", "rating": 5.0}
{"parent_asin": "PRODUCT_B", "text": "The package arrived late.", "rating": 2.0}
```

Cada línea se convierte en un diccionario con `json.loads()`. No se utiliza
`json.load()` sobre el archivo completo porque el archivo contiene varios
objetos independientes, sin una lista que los agrupe.

La extensión `.gz` indica compresión con gzip. `gzip.open()` permite leer el
texto sin descomprimir el archivo manualmente.

## Leer las reseñas

Desde la raíz de tu proyecto, después de guardar los archivos en `data/`:

```python
import gzip
import json

reviews = []
with gzip.open("data/reviews.jsonl.gz", "rt", encoding="utf-8") as file:
    for line in file:
        if line.strip():
            review = json.loads(line)
            reviews.append(review)

print("Reviews:", len(reviews))
print(reviews[0]["text"])
print(reviews[0]["rating"])
print(reviews[0]["parent_asin"])
```

`"rt"` abre el archivo para leer texto. `reviews` es una lista de diccionarios;
puedes recorrerla para obtener los textos, las valoraciones y los identificadores
que acompañarán a las filas de tu matriz de vectores.

Los metadatos se leen de la misma forma, cambiando la ruta por
`data/products.jsonl.gz`. Después puedes relacionar los registros
por `parent_asin`. No relaciones los dos archivos por posición: sus filas no
tienen por qué corresponderse.

## Campos principales

| Archivo | Campo | Uso |
|---|---|---|
| Reseñas | `text` | Texto que se utiliza en la búsqueda. |
| Reseñas | `rating` | Valoración de 1 a 5 estrellas. |
| Reseñas | `parent_asin` | Identificador del producto al que pertenece la reseña. |
| Metadatos | `parent_asin` | Identificador para relacionar el producto con sus reseñas. |
| Metadatos | `title` | Nombre del producto. |
| Metadatos | `description` | Descripción del producto, que puede contener varios fragmentos. |

Para el análisis, utiliza las valoraciones de las reseñas que cargaste. El campo
`average_rating` de los metadatos es la valoración mostrada en la página del
producto y no tiene por qué coincidir con la media de esas reseñas.

Trabaja con ambos archivos completos. Si excluyes textos vacíos u otros registros,
documenta la regla y conserva la correspondencia entre textos, vectores y
metadatos. Asigna a cada reseña un identificador estable basado en su número de
línea original: `parent_asin` identifica un producto, no una reseña individual.

Las respuestas de las herramientas deben identificar las reseñas recuperadas y
distinguir opiniones de usuarios de información del catálogo. Indica cuántas
reseñas respaldan cada estadística.

[Fuente original, archivos por categoría y diccionario de datos](https://amazon-reviews-2023.github.io/).
