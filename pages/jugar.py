"jugar: ¿Quien es el goleador? se muestran estadisticas y se elige entre 4 opciones. "
import random
import streamlit as st 
from scr.data import obtener_datos
df = obtener_datos()
rondas = 10
st.title("🎮 Jugar")
with st.expander("📖 Instrucciones", expanded=True):
    st.markdown(
        f"""
        - Verás las estadísticas de un goleador del Mundial 2026.
        - Elige entre 4 opciones quién es.
        - Cada partida tiene {rondas} rondas; cada acierto suma puntos.
        """
    )

partida = st.session_state.partida

if partida is None:
    if st.button("▶️ Empezar partida", type="primary"):
        # TODO: crear la partida (rondas jugadores al azar con random.simple)
        st.session_state.partida = {"ronda": 0, "puntos": 0}
        st.rerun()
else:
    st.subheader(f"ronda {partida['ronda'] + 1 } de {rondas} ·  ⭐ {partida['puntos']} puntos")
    # TODO: mostrar las estadisticas del jugador y 4 opciones con st.radio
    col1, col2 = st.columns(2)
    col1.button("✅ Confirmar respuesta", type="primary")
    col2.button("➡️ Siguiente jugador")
    # TODO: al terminar, guardar la partida en st.session_state.historial

if st.button("🔄 Nueva partida"):
    # Reinicia solo la partida en curso: el historial se conserva.
    st.session_state.partida = None
    st.rerun()