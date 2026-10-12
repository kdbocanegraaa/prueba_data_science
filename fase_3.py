# Fase 3: Modelado Predictivo y Optimización Financiera

# Librerias a usar:
import os
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression # Regresión Logística
from sklearn.ensemble import RandomForestClassifier # Random Forest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

# Definición de rutas relativas dinámicas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN_DATA_PATH = os.path.join(BASE_DIR, "data", "retencion_clientes_limpio.csv")

# Cargar archivo de datos de muestras
df = pd.read_csv(CLEAN_DATA_PATH, sep=',')


# 1. Modelado Predictivo: Regresión Logística y Random Forest

# Definir la variable objetivo (y) y las variables predictoras (X)
X = df[['edad', 'ticket_promedio', 'total_compras', 'deudor_alta_viabilidad', 'session_nulo','session_mins_imputado']].fillna(0)
y = df['churn_flag']

# Dividir en conjuntos de entrenamiento (Train) y prueba (Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Escalar variables para Regresión Logística
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -------------------------------------------------------------
# MODELO 1: Regresión Logística (con class_weight='balanced')
# -------------------------------------------------------------
modelo_lr = LogisticRegression(random_state=42, class_weight='balanced')
modelo_lr.fit(X_train_scaled, y_train)
y_pred_lr = modelo_lr.predict(X_test_scaled)
y_prob_lr = modelo_lr.predict_proba(X_test_scaled)[:, 1]

print("=== REGRESIÓN LOGÍSTICA (BALANCEADA) ===")
print("ROC-AUC Score:", roc_auc_score(y_test, y_prob_lr))
print(classification_report(y_test, y_pred_lr))

# -------------------------------------------------------------
# MODELO 2: Random Forest (con class_weight='balanced')
# -------------------------------------------------------------
modelo_rf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
modelo_rf.fit(X_train, y_train)
y_pred_rf = modelo_rf.predict(X_test)
y_prob_rf = modelo_rf.predict_proba(X_test)[:, 1]

print("=== RANDOM FOREST (BALANCEADO) ===")
print("ROC-AUC Score:", roc_auc_score(y_test, y_prob_rf))
print(classification_report(y_test, y_pred_rf))


# 2. Calibración y Ajuste de Umbral (Threshold Tuning):

# Definición de la Función de Pérdida Financiera Operativa
def evaluar_costo_operativo(y_true, y_probs, umbral, costo_fp=15, costo_fn=70):
    """
    Calcula el Costo Total de Errores Financieros según las decisiones del modelo.
    
    Parámetros:
    - costo_fp: Costo de incentivar/retener a un cliente que NO iba a cancelar ($15 USD).
    - costo_fn: Pérdida económica por NO detectar a un cliente que abandona ($100 USD).
    """
    # Convertir probabilidades en decisiones binarias según el umbral
    y_pred = (y_probs >= umbral).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    
    # Ecuación de Costo Financiero
    costo_total = (fp * costo_fp) + (fn * costo_fn)
    return costo_total, fp, fn, tp, tn

# Creación de la Malla / Grid Search (100 puntos entre 0.01 y 0.99)
malla_umbrales = np.linspace(0.01, 0.99, 100)
resultados_malla = []

# Iterar sobre cada punto de la malla para evaluar el desempeño financiero
for u in malla_umbrales:
    costo, fp, fn, tp, tn = evaluar_costo_operativo(
        y_test, y_prob_rf, umbral=u, costo_fp=15, costo_fn=70
    )
    resultados_malla.append({
        'umbral': u, 
        'costo_total': costo, 
        'FP': fp, 
        'FN': fn, 
        'TP': tp, 
        'TN': tn
    })

# Convertir los resultados a un DataFrame de Pandas
df_malla = pd.DataFrame(resultados_malla)

# Extraer el Modelo Base (umbral = 0.50) y el Umbral Óptimo (Mínimo Costo)
modelo_base = df_malla.loc[(df_malla['umbral'] - 0.50).abs().idxmin()]
modelo_optimo = df_malla.loc[df_malla['costo_total'].idxmin()]

# Presentación Cuantitativa del Beneficio Financiero
print("\n=================================================")
print("  EVALUACIÓN FINANCIERA Y CALIBRACIÓN DE UMBRAL  ")
print("=================================================")
print(f"1. Modelo Base (Umbral Estándar 0.50):")
print(f"   - Costo Total por Errores: ${modelo_base['costo_total']:,.2f} USD")
print(f"   - Falsos Negativos (Churn no detectado): {int(modelo_base['FN'])}")
print(f"   - Falsos Positivos (Gasto inútil de retención): {int(modelo_base['FP'])}")

print(f"\n2. Modelo Optimizado (Umbral Óptimo {modelo_optimo['umbral']:.2f}):")
print(f"   - Costo Total por Errores: ${modelo_optimo['costo_total']:,.2f} USD")
print(f"   - Falsos Negativos (Churn no detectado): {int(modelo_optimo['FN'])}")
print(f"   - Falsos Positivos (Gasto inútil de retención): {int(modelo_optimo['FP'])}")

ahorro_neto = modelo_base['costo_total'] - modelo_optimo['costo_total']
mejora_pct = (ahorro_neto / modelo_base['costo_total']) * 100

print(f"\n3. Impacto Operativo Demostrado:")
print(f"   - Ahorro Neto Obtenido: ${ahorro_neto:,.2f} USD")
print(f"   - Reducción del Costo Operativo: {mejora_pct:.1f}%")
