# Prueba Técnica — Científico de Datos (Tranqui Finanzas)
**Candidato:** Kevin Bocanegra  
**Entorno de Desarrollo:** Python 3.11  

---

## 📁 Estructura del Repositorio

```text
├── README.md                           <-- Documentación y respuestas analíticas
├── requirements.txt                    <-- Dependencias del proyecto
├── fase_1.py                           <-- Script: Calidad de Datos y Análisis Crítico (EDA)
├── fase_2.py                           <-- Script: Ingeniería de Características con Reglas de Negocio
├── fase_3.py                           <-- Script: Modelado Predictivo y Optimización Financiera
├── fase_4.py                           <-- Script: Comunicación Ejecutiva y Traducción de Resultados
├── data/
│   ├── retencion_clientes.xls          <-- Dataset base (1.500 registros)
│   └── retencion_clientes_limpio.csv   <-- Dataset depurado (1,393 registros)
└── reports/
    ├── informe_ejecutivo_retencion.pdf <-- Reporte formal para Gerencia y Finanzas
    └── figures/
        ├── grafico_1_campanas.png      <-- Visualización de hallazgos campaña de origen
        └── grafico_2_umbrales.png      <-- Análisis de costo e impacto financiero por umbrales

```

 ## Requisitos y Ejecución:

1. Instalar dependencias necesarias:
```text
pip install -r requirements.txt
```
2. Ejecución secuencial de los scripts por fase:
```text
python fase_1.py
python fase_2.py
python fase_3.py
python fase_4.py
```

## Respuestas de la Prueba Técnica para Científico de Datos en Tranqui Finanzas.

<b> Fase 1: Calidad de Datos y Análisis Crítico (EDA) </b>

1. Auditoria Metodológica:

	Extraer información:

	a.  Previsualizando el archivo con las muestras se evidencia que viene en formato .csv, con varias columnas relacionadas con datos demográficos de la deuda del cliente junto con la campaña estratégica especial que se usó, y adicionalmente trae una columna llamada “metadatos_sesion” relacionada al tiempo de sesión que tuvo el cliente al momento de registrarse en el Portal, esta columna no trae datos para todos los usuarios, algunos vienen en formato json y otros separados por ||.

	b. Teniendo en cuenta lo anterior se realizó un script de extracción en python donde se carga el dataframe, se extraen las columnas de “metadatos_sesion”, y por último se exporta el Excel limpio para analizar. Este script es el "fase_1.py".

	Hallazgos:

	a.  Tomando en cuenta un indicador que compara la fecha de registro con fecha de cancelación, donde si "fecha_registro" > "fecha_cancelacion" se marca como 1, de lo contrario como 0. Este se llamará "indicador_fecha" y se evidencia que: 

		1.  Existen 90 usuarios con "indicador_fecha" = 1 y con "fecha_cancelacion" existente, lo cual no tiene sentido pues "fecha_registro" corresponde a la fecha de registro en la que el usuario se registró en el Portal de Autogestión y "fecha_cancelación" corresponde a la fecha en la que el usuario abandona el proceso antes de consolidar su acuerdo de pago. Otra suposición de estos usuarios es que esa fecha de cancelación es la última que registra el sistema, y puede que el usuario volvió a registrarse nuevamente al portal ocasionando que sea mayor esta fecha y teniendo este bug. Ejemplo: "customer_id" = TRQ-00021.

		2.  Existen 261 usuarios con "indicador_fecha" = 0, es decir, abandonaron el proceso antes de consolidar su acuerdo de pago. Ejemplo: "customer_id" = TRQ-00032.

		3.  Existen 1.149 usuarios con "indicador_fecha" = 1 y sin "fecha_cancelacion" existente. Estos usuarios son los que debemos mantener en el proceso de consolidar su acuerdo. Ejemplo: "customer_id" = TRQ-00014.

	b.	En la columna "edad" existen 19 usuarios con edad negativa, que se marcan como '-99'. Esto puede ser por un error al traer los datos que se marcan de esta forma, ya que de lo contrario no tiene sentido este valor pues los usuarios que se registran son usuarios con cuentas en mora. Ejemplo: "customer_id" = TRQ-00024 .

	c. Sobre la columna metadatos_sesions:

		1.	No todos los usuarios cuentan con información de esta columna. Son 531 usuarios, correspondiendo a un 35% del total usuarios registrados.

		2.	Los que sí cuentan con información (969 usuarios), tienen 3 columnas, que relaciona la interacción que tuvieron con el portal de autogestión. Se evidencian gestiones usando celular o computador, el tipo de navegador y el tiempo de sesión en el portal.

2.	Resolución de ambigüedad:

    a.	Los 90 usuarios con fecha de cancelación menor a la fecha de registro no se tomarán en la muestra para el análisis, esto debido a su incongruencia con las fechas ocasionando que alteren los datos del entrenamiento de los modelos a usar. Esto corresponde a un 25% del total de usuario marcados como "churn_flag" = 1.

    b.	Los 18 usuarios con edad de mora negativa no se considerarán en la muestra para el análisis, esto debido a que este valor alterará el entrenamiento de los modelos a usar.

    c.	De la anterior limpieza quedan 1.393 usuarios, de los cuales 893 cuentan con información en "metadatos_sesion" para analizar. Con esto en cuenta, para los 500 usuarios que no cuentan con tiempo de sesión se crea la columna "session_mins_imputado" con la mediana de los tiempos de sesión de los otros 893 usuarios. Esto para tener una similar a los demás y no afecten estos valores nulos al momento de entrenar los modelos.

<b> Fase 2: Ingeniería de Características con Reglas de Negocio </b>

1.  Script python: "fase_2.py"

2.	Se creó el indicador "session_mins_imputado" con la mediana de los usuarios que sí contaban con tiempo de sesión en el portal con el fin de no alterar la data para entrenar los modelos. Más detalle en el item de Fase 1: 2.c.

<b> Fase 3: Modelado Predictivo y Optimización Financiera </b>

1.	Se usaron 2 modelos: Regresión logística y Random forest. En ambos modelos se tuvo que la probabilidad de que un usuario abandone el portal de negocio está dada al azar, alrededor de 52% en ROC-AUC.

2.	Función matemática operativa: costo_total_errores_financieros(u) = (FP(u)*15)+(FN(u)*70), donde u es el umbral. Se halló el umbral, el cual es de 22%, dando $645 USD de ahorro neto, es decir, un 17.4% de mejora respecto al umbral estándar. Más detalle en el resultado del script "fase_3.py".

<b> Fase 4: Comunicación Ejecutiva y Traducción de Resultados </b>

1. Respuesta en informe_ejecutivo_retencion.pdf
2. Gráficas creadas por medio del script "fase_4.py" y con las imágenes guardadas en "reports/figures" como "grafico_1_campanas.png" y "grafico_2_umbrales.png".
