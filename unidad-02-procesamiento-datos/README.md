# Unidad 2: Procesamiento y representación de datos para IA

Trabajaremos con arreglos, tablas, tensores y visualizaciones para preparar datos,
comprobar sus transformaciones y explorar sus características. Las notebooks
servirán para experimentar y explicar resultados; los proyectos con `uv`
permitirán repetir el procesamiento desde la terminal.

## Entrega de prácticas

La fecha límite para entregar las prácticas de la Unidad 2 es el **13 de octubre de 2026**.
Envía los entregables mediante el [formulario de entrega](https://docs.google.com/forms/d/e/1FAIpQLScOPQOB1sgjXsZbrealNcJ_U8Aa-bqtds5SozcSsRNSek7FxA/viewform?usp=publish-editor).

## Contenido

| Sesión | Tema | Trabajo principal |
|---|---|---|
| 1 | [NumPy y vectorización](./sesion-01-numpy/README.md) | Formas, tipos, selección, vistas, operaciones vectorizadas y broadcasting con mediciones. |
| 2 | [pandas y paso a NumPy](./sesion-02-pandas/README.md) | Cargar, limpiar, agrupar y unir datos de Titanic; extraer una matriz numérica. |
| 3 | [PyTorch y datasets](./sesion-03-pytorch/README.md) | Tensores, `Dataset`, `DataLoader` y exploración de CIFAR-10 por lotes. |
| 4 | [Visualización](./sesion-04-visualizacion/README.md) | Histogramas, porcentajes por grupo y cuadrículas de imágenes con Matplotlib. |

Las notebooks se numeran de forma continua dentro de la unidad: `u2_n1`,
`u2_n2`, `u2_n3`, etc.

## Notebooks en VS Code

Instala las extensiones **Python** y **Jupyter** de VS Code. Desde la carpeta del
proyecto de cada sesión, ejecuta `uv sync --locked` en la terminal integrada y
abre la notebook mediante el enlace de su README. En la esquina superior derecha,
elige **Select Kernel → Python Environments → `.venv`**. Si `.venv` no aparece,
usa **Select Another Kernel** y selecciona el intérprete del proyecto:
`.venv/bin/python` en macOS/Linux o `.venv/Scripts/python.exe` en Windows.

Cada proyecto declara `ipykernel` como dependencia de desarrollo. Al cambiar de
proyecto, selecciona el kernel de su propia `.venv`; reiniciar el kernel borra las
variables que habían quedado en memoria.

[Guía oficial de notebooks en VS Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks) ·
[Entornos y kernels de VS Code](https://code.visualstudio.com/docs/datascience/jupyter-kernel-management) ·
[uv con VS Code y notebooks](https://docs.astral.sh/uv/guides/integration/jupyter/#using-jupyter-from-vs-code)

## Ejercicios

La [sesión 1](./sesion-01-numpy/README.md) tiene ejercicios en las notebooks y
una práctica de aplicación. La [sesión 2](./sesion-02-pandas/README.md) tiene
ejercicios en su notebook y en `PRACTICA.md`. La
[sesión 3](./sesion-03-pytorch/README.md) combina ejercicios de tensores en su
notebook y una ampliación del resumen por clase en `PRACTICA.md`. La [sesión 4](./sesion-04-visualizacion/README.md) contiene dos ejercicios
de visualización en su notebook. Cada README de sesión explica dónde resolverlos y cómo ejecutar sus materiales.

## Producto de la unidad

El trabajo avanza desde una matriz de mediciones hasta una tabla con etiquetas,
una selección de variables numéricas y formas de examinar los datos. Los archivos
generados en la sesión 2 permiten retomar la representación numérica en PyTorch y
la tabla preparada en visualización.
