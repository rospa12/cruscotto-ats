import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cabina di Regia ATS Medio Molise", layout="wide")
st.title("📊 Cabina di Regia: ATS Medio Molise")
st.markdown("Monitoraggio FUA 2026, LEPS e Progetti di Inclusione Sociale")

try:
    # Lettura dei dati (Assicurati che i nomi dei fogli siano esatti in Excel)
    df_budget = pd.read_excel("dati_ats.xlsx", sheet_name="Budget_FUA")
    df_impatto = pd.read_excel("dati_ats.xlsx", sheet_name="Target_LEPS")
    df_progetto = pd.read_excel("dati_ats.xlsx", sheet_name="Progetti_ATS")

    # Creazione delle schede (Tabs)
    tab1, tab2 = st.tabs(["🛡️ Area Welfare e LEPS", "🏢 Area Progetti e Infrastrutture Sociali"])

    with tab1:
        st.header("Gestione Fondo Unico d'Ambito (FUA 2026) e Target di Servizio")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Ripartizione Finanziaria FUA")
            fig_budget = px.pie(df_budget, values="Budget 2026", names="Voce di Finanziamento", hole=0.4)
            st.plotly_chart(fig_budget, use_container_width=True)
            
        with col2:
            st.subheader("Avanzamento Livelli Essenziali (LEPS)")
            fig_impatto = px.line(df_impatto, x="Trimestre", y=["Assunzioni Assistenti Sociali", "Famiglie PIPPI Prese in Carico"], markers=True)
            st.plotly_chart(fig_impatto, use_container_width=True)

    with tab2:
        st.header("Avanzamento Progetti e Infrastrutture PNRR/FSE+")
        st.markdown("Monitoraggio dei centri territoriali e dei servizi di inclusione.")
        
        df_progetto["Inizio"] = pd.to_datetime(df_progetto["Inizio"])
        df_progetto["Fine"] = pd.to_datetime(df_progetto["Fine"])
        
        fig_gantt = px.timeline(df_progetto, x_start="Inizio", x_end="Fine", y="Task", color="Completamento",
                                color_continuous_scale="Blues", title="Cronoprogramma Interventi ATS")
        fig_gantt.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_gantt, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Errore di lettura: {e}. Controlla che il file Excel sia salvato e chiuso.")