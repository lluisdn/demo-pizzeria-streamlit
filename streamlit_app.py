import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuració de pàgina per a tauleta/mòbil
st.set_page_config(page_title="Operacions - Pizzeria", layout="wide")

st.title("🍕 Diagnòstic Operatiu i Escandallat")
st.caption("Anàlisi de marges per porció, pics de demanda i propostes de creixement")

st.divider()

# ==========================================
# 1. TAULA D'ESCANDALLAT I MARGES PER TROS
# ==========================================
st.subheader("1. Anàlisi de Marge Directe per Porció (Escandallat)")

# Sabors de la pizzeria
data_pizzas = {
    "Pizza / Porció": ["Escalivada", "Carbassó", "Ceba", "Empanada", "Albergínia i Mel", "Ceba i Bolets"],
    "Preu Venda (€)": [2.40, 2.30, 2.20, 2.80, 2.60, 2.50],
    "Cost Ingredients (€)": [0.60, 0.50, 0.40, 0.90, 0.70, 0.65],
    "Cost Massa i Embolic (€)": [0.20, 0.20, 0.20, 0.20, 0.20, 0.20],
}

df_pizzas = pd.DataFrame(data_pizzas)
df_pizzas["Cost Total (€)"] = df_pizzas["Cost Ingredients (€)"] + df_pizzas["Cost Massa i Embolic (€)"]
df_pizzas["Marge Net (€)"] = df_pizzas["Preu Venda (€)"] - df_pizzas["Cost Total (€)"]
df_pizzas["% Marge"] = ((df_pizzas["Marge Net (€)"] / df_pizzas["Preu Venda (€)"]) * 100).round(1)

# Renderitzat de la taula interactiva
st.dataframe(
    df_pizzas.style.format({
        "Preu Venda (€)": "{:.2f} €",
        "Cost Ingredients (€)": "{:.2f} €",
        "Cost Massa i Embolic (€)": "{:.2f} €",
        "Cost Total (€)": "{:.2f} €",
        "Marge Net (€)": "{:.2f} €",
        "% Marge": "{:.1f} %"
    }),
    use_container_width=True,
    hide_index=True
)

st.divider()

# ==========================================
# 2. CORBES DE DEMANDA ACUMULADA VS. CAPACITAT
# ==========================================
st.subheader("2. Corbes de Demanda vs. Capacitat del Forn")

# Selector de dia per a la demo
dia_seleccionat = st.radio("Selecciona el dia per avaluar la corba:", ["Divendres", "Dissabte"], horizontal=True)

# Simulació d'hores (12:00 a 23:00)
hores = [f"{h}:00" for h in range(12, 24)]

if dia_seleccionat == "Divendres":
    # Divendres: Pic moderat al migdia (13-15h), pic molt fort a la nit (20-22:30h)
    escalivada      = [8,  18, 22, 10, 5, 5, 12, 30, 40, 35, 18, 8]
    carbasso        = [6,  14, 18,  8, 4, 4, 10, 24, 32, 28, 14, 6]
    ceba            = [10, 22, 26, 12, 6, 6, 14, 35, 45, 40, 20, 8]
    empanada        = [5,  12, 15,  6, 3, 3,  8, 20, 25, 22, 10, 4]
    alberginia_mel  = [6,  15, 20,  8, 4, 4, 10, 26, 35, 30, 15, 5]
    ceba_bolets     = [5,  14, 19,  8, 4, 4, 10, 25, 33, 28, 13, 5]
else:
    # Dissabte: Pics molt alts tant al migdia com per la nit
    escalivada      = [12, 28, 32, 14, 8, 10, 20, 38, 45, 42, 22, 10]
    carbasso        = [10, 22, 26, 12, 6,  8, 16, 30, 38, 34, 18,  8]
    ceba            = [14, 32, 38, 16, 8, 12, 24, 42, 50, 46, 26, 12]
    empanada        = [8,  18, 22, 10, 4,  6, 12, 26, 30, 28, 14,  6]
    alberginia_mel  = [10, 24, 28, 12, 6,  8, 18, 34, 42, 38, 20,  8]
    ceba_bolets     = [8,  22, 26, 10, 5,  7, 16, 32, 40, 35, 18,  7]

# Lítim de producció diari constant (línia recta)
capacitat_maxima = [120] * len(hores)

# Creació del gràfic amb Plotly
fig = go.Figure()

# Àrees acumulades per tipus de pizza/producte
fig.add_trace(go.Scatter(x=hores, y=ceba, name="Ceba", mode='lines', stackgroup='one', fillcolor='rgba(255, 99, 71, 0.6)'))
fig.add_trace(go.Scatter(x=hores, y=escalivada, name="Escalivada", mode='lines', stackgroup='one', fillcolor='rgba(255, 165, 0, 0.6)'))
fig.add_trace(go.Scatter(x=hores, y=carbasso, name="Carbassó", mode='lines', stackgroup='one', fillcolor='rgba(154, 205, 50, 0.6)'))
fig.add_trace(go.Scatter(x=hores, y=alberginia_mel, name="Albergínia i Mel", mode='lines', stackgroup='one', fillcolor='rgba(147, 112, 219, 0.6)'))
fig.add_trace(go.Scatter(x=hores, y=ceba_bolets, name="Ceba i Bolets", mode='lines', stackgroup='one', fillcolor='rgba(222, 184, 135, 0.6)'))
fig.add_trace(go.Scatter(x=hores, y=empanada, name="Empanada", mode='lines', stackgroup='one', fillcolor='rgba(70, 130, 180, 0.6)'))

# Línia recta de capacitat màxima de producció
fig.add_trace(go.Scatter(
    x=hores, y=capacitat_maxima, 
    name="Capacitat Màxima Forn (120 porcions/h)", 
    mode='lines', 
    line=dict(color='red', width=3, dash='dash')
))

fig.update_layout(
    title=f"Demanda Acumulada per Hores ({dia_seleccionat}) vs. Límit de Producció",
    xaxis_title="Hora del Dia",
    yaxis_title="Porcions Demandades / Hora",
    hovermode="x unified",
    height=450,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

st.error("⚠️ **Punt Crític Detectat:** En les franges de 20:00 a 22:30 la corba de demanda acumulada supera la línia vermella de capacitat. En aquest moment es produeix pèrdua de clients per temps d'espera o falta de porcions llistes al taulell.")

st.divider()

# ==========================================
# 3. PROPOSTES DE VALOR I PLAN D'ACCIÓ
# ==========================================
st.subheader("3. Propostes Estratègiques de Millora")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("### 🛒 1. Comandes En Línia Directes")
    st.write(
        "Implementar un canal propi de **Takeaway/Click & Collect** sense pagar comissions a plataformes externes (tipus Glovo/Uber Eats). "
        "Permet al client encarregar i pagar per avançat, aplanant la corba de demanda en els pics en repartir els encàrrecs per franges horàries."
    )

with col_b:
    st.markdown("### ⚡ 2. Enfornat Previ Optimitzat")
    st.write(
        "Utilitzar les dades històriques de vendes per hora per programar la producció de massa i el forn **30 minuts abans del pic de demanda**. "
        "Garanteix tenir el taulell carregat al 100% amb les varietats estrella just quan comença la cua a la caixa."
    )

with col_c:
    st.markdown("### 📱 3. Presència Digital Local")
    st.write(
        "Crear una estratègia a xarxes socials centrada en contingut visual del producte acabat d'enfornar i enllaços directes al canal de comandes. "
        "Captura clients potencials de la zona que volen comprar però no volen fer cues a ciegues."
    )
