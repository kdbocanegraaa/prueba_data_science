# Fase 4: Comunicación Ejecutiva y Traducción de Resultados

import os
import pandas as pd

import matplotlib.pyplot as plt

# Definición de rutas relativas dinámicas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN_DATA_PATH = os.path.join(BASE_DIR, "data", "retencion_clientes_limpio.csv")
F1_PATH = os.path.join(BASE_DIR, "reports" ,"figures", "grafico_1_campanas.png")
F2_PATH = os.path.join(BASE_DIR, "reports" ,"figures", "grafico_2_umbrales.png")


# Cargar archivo de datos de muestras
df = pd.read_csv(CLEAN_DATA_PATH, sep=',')


# Configuración visual ejecutiva
plt.style.use('seaborn-v0_8-whitegrid')

# -------------------------------------------------------------
# GRÁFICO 1: Barras Apiladas - Retención vs Churn por Campaña
# -------------------------------------------------------------
ct = pd.crosstab(df['campana_origen'], df['churn_flag'])
ct.columns = ['Retenidos (0)', 'Cancelados / Churn (1)']

fig, ax = plt.subplots(figsize=(8, 5))
colors = ['#2b5c8f', '#d9534f'] # Azul corporativo y Rojo alerta

bars = ct.plot(kind='bar', stacked=True, color=colors, ax=ax, width=0.55, edgecolor='none')

plt.title('Distribución de Retención y Cancelación por Campaña de Origen', fontsize=13, fontweight='bold', pad=15)
plt.xlabel('Campaña de Origen', fontsize=10, fontweight='bold')
plt.ylabel('Cantidad de Usuarios', fontsize=10, fontweight='bold')
plt.xticks(rotation=0, fontsize=10)
plt.yticks(fontsize=10)
plt.legend(title='Estado del Cliente', frameon=True, facecolor='white', edgecolor='none')

# Etiquetas de porcentaje sobre cada columna
total_por_campana = ct.sum(axis=1)
for i, col in enumerate(ct.index):
    churn = ct.loc[col, 'Cancelados / Churn (1)']
    tot = total_por_campana[col]
    pct_churn = (churn / tot) * 100
    ax.text(i, tot + 8, f'Churn: {pct_churn:.1f}%', ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#d9534f')

plt.tight_layout()
plt.savefig(F1_PATH, dpi=300)
plt.show()

# -------------------------------------------------------------
# GRÁFICO 2: Comparativa Financiera - Modelo Base vs Optimizado
# -------------------------------------------------------------
# Valores calculados en la malla de prueba (Test Set = 279 clientes)
costos_data = {
    'Modelo / Estrategia': ['Modelo Base\n(Umbral Standard 0.50)', 'Modelo Optimizado\n(Umbral Calibrado 0.22)'],
    'Falsos Positivos ($15 c/u)': [32 * 15, 157 * 15], # $480 vs $2,355  
    'Falsos Negativos ($70 c/u)': [46 * 70, 10 * 70]   # $3,220 vs $700
}

df_costos = pd.DataFrame(costos_data).set_index('Modelo / Estrategia')

fig, ax = plt.subplots(figsize=(8, 4.5))
colors_fin = ['#f0ad4e', '#c9302c'] # Naranja (FP) y Rojo oscuro (FN)

bars_fin = df_costos.plot(kind='barh', stacked=True, color=colors_fin, ax=ax, width=0.45, edgecolor='none')

plt.title('Impacto Financiero Operativo: Modelo Base vs. Modelo Optimizado', fontsize=13, fontweight='bold', pad=15)
plt.xlabel('Pérdida Económica Total por Errores ($ USD)', fontsize=10, fontweight='bold')
plt.ylabel('')
plt.yticks(fontsize=10)
plt.legend(title='Desglose de Costo Financiero', frameon=True, facecolor='white', edgecolor='none')

# Anotar totales al final de cada barra
totales = df_costos.sum(axis=1)
for i, (idx, total) in enumerate(totales.items()):
    ax.text(total + 100, i, f'${total:,.0f} USD', va='center', ha='left', fontsize=11, fontweight='bold', color='#222222')

plt.xlim(0, 6200)
plt.tight_layout()
plt.savefig(F2_PATH, dpi=300)
plt.show()