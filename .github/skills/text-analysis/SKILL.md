
---
name: text-analysis
description: >-
  Analiza texto en español mediante reglas configurables para calcular
  estadísticas, extraer palabras clave, estimar sentimiento léxico
  y producir un resumen extractivo. Utilizar cuando una solicitud
  requiera análisis de texto sin generación libre de contenido.
---

# Text Analysis Skill

## Objetivo

Procesar texto en español mediante operaciones deterministas y resultados
estructurados, utilizando las reglas del recurso `references/processing_rules.json`.

## Instrucciones de ejecución

1. Validar que el texto recibido no esté vacío.
2. Leer las reglas desde el recurso JSON de esta skill.
3. Calcular el número de caracteres, palabras y oraciones.
4. Aplicar las reglas léxicas configuradas para estimar el sentimiento.
5. Extraer palabras clave según las frecuencias y exclusiones definidas.
6. Crear un resumen extractivo cuando la operación lo solicite.
7. Devolver resultados estructurados y señalar el nombre de la skill utilizada.

## Reglas de comportamiento

- No inventar información que no aparezca en el texto.
- No presentar el sentimiento léxico como una evaluación psicológica.
- No afirmar que se utilizó un modelo de lenguaje.
- Respetar la operación solicitada por el cliente.
- Utilizar los recursos de esta skill como fuente de configuración.
- Mantener el procesamiento reproducible para una misma entrada.

## Operaciones disponibles

- `summary`: genera un resumen extractivo.
- `sentiment`: calcula una estimación léxica de sentimiento.
- `keywords`: extrae palabras clave.
- `full`: devuelve todos los resultados.

## Resultado esperado

Una respuesta JSON con estadísticas del texto, resultados de la operación,
la identificación de la skill y los campos definidos por la API.
