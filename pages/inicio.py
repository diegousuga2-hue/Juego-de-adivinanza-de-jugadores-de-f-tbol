"pagina de inicio: presentacion, datos, funcionalidades e indicadores."
import streamlit as st
from scr.data import obtener_datos
from scr.estilos import EQUIPO, NOMBRE_APP

df = obtener_datos()
st.title(f"⚽ {NOMBRE_APP}")
st.write("Adivina que goleador del mundial 2026 se esconde detras de sus estadisticas.")

st.header("📚 Sobre los datos")
st.write(
    "perfiles, goles, asistencias y tarjetas de los 50 maximos goleadores del mundial 2026."
    "fuentes: losmundialesdefutbol.com, futboltotal.futbol (API-Sports) y wikipedia."
)

st.header("🧭 Funcionalidades")
col1, col2, col3 = st.columns(3)
col1.page_link("pages/explorar.py", label="explorar los datos", icon="📊")
col2.page_link("pages/jugar.py", label="jugar", icon="🎮")
col3.page_link("pages/mis_datos.py", label="ver mis datos", icon="👤")

st.header("🔢 Indicadores")
m1, m2, m3 = st.columns(3)
m1.metric("jugadores", len(df))
m2.metric("goles en el mundial", int(df["goles_mundial"].sum()))
m3.metric("selecciones", df["seleccion"].nunique())

st.header("👥 Acerca de")
st.write(f"equipo **{EQUIPO}**: diego alejandro usuga rojas, jesus david plazas rojas y solanye andrea suarez quiceno.")
# TODO: foto de los integrantes (assets/) y objetivos del proyecto.

st.header("📝 Créditos y licencias")
st.caption("TODO: fuentes de datos, recursos graficos y licencia del software.")
