# Cómo funciona (guía para explicarlo en una entrevista)

## Las piezas
- **`BookerClient`**: centraliza URLs, headers, token y reintentos. Si la API cambia una ruta, se toca un solo lugar.
- **Fixtures** (`conftest.py`): `client` y `token` se crean una vez por ejecución (`scope="session"`). `booking` crea una reserva para el test y la borra al final con `yield`.
- **Factories**: datos únicos en cada test, así no chocan entre sí ni con otros usuarios de la API pública.
- **JSON Schema**: valida la *forma* de la respuesta (tipos y campos obligatorios), no solo los valores. Eso es contract testing.

## Preguntas típicas
- **¿Qué es un test flaky y cómo lo evitás?** Un test que a veces pasa y a veces no. Lo evito con datos únicos, limpieza después de cada test y reintentos solo para errores de infraestructura (502/503/504), nunca para errores de lógica.
- **¿Por qué `xfail(strict=True)`?** Documenta un bug conocido sin romper el pipeline. Si el bug se arregla, el test pasa y `strict` lo marca como fallo para que lo actualices.
- **¿Smoke vs regresión?** Smoke: pocas pruebas rápidas para saber si vale la pena seguir. Regresión: todo el comportamiento.
- **¿Por qué un cron en el CI?** La API puede cambiar aunque mi código no cambie. Correr todos los días detecta esos cambios.

## Cómo reportaste los bugs
Mirá `BUGS.md`: cada uno tiene esperado vs. obtenido, severidad, pasos para reproducir e impacto. Es el mismo formato que usarías en Jira.
