# prueba_data_science - Kevin Bocanegra
Respuestas de la Prueba Técnica para Científico de Datos en Tranqui Finanzas.

Fase 1: Calidad de Datos y Análisis Crítico (EDA)

1. Auditoria Metodológica:

	Extraer información:

	a.  Preevisualizando el archivo con las muestras se evidencia que viene en formato .csv, con varias columnas relacionadas con datos demográficos de la deuda del cliente junto con la campaña estratégica especial que se usó, y adicionalmente trae una columna llamada “metadatos_sesion” relacionada al tiempo de sesión que tuvo el cliente al momento de registrarse en el Portal, esta columna no trae datos para todos los ususarios, algunos vienen en formato json y otros separados por ||.

	b. Teniendo en cuenta lo anterior se realizó un script de extracción en python donde se carga el dataframe, se extraen las columnas de “metadatos_sesion”, y por último se exporta el Excel limpio para analizar.

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

Fase 2: Ingeniería de Características con Reglas de Negocio
1.  Script python
2. Viene relacionado al punto Fase 1: 2.c
Fase 3:
1.	Se usaron 2 modelos, Regresión logística, random forest, en ambos modelos se tuvo que la probabilidad de que un usuario abandone el portal de negocio está dada al azar, alrededor de 52%
2.	costo_total_errores_financieros(u) = (FP(u)*15)+(FP(u)*70), donde u es el umbral.
Fase 4:
	E structura de Reporte Ejecutivo (Máximo 3 párrafos): Redacta la síntesis formal dirigida a la Gerencia de Operaciones y a la Dirección Financiera. El texto debe concluir con absoluta claridad: ¿Qué estrategia o campaña de origen demostró retener mejor a los deudores?, ¿Cuánto presupuesto/dinero proyecta ahorrar el modelo calibrado a la organización en comparación con un escenario sin segmentación predictiva? y ¿Cuál es tu recomendación inmediata para la puesta en producción?

Se cargaron 1.500 registros de la muestra dada, de los cuales se limpiaron datos incongruentes y quedaron 1.396 registros para la muestra a considerar, donde un 35% no contiene datos referentes a la sesión que tuvieron al ingresar al portal de autogestión. Con esto en cuenta se crearon variables como la de identificar un deudor de alta viabilidad, identificar los clientes con y sin datos referentes a su sesión en el portal de autogestión. En total fueron 9 variables que se usaron para entrenar dos modelos predictivos, el de Regresión Logística y el de Random Forest, con el fin de saber la probabilidad de que un usuario fuera churn.
Los resultados de los modelos lanzaron que se tuvo un ROC-AUC muy cercano al 50%, dando un escenario de azar. Con este escenario de azar se concluye que las campañas de origen realmente no están funcionando para retener a los deudores. Con esto en cuenta, evaluando las pérdidas que se podrían obtener entre usuarios Falsos positivos (FP) y Falsos negativos (FN), donde por cada FP se pierden $15 USD y por cada FN se pierden $70 USD, dado un umbral estándar de 50%, se tienen unas pérdidas de $3.700 USD. Optimizando este modelo se obtuvo un umbral de 22%, dando unas pérdidas de $3.055, es decir, un $645 USD de ahorro neto, dando un 17.4% de mejora.
Se recomienda usar el modelo optimizado para campañas de cobranza y retención de usuarios en el portal de autogestión. Adicionalmente, para mejorar la tasa de ROC-AUC con los modelos estadísticos necesitamos enriquecer el dataset con más usuarios churn, dado que la muestra fue muy reducida, donde un 35% de las muestras venían incongruentes con su fecha de cancelación vs fecha de registro, además, necesitamos que todos los usuarios tengan disponible los datos sobre su registro usando el portal de autogestión, además de trae otras variables como el tipo de producto del usuario, y el medio de comunicación que se usó para que contactar al cliente informándole que usara el aplicativo.
