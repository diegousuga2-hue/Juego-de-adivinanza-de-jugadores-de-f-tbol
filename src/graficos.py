"""Datos derivados y gráficos de la página Explorar (Plotly).

Trabaja solo con las columnas de data/datos.csv:
edad, posicion, goles, partidos, asistencias y faltas."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.estilos import PALETA

COLOR_POSICION = {
    "Delantero": PALETA["cesped"],
    "Mediocampista": PALETA["oro"],
    "Defensa": "#4A6FA5",
}
COLORES_RADAR = [PALETA["cesped"], PALETA["oro"], "#4A6FA5", "#C0392B"]

# ejes del radar: (columna, etiqueta que se muestra)
EJES_RADAR = [
    ("goles", "Goles"),
    ("asistencias", "Asistencias"),
    ("partidos", "Partidos"),
    ("goles_por_partidos", "Goles por partido"),
    ("faltas", "Faltas"),
]

def preparar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega el número del jugador y las columnas derivadas.

    - n: orden del jugador en la base (la base está ordenada de más a menos goles).
    - etiqueta: nombre del jugador (si hay fichas) o «Jugador n.º 1».
    - goles_por_partido: goles ÷ partidos.
    - participaciones: goles + asistencias (las asistencias sin dato cuentan como 0)."""

    datos = df.copy()
    datos.insert(0, range(1, len(datos) + 1))
    if "jugadores" in datos.columns:
        datos["etiqueta"] = datos["jugador"]
    else:
        datos["etiqueta"] = "Jugador n.º" + datos["n"].astype(str)
    datos["goles_por_partido"] = (datos["goles"] / datos["partidos"]).round(2)
    datos["participaciones"] = datos["goles"] + datos ["asistencias"].fillna(0)
    return datos

def _color(nombre: str, i: int) -> str:
    """Usa el color de la posición si el nombre empieza por ella; si no, uno de la paleta."""
    for posicion, color in COLOR_POSICION.items():
        if nombre.startswith(posicion):
            return color
    return COLORES_RADAR[i % len(COLORES_RADAR)]

def _perfil(valores: pd.Series, maximos: pd.Series):
    """Devuelve (valores reales, valores de 0 a 100) para los ejes del radar"""
    columnas = [col for col, _ in EJES_RADAR]
    reales = [float(valores[col]) if pd.notna(valores[col]) else 0.0 for col in columnas]
    relativos = [(v / maximos[col] * 100) if maximos[col] else 0.0 for v, col in zip(reales, columnas)]
    return reales, relativos

def figura_radar(perfiles: dict, df_total: pd.DataFrame, referencia: pd.Series = None) -> go.Figure:
    """Radar comparativo.

    perfiles: {nombre: Series con las columnas de EJES_RADAR}.
    referencia: perfil opcional que se dibuja punteado (por ejemplo, el promedio del grupo).
    Cada eje va de 0 a 100 respecto al máximo de TODOS los jugadores (df_total), así los
    ejes son comparables aunque tengan escalas distintas. Los datos sin valor se dibujan como 0."""

    columnas = [col for col, _ in EJES_RADAR]
    etiquetas = [etiqueta for _, etiqueta in EJES_RADAR]
    maximos = df_total[columnas].max()

    fig = go.Figure()
    elementos = list(perfiles.items())
    if referencia is not None:
        elementos.append(("Promedio del grupo", referencia))

    for i, (nombre, valores) in enumerate(elementos):
        es_referencia = referencia is not None and i == len(elementos) - 1
        reales, relativos = _perfil(valores, maximos)
        reales = [round(v, 2) for v in reales]
        fig.add_trace(go.Scatterpolar(
            r=relativos + relativos[:1],
            theta=etiquetas + etiquetas[:1],
            customdata=reales + reales[:1],
            name=nombre,
            fill="none" if es_referencia else "toself",
            opacity=1 if es_referencia else 0.55,
            line=dict(color="#7F8C8D" if es_referencia else _color(nombre, i),
                      dash="dash" if es_referencia else "solid", width=2),
            hovertemplate="%{theta}: %{customdata}<extra>%{fullData.name}<extra>",
        ))
    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0, 100], showticklabels=False)),
        legend=dict(orientacion="h", yanchor="bottom", y=-0.2),
        margin=dict(t=30, b=30, l=40, r=40),
        height=450,
    )
    return fig

def figura_participaciones(df: pd.DataFrame, cantidad: int = 10) -> go.Figure:
    """Barras apiladas (goles + asistencias) de los jugadores con más participaciones en gol."""
    datos = df.sort_values(["participaciones", "goles"], ascending=False).head(cantidad).iloc[::-1]
    nombres = datos["etiqueta"] + "." + datos["posicion"]
    fig = go.Figure()
    fig.add_trace(go.Bar(y=nombres, x=datos["goles"], name="Goles", orientacion="h",
                         marker_color=PALETA["cesped"]))
    fig.add_trace(go.Bar(y=nombres, x=datos["asistencias"].fillna(0), name="Asistencias",
                         orientation="h", marker_color=PALETA["oro"]))
    fig.update_layout(barmode="stack", xaxis_title="Goles + asistencias", yaxis_title="",
                      legend=dict(orientacion="h", yanchor="bottom", y=1.02),
                      height=max(320, 34 * len(datos) + 120))
    return fig

def figura_dispersion(df: pd.DataFrame) -> go.Figure:
    """Partidos jugados frente a goles; el tamaño de la burbuja son las asistencias."""
    datos = df.assign(burbuja=df["asistencias"].fillna(0) + 1)
    fig = px.scatter(
        datos, x="partidos", y="goles", size="burbuja", color="posicion", size_max=26, opacity=0.7,
        color_discrete_map=COLOR_POSICION, hover_name="etiqueta",
        hover_data={"edad": True, "asistencias": True, "burbuja": False},
    )
    fig.update_layout(xaxis_title="Partidos jugados", yaxis_title="Goles",
                      legend_title="Posicion", height=420)
    return fig

def figura_distribucion_goles(df: pd.DataFrame) -> go.Figure:
    """Cuántos jugadores hay con cada cantidad de goles, separados por posición."""
    fig = px.histogram(df, x="goles", color="posicion", color_discrete_map="COLOR_POSICION",
                       text_auto=True)
    fig.update_layout(xaxis_title="Goles en el mundial", yaxis_title="Numero de jugadores",
                      legend_title="Posicion", bargap=0.15, xaxis=dict(dtick=1), height=420)
    return fig

def figura_edad_por_posicion(df: pd.DataFrame) -> go.Figure:
    """Diagrama de caja: cómo se distribuye la edad en cada posición."""
    fig = px.box(df, x="posicion", y="edad", color="posicion", points="all",
                 hover_name="etiqueta", color_discrete_map=COLOR_POSICION)
    fig.update_layout(xaxis_title="Posicion", yaxis_title="Edad (años)", showlegend=False, height=420)
    return fig

def figura_correlaciones(df: pd.DataFrame) -> go.Figure:
    """Mapa de calor con la correlación entre las variables numéricas (de -1 a 1)."""
    nombres = {"edad": "Edad", "goles": "Goles", "asistencias": "Asistencias", 
               "partidos": "Partidos", "faltas": "Faltas"}
    correlacion = df[list(nombres)].corr().round(2).rename(index=nombres, columns=nombres)
    fig = px.imshow(
        correlacion, text_auto=True, zmin=-1, zmax=1,
        color_continuous_scale=[[0, "#C0392B"], [0.5, "#FFFFFF"], [1, PALETA["cesped"]]],
    )
    fig.update_layout(height=420, coloraxis_colorbar_title="correlacion")
    return fig

def figura_por_seleccion(df: pd.DataFrame) -> go.Figure:
    """Goles totales de los jugadores filtrados, agrupados por selección."""
    resumen = (
        df.groupby("seleccion", as_index=False)
        .agg(goles=("goles", "sum"), jugadores=("etiqueta", "count"))
        .sort_values("goles", ascending=False)
    )
    fig = px.bar(resumen, x="seleccion", y="goles", text="goles", hover_data=["jugadores"],
                 color_discrete_sequence=[PALETA["cesped"]])
    fig.update_layout(xaxis_title="Seleccion", yaxis_title="Goles", height=420)
    return fig
