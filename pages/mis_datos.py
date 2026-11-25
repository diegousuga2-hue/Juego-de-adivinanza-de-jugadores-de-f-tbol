"mis datos: resumen de la actividad del usuario durante la sesion."
import pandas as pd
import streamlit as st
import plotly.express as px

from src.data import cargar_datos
from src.estilos import PALETA
from src.fichas import unir_fichas
from src.juego import PUNTOS_ACIERTOS

st.title("👤 Mis datos")
st.caption("Resumen de lo que has hecho en esta sesión. Se actualiza solo mientras juegas y exploras.")


historial = st.session_state.historial
consultados = st.session_state.registros_consultados

# Estado sin actividad
if not historial and not consultados:
    st.info("🎯 Aún no hay actividad. Juega una partida en 🎮 Jugar o abre la ficha de un jugador "
        "en 📊 Explorar, y vuelve aquí.")
    st.stop()

hist = pd.DataFrame(historial)
partidas = len(hist)

# Resumen
st.subheader("🏆 Resumen")
c1, c2, c3, c4 = st.columns(4)
c1.metric("partidas jugadas", partidas)
c2.metric("mejor puntaje", int(hist["puntos"].sum()) if partidas else 0)
c3.metric("mejor resultado", int(hist["puntos"].max()) if partidas else 0)
c4.metric("jugadores consultados", len(consultados))

# Estadisticas del juego
st.subheader("🎮 Estadísticas de juego")
if not partidas:
    st.info("Todavía no has terminado ninguna partida. Ve a 🎮 Jugar para empezar.")
else:
    e1, e2, e3, e4 = st.columns(4)
    e1.metric("puntaje promedio", round(hist["puntos"].mean(), 1))
    e2.metric("porcentaje de aciertos", f"{hist['aciertos'].sum() / hist['rondas'].sum() * 100:.0f} %")
    e3.metric("pistas por partida", round(hist["pistas"].mean(), 1))
    e4.metric("tiempo promedio", f"{hist['segundos'].mean():.0f} s")

    # visualizacion del progreso
    st.subheader("📈 Mi progreso")
    g1, g2 = st.columns(2)
    with g1:
        fig = px.line(hist, x="partida", y="puntos", markers=True,
                      color_discrete_sequence=PALETA["cesped"])
        fig.update_layout(title="puntaje por partida", xaxis_title="Partida", yaxis_title="Puntos",
                          yaxis_range=[0, hist["rondas"].max() * PUNTOS_ACIERTOS],
                          xaxis=dict(dtick=1), heigth=350)
        st.plotly_chart(fig)
    with g2:
        fig = px.bar(hist, x="partida", y="aciertos", text="aciertos", hover_data=["pistas"],
                     color_discrete_sequence=[PALETA["oro"]])
        fig.update_layout(title="Aciertos por partida", xaxis_title="Partida", yaxis_title="Aciertos",
                          yaxis_range=[0, hist["rondas"].max()], xaxis=dict(dtick=1), height=350)
        st.plotly_chart(fig)
    if partidas == 1:
        st.caption("Juega más partidas para ver como evoluciona tu puntaje.")

    # historial
    st.subheader("📜 Historial de partidas")
    tabla = hist.rename(columns={
        "partida": "Partida", "hora": "Hora", "puntos": "Puntos", "aciertos": "Aciertos",
                "rondas": "Rondas", "pistas": "Pistas", "segundos": "Segundos",
    })
    st.dataframe(tabla.loc[::-1], hide_index=True)

# jugadores consultados
st.subheader("🔍 Jugadores consultados en Explorar")
if not consultados:
    st.info("Aun no has abierto la ficha de ningún jugador en 📊 Explorar.")
else:
    datos = cargar_datos()
    fichas, aviso = unir_fichas(datos) if not datos.empty else (datos, "sin datos")
    vistos = fichas[fichas["jugador"].isin(consultados)] if aviso is None else pd.DataFrame()
    if vistos.empty:
        st.write(",".join(consultados))
    else:
        st.dataframe(
            vistos[["jugador", "seleccion", "club", "posicion", "edad", "goles", "asistencias", "partidos"]]
            .rename(columns={"jugador": "Jugador", "seleccion": "Selección", "club": "Club",
                                         "posicion": "Posición", "edad": "Edad", "goles": "Goles",
                                         "asistencias": "Asistencias", "partidos": "Partidos"}),
            hide_index=True,            
        )

