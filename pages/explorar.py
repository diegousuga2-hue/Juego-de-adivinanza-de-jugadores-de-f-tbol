"Explorar: tabla, filtros, ficha del jugador, estadísticas y gráficos comparativos."
from pathlib import Path

import pandas as pd
import streamlit as st

from src import graficos
from src.data import obtener_datos
from src.fichas import unir_fichas

RAIZ = Path(__file__).resolve().parent.parent
COLUMNAS_NECESARIAS = ["edad", "posicion", "goles", "partidos", "asistencias", "faltas"]

st.title("📊 Explorar")
st.caption("Filtra a los 50 goleadores del Mundial 2026, consulta cada ficha y compáralos.")

df = obtener_datos()
faltantes = [col for col in COLUMNAS_NECESARIAS if col not in df.columns]
if faltantes:
    st.error("A data/datos.csv le faltan estas columnas:" + ",".join(faltantes))
    st.stop()

df, aviso_fichas = unir_fichas(df)
CON_FICHAS = aviso_fichas is None
if not CON_FICHAS:
    st.info(aviso_fichas)
df = graficos.preparar_datos(df)

# Filtros
RANGOS = {col: (int(df[col].min()), int(df[col].max())) for col in ("edad", "goles", "partidos")}
FILTROS_INICIALES = {
    "f_nombre": "",
        "f_seleccion": [],
        "f_posicion": [],
        "f_edad": RANGOS["edad"],
        "f_goles": RANGOS["goles"],
        "f_partidos": RANGOS["partidos"],
}
for clave, valor in FILTROS_INICIALES.items():
    st.session_state.setdefault(clave, valor)

def limpiar_filtros():
    """Devuelve todos los filtros a su valor inicial."""
    for clave, valor in FILTROS_INICIALES.items():
        st.session_state[clave] = valor

st.sidebar.header("🔎 Filtros")
if CON_FICHAS:
    st.sidebar.text_input("Buscar jugador", key="f_nombre")
    st.sidebar.multiselect("Seleccion", sorted(df["seleccion"].unique()), key="f_seleccion")
st.sidebar.multiselect("Posición", sorted(df["posicion"].unique()), key="f_posicion")
st.sidebar.slider("Rango de edad", *RANGOS["edad"], key="f_edad")
st.sidebar.slider("Rango de goles", *RANGOS["goles"], key="f_goles")
st.sidebar.slider("Rango de partidos", *RANGOS["partidos"], key="f_partidos")
st.sidebar.button("🧹 Limpiar filtros", on_click=limpiar_filtros)

filtrado = df[
    df["edad"].between(*st.session_state.f_edad)
        & df["goles"].between(*st.session_state.f_goles)
        & df["partidos"].between(*st.session_state.f_partidos)
]
if st.session_state.f_posicion:
    filtrado = filtrado[filtrado["posicion"].isin(st.session_state.f_posicion)]
if CON_FICHAS:
    if st.session_state.f_seleccion:
        filtrado = filtrado[filtrado["seleccion"].isin(st.session_state.f_seleccion)]
    if st.session_state.f_nombre.strip():
        filtrado = filtrado[
            filtrado["jugador"].str.contains(st.session_state.f_nombre.strip(), case=False, na=False)
        ]
filtrado = filtrado.reset_index(drop=True)

if filtrado.empty:
    st.warning("Ningún jugador cumple esos filtros. Prueba con otros valores o pulsa «Limpiar filtros».")
    st.stop()

# estadisticas
c1, c2, c3, c4 = st.columns(4)
c1.metric("Jugadores", len(filtrado))
c2.metric("Goles totales", int(filtrado["goles"].sum()))
c3.metric("Edad promedio", round(filtrado["edad"].mean(), 1))
c4.metric("Goles por partido", round(filtrado["goles"].sum() / filtrado["partidos"].sum(), 2))

# tabla
st.subheader("📋 Jugadores")
st.caption(
    "Haz clic en una fila para ver su ficha (Ctrl + clic para elegir varias y compararlas en el radar). "
    "Vacío = sin dato."
)
if CON_FICHAS:
    COLUMNAS_TABLA = {"jugador": "Jugador", "seleccion": "Selección", "club": "Club"}
else:
    COLUMNAS_TABLA = {"n": "N.º"}
COLUMNAS_TABLA.update({
    "posicion": "Posición", "edad": "Edad", "goles": "Goles", "asistencias": "Asistencias",
    "partidos": "Partidos", "faltas": "Faltas", "goles_por_partido": "Goles/partido",
    "participaciones": "Goles + asist.",
})
evento = st.dataframe(
    filtrado[list(COLUMNAS_TABLA)].rename(columns=COLUMNAS_TABLA),
    on_select="rerun",
    selection_mode="multi-row",
    hide_index=True,
)
columnas_descarga = [c for c in ["jugador", "seleccion", "club"] + COLUMNAS_NECESARIAS if c in filtrado.columns]
st.download_button(
    "📥 Descargar datos filtrados (CSV)",
    filtrado[columnas_descarga].to_csv(index=False).encode("utf-8"),
    file_name="goleadores_filtrados.csv",
    mime="text/csv",
)

# ficha del registro
def mostrar_imagen(ruta, ancho):
    """Muestra una imagen del proyecto; si no existe, avisa sin romper la página."""
    if isinstance(ruta, str) and (RAIZ / ruta).exists():
            st.image(str(RAIZ / ruta), width=ancho)
    else:
        st.caption("🖼️ Imagen no disponible")

