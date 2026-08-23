import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuración de página para tablet/móvil
st.set_page_config(page_title="Operaciones - Pizzería", layout="wide")

st.title("🍕 Diagnóstico Operativo y Escandallo")
st.caption("Análisis de márgenes por porción, picos de demanda y propuestas de crecimiento")

st.divider()

# ==========================================
# 1. TABLA DE ESCANDALLO Y MÁRGENES POR TROZO
# ==========================================
st.subheader("1. Análisis de Margen Directo por Porción (Escandallo)")

data_pizzas = {
    "Pizza / Porción": ["Margarita Clásica", "Pepperoni & Queso", "Cuatro Quesos", "Especial de la Casa", "Vegetariana"],
    "Precio Venta (€)": [2.20, 2.50, 2.60, 2.80, 2.40],
    "Coste Ingredientes (€)": [0.45, 0.70, 0.85, 0.95, 0.55],
    "Coste Masa y Envoltorio (€)": [0.20, 0.20, 0.20, 0.20, 0.20],
}

df_pizzas = pd.DataFrame(data_pizzas)
df_pizzas["Coste Total (€)"] = df_pizzas["Coste Ingredientes (€)"] + df_pizzas["Coste Masa y Envoltorio (€)"]
df_pizzas["Margen Neto (€)"] = df_pizzas["Precio Venta (€)"] - df_pizzas["Coste Total (€)"]
df_pizzas["% Margen"] = ((df_pizzas["Margen Neto (€)"] / df_pizzas["Precio Venta (€)"]) * 100).round(1)

# Renderizado de la tabla interactiva
st.dataframe(
    df_pizzas.style.format({
        "Precio Venta (€)": "{:.2f} €",
        "Coste Ingredientes (€)": "{:.2f} €",
        "Coste Masa y Envoltorio (€)": "{:.2f} €",
        "Coste Total (€)": "{:.2f} €",
        "Margen Neto (€)": "{:.2f} €",
        "% Margen": "{:.1f} %"
    }),
    use_container_width=True,
    hide_index=True
)

st.divider()

# ==========================================
# 2. CURVAS DE DEMANDA ACUMULADA VS. CAPACIDAD
# ==========================================
st.subheader("2. Curvas de Demanda vs. Capacidad del Horno")

# Selector de día para la demo
dia_seleccionado = st.radio("Selecciona el día para evaluar la curva:", ["Viernes", "Sábado"], horizontal=True)

# Simulación de horas (12:00 a 23:00)
horas = [f"{h}:00" for h in range(12, 24)]

if dia_seleccionado == "Viernes":
    # Viernes: Pico moderado a mediodía (13-15h), pico muy fuerte de noche (20-22:30h)
    margarita = [10, 25, 30, 15, 10, 10, 20, 45, 60, 50, 25, 10]
    pepperoni = [8,  20, 25, 10,  5,  5, 15, 35, 50, 40, 20,  5]
    especial  = [5,  15, 20,  5,  5,  5, 10, 30, 40, 30, 15,  5]
else:
    # Sábado: Picos muy altos tanto a mediodía como por la noche
    margarita = [15, 40, 45, 20, 10, 15, 30, 55, 65, 60, 35, 15]
    pepperoni = [12, 35, 40, 15,  8, 10, 25, 45, 55, 50, 25, 10]
    especial  = [10, 25, 30, 10,  5,  8, 20, 40, 45, 40, 20,  5]

# Límite de producción diario constante (línea recta)
capacidad_maxima = [100] * len(horas)

# Creación del gráfico con Plotly
fig = go.Figure()

# Áreas acumuladas por tipo de pizza
fig.add_trace(go.Scatter(x=horas, y=margarita, name="Margarita Clásica", mode='lines', stackgroup='one', fillcolor='rgba(255, 99, 71, 0.6)'))
fig.add_trace(go.Scatter(x=horas, y=pepperoni, name="Pepperoni & Queso", mode='lines', stackgroup='one', fillcolor='rgba(255, 165, 0, 0.6)'))
fig.add_trace(go.Scatter(x=horas, y=especial, name="Especiales / Resto", mode='lines', stackgroup='one', fillcolor='rgba(154, 205, 50, 0.6)'))

# Línea recta de capacidad máxima de producción (Horno + Vitrina)
fig.add_trace(go.Scatter(
    x=horas, y=capacidad_maxima, 
    name="Capacidad Máxima Horno (100 porciones/h)", 
    mode='lines', 
    line=dict(color='red', width=3, dash='dash')
))

fig.update_layout(
    title=f"Demanda Acumulada por Horas ({dia_seleccionado}) vs. Límite de Producción",
    xaxis_title="Hora del Día",
    yaxis_title="Porciones Demandadas / Hora",
    hovermode="x unified",
    height=450,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

st.error("⚠️ **Punto Crítico Detectado:** En las franjas de 20:00 a 22:30 la curva de demanda acumulada supera la línea roja de capacidad. En ese momento hay pérdida de clientes por tiempo de espera o falta de porciones listas.")

st.divider()

# ==========================================
# 3. PROPUESTAS DE VALOR Y PLAN DE ACCIÓN
# ==========================================
st.subheader("3. Propuestas Estratégicas de Mejora")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("### 🛒 1. Pedidos Online Directos")
    st.write(
        "Implementar un canal propio de **Takeaway/Click & Collect** sin pasar por comisiones de plataformas tipo Glovo. "
        "Permite al cliente encargar y pagar por adelantado, aplanando la curva de demanda en picos al repartir los encargos por franjas."
    )

with col_b:
    st.markdown("### ⚡ 2. Pre-horneado Optimizado")
    st.write(
        "Utilizar los datos históricos de ventas por hora para programar la producción de masa y hornos **30 minutos antes del pico**. "
        "Garantiza tener la vitrina cargada al 100% con los sabores estrella justo cuando empieza la cola en mostrador."
    )

with col_c:
    st.markdown("### 📱 3. Presencia Digital Local")
    st.write(
        "Crear una estrategia en redes sociales centrada en contenido visual del producto recién horneado y enlaces directos al canal de pedidos. "
        "Captura clientes potenciales que están en la zona pero no quieren hacer colas a ciegas."
    )
