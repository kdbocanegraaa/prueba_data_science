# Fase 1: Calidad de Datos y Análisis Crítico (EDA)

import os
import pandas as pd
import json

# Definición de rutas relativas dinámicas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "retencion_clientes.xls")
CLEAN_DATA_PATH = os.path.join(BASE_DIR, "data", "retencion_clientes_limpio.csv")

# Cargar archivo de datos de muestras
df = pd.read_csv(RAW_DATA_PATH, sep=',')

# Función para extraer las columnas de metadatos_sesion
def procesar_metadatos(x):
    # Si es un valor nulo o no es texto, devolver diccionario vacío
    if pd.isna(x) or not isinstance(x, str):
        return {'device': None, 'browser': None, 'session_mins': None}
    
    x = x.strip()
    
    # Separar los de formato JSON '{"device": "Mobile", "browser": "Safari", "session_mins": 65}'
    if x.startswith('{') and x.endswith('}'):
        try:
            return json.loads(x)
        except Exception:
            pass
            
    # Separar los de formato 'device: Mobile || browser: Android_Webview || session_mins: 83'
    res = {}
    partes = x.split('||')
    for parte in partes:
        if ':' in parte:
            clave, valor = parte.split(':', 1)
            res[clave.strip()] = valor.strip()
            
    return res

# Extraer y expandir la columna metadatos_sesion
meta_dict = df['metadatos_sesion'].apply(procesar_metadatos)
meta_df = pd.DataFrame(list(meta_dict))

# Integrar las columnas al DataFrame original
df['device'] = meta_df['device']
df['browser'] = meta_df['browser']
df['session_mins'] = pd.to_numeric(meta_df['session_mins'], errors='coerce')

# Clasificador de usuarios con tiempo de sesión vacío
df['session_nulo'] = df['session_mins'].isna().astype(int)

# Imponer la mediana a estos usuarios para posterior modelado
mediana_session = df['session_mins'].median()
df['session_mins_imputado'] = df['session_mins'].fillna(mediana_session)

# Eliminar la columna metadatos_sesion original
df.drop(columns=['metadatos_sesion'], inplace=True)

# Exportar el dataset procesado a la carpeta data/ (Ruta relativa)
df.to_csv(CLEAN_DATA_PATH, index=False)
print(f"Fase 1 completada exitosamente. Dataset limpio guardado en: {CLEAN_DATA_PATH}")
