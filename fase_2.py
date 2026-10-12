# Fase 2: Ingeniería de Características con Reglas de Negocio

import os
import pandas as pd

# Traer dataframe limpio


# Sacar promedio de total_compras 
prom_total_compras = df['total_compras'].mean()

print(prom_total_compras)

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

print(df.sort_values('deudor_alta_viabilidad', ascending=False).head())
