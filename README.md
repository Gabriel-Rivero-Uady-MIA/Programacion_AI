# Programación para Inteligencia Artificial

Repositorio de materiales para la asignatura **Programación para Inteligencia
Artificial** de la Maestría en Inteligencia Artificial.

## Organización

Los materiales se agrupan por unidad y sesión. Cada sesión contiene su guía,
recursos y actividades.

| Unidad | Contenido | Materiales de trabajo |
|---|---|---|
| [1. Python moderno para IA](./unidad-01-python-moderno/README.md) | Fundamentos de Python, tipado, modelos de datos, iteración, concurrencia y reproducibilidad. | Notebooks, una aplicación con `uv` y archivos de práctica. |
| [2. Procesamiento y representación de datos](./unidad-02-procesamiento-datos/README.md) | NumPy, Pandas, integración de datos, tensores y visualización. | Notebooks dentro de proyectos con `uv` y archivos de práctica. |
| [3. Integración y calidad de aplicaciones de IA](./unidad-03-integracion-calidad/README.md) | SQL y NoSQL desde Python, workflows y subgraphs con LangGraph; agentes, guardrails y MCP con LangChain (opcional). | Proyectos con `uv`, notebooks y prácticas. |

La raíz del repositorio funciona como guía del curso y no constituye un proyecto
de Python. Los proyectos administran sus dependencias de manera independiente.

## Proyecto final

El [proyecto final](./proyecto-final/README.md) integra las unidades 1 y 2: un
servidor MCP por HTTP local para buscar y analizar una selección de Electronics,
con embeddings y operaciones de PyTorch o NumPy. Incluye los datos, una notebook
de exploración y guías de desarrollo y conexión.

**Fecha límite: 26 de octubre de 2026.** Consulta sus entregables y evaluación en
el README del proyecto. La unidad 3 puede incorporarse como ampliación opcional.

## Ejercicios

Listas de cotejo por unidad: [Unidad 1](./unidad-01-python-moderno/LISTA_COTEJO.md),
[Unidad 2](./unidad-02-procesamiento-datos/LISTA_COTEJO.md) y
[Unidad 3](./unidad-03-integracion-calidad/LISTA_COTEJO.md).

Cada sesión tiene un `PRACTICA.md` con la cantidad de ejercicios, dónde
resolverlos y los entregables. Los enunciados están en las notebooks o en
`PRACTICA.md` y `CALIDAD.md`, según la actividad. Los enlaces para abrir notebooks
en Google Colab también se encuentran en el README de la sesión correspondiente.

| Unidad | Sesión | Ejercicios | Práctica y entregables |
|---|---|---|---|
| 1 | 1. Curso acelerado y Zen de Python | 12 | [PRACTICA.md](./unidad-01-python-moderno/sesion-01-curso-acelerado-python/PRACTICA.md) |
| 1 | 2. Tipado y Pydantic | 8 | [PRACTICA.md](./unidad-01-python-moderno/sesion-02-tipado-pydantic/PRACTICA.md) |
| 1 | 3. Iteración, recursos y concurrencia | 4 | [PRACTICA.md](./unidad-01-python-moderno/sesion-03-iteracion-recursos-concurrencia/PRACTICA.md) |
| 1 | 4. Organización, reproducibilidad y MCP local | 7 | [PRACTICA.md](./unidad-01-python-moderno/sesion-04-reproducibilidad/PRACTICA.md) |
| 2 | 1. NumPy y vectorización | 11 | [PRACTICA.md](./unidad-02-procesamiento-datos/sesion-01-numpy/PRACTICA.md) |
| 2 | 2. Tablas con pandas | 5 | [PRACTICA.md](./unidad-02-procesamiento-datos/sesion-02-pandas/PRACTICA.md) |
| 2 | 3. Tensores y datasets con PyTorch | 5 | [PRACTICA.md](./unidad-02-procesamiento-datos/sesion-03-pytorch/PRACTICA.md) |
| 2 | 4. Visualización de datos | 2 | [PRACTICA.md](./unidad-02-procesamiento-datos/sesion-04-visualizacion/PRACTICA.md) |
| 3 | 1. Python como cliente SQL y NoSQL | 3 | [PRACTICA.md](./unidad-03-integracion-calidad/sesion-01-sql-nosql/PRACTICA.md) |
| 3 | 2. Workflows de datos con LangGraph | 2 | [PRACTICA.md](./unidad-03-integracion-calidad/sesion-02-langgraph/PRACTICA.md) |
| 3 | 3. Agentes con LangChain · opcional | Sin entregable | [PRACTICA.md](./unidad-03-integracion-calidad/sesion-03-langchain/PRACTICA.md) |

En las sesiones con notebooks, entrega una copia con los ejercicios resueltos,
resultados y explicaciones. Cuando la práctica incluye un proyecto, entrega
también el código y los archivos indicados en su `PRACTICA.md`.

## Presentaciones de la unidad 1

1. [Introducción a Programación para Inteligencia Artificial (PDF)](https://drive.google.com/file/d/1Ls0122l-Fyyb7-adEzKu6HVJqUk8rHun/view?usp=sharing)
2. [PEP, anotaciones de tipo y Pydantic (PDF)](https://drive.google.com/file/d/1_2Bp0DOJYRTTAVd6tD1gruzsVrnT5Bru/view?usp=drivesdk)
3. [Iteración, recursos y concurrencia (PDF)](https://drive.google.com/file/d/1gMZ1HGejLwIAsZf80W7OjOz9Ktkw5Arz/view?usp=drivesdk)
4. [Organización y reproducibilidad de proyectos con uv (PDF)](https://drive.google.com/file/d/1L7z6CxmTSq6CT-fPHlxq593WCAa2HRcI/view?usp=drivesdk)

## Presentaciones de la unidad 2

1. [NumPy y vectorización (PDF)](https://drive.google.com/file/d/1nd5-nHeYSDUZgLEwXG9WLvCaIF-c_oPl/view?usp=drivesdk)
2. [Tablas con pandas y Titanic (PDF)](https://drive.google.com/file/d/1fgePaMIGZf_aMCW_2T3xgsepiQbHjG82/view?usp=drivesdk)
3. [Tensores y datasets con PyTorch (PDF)](https://drive.google.com/file/d/19Jbf46jSTM2edUpSugP48twTpEXfJVj4/view?usp=drivesdk)
4. [Visualización de datos (PDF)](https://drive.google.com/file/d/19PdTA8ILRMk53OZG0Cddl8fo4GeTniYx/view?usp=drivesdk)

## Presentaciones de la unidad 3

1. [Python como cliente SQL y NoSQL (PDF)](https://drive.google.com/file/d/11EPsoBrk9rm0xkdjXOy0PuIkdz48iXc5/view?usp=drivesdk)
2. [Workflows de datos con LangGraph (PDF)](https://drive.google.com/file/d/10Oltc1j8sLw8XvC9iIovqiQYm0wEzsZV/view?usp=drivesdk)
3. [Agentes con LangChain · opcional (PDF)](https://drive.google.com/file/d/1UZk2iv7_CTsek4SLgyDy14KKZe0FVrE5/view?usp=drivesdk)
