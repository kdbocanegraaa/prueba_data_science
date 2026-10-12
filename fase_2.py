# Fase 2: Ingeniería de Características con Reglas de Negocio

import os
import pandas as pd

# Definición de rutas relativas dinámicas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN_DATA_PATH = os.path.join(BASE_DIR, "data", "retencion_clientes_limpio.csv")

# Cargar archivo de datos de muestras
df = pd.read_csv(CLEAN_DATA_PATH, sep=',')

# Sacar promedio de total_compras 
prom_total_compras = df['total_compras'].mean()

print(f"Promedio: {prom_total_compras}")

# Crear marca con la Excepción Regulatoria para los ususarios con campaña Black Friday
condicion_black_friday = (
    (df['total_compras'] > prom_total_compras) & 
    (df['ticket_promedio'] > 20) & 
    (df['campana_origen'] == 'Black Friday') 
)

# Crear marca para los demás que no tienen campaña Black Friday
condicion_otros = (
    (df['total_compras'] > prom_total_compras) & 
    (df['ticket_promedio'] > 50) & 
    (df['campana_origen'] != 'Black Friday') 
)

# Definir la columna 'deudor_alta_viabilidad' basada en las condiciones
df['deudor_alta_viabilidad'] = (condicion_black_friday | condicion_otros).astype(int)

# Ver dataframe creado con la nueva columna
print(df.sort_values('deudor_alta_viabilidad', ascending=False).head())

# Sobreescribir el archivo limpio con la nueva columna
df.to_csv(CLEAN_DATA_PATH, index=False)