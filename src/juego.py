"""Lógica del juego ¿Quien es el goleador? (sin Streamlit, para poder probarla por separado)."""
import random
import time

RONDAS = 10
OPCIONES = 4
PUNTOS_ACIERTOS = 10
COSTO_PISTA = 3
PISTAS = [("seleccion", "Seleccion"), ("club", "Club")]
MAX_PISTAS = len(PISTAS)

def calificaciones(aciertos: int, rondas: int) -> str:
    """Devuelve un mensaje según el porcentaje de aciertos."""
    porcentaje = aciertos / rondas * 100 if rondas else 0
    if porcentaje >= 90:
        return "🏆 ¡Crack del fútbol! Conoces a los goleadores como nadie."
    elif porcentaje >= 60:
        return "👏 ¡Muy bien! Conoces bastante a estos goleadores."
    elif porcentaje >= 30:
        return "🙂 Nada mal. Con otra partida mejoras seguro."
    return "📚 Sigue practicando: explora los datos y vuelve a intentarlo."

class Partida:
    """Una partida: jugadores al azar, cada uno con 4 opciones de respuesta."""

    def __init__(self, df, rondas: int = RONDAS):
        self.df = df
        self.jugadores = df.sample(n=min(rondas, len(df))).to_dict("records")
        self.ronda = 0
        self.puntos = 0
        self.aciertos = 0
        self.pista_total = 0
        self.inicio = time.time()
        self.segundos = None
        self.resultados = []
        self.guardada = False
        self._nueva_ronda()

    # estado
    @property
    def total_rondas(self) -> int:
        return len(self.jugadores)

    @property
    def terminada(self) -> bool:
        return self.ronda >= self.total_rondas

    @property
    def jugador(self) -> dict:
        """Datos del jugador que hay que adivinar en la ronda actual."""
        return self.jugadores[self.ronda]

    # rondas
    def _nueva_ronda(self):
        """Prepara la ronda: reinicia pistas y arma las 4 opciones de respuesta."""
        self.pistas = 0
        self.respondida = False
        self.ultimo = None
        if self.terminada:
            self.segundos = round(time.time() - self.inicio)
            return
        correcto = self.jugador["jugador"]
        posicion = self.jugador["posicion"]
        otros = self.df[self.df["jugador"] != correcto]
        mismos = otros.loc[otros["posicion"] == posicion, "jugador"].tolist()
        distintos = otros.loc[otros["posicion"] != posicion, "jugador"].tolist()
        random.shuffle(mismos)
        random.shuffle(distintos)
        distractores = (mismos + distintos)[:OPCIONES - 1]
        self.opciones = distractores + [correcto]
        random.shuffle(self.opciones)

    def pedir_pista(self) -> bool:
        """Revela una pista más (cuesta puntos). Devuelve False si ya no se puede."""
        if self.respondida or self.pistas >= MAX_PISTAS:
            return False
        self.pistas += 1
        self.pista_total += 1
        return True

    def pistas_reveladas(self) -> list:
        """Lista de (título, valor) de las pistas pedidas en esta ronda."""
        return [(titulo, self.jugador[campo]) for campo, titulo in PISTAS[:self.pistas]]

    def puntos_posibles(self) -> int:
        """Puntos que se ganarían si se acierta ahora."""
        return max(PUNTOS_ACIERTOS - COSTO_PISTA * self.pistas, 0)

    def responder(self, eleccion: str):
        """Califica la respuesta, suma los puntos y guarda el resultado de la ronda."""
        if self.respondida:
            return self.ultimo
        correcto = self.jugador["jugador"]
        acierto = eleccion == correcto
        ganados = self.puntos_posibles() if acierto else 0
        self.puntos += ganados
        self.aciertos += int(acierto)
        self.respondida = True
        self.ultimo = {"acierto": acierto, "puntos": ganados, "correcto": correcto}
        self.resultados.append({
            "Ronda": self.ronda + 1,
            "Jugador": correcto,
            "Tu respuesta": eleccion,
            "Acerto": "✅" if acierto else "❌",
            "Pistas": self.pistas,
            "Puntos": ganados,
        })
        return self.ultimo

    def siguiente(self):
        """Pasa a la siguiente ronda (o termina la partida)."""
        self.ronda += 1 
        self._nueva_ronda()

    def registro(self, numero: int) -> dict:
        """Resumen de la partida para el historial de la sesión (lo usa Mis datos)."""
        return {
            "partida": numero,
            "hora": time.strftime("%H:%M:%S"),
            "puntos": self.puntos,
            "aciertos": self.aciertos,
            "rondas": self.total_rondas,
            "pistas": self.pista_total,
            "segundos": self.segundos    
        }