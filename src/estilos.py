"identidad compartida de la aplicacion."
import streamlit as st
NOMBRE_APP = "Balón de Oro"
EQUIPO = "Balón de Oro"
PALETA = {
    "cesped": "#0B5D3B",
    "oro": "#E3A81B",
    "fondo": "#F4F7F3",
    "tarjeta": "#E4EDE3",
    "texto": "#14231B",
}
def aplicar_estilos():
    "muestra el nombre de la app con componentes nativos de streamlit."
    st.title(NOMBRE_APP)
    st.caption(EQUIPO)

