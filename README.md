# LeadNormalizer - MVP de Normalización y Depuración de Base de Prospección

## 1. Objetivo

Desarrollar una aplicación web liviana y portable para que usuarios de negocio, marketing o campañas puedan:

- Cargar una base de prospección en formato Excel.
- Validar automáticamente la estructura del archivo.
- Normalizar cabeceras y datos.
- Cruzar la información contra una base exportada desde CRM.
- Eliminar registros inválidos o ya tratados.
- Generar archivos de salida para reutilización.
- Obtener métricas y KPIs del proceso.

La solución debe ser escalable, mantenible y compatible con el ecosistema Microsoft, permitiendo en una etapa futura integrarse con Azure, Dataverse o Dynamics CRM.

---

## Instalación y Uso

Hay dos formas de usar LeadNormalizer, según quién la use:

### Opción A — Usuario final (no requiere instalar Python)

1. Descargar `dist/LeadNormalizer_Portable.zip` (incluye un Python embebido con todas las dependencias ya instaladas).
2. Descomprimirlo en cualquier carpeta.
3. Doble clic en `LeadNormalizer.bat`.

Abre una ventana de escritorio propia (no una pestaña de navegador) con la app lista para usar. No necesita conexión a internet ni instalar nada adicional.

### Opción B — Desarrollo (clonando el repositorio)

Requiere tener [Python 3.10+](https://www.python.org/downloads/) instalado (marcando "Add to PATH" durante la instalación en Windows).

1. Clonar el repositorio.
2. Doble clic en `install.bat` (o ejecutarlo desde una terminal). Crea el entorno virtual `.venv`, instala las dependencias (incluyendo `pytest`) y genera datos de ejemplo en `data/sample/`.
3. Doble clic en `LeadNormalizer.bat` para abrir la app como ventana de escritorio, o correr `streamlit run app.py` para abrirla en el navegador en modo desarrollo (con auto-reload).

Para correr los tests: `.venv\Scripts\python.exe -m pytest`

### Generar el zip portable

Para reconstruir `dist/LeadNormalizer_Portable.zip` después de modificar el código:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_portable_zip.ps1
```

El script descarga y cachea el runtime de Python embebido en `build/` (no vuelve a descargarlo en corridas posteriores) e instala en él únicamente las dependencias de `requirements.txt` (sin `pytest`, que es solo para desarrollo).

---

## Alcance Funcional MVP

### Entradas

1. Excel Crudo (BaseProspeccion).
2. Excel CRM exportado desde Dynamics/CRM.

### Flujo

Carga Excel Crudo → Validación → Normalización → Cruce CRM → Reglas de Descarte → Generación de Salidas → KPIs.

### Validaciones

Columnas obligatorias:

- NUMERO_DOCUMENTO
- EMAIL
- NOMBRE
- APELLIDO

### Normalización de Cabeceras

Ejemplos:

- Mail → EMAIL
- e-mail → EMAIL
- Numero Documento → NUMERO_DOCUMENTO
- DNI → NUMERO_DOCUMENTO

La aplicación deberá informar al usuario cada corrección detectada.

### Reglas de Descarte

- DUPLICADO_CRM
- DUPLICADO_ARCHIVO
- SIN_DOCUMENTO
- SIN_EMAIL

### Salidas

#### BaseProspeccionNormalizada.xlsx

Contendrá únicamente registros válidos.

#### BaseProspeccionDescartada.xlsx

Contendrá registros descartados con columna MOTIVO_DESCARTE.

### Dashboard KPI

Indicadores:

- Registros Crudos
- Registros Válidos
- Duplicados CRM
- Duplicados Archivo
- Sin Documento
- Sin Email
- Total Descartados

Gráficos:

- Barras
- Torta por motivo de descarte

---

## Stack Tecnológico MVP

### Streamlit

Responsable de:

- UI Web
- Upload de archivos
- Descarga de resultados
- Visualización de KPIs

### Pandas

Responsable de:

- Lectura Excel
- Transformaciones
- Cruces
- Normalización
- Métricas

### OpenPyXL

Responsable de:

- Generación de Excels
- Formateo
- Hoja Auditoría

### Plotly

Responsable de:

- Gráficos interactivos
- Dashboard KPI

### pywebview

Responsable de:

- Envolver la UI de Streamlit en una ventana de escritorio nativa (sin barra de navegador), usada por `desktop_app.py` y el lanzador `LeadNormalizer.bat`.

---

## Estructura del Proyecto

```text
prospeccionProcessor/
│
├── app.py                      # UI Streamlit
├── desktop_app.py               # Wrapper pywebview (ventana de escritorio)
├── install.bat                  # Setup para desarrollo (crea .venv + deps)
├── LeadNormalizer.bat           # Lanzador de la app como ventana de escritorio
├── config/
│   ├── headers.json             # Alias de cabeceras reconocidas
│   └── rules.json               # Columnas obligatorias, clave de cruce CRM, prioridad de descarte
├── core/
│   ├── validator.py
│   ├── normalizer.py
│   ├── matcher.py
│   ├── discard_rules.py
│   ├── report_generator.py
│   └── audit.py
├── scripts/
│   ├── generate_sample_data.py  # Genera Excels de ejemplo en data/sample/
│   └── build_portable_zip.ps1   # Arma dist/LeadNormalizer_Portable.zip
├── tests/
├── data/sample/                 # Excels de ejemplo (generados por scripts/generate_sample_data.py)
├── outputs/
├── build/                       # Cache del runtime embebido (regenerable con build_portable_zip.ps1; versionado via Git LFS)
├── dist/                        # Zip portable final (regenerable; versionado via Git LFS)
├── requirements.txt              # Dependencias de produccion
├── requirements-dev.txt          # + pytest, para desarrollo
└── README.md
```

---

## Roadmap Futuro

### Fase 2

- Reglas parametrizables.
- Configuración por JSON.
- Múltiples campañas.

### Fase 3

- Integración Dataverse.
- Integración Dynamics CRM.

### Fase 4

- Azure Functions.
- Azure Storage.
- Azure App Service.

### Fase 5

- Power BI.
- Históricos.
- Calidad de datos.

---

## Estimación de Tokens para IA

### Solo cabeceras

500 a 2.000 tokens.

### Cabeceras + muestra de datos

5.000 a 15.000 tokens.

### Excel completo (no recomendado)

Más de 200.000 tokens.

### Estrategia recomendada

Enviar:

- Cabeceras
- Primeras 50 filas
- Reglas actuales

para minimizar costos y maximizar precisión.

---

## Conclusión

MVP recomendado: **Streamlit + Pandas + OpenPyXL + Plotly**.

Permite construir rápidamente una solución portable, escalable y alineada con una futura evolución hacia Azure, Dataverse o .NET, conservando la lógica de negocio y las reglas de calidad de datos.
