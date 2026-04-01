
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cabina di Regia ATS Medio Molise", layout="wide")
st.title("📊 Cabina di Regia: ATS Medio Molise")
st.markdown("Monitoraggio FUA 2026, LEPS, Infrastrutture, Fundraising e Impatto")

try:
    # Lettura dei dati dai 4 fogli
    df_budget = pd.read_excel("dati_ats.xlsx", sheet_name="Budget_FUA")
    df_impatto = pd.read_excel("dati_ats.xlsx", sheet_name="Target_LEPS")
    df_progetto = pd.read_excel("dati_ats.xlsx", sheet_name="Progetti_ATS")
    df_bandi = pd.read_excel("dati_ats.xlsx", sheet_name="Pipeline_Bandi")

    # Creazione di 4 schede (Tabs)
    tab1, tab2, tab3, tab4 = st.tabs([
        "🛡️ Area Welfare e LEPS", 
        "🏢 Infrastrutture Sociali", 
        "💶 Pipeline Bandi", 
        "🌍 Impatto Agenda 2030"
    ])

    # --- TAB 1: WELFARE ---
    with tab1:
        st.header("Gestione Fondo Unico d'Ambito (FUA) e Target")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Ripartizione Finanziaria FUA")
            fig_budget = px.pie(df_budget, values=df_budget.columns[2], names=df_budget.columns[0], hole=0.4)
            st.plotly_chart(fig_budget, use_container_width=True)
        with col2:
            st.subheader("Avanzamento Livelli Essenziali (LEPS)")
            fig_impatto_line = px.line(df_impatto, x=df_impatto.columns[0], y=df_impatto.columns[1:], markers=True)
            st.plotly_chart(fig_impatto_line, use_container_width=True)

    # --- TAB 2: PROGETTI E INFRASTRUTTURE ---
    with tab2:
        st.header("Avanzamento Progetti ATS")
        df_progetto[df_progetto.columns[1]] = pd.to_datetime(df_progetto[df_progetto.columns[1]])
        df_progetto[df_progetto.columns[2]] = pd.to_datetime(df_progetto[df_progetto.columns[2]])
        fig_gantt = px.timeline(df_progetto, x_start=df_progetto.columns[1], x_end=df_progetto.columns[2], 
                                y=df_progetto.columns[0], color=df_progetto.columns[3],
                                color_continuous_scale="Blues", title="Cronoprogramma Interventi")
        fig_gantt.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_gantt, use_container_width=True)

    # --- TAB 3: FUNDRAISING E BANDI EUROPEI ---
    with tab3:
        st.header("Radar Finanziamenti e Co-progettazione")
        col3, col4 = st.columns([2, 1])
        with col3:
            st.dataframe(df_bandi, use_container_width=True, hide_index=True)
        with col4:
            st.subheader("Potenziale Economico")
            fig_bandi = px.bar(df_bandi, x=df_bandi.columns[4], y=df_bandi.columns[3], 
                               color=df_bandi.columns[4], title="Budget Richiesto per Stato (€)")
            st.plotly_chart(fig_bandi, use_container_width=True)

    # --- TAB 4: IMPATTO OPEN IMPACT (AGENDA 2030) ---
    with tab4:
        st.header("🌍 Valutazione di Impatto: Agenda 2030")
        st.markdown("Distribuzione dei fondi per gli Obiettivi di Sviluppo Sostenibile (SDG) dell'ONU.")
        
        # Grafico a Raggiera (Sunburst) - Legge colonna 4 (SDG) e colonna 5 (Budget)
        fig_sunburst = px.sunburst(
            df_progetto, 
            path=[df_progetto.columns[4], df_progetto.columns[0]], 
            values=df_progetto.columns[5],
            color=df_progetto.columns[4],
            title="Investimenti ATS per Obiettivi ONU"
        )
        fig_sunburst.update_traces(textinfo="label+percent entry")
        st.plotly_chart(fig_sunburst, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Errore di lettura: {e}. Controlla che i nomi dei fogli e il file Excel siano corretti e salvati.")