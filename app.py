"archivo principal: configura la app y arma el menu de navegacion."
from pathlib import Path

import streamlit as st

from src.estado import iniciar_estado
from src.estilos import EQUIPO, NOMBRE_APP, aplicar_estilos

# configuracion general de la pagina
st.set_page_config(page_title=NOMBRE_APP, page_icon="⚽", layout="wide")
aplicar_estilos()
iniciar_estado()
logo = Path("assets/logo.jpeg")

#logo pequeño en la barra lateral
if logo.exists():
    st.logo(str(logo))

# menu de navegacion con un emoji para cada pagina
paginas = [
    st.Page("pages/inicio.py", title="inicio", icon="🏠", default=True),
    st.Page("pages/explorar.py", title="explorar", icon="📊"),
    st.Page("pages/jugar.py", title="jugar", icon="🎮"),
    st.Page("pages/mis_datos.py", title="mis datos", icon="👤"),
]
navegacion = st.navigation(paginas)

# logo grande debajo de las opciones de navegacion
if logo.exists():
    st.sidebar.image(str(logo), width=180)
st.sidebar.markdown(f"### ⚽ {NOMBRE_APP}") 
st.sidebar.caption(f"equipo {EQUIPO}")
navegacion.run()

