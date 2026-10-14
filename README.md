# SkillAPI — FastAPI & Agent Skills Integration

## 1. Descripción del proyecto

SkillAPI es una API REST desarrollada con FastAPI que permite analizar texto en español mediante una skill personalizada.

El sistema procesa solicitudes HTTP, valida los datos de entrada y aplica reglas configurables para obtener estadísticas, palabras clave, una estimación léxica del sentimiento y un resumen extractivo.

El proyecto demuestra separación de responsabilidades, modularidad y personalización del comportamiento mediante una skill ubicada en `.github/skills/`.

**Nota:** la implementación actual utiliza procesamiento determinista y reglas configurables. No se conecta a un modelo de lenguaje externo.

## 2. Tecnologías

- Python
- FastAPI
- Pydantic
- Uvicorn
- HTTPX y `unittest` para pruebas
- Git y GitHub

## 3. Estructura del proyecto

```text
SkillAPI/
├── .github/
│   └── skills/
│       └── text-analysis/
│           ├── SKILL.md
│           └── references/
│               └── processing_rules.json
├── app/
│   ├── main.py
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   └── config.py
│   ├── schemas/
│   │   └── text.py
│   └── services/
│       ├── agent_service.py
│       └── skill_loader.py
├── tests/
│   └── test_api.py
├── docs/
│   └── nota_tecnica.md
├── requirements.txt
├── .gitignore
└── README.md
```

## 4. Endpoints disponibles

| Método | Endpoint | Función |
|---|---|---|
| GET | `/` | Información general de la API |
| GET | `/api/v1/health` | Verificación de disponibilidad |
| GET | `/api/v1/skills` | Lista las skills disponibles |
| POST | `/api/v1/analyze` | Analiza el texto enviado |

La documentación interactiva de FastAPI se encuentra en `/docs`.

## 5. Operaciones de análisis

El endpoint `POST /api/v1/analyze` acepta las operaciones:

- `summary`: genera un resumen extractivo.
- `sentiment`: estima el sentimiento mediante palabras configuradas.
- `keywords`: extrae palabras clave.
- `full`: devuelve todos los resultados.

Ejemplo de solicitud:

```json
{
  "text": "El proyecto funciona excelente y el resultado es positivo.",
  "operation": "full"
}
```

La respuesta incluye estadísticas del texto, palabras clave, sentimiento, resumen y el nombre de la skill utilizada.

## 6. Skill personalizada

La skill `text-analysis` está definida en:

`.github/skills/text-analysis/SKILL.md`

Su propósito es orientar el procesamiento del texto y establecer reglas reproducibles. El recurso `references/processing_rules.json` contiene las palabras excluidas, los términos positivos y negativos y los límites de resultados.

El cargador de skills lee ambos archivos. El servicio de análisis utiliza sus reglas para calcular los resultados. Por tanto, modificar el recurso de configuración puede cambiar el comportamiento de la API sin modificar sus endpoints.

## 7. Instalación

Se recomienda Python 3.11 o superior.

Crear el entorno virtual:

```powershell
python -m venv .venv
```

Instalar dependencias:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 8. Ejecutar la API

Desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Abrir `http://127.0.0.1:8000/docs` para explorar y probar los endpoints.

## 9. Ejecutar las pruebas

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

El resultado debe comprobarse mediante la ejecución real del comando. No se consideran aprobadas las pruebas hasta verificar su salida.

## 10. Uso consciente de IA

Las herramientas de IA pueden ayudar a proponer estructuras, código y casos de prueba. Las sugerencias deben revisarse, ejecutarse y corregirse cuando sea necesario.

En esta versión, el procesamiento se realiza mediante reglas explícitas y código Python. No se atribuyen capacidades de inferencia a un LLM que no está integrado.

## 11. Mejoras futuras

- Integración opcional con un modelo de lenguaje.
- Ampliación de las skills.
- Mejoras en la clasificación semántica.
- Más pruebas de integración y validación de recursos.
- Métricas y registros de ejecución.