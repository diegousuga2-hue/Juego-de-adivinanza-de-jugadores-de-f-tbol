<p align="center">
  <img src="assets/logo.jpeg" alt="Logo de Adivina al Goleador" width="220">
</p>

# ⚽ Adivina al Goleador

**Equipo Balón de Oro** · Algoritmia y Programación 2026-2
Universidad de Antioquia – Facultad de Ingeniería – Departamento de Ingeniería Industrial
Docente: Cindy Natally Estrada Jiménez

> Una aplicación web hecha con Streamlit para explorar las estadísticas de los 50 máximos goleadores del Mundial 2026 y poner a prueba tu conocimiento de fútbol adivinando quién es cada jugador.

---

## 👥 Integrantes

| Foto | Integrante | Correo institucional |
|---|---|---|
| ![Diego] | **Diego Alejandro Usuga Rojas** | diego.usuga2@udea.edu.co |
| ![Jesus]| **Jesus David Plazas Rojas** | jesus.plazas@udea.edu.co |
| ![Solanye] | **Solanye Andrea Suárez Quiceno** | solanye.suarez@udea.edu.co |

### 🎓 Vínculos académicos y descripción

**Diego Alejandro Usuga Rojas**
- Programa académico: *[escribir el programa]*
- Habilidades y fortalezas: *[escribir una descripción corta]*

**Jesus David Plazas Rojas**
- Programa académico: *[escribir el programa]*
- Habilidades y fortalezas: *[escribir una descripción corta]*

**Solanye Andrea Suárez Quiceno**
- Programa académico: *[escribir el programa]*
- Habilidades y fortalezas: *[escribir una descripción corta]*

---

## 📌 Nombre del proyecto y detalles

**Adivina al Goleador** (proyecto: *Juego de adivinanza de jugadores de fútbol*).

La aplicación muestra las estadísticas de un goleador del Mundial 2026 (posición, edad, goles, partidos, asistencias y faltas) y el usuario debe identificar entre tres opciones de jugadores que se muestran en la pantalla, de qué jugador se trata entre las opciones. Además, permite consultar y filtrar los datos y revisar el historial de partidas de la sesión.

## 🔭 Reporte de visión

**Descripción general.** Adivina al Goleador combina entretenimiento y análisis de datos deportivos. A partir de una base de datos real, limpiada con Python y Pandas, la aplicación ofrece cuatro secciones: Inicio, Explorar, Jugar y Mis datos.

**Objetivo general.** Desarrollar una aplicación web interactiva que permita a los usuarios poner a prueba sus conocimientos sobre fútbol mediante un juego de adivinanza de jugadores, usando estadísticas reales, la idea es identificar la mayor catidad de jugadores y conseguir elegir menos incorrectos posibles.

**Objetivos específicos.**
1. Recopilar, organizar y limpiar una base de datos real de estadísticas de jugadores de fútbol con Python y Pandas.
2. Diseñar e implementar una aplicación web con Streamlit que permita consultar estadísticas, visualizarlas en tablas y gráficos, y jugar.
3. Implementar una dinámica de juego en la que el usuario identifique jugadores a partir de sus estadísticas, acumule puntos y consulte su desempeño e historial.

**Beneficios.**
- Aprender datos reales del Mundial 2026 de una forma lúdica.
- Explorar estadísticas con filtros, indicadores y gráficos sin necesidad de saber programar.
- Aplicar en un proyecto completo los conceptos del curso: funciones, ciclos, condicionales, listas, diccionarios, Pandas, programación orientada a objetos y Streamlit.

## 🧭 Funcionalidades

| Página | Qué ofrece |
|---|---|
| 🏠 **Inicio** | Presentación, fuente de los datos, indicadores generales, equipo y créditos |
| 📊 **Explorar** | Tabla interactiva, filtros, detalle del jugador, estadísticas y gráficos |
| 🎮 **Jugar** | Juego de adivinanza con puntaje, retroalimentación y reinicio de partida |
| 👤 **Mis datos** | Resumen, historial y progreso de las partidas de la sesión |

## 📊 Datos

- **Temática:** deportes (fútbol) – los 50 máximos goleadores del Mundial 2026.
- **Fuentes:** losmundialesdefutbol.com (goles y partidos), futboltotal.futbol – API-Sports (asistencias y faltas) y Wikipedia (fecha de nacimiento y posición).
- **Limpieza:** se realiza en `data/limpieza.ipynb` y genera el archivo `data/datos.csv`, que es el que usa la aplicación.
- **Variables principales:** jugador, selección, posición, edad, goles, partidos, asistencias y faltas.

## 🛠️ Tecnologías

Python · Pandas · Streamlit · Plotly Express · Jupyter Notebook · Git y GitHub

## ▶️ Cómo ejecutar la aplicación

1. Instala Python 3.10 o superior.
2. Clona el repositorio y entra a la carpeta del proyecto.
3. Instala las librerías:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecuta la aplicación desde la carpeta raíz:
   ```bash
   streamlit run app.py
   ```
5. Se abrirá en el navegador en `http://localhost:8501`.

## 🗂️ Estructura del repositorio

```
├── .streamlit/config.toml   # paleta de colores
├── actas/                   # actas de entendimiento, colaboración y responsabilidad
├── app.py                   # archivo principal
├── assets/                  # logo y fotos de los integrantes
├── data/
│   ├── raw/                 # base de datos original
│   ├── limpieza.ipynb       # limpieza de datos
│   └── datos.csv            # datos listos para usar
├── docs/                    # licencia, requisitos, cronograma, presupuesto, versionado y manual
├── pages/                   # inicio, explorar, jugar y mis_datos
├── src/                     # carga de datos y utilidades
├── requirements.txt
└── README.md
```

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **Creative Commons Atribución-NoComercial-CompartirIgual 4.0 (CC BY-NC-SA 4.0)**. Más detalles en [`docs/LICENSE.md`](docs/LICENSE.md).

## 🙏 Créditos

Datos: losmundialesdefutbol.com, futboltotal.futbol (API-Sports) y Wikipedia. Logo y recursos gráficos: elaborados por el equipo Balón de Oro.
