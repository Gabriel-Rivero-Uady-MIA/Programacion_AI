# Práctica: un catálogo reproducible con MCP

Resuelve **7 ejercicios**: los ejercicios 1–5 de este documento y los ejercicios
6–7 de [CALIDAD.md](./CALIDAD.md#ejercicios-de-calidad).

[GUIA.md](./GUIA.md) explica cómo construir el proyecto en ocho secciones;
esas secciones no son ejercicios adicionales. Crear un repositorio Git o un
commit no es requisito de entrega: para comprobar la reproducción basta una
copia del proyecto sin `.venv`.

## Ejercicio 1 · Punto de entrada

Ejecuta `uv run python -c "import main"`. Explica por qué no consulta el catálogo.
Identifica también la condición que impide iniciar el transporte al importar
`server.py`. Distingue registrar una herramienta de iniciar el servidor.

## Ejercicio 2 · Datos y argumentos

Copia `data/courses.json` a `data/extra_courses.json` y agrega un curso cuyo título
incluya Python. Usa `--catalog` para consultar esa copia desde `main.py` y comprueba
que aparecen tres resultados. Prueba una ruta inexistente y registra el código
de salida. La herramienta MCP sigue usando el catálogo predeterminado.

## Ejercicio 3 · Niveles y destinos

Compara una misma consulta con DEBUG, INFO y ERROR. Después usa
`--log-level ERROR --log-file logs/app.log`. Explica por qué el archivo conserva
mensajes que no aparecen en consola y por qué stdout debe reservarse al protocolo
en `server.py`.

## Ejercicio 4 · Mejorar el diagnóstico

Añade al mensaje INFO de `catalog/search.py` la cantidad total de cursos leídos,
además de la cantidad de coincidencias. Usa argumentos de logging. Comprueba
que la consulta directa y la llamada MCP siguen devolviendo los mismos cursos.

## Ejercicio 5 · Reproducción y llamada MCP

Desde una copia limpia, ejecuta `uv sync --locked` y `client.py` con `python`,
`astronomy` y una cadena de espacios. Identifica la herramienta disponible y
distingue respuesta vacía de error. Explica qué aportan `pyproject.toml`,
`uv.lock` y `.python-version` y por qué no se entrega `.venv`.

## Entregables

- El proyecto con código, datos pequeños, `pyproject.toml`, `uv.lock`,
  `.python-version` y `Makefile`.
- Un README con comandos, resultados de las llamadas y explicaciones de los
  ejercicios, incluida la evidencia de las comprobaciones de calidad. Puedes
  pegar la salida de terminal en bloques de código o incluir capturas donde se
  vean los comandos y sus resultados; cualquiera de las dos opciones es válida.

Para calidad, muestra el aviso de Ruff por el import sin usar y su corrección,
y el resultado final de Ruff, mypy y pytest sobre las pruebas existentes. No se
pide crear pruebas nuevas.

Comprueba la ejecución desde una copia limpia. Entrega el proyecto sin `.venv`,
cachés ni logs.
