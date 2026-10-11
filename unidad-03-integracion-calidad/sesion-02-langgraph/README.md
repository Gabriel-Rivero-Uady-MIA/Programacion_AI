# Sesión 2: Workflows de datos con LangGraph

Organizaremos la selección y el análisis de documentos mediante `TypedDict`,
estado con Pydantic, nodos, rutas, paralelismo, `Command` y subgraphs. Es la última sesión obligatoria: el workflow usa
funciones Python y no requiere una API key.

## Entrega de prácticas

La fecha límite para entregar las prácticas de la Unidad 3 es el **19 de octubre de 2026**.
Envía los entregables mediante el [formulario de entrega](https://docs.google.com/forms/d/e/1FAIpQLSd0_iF2IEHUsLu2WXZuq-GwOSBUTfPyKNV4ht_mbH070wxljg/viewform?usp=publish-editor).

## Material

- [Presentación (PDF)](https://drive.google.com/file/d/10Oltc1j8sLw8XvC9iIovqiQYm0wEzsZV/view?usp=drivesdk).

- [Notebook](./u3_n3_langgraph_workflows.ipynb): ejemplos y **2 ejercicios**.
- [sample_data.py](./sample_data.py): catálogo de documentos utilizado en la notebook.
- [PRACTICA.md](./PRACTICA.md): entregables.
- [Fuentes oficiales](./FUENTES.md).

## Preparación

Abre esta carpeta en VS Code o PyCharm y ejecuta:

```bash
uv sync --locked
```

Selecciona `.venv` como intérprete y kernel. En VS Code utiliza las extensiones
Python y Jupyter; en PyCharm utiliza su integración de notebooks.

La notebook empieza con `TypedDict`; después compara el estado con Pydantic
y la validación explícita de un resultado dentro de un nodo. Los ejemplos de
paralelismo y `Command` son guiados y no añaden ejercicios.

Los diagramas con `draw_mermaid_png()` necesitan conexión para su renderizado
predeterminado. Si no está disponible, la notebook muestra el texto Mermaid;
los workflows siguen ejecutándose localmente.

## Grafos de datos y de ejecución

Neo4j almacena entidades y relaciones; LangGraph organiza pasos de un programa.
Aquí usamos *graph engineering* como una forma de describir el diseño de ese
flujo —estado, operaciones y decisiones—, no como el nombre de una API.
Un nodo podría consultar una base o ejecutar un modelo; no necesita hacerlo.

[Volver a la unidad](../README.md)
