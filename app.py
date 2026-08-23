import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuración de página móvil/tablet
st.set_page_config(page_title="Demo Operativa - Pizzería", layout="wide")

st.title("🍕 Monitor de Operaciones y Capacidad")
st.caption("Simulación de picos de demanda, cuellos de botella y venta perdida")

# 1. Métricas clave (KPIs)
col1, col2, col3 = st.columns(3)
col1.metric("Venta Max. Estimada / Hora", "120 Porciones", "Límite Horno")
col2.metric("Tiempo Medio en Caja", "45 seg / cliente", "Fricción Alta")
col3.metric("Pérdida por Cola (Estimada)", "15-20%", "Gente que se va")

st.divider()

# 2. Mapa de calor de demanda por franja horaria
st.subheader("🔥 Concentración de la Demanda (Viernes a Domingo)")

horas = [f"{h}:00" for h in range(18, 24)]
dias = ["Viernes", "Sábado", "Domingo"]
# Datos de porciones demandadas
demanda = np.array([
    [20, 45, 110, 130, 85, 30],  # Viernes
    [25, 50, 125, 140, 90, 35],  # Sábado
    [15, 35, 95,  115, 60, 20]   # Domingo
])

fig_heatmap = px.imshow(
    demanda, 
    x=horas, 
    y=dias, 
    color_continuous_scale="Reds",
    labels=dict(x="Hora", y="Día", color="Porciones"),
    text_auto=True
)
fig_heatmap.update_layout(height=300)
st.plotly_chart(fig_heatmap, use_container_width=True)

st.info("💡 **Conclusión del gráfico:** Entre las 20:30 y las 22:30 la demanda supera la capacidad máxima del horno (120 porciones/h). Un canal de pedido online escalonado reparte la carga.")

st.divider()

# 3. Comparativa de Canales (Mostrador vs. Online Directo)
st.subheader("🚀 Impacto de Abrir Canal Pedido Online (Takeaway)")

data_canales = pd.DataFrame({
    "Canal": ["Mostrador Actual", "Mostrador + Online Directo"],
    "Porciones Despachadas / Noche": [350, 480],
    "Cuello de Botella en Caja": ["Alto", "Bajo"]
})

fig_bar = px.bar(
    data_canales, 
    x="Canal", 
    y="Porciones Despachadas / Noche", 
    color="Canal",
    text="Porciones Despachadas / Noche",
    color_discrete_sequence=["#EF553B", "#00CC96"]
)
fig_bar.update_layout(height=350, showlegend=False)
st.plotly_chart(fig_bar, use_container_width=True)
