import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cabina di Regia ATS Medio Molise", layout="wide")
st.title("📊 Cabina di Regia: ATS Medio Molise")
st.markdown("Monitoraggio FUA 2026, LEPS e Progetti di Inclusione Sociale")

try:
    # Lettura dei dati
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
            # Legge in automatico i dati indipendentemente dal titolo della colonna
            fig_budget = px.pie(df_budget, values=df_budget.columns[2], names=df_budget.columns[0], hole=0.4)
            st.plotly_chart(fig_budget, use_container_width=True)
            
        with col2:
            st.subheader("Avanzamento Livelli Essenziali (LEPS)")
            # Assegna la prima colonna all'asse X e le restanti all'asse Y in automatico
            fig_impatto = px.line(df_impatto, x=df_impatto.columns[0], y=df_impatto.columns[1:], markers=True)
            st.plotly_chart(fig_impatto, use_container_width=True)

    with tab2:
        st.header("Avanzamento Progetti e Infrastrutture PNRR/FSE+")
        st.markdown("Monitoraggio dei centri territoriali e dei servizi di inclusione.")
        
        # Converte in automatico le date (colonne 2 e 3)
        df_progetto[df_progetto.columns[1]] = pd.to_datetime(df_progetto[df_progetto.columns[1]])
        df_progetto[df_progetto.columns[2]] = pd.to_datetime(df_progetto[df_progetto.columns[2]])
        
        # Crea il Gantt leggendo le colonne per posizione (0=Task, 1=Inizio, 2=Fine, 3=Completamento)
        fig_gantt = px.timeline(df_progetto, x_start=df_progetto.columns[1], x_end=df_progetto.columns[2], 
                                y=df_progetto.columns[0], color=df_progetto.columns[3],
                                color_continuous_scale="Blues", title="Cronoprogramma Interventi ATS")
        fig_gantt.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_gantt, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Errore di lettura: {e}. Controlla che il file Excel sia salvato e chiuso.")