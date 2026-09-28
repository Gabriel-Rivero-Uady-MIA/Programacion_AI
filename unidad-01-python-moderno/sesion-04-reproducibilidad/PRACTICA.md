# Práctica: un catálogo reproducible con MCP

Trabaja sobre el proyecto que construiste en [GUIA.md](./GUIA.md).

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

Entrega código, datos pequeños y un README con comandos de ejecución y resultados
esperados. Incluye la evidencia de las llamadas y tus explicaciones. Los logs,
el entorno y las salidas generadas deben quedar fuera de Git.
