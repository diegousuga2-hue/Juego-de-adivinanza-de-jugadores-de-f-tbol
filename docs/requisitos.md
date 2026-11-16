# Especificación de requisitos

**Proyecto:** Adivina al Goleador · **Equipo:** Balón de Oro · **Curso:** Algoritmia y Programación 2026-2

## 1. Introducción

### 1.1 Propósito
Describir lo que debe hacer la aplicación web (requisitos funcionales) y las condiciones de calidad con las que debe operar (requisitos no funcionales).

### 1.2 Alcance
Aplicación web hecha con Streamlit, con cuatro páginas (Inicio, Explorar, Jugar y Mis datos), basada en los datos de los 50 máximos goleadores del Mundial 2026.

**No contempla:** un videojuego de fútbol en tiempo real, simulación de partidos, apuestas deportivas, transmisión de encuentros ni conexión con plataformas deportivas en vivo.

### 1.3 Usuarios
Aficionados al fútbol y estudiantes que quieran explorar estadísticas de forma interactiva. No se requiere registro ni inicio de sesión.

---

## 2. Requisitos funcionales

### Datos y navegación
| ID | Requisito |
|---|---|
| RF-01 | La aplicación debe cargar los datos procesados desde `data/datos.csv`. |
| RF-02 | La aplicación debe ofrecer un menú para navegar entre las cuatro páginas: Inicio, Explorar, Jugar y Mis datos. |
| RF-03 | La aplicación debe conservar la información de la sesión (partidas y registros consultados) entre interacciones y páginas, usando `st.session_state`. |
| RF-04 | La aplicación debe manejar valores faltantes, errores de entrada y situaciones sin resultados mostrando mensajes claros. |

### Página Inicio
| ID | Requisito |
|---|---|
| RF-05 | Debe mostrar el nombre de la aplicación, el logo y una descripción breve de su propósito. |
| RF-06 | Debe explicar la temática de los datos, su fuente y su relevancia. |
| RF-07 | Debe describir las funcionalidades y permitir acceder a cada sección. |
| RF-08 | Debe mostrar al menos tres indicadores generales (por ejemplo, número de jugadores, goles totales y edad promedio). |
| RF-09 | Debe presentar al equipo desarrollador y los objetivos del proyecto. |
| RF-10 | Debe reconocer las fuentes de datos, los recursos gráficos y las licencias. |

### Página Explorar
| ID | Requisito |
|---|---|
| RF-11 | Debe mostrar los datos en una tabla interactiva que permita seleccionar registros. |
| RF-12 | Debe ofrecer al menos tres filtros (por ejemplo, selección, posición y rango de goles). |
| RF-13 | Debe presentar el detalle del jugador seleccionado. |
| RF-14 | Debe calcular al menos tres indicadores descriptivos a partir de los datos filtrados. |
| RF-15 | Debe incluir al menos dos gráficos que ayuden a identificar patrones o diferencias. |
| RF-16 | Debe actualizar tabla, indicadores y gráficos según los filtros elegidos. |
| RF-17 | Debe mostrar un aviso cuando ningún jugador cumpla los filtros. |

### Página Jugar
| ID | Requisito |
|---|---|
| RF-18 | Debe explicar el objetivo, las reglas y la forma de participar. |
| RF-19 | Debe permitir iniciar una partida compuesta por varias rondas. |
| RF-20 | En cada ronda debe mostrar las estadísticas de un jugador elegido al azar y varias opciones de respuesta. |
| RF-21 | Debe verificar la respuesta del usuario y dar retroalimentación (correcta o incorrecta). |
| RF-22 | Debe calcular el puntaje y mostrar el resultado al terminar la partida. |
| RF-23 | Debe registrar las partidas jugadas durante la sesión (cantidad, puntajes y mejor resultado). |
| RF-24 | Debe permitir iniciar una nueva partida sin perder las estadísticas acumuladas. |

### Página Mis datos
| ID | Requisito |
|---|---|
| RF-25 | Debe mostrar un resumen de actividad: partidas jugadas, puntaje acumulado, mejor resultado y jugadores consultados. |
| RF-26 | Debe presentar estadísticas de desempeño mediante indicadores, tablas o gráficos. |
| RF-27 | Debe mostrar el historial de partidas (orden, resultado y puntaje). |
| RF-28 | Debe incluir un gráfico de la evolución de los resultados. |
| RF-29 | Debe mostrar un mensaje claro cuando el usuario todavía no tenga actividad. |
| RF-30 | Debe actualizarse automáticamente con las interacciones reales del usuario durante la sesión. |

---

## 3. Requisitos no funcionales

| ID | Categoría | Requisito |
|---|---|---|
| RNF-01 | Rendimiento | Las páginas deben cargar en pocos segundos; los datos se leen una sola vez usando caché. |
| RNF-02 | Usabilidad | La interfaz debe ser legible y fácil de entender, con botones e íconos claros y mensajes de retroalimentación. |
| RNF-03 | Identidad visual | Las cuatro páginas deben compartir nombre, logo y paleta de colores (verde `#0B5D3B` y oro `#E3A81B`). |
| RNF-04 | Fiabilidad | La aplicación no debe cerrarse por entradas inválidas, archivos inexistentes o datos vacíos; debe usar manejo de excepciones. |
| RNF-05 | Compatibilidad | Debe funcionar con Python 3.10 o superior y en navegadores web actuales. |
| RNF-06 | Mantenibilidad | El código debe estar organizado en archivos y carpetas con nombres descriptivos, con funciones documentadas. |
| RNF-07 | Portabilidad | Debe poder instalarse y ejecutarse en otro equipo con `pip install -r requirements.txt` y `streamlit run app.py`. |
| RNF-08 | Privacidad y seguridad | No debe solicitar datos personales; la información de la sesión no se guarda de forma permanente. |
| RNF-09 | Legalidad | Debe reconocer las fuentes de los datos y respetar las licencias y condiciones de uso de los recursos empleados. |
| RNF-10 | Documentación | Debe contar con README, licencia, requisitos, plan de proyecto, plan de versionado y manual de usuario en el repositorio. |
