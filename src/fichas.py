"""Une la información de las fichas (nombre, selección, club, foto) con data/datos.csv.

datos.csv NO se modifica: las fichas están en data/fichas.csv y se unen por el orden de las filas.
Para asegurar que cada ficha corresponde a su fila, se comprueba que edad, posición, goles,
partidos, asistencias y faltas coincidan en todas las filas."""

from pathlib import Path
import pandas as pd

RUTA_FICHAS = Path(__file__).resolve().parent.parent / "data" / "fichas.csv"
COLUMNAS_COMPARAR = ["edad", "posicion", "goles", "partidos", "asistencias", "faltas"]
COLUMNAS_FICHA = ["puesto", "jugador", "seleccion", "club", "amarillas", "rojas",
                  "goles_seleccion", "foto", "escudo"]

def unir_fichas(df: pd.DataFrame):
    """Devuelve (datos, aviso).
    
    si todo coincide, datos trae ademas las columnas de la ficha y aviso es None.
    si algo falla, devuelve los datos sin cambios y un texto que explica el motivo."""
    try:
        fichas = pd.read_csv(RUTA_FICHAS)
    except FileNotFoundError:
        return df, "No se encontró data/fichas.csv: se muestran los jugadores sin nombre ni foto. "
    if len(fichas) != len(df):
        return df, "data/fichas.csv no tiene el mismo numero de filas que datos.csv."

    base = df.reset_index(drop=True)
    for columna in COLUMNAS_COMPARAR:
        iguales = (base[columna] == fichas[columna]) | (base[columna].isna() & fichas[columna].isna())
        if not iguales.all():
            return df, f"las fichas no coinciden con datos.csv en la columna {columna}. "

    union = base.copy()
    for columna in COLUMNAS_FICHA:
        union[columna] = fichas[columna]
    return union, None