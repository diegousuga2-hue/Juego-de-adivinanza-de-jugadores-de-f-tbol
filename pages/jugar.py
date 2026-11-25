"""ugar: ¿Quien es el goleador? 10 rondas con 4 opciones cada una."""
from pathlib import Path

import pandas as pd
import streamlit as st

from src.data import obtener_datos
from src.fichas import unir_fichas
from src.juego import COSTO_PISTA, MAX_PISTAS, OPCIONES, PUNTOS_ACIERTO, RONDAS, Partida, calificacion

RAIZ = Path(__file__).resolve().parent.parent

st.title("🎮 Jugar")
st.subheader("¿Quien es el goleador?")

df, aviso = unir_fichas(obtener_datos()) 
if aviso:
    st.error(f"El juego necesita los nombres de los jugadores. {aviso}")
    st.stop

def mostrar_imagen(ruta, ancho):
    """Muestra una imagen del proyecto; si no existe, avisa sin romper la página."""
    if isinstance(ruta, str) and (RAIZ / ruta).exists():
        st.image(str(RAIZ / ruta), width=ancho)
    else:
        st.caption("🖼️ Imagen no disponible")

def texto_dato(valor):
    """Devuelve el valor como texto, o «s/d» (sin dato) si está vacío."""
    return "s/d" if pd.isna(valor) else f"{valor:g}" if isinstance(valor, (int, float)) else str(valor)

partida = st.session_state.partida
historial = st.session_state.historial

# instrucciones
with st.expander("📖 Instrucciones", expanded=partida is None):
    st.markdown(
        f"""**Objetivo:** adivinar de qué goleador del Mundial 2026 se trata.
        
                1. Cada partida tiene **{RONDAS} rondas**.
                2. En cada ronda verás las estadísticas de un jugador (posición, edad, goles, asistencias, partidos y faltas).
                3. Elige entre **{OPCIONES} opciones** quién es y pulsa **Confirmar respuesta**.
                4. Acertar suma **{PUNTOS_ACIERTO} puntos**. Si te atascas, puedes pedir hasta **{MAX_PISTAS} pistas**
                   (selección y club), pero cada una **resta {COSTO_PISTA} puntos**.
                5. Al final verás tu puntaje. Tus partidas quedan guardadas mientras dure la sesión."""
    )

# registro de partidas
st.markdown("### 🏅 Tus partidas en esta sesión")
r1, r2, r3 = st.columns(3)
r1.metric("Partidas jugadas", len(historial))
r2.metric("Mejor puntaje", max((p["puntos"] for p in historial), default=0))
r3.metric("Puntaje promedio", round(sum(p["puntos"] for p in historial) / len(historial), 1) if historial else 0)

# sin partida
if partida is None:
    st.info("Pulsa «Empezar partida» para jugar.")
    if st.button("▶️ Empezar partida", type="primary"):
        st.session_state.partida = Partida(df)
        st.rerun()
    st.stop()

# partida terminada
if partida.terminada:
    if not partida.guardada:
        historial.append(partida.registro(len(historial) + 1))
        partida.guardada = True
        if partida.aciertos >= 0.8 * partida.total_rondas:
            st.balloons()

    st.subheader("🏁 Resultado de la partida")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Puntaje", f"{partida.puntos} / {partida.total_rondas * PUNTOS_ACIERTO}")
    m2.metric("Aciertos", f"{partida.aciertos} / {partida.total_rondas}")
    m3.metric("Pistas usadas", partida.pistas_total)
    m4.metric("Tiempo", f"{partida.segundos} s")
    st.write(calificacion(partida.aciertos, partida.total_rondas))

    anteriores = [p["puntos"] for p in historial[:-1]]
    if anteriores and partida.puntos > max(anteriores):
        st.success("🌟 ¡Nuevo mejor puntaje de la sesión!")

    st.dataframe(pd.DataFrame(partida.resultados), hide_index=True)
    if st.button("🔄 Jugar otra partida", type="primary"):
        st.session_state.partida = Partida(df)
        st.rerun()
    st.stop()

# partida en curso
j = partida.jugador
st.progress(partida.ronda / partida.total_rondas, text=f"Ronda {partida.ronda + 1} de {partida.total_rondas}")
st.markdown(f"**⭐ Puntos acumulados: {partida.puntos}**")

stats = st.columns(6)
for columna, (titulo, valor) in zip(stats, [
    ("Posición", j["posicion"]), ("Edad", j["edad"]), ("Goles", j["goles"]),
        ("Asistencias", j["asistencias"]), ("Partidos", j["partidos"]), ("Faltas", j["faltas"]),
]):
    columna.metric(titulo, texto_dato(valor))

for titulo, valor in partida.pistas_reveladas():
    st.info(f"💡 **{titulo}:** {valor}")
if not partida.respondida and partida.pistas < MAX_PISTAS:
    if st.button(f"💡 Pedir pista (-{COSTO_PISTA} puntos"):
        partida.pedir_pista()
        st.rerun()

eleccion = st.radio(
    "¿Quien es este goleador?",
    partida.opciones,
    index=None,
    key=f"opcion_{partida.ronda}",
    disabled=partida.respondida,
)

if not partida.respondida:
    st.caption(f"Si aciertas ahora ganas {partida.puntos_posibles()} puntos.")
    if st.button("✅ Confirmar respuesta", type="primary", disabled=eleccion is None):
        partida.responder(eleccion)
        st.rerun()
else:
    resultado = partida.ultimo
    if resultado["aciertos"]:
        st.success(f"¡Correcto! Es **{resultado['correcto']}**. +{resultado['pintos']} puntos.")
    else:
        st.error(f"Casi. Era **{resultado['correcto']}**. +0 puntos.")

    col_foto, col_datos = st.columns([1, 3])
    with col_foto:
        mostrar_imagen(j["foto"], 200)
    with col_datos:
        mostrar_imagen(j["escudo"], 70)
        st.markdown(f"**{j['jugador']}** · {j['seleccion']} · {j['club']}")

    ultima = partida.ronda + 1 == partida.total_rondas
    if st.button("🏁 Ver resultado" if ultima else "➡️ Siguiente jugador", type="primary"):
        partida.siguiente()
        st.rerun()

st.divider()
if st.button("🔄 Reiniciar partida"):
    st.session_state.partida = None
    st.rerun()