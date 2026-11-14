"explorar: tabla de jugadores y sus estadisticas."
import plotly.express as px
import streamlit as st
from scr.data import obtener_datos
df = obtener_datos()
st.title("📊 explorar")
# filtros barra lateral
st.sidebar.header("🔎 filtros")
selecciones = st.sidebar.multiselect("seleccion", sorted(df["seleccion"].unique()))
posiciones = st.sidebar.multiselect("posicion", sorted(df["posicion"].unique()))
min_g, max_g = int(df["goles_mundial"].min()), int(df["goles_mundial"].max())
rango = st.sidebar.slider("goles en el mundial", min_g, max_g, (min_g, max_g))

filtrado = df[df["goles_mundial"].between(*rango)]
if selecciones:
    filtrado = filtrado[filtrado["seleccion"].isin(selecciones)]
if posiciones:
    filtrado = filtrado[filtrado["posicion"].isin(posiciones)]

if filtrado.empty:
    st.warning("ningun jugador cumple esos filtros. prueba con otros valores.")
    st.stop()

# estadisticas
c1, c2, c3 = st.columns(3)
c1.metric("jugadores", len(filtrado))
c2.metric("goles totales", int(filtrado["goles_mundial"].sum()))
c3.metric("edad promedio", round(filtrado["edad"].mean(), 1))

# tabla con seleccion
st.subheader("📋 jugadores")
tabla = st.dataframe(filtrado, on_select="rerun", selection_mode="single-row", hide_index=True)
if tabla.selection.rows:
    jugador = filtrado.iloc[tabla.selection.rows[0]]
    st.subheader(f"🔍 {jugador['jugador']}")
    st.write(f"{jugador['seleccion']} · {jugador['posicion']} · {jugador['club']}")
    # TODO: mostrar mas detalle y guardar el registro en st.session_state.registros_consultados

# graficos
st.subheader("📈 visualizaciones")
# TODO: al menos dos graficos con plotly express, por ejemplo:
# px.bar(filtrado, x="jugador", y="goles_mundail")
# px.scatter(filtrado, x="partidos", y="goles_mundial", color="posicion")    