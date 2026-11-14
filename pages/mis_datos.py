"mis datos: resumen de la actividad del usuario durante la sesion."
import pandas as pd
import streamlit as st
st.title("👤 Mis datos")

historial = st.session_state.historial
consultados = st.session_state.registros_consultados

if not historial and not consultados:
    st.info("🎯 Aún no hay actividad. Juega una partida o explora los datos y vuelve aquí.")
    st.stop()

st.subheader("🏆 Resumen")
c1, c2, c3 = st.columns(3)
c1.metric("partidas jugadas", len(historial))
c2.metric("mejor puntaje", max((p["puntos"] for p in historial), default=0))
c3.metric("jugadores consultados", len(consultados))

if historial:
    st.subheader("📜 Historial")
    st.dataframe(pd.DataFrame(historial), hide_index=True)
    #TODO: grafico de la evolucion de los puntajes (plotly express)
