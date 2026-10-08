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

---

## Estructura del Proyecto

```text
LeadNormalizer/
│
├── app.py
├── config/
│   ├── headers.json
│   └── rules.json
├── core/
│   ├── validator.py
│   ├── normalizer.py
│   ├── matcher.py
│   ├── discard_rules.py
│   ├── report_generator.py
│   └── audit.py
├── tests/
├── outputs/
├── requirements.txt
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

MVP recomendado:

**Streamlit + Pandas + OpenPyXL + Plotly**

Permite construir rápidamente una solución portable, escalable y alineada con una futura evolución hacia Azure, Dataverse o .NET, conservando la lógica de negocio y las reglas de calidad de datos.
