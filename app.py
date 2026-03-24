import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard ATS Medio Molise", layout="wide")
st.title("📊 Dashboard Direzionale: Piano Sociale di Zona 2026-2028")
st.markdown("Monitoraggio dati sincronizzato con Excel - ATS Medio Molise")

try:
    # --- 1. LEGGI I DATI DA EXCEL ---
    df_budget = pd.read_excel("dati_ats.xlsx", sheet_name="Budget")
    df_impatto = pd.read_excel("dati_ats.xlsx", sheet_name="Impatto")
    df_gantt = pd.read_excel("dati_ats.xlsx", sheet_name="Gantt")

    # --- 2. VISTA BREAKDOWN COSTI ---
    st.header("1. Breakdown Finanziario (FUA 2026)")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribuzione Budget per Fondo")
        fig_budget = px.pie(df_budget, values="Budget 2026", names="Voce di Finanziamento", hole=0.4)
        st.plotly_chart(fig_budget, use_container_width=True)

    with col2:
        st.subheader("Allocazione per Categoria di Intervento")
        fig_bar = px.bar(df_budget, x="Categoria", y="Budget 2026", color="Voce di Finanziamento")
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # --- 3. VISTA IMPATTO SOCIALE ---
    st.header("2. Analisi Impatto: Target di Servizio")
    fig_impatto = px.line(df_impatto, x="Trimestre", y=["Assunzioni Assistenti Sociali", "Famiglie PIPPI"], 
                          markers=True, title="Avanzamento Target (LEPS)")
    st.plotly_chart(fig_impatto, use_container_width=True)

    st.divider()

    # --- 4. VISTA GANTT ---
    st.header("3. Cronoprogramma di Transizione (Gantt)")
    df_gantt["Inizio"] = pd.to_datetime(df_gantt["Inizio"])
    df_gantt["Fine"] = pd.to_datetime(df_gantt["Fine"])

    fig_gantt = px.timeline(df_gantt, x_start="Inizio", x_end="Fine", y="Task", color="Completamento",
                            color_continuous_scale="Greens", title="Fasi di Attuazione")
    fig_gantt.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_gantt, use_container_width=True)

except FileNotFoundError:
    st.error("⚠️ Errore: Non riesco a trovare il file 'dati_ats.xlsx'. Assicurati di averlo salvato nella cartella 'Cruscotto'.")
except Exception as e:
    st.error(f"⚠️ C'è un problema con i dati nel file Excel: {e}")