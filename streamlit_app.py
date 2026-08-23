import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Configuració de pàgina per a tauleta/mòbil
st.set_page_config(page_title="Coques i Panadons Montse", layout="wide")

# Capçalera amb el nom del local
st.title("🍕 Coques i Panadons Montse")
# st.subtitle("Diagnòstic Operatiu, Escandallat i Pla de Creixement")

st.divider()

# ==========================================
# 1. TAULA D'ESCANDALLAT I MARGES PER TROS
# ==========================================
st.subheader("1. Anàlisi dels marges per porció")

data_pizzas = {
    "Producte / Varietat": ["Escalivada", "Carbassó", "Ceba", "Empanada / Panadó", "Albergínia i Mel", "Ceba i Bolets"],
    "Preu Venda (€)": [2.40, 2.30, 2.20, 2.80, 2.60, 2.50],
    "Cost Ingredients (€)": [0.60, 0.50, 0.40, 0.90, 0.70, 0.65],
    "Cost Massa i Embolic (€)": [0.20, 0.20, 0.20, 0.20, 0.20, 0.20],
}

df_pizzas = pd.DataFrame(data_pizzas)
df_pizzas["Cost Total (€)"] = df_pizzas["Cost Ingredients (€)"] + df_pizzas["Cost Massa i Embolic (€)"]
df_pizzas["Marge Net (€)"] = df_pizzas["Preu Venda (€)"] - df_pizzas["Cost Total (€)"]
df_pizzas["% Marge"] = ((df_pizzas["Marge Net (€)"] / df_pizzas["Preu Venda (€)"]) * 100).round(1)

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
# 2. CORBES DE DEMANDA VS. CAPACITAT (HORARI REAL)
# ==========================================
st.subheader("2. Demanda vs. Capacitat (Horari: 9h-14h i 17h-21h)")

dia_seleccionat = st.radio("Selecciona el dia per avaluar la corba:", ["Divendres", "Dissabte"], horizontal=True)

# Hores reals d'apertura (amb parada de 14h a 17h)
hores = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00 (Tancat)", "17:00 (Obert)", "18:00", "19:00", "20:00", "21:00"]

if dia_seleccionat == "Divendres":
    # Matí estable, pico a les 13h-14h. Tarda pico molt fort a les 19h-20:30h
    escalivada      = [5,  8, 12, 18, 25, 0, 0, 15, 25, 30, 15]
    carbasso        = [4,  6, 10, 14, 20, 0, 0, 12, 20, 24, 10]
    ceba            = [6, 10, 15, 22, 30, 0, 0, 18, 30, 35, 18]
    empanada        = [3,  5,  8, 12, 18, 0, 0, 10, 16, 20,  8]
    alberginia_mel  = [4,  6, 10, 15, 22, 0, 0, 12, 22, 26, 12]
    ceba_bolets     = [3,  5,  9, 14, 20, 0, 0, 11, 20, 25, 10]
else:
    # Dissabte: Pics alts a migdia (compres de cap de setmana) i a la tarda
    escalivada      = [8, 12, 18, 25, 32, 0, 0, 18, 28, 32, 18]
    carbasso        = [6, 10, 14, 20, 26, 0, 0, 14, 22, 26, 12]
    ceba            = [9, 15, 22, 30, 38, 0, 0, 22, 34, 38, 20]
    empanada        = [5,  8, 12, 16, 22, 0, 0, 12, 18, 22, 10]
    alberginia_mel  = [6, 10, 15, 22, 28, 0, 0, 15, 24, 28, 14]
    ceba_bolets     = [5,  9, 14, 20, 25, 0, 0, 14, 22, 25, 12]

# Capacitat màxima ajustada a 90 porcions per hora (0 quan està tancat)
capacitat_maxima = [90, 90, 90, 90, 90, 45, 45, 90, 90, 90, 90, 90]

fig = go.Figure()

fig.add_trace(go.Scatter(x=hores, y=ceba, name="Ceba", mode='lines', stackgroup='one', fillcolor='rgba(255, 99, 71, 0.6)'))
fig.add_trace(go.Scatter(x=hores, y=escalivada, name="Escalivada", mode='lines', stackgroup='one', fillcolor='rgba(255, 165, 0, 0.6)'))
fig.add_trace(go.Scatter(x=hores, y=carbasso, name="Carbassó", mode='lines', stackgroup='one', fillcolor='rgba(154, 205, 50, 0.6)'))
fig.add_trace(go.Scatter(x=hores, y=alberginia_mel, name="Albergínia i Mel", mode='lines', stackgroup='one', fillcolor='rgba(147, 112, 219, 0.6)'))
fig.add_trace(go.Scatter(x=hores, y=ceba_bolets, name="Ceba i Bolets", mode='lines', stackgroup='one', fillcolor='rgba(222, 184, 135, 0.6)'))
fig.add_trace(go.Scatter(x=hores, y=empanada, name="Empanada / Panadó", mode='lines', stackgroup='one', fillcolor='rgba(70, 130, 180, 0.6)'))

fig.add_trace(go.Scatter(
    x=hores, y=capacitat_maxima, 
    name="Capacitat Forn (90 porcions/h)", 
    mode='lines', 
    line=dict(color='red', width=3, dash='dash')
))

fig.update_layout(
    title=f"Demanda Acumulada per Hores ({dia_seleccionat}) vs. Capacitat del Local",
    xaxis_title="Hora del Dia",
    yaxis_title="Porcions Demandades / Hora",
    hovermode="x unified",
    height=450,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

st.error("⚠️ **Punt Crític Operatiu:** Les franges de 13:00 a 14:00 i de 19:00 a 20:30 la demanda frega o supera la capacitat de 90 porcions/hora del forn, generant cues al carrer i pèrdua de clients que no volen esperar.")

st.divider()

# ==========================================
# 3. PROPOSTES ESTRATÈGIQUES I NOU CANALS
# ==========================================
st.subheader("3. Oportunitats Estratègiques de Creixement")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⚡ 1. Enfornat Previ Optimitzat")
    st.write(
        "Utilitzar les dades històriques de vendes per hores per programar la producció, anticipant agotament de certs gustos **30 minuts abans del pic de demanda**. "
        "Garaneix tenir el taulell carregat al 100% amb les varietats estrella just al començament de les hores pic."
    )
    
    st.markdown("### 🌐 3. Nova Web i Comandes En Línia (Takeaway)")
    st.write(
        "**Problema actual:** La pàgina web del local està inactiva, perdent visibilitat a Google i comandes directes.\n\n"
        "**Solució:** Reactivar una web senzilla amb canal de comanda i pagament previ. "
        "Permet programar la recollida en hores de menys carga i aplanar els pics de demanda de migdia i tarda."
    )  

with col2:
    st.markdown("### 💳 2. Programa de Fidelització de Clients")
    st.write(
        "**Objectiu:** Convertir el comprador ocasional en habitual mitjançant una targeta de fidelització (física o digital per mòbil).\n\n"
        "**Mecanisme:** Premis per acumulació de compres (ex: la 10a porció o coca dolça de regal), augmentant la freqüència de visita setmanal."
    )

    st.markdown("### 🏪 4. Distribució B2B (Locals de Menjar Preparat i Bars)")
    st.write(
        "**Escalabilitat externa:** Vendre coques i panadons en format d'engròs a bars de la zona, cafeteries o establiments de menjar preparat.\n\n"
        "**Impacte:** Garanteix un volum de producció constant a primera hora del matí (fora dels pics de venda directa del local)."
    )
