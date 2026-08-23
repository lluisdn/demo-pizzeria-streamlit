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
# BARRA LATERAL: SELECTOR DE LOCAL
# ==========================================
st.sidebar.header("⚙️ Configuració de la Demo")
local_seleccionat = st.sidebar.selectbox(
    "Selecciona el Local a analitzar:",
    ["Tots els locals (Consolidat)", "Local 1: Centre", "Local 2: Estació", "Local 3: Nord"]
)

# Factores multiplicadores según selección para simular datos por local
multiplicadors = {
    "Tots els locals (Consolidat)": 3.0,
    "Local 1: Centre": 1.2,
    "Local 2: Estació": 1.0,
    "Local 3: Nord": 0.8
}
mult = multiplicadors[local_seleccionat]

# ==========================================
# 1. METRIQUES CLAU (KPIS A DALT DE TOT)
# ==========================================
st.subheader(f"📊 Mètriques Clau de Facturació i Vendes — {local_seleccionat}")

facturacio_base = 1845.50 * mult
unitats_base = int(750 * mult)
tiquet_mitja = 4.85 if "Consolidat" not in local_seleccionat else 4.85
top_producte = "Escalivada" if local_seleccionat != "Local 3: Nord" else "Panadó / Empanada"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Facturació Diària Estima", value=f"{facturacio_base:,.2f} €", delta="+12.4% vs setm. ant.")

with col2:
    st.metric(label="Unitats Venudes / Dia", value=f"{unitats_base} porcions", delta="+8.1%")

with col3:
    st.metric(label="Tiquet Mitjà per Client", value=f"{tiquet_mitja:.2f} €", delta="+0.25 €")

with col4:
    st.metric(label="Producte Més Venut", value=top_producte)

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
capacitat_maxima = [100, 100, 100, 100, 100, 50, 50, 100, 100, 100, 100, 50]

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
# 4. CONTROL DE VARIACIÓ D'INVENTARIS I MERMES
# ==========================================
st.subheader("3. Control de Variació d'Inventaris i Mermes (Sobrants pel Tancament)")

st.write("Avaluació del producte no venut al tancament dels torns (14:00h i 21:00h) per optimitzar l'última enfornada i reduir el devaluat d'inventari.")

data_inventari = {
    "Producte": ["Escalivada", "Carbassó", "Ceba", "Empanada / Panadó", "Albergínia i Mel", "Ceba i Bolets"],
    "Sobrant Torn 14:00h (Porcions)": [int(4 * mult), int(3 * mult), int(6 * mult), int(2 * mult), int(3 * mult), int(2 * mult)],
    "Sobrant Torn 21:00h (Porcions)": [int(7 * mult), int(5 * mult), int(8 * mult), int(4 * mult), int(4 * mult), int(5 * mult)],
}

df_inv = pd.DataFrame(data_inventari)
df_inv["Total Sobrant (Porcions)"] = df_inv["Sobrant Torn 14:00h (Porcions)"] + df_inv["Sobrant Torn 21:00h (Porcions)"]
# Cost mitjà de producció ~ 0.80€
df_inv["Cost Econòmic Merma (€)"] = (df_inv["Total Sobrant (Porcions)"] * 0.80).round(2)

col_inv1, col_inv2 = st.columns([2, 1])

with col_inv1:
    st.dataframe(
        df_inv.style.format({
            "Cost Econòmic Merma (€)": "{:.2f} €"
        }),
        use_container_width=True,
        hide_index=True
    )

with col_inv2:
    total_mermes_cost = df_inv["Cost Econòmic Merma (€)"].sum()
    total_porcions_sobrants = df_inv["Total Sobrant (Porcions)"].sum()
    st.warning(f"📉 **Impacte de Mermes:**\n\n* **Porcions sobrants/dia:** {total_porcions_sobrants} unitats\n* **Cost directe en matèria prima:** {total_mermes_cost:.2f} € / dia\n\n*Ajustant l'últim batch d'enfornat 45 minuts abans del tancament es pot reduir aquesta tírria un 65%.*")

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
