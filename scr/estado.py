"estado de sesion compartido entre paginas (st.session_state)."
import streamlit as st
def iniciar_estado():
    "crea las variables de sesion la primera vez que se abre la app."
    st.session_state.setdefault("partida", None ) #partida en curso
    st.session_state.setdefault("historial", []) #partidas terminadas
    st.session_state.setdefault("registros_consultados", []) #jugadores vistos en explorar
