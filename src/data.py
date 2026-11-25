"carga de datos de entrada (data/datos.csv)."
from pathlib import Path
import pandas as pd
import streamlit as st
RUTA_DATOS = Path(__file__).resolve().parent.parent / "data" / "datos.csv"
@st.cache_data
def cargar_datos() -> pd.DataFrame:
    "lee datos csv. si falla, devuelve un dataframe vacio."
    try:
        return pd.read_csv(RUTA_DATOS)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame()

def obtener_datos() -> pd.DataFrame:
    "devuelve los datos o detiene la pagina con un mensaje claro."
    df = cargar_datos()
    if df.empty:
        st.error("no se pudo leer data/datos.cvs. revisa que el archivo exista y no este vacio.")
        st.stop()
    return df
