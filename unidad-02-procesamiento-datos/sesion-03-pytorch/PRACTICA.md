# Práctica: proporciones por clase

## Ejercicio 5

Amplía `label_summary` en `data_lab/inspection.py` para incluir una columna
`proportion` con la fracción de muestras de cada clase. Usa como denominador la
cantidad de etiquetas recibidas, que puede cambiar con `--limit`.

1. Conserva `class_id`, `class_name` y `count`. Incluye las clases con conteo cero.
2. Actualiza la anotación del retorno para admitir también valores `float`.
3. Añade una prueba con etiquetas `[0, 0, 2, 2, 2]` y nombres de clase
   `["class_a", "class_b", "class_c"]`. Comprueba conteos `[2, 0, 3]`,
   proporciones `[0.4, 0.0, 0.6]` y suma aproximadamente igual a uno.
4. Ejecuta `main.py --limit 10 --batch-size 4` mediante `uv run --locked python`
   y comprueba que `class_counts.csv` incluya la columna nueva. `main.py` obtiene
   los encabezados del resumen, por lo que no hace falta duplicar allí el cálculo.
5. Explica por qué cambiar `batch_size` no debería alterar estos conteos, mientras
   que cambiar `limit` puede hacerlo. Conserva `shuffle=False` y `drop_last=False`.

## Entrega

- Notebook con los ejercicios 1–4 resueltos y sus interpretaciones.
- Función modificada y prueba del ejercicio 5.
- CSV generado y una explicación breve del denominador utilizado.

Reinicia el kernel y ejecuta toda la notebook. Ejecuta también las pruebas y
comprobaciones indicadas en el README.
