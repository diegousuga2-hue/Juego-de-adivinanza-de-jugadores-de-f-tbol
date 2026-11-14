"identidad compartida de la aplicacion."
import streamlit as st
NOMBRE_APP = "Balón de Oro"
EQUIPO = "Balón de Oro"
def aplicar_estilos():
    "muestra el nombre de la app con componentes nativos de streamlit."
    st.title(NOMBRE_APP)
    st.caption(EQUIPO)

