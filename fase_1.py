# Prueba data_science

# Fase 1: Calidad de Datos y Análisis Crítico (EDA)

# 1. Auditoría Metodológica:
import pandas as pd
import json

# Leer archivo .csv
df = pd.read_csv(r"C:\Users\Kevin Bocanegra\Downloads\retencion_clientes.xls", sep=',')

# Función para procesar los datos de metadatos_sesion 
def procesar_metadatos(x):
    # Si es un valor nulo o no es texto, devolver diccionario vacío
    if pd.isna(x) or not isinstance(x, str):
        return {'device': None, 'browser': None, 'session_mins': None}
    
    x = x.strip()
    
    # Separar los formato JSON '{"device": "Mobile", "browser": "Safari", "session_mins": 65}'
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

# Separar las columnas de metadatos_sesion
meta_dict = df['metadatos_sesion'].apply(procesar_metadatos)

# Crear dataframe a partir del diccionario de metadatos_sesion
meta_df = pd.DataFrame(list(meta_dict))

# Traer las columnas de metadatos_sesion al dataframe original
df['device'] = meta_df['device']
df['browser'] = meta_df['browser']
df['session_mins'] = pd.to_numeric(meta_df['session_mins'], errors='coerce')

# Crear clasificador que identifique los usuarios con tiempo de sesión nulo
df['session_nulo'] = df['session_mins'].isna().astype(int)

# Dejar los nulos de session_mins con la mediana para el posterior entrenamiento
mediana_session = df['session_mins'].median()
df['session_mins_imputado'] = df['session_mins'].fillna(mediana_session)

# Eliminar columna metadatos_sesion ya que ahora es innecesaria, pues ya se extrajo lo que se necesitaba
df.drop(columns=['metadatos_sesion'], inplace=True)

# Exportar a Excel
df.to_excel(r"C:\Users\Kevin Bocanegra\Downloads\retencion_clientes_limpio.xlsx", index=False)
