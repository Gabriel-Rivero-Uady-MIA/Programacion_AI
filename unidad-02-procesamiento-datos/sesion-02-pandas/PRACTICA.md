# Práctica: comprobar un grupo adicional

## Ejercicio 5

En `titanic/analysis.py`, añade una función `missing_age_by_class(prepared)` que
devuelva una tabla con una fila por `Pclass` y dos columnas adicionales:
`passengers` (cantidad de pasajeros) y `missing_age_rate` (proporción de edades
ausentes). Reutiliza la columna `age_missing` generada por `prepare_passengers`.

Llama la función desde `main.py` y guarda la tabla como
`outputs/missing_age_by_class.csv`. Comprueba que el total de pasajeros agrupados
es 891 y que la proporción de cada clase se encuentra entre cero y uno. Añade
una prueba pequeña con datos construidos por ti para comprobar las proporciones,
sin depender únicamente del CSV completo. Usa `dropna=False` al agrupar, como
en la notebook, para conservar pasajeros cuya clase pudiera estar ausente.

Explica en dos o tres frases por qué una proporción por clase informa algo que
el conteo total de 177 edades ausentes no muestra. No interpretes la asociación
como una causa.

## Entrega

- Notebook con los ejercicios 1–4 y sus resultados interpretados.
- Función, llamada desde la aplicación, archivo de salida y prueba del ejercicio 5.
