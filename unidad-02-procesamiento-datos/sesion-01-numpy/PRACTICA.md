# Práctica: seleccionar y resumir mediciones

## Ejercicios durante la exploración

La sesión contiene 11 ejercicios: los ejercicios 1–8 están en la notebook de
exploración; el 9 se resuelve en una celda nueva de esa misma notebook. Los
ejercicios 10 y 11 están en la notebook de reporte. Esta práctica detalla
también la implementación del 11; es el mismo trabajo, no un ejercicio adicional.
En cada uno, escribe primero el resultado o la forma esperada y luego comprueba tu
propuesta con NumPy.

| Ejercicio | Trabajo | Evidencia |
|---|---|---|
| 1 | Distinguir un vector y una matriz de una fila | `shape`, `ndim` y significado |
| 2 | Elegir un tipo para temperaturas decimales | Conversión que conserve `22.75` |
| 3 | Seleccionar las últimas tres rondas y dos salas | Matriz de forma `(3, 2)` |
| 4 | Conservar una columna como matriz | Forma `(8, 1)` |
| 5 | Filtrar por intervalo de temperatura | Tres rondas de la sala sur |
| 6 | Modificar una selección sin afectar el original | Comprobación de independencia |
| 7 | Convertir temperaturas sin un ciclo explícito | Nueva matriz en Fahrenheit de forma `(8, 3)` |
| 8 | Excluir filas con valores no finitos | Máscara y conteo de filas rechazadas |
| 9 | Comparar cada sala con su propia media | Matriz de diferencias con forma `(8, 3)` |
| 10 | Interpretar dos reportes | Comparación de las filas usadas en cada cálculo |
| 11 | Seleccionar rondas por umbral | Función reutilizable, pruebas y resultados |

## Ejercicio 9: diferencias respecto de la media

Calcula la media de cada sala y réstala de `readings` sin escribir un ciclo por
ronda. Comprueba que la matriz resultante conserva la forma `(8, 3)` y que la
media de cada columna de diferencias es aproximadamente cero. Explica cómo se
alinean las formas `(8, 3)` y `(3,)` y por qué no se resta la media general.

## Ejercicio 11: aplicación independiente

En `02-reporte-mediciones`, crea `measurements/selection.py` con una función
`select_warm_rounds(readings, threshold)` que devuelva las filas donde la sala norte
sea mayor o igual al umbral. La selección debe conservar las tres columnas y no
modificar la entrada. Recibe una matriz no vacía de tres columnas y valores
finitos; reutiliza la comprobación de forma existente y rechaza valores no finitos,
incluido un umbral no finito, con `ValueError`.

1. Llámala desde la notebook de reporte después de seleccionar filas completas.
2. Para el archivo original y umbral `27`, comprueba las tres filas esperadas:
   `[[27, 29, 25], [28, 30, 26], [29, 31, 27]]`.
3. Para umbral `100`, devuelve un arreglo vacío de forma `(0, 3)`. No llames a
   `summarize` sobre ese resultado: explica por qué no habría una media definida.
4. Comprueba que modificar la selección no cambia el arreglo original.
5. Añade pruebas para el umbral exacto, ninguna coincidencia y entrada no finita.
6. Compara las medias de la selección con las del conjunto completo. Describe la
   selección realizada sin atribuir el cambio a una causa externa.

## Entrega

- Notebooks con los ejercicios resueltos y resultados explicados.
- El módulo nuevo y sus pruebas en el proyecto de reporte.
- Un párrafo que explique los ejes, el criterio de filtrado y la diferencia entre
  selección y modificación del archivo original.

## Criterios de revisión

- Las formas coinciden con la interpretación de filas y columnas.
- Las selecciones incluyen los límites pedidos y conservan el orden de las salas.
- La entrada no cambia por efectos de memoria compartida.
- Las pruebas cubren resultados válidos y casos límite.
- El proyecto se ejecuta con `uv sync --locked` y las notebooks desde un kernel limpio.