def texto_dato(valor):
    """Devuelve el valor como texto, o «s/d» (sin dato) si está vacío."""
    if pd.isna(valor):
        return "s/d"
    return f"{valor:g}" if isinstance(valor, (int, float)) else str(valor)

def mostrar_metricas(j):
    """Cinco indicadores del jugador, comparados con el promedio del grupo filtrado."""
    variables = [("goles", "Goles"), ("asistencias", "Asistencias"), ("partidos", "Partidos"),
                     ("goles_por_partido", "Goles/partido"), ("faltas", "Faltas")]
    for columna, (campo, titulo) in zip(st.columns(len(variables)), variables):
        valor = j[campo]
        if pd.isna(valor):
            columna.metric(titulo, "s/d")
        else:
            diferencia = valor - filtrado[campo].mean()
            columna.metric(titulo, f"{valor:g}", delta=f"{diferencia:+.2f} vs. promedio", delta_color="off")

seleccionados = evento.selection.rows
if seleccionados:
    j = filtrado.iloc[seleccionados[0]]
    if j["etiqueta"] not in st.session_state.registros_consultados:
        st.session_state.registros_consultados.append(j["etiqueta"])

    st.subheader(f"🔍 Ficha: {j['etiqueta']}")
    if CON_FICHAS:
        col_foto, col_datos = st.columns([1, 3])
        with col_foto:
            mostrar_imagen(j["foto"], 230)
        with col_datos:
            col_escudo, col_texto = st.columns([1, 4])
            with col_escudo:
                mostrar_imagen(j["escudo"], 80)
            with col_texto:
                st.markdown(
                    f"**Selección:** {j['seleccion']} · **Posición:** {j['posicion']} · **Edad:** {j['edad']} años  \n"
                    f"**Club actual:** {j['club']} · **Puesto entre los goleadores:** {j['puesto']}."
                )
            mostrar_metricas(j)
            st.caption(
                f"Amarillas: {texto_dato(j['amarillas'])} · Rojas: {texto_dato(j['rojas'])} · "
                f"Goles con su selección: {texto_dato(j['goles_seleccion'])} · "
                "La flecha compara con el promedio del grupo filtrado."
            )
    else:
        st.caption(f"{j['posicion']} · {j['edad']} años · la flecha compara con el promedio del grupo filtrado")
        mostrar_metricas(j)

# Radar
st.subheader("🕸️ Radar comparativo")
modo = st.radio("Comparar", ["Posiciones (promedio)", "Jugadores seleccionados"], horizontal=True)
columnas_radar = [col for col, _ in graficos.EJES_RADAR]

if modo.startswith("Posiciones"):
    promedios = filtrado.groupby("posicion")[columnas_radar].mean()
    perfiles = {f"{posicion} (promedio)": fila for posicion, fila in promedios.iterrows()}
    st.plotly_chart(graficos.figura_radar(perfiles, df))
elif seleccionados:
    elegidos = filtrado.iloc[seleccionados[:4]]
    perfiles = {fila["etiqueta"]: fila for _, fila in elegidos.iterrows()}
    st.plotly_chart(graficos.figura_radar(perfiles, df, referencia=filtrado[columnas_radar].mean()))
    if len(seleccionados) > 4:
        st.caption("Se muestran solo los primeros 4 jugadores seleccionados.")
else:
    st.info("Selecciona de 1 a 4 filas en la tabla de arriba para compararlas con el promedio del grupo.")

st.caption(
    "Cada eje va de 0 a 100 respecto al máximo de los 50 goleadores (100 = el mejor del grupo en esa variable)."
    "Pasa el cursor para ver el valor real. Los datos sin valor se dibujan como 0."
)
# otros graficos
st.subheader("📈 Más comparativas")
nombres_tabs = ["🏆 Goles + asistencias", "🔵 Partidos vs goles", "📊 Distribución de goles",
                "🎂 Edad por posición", "🔗 Correlaciones"]
if CON_FICHAS:
    nombres_tabs.append("🌍 Por selección")
tabs = st.tabs(nombres_tabs)
with tabs[0]:
    st.plotly_chart(graficos.figura_participaciones(filtrado))
    st.caption("Los 10 jugadores con más participaciones en gol (goles + asistencias) del grupo filtrado.")
with tabs[1]:
    st.plotly_chart(graficos.figura_dispersion(filtrado))
    st.caption("Cada burbuja es un jugador y su tamaño indica las asistencias. Más arriba = más goles con los mismos partidos.")
with tabs[2]:
    st.plotly_chart(graficos.figura_distribucion_goles(filtrado))
    st.caption("Cuántos jugadores marcaron cada cantidad de goles; la mayoría se concentra en pocos goles.")
with tabs[3]:
    st.plotly_chart(graficos.figura_edad_por_posicion(filtrado))
    st.caption("Distribución de la edad según la posición (la caja muestra el 50 % central de los jugadores).")
with tabs[4]:
    st.plotly_chart(graficos.figura_correlaciones(filtrado))
    st.caption("Verde = las variables suben juntas; rojo = una sube y la otra baja. Con pocos jugadores, interprétalo con cuidado.")
if CON_FICHAS:
    with tabs[5]:
            st.plotly_chart(graficos.figura_por_seleccion(filtrado))
            st.caption("Suma de goles de los jugadores filtrados de cada selección.")
