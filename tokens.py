from dataclasses import dataclass
from enum import StrEnum


class TipoToken(StrEnum):
    NUMERO = "NUMERO"
    BOOLEANO = "BOOLEANO"
    TIPO_BOOLEANO = "TIPO_BOOLEANO"
    TIPO_TEXTO = "TIPO_TEXTO"
    TIPO_NUMERICO = "TIPO_NUMERICO"
    CONSOLA = "CONSOLA"
    COMENTARIO = "COMENTARIO"
    CONECTOR_Y = "CONECTOR_Y"
    CONECTOR_O = "CONECTOR_O"
    CONECTOR_SI = "CONECTOR_SI"
    CONECTOR_ENTONCES = "CONECTOR_ENTONCES"
    CONECTOR_SINO = "CONECTOR_SINO"
    CONECTOR_CLOK = "CONECTOR_CLOK"
    ACCION = "ACCION"
    IDENTIFICADOR = "IDENTIFICADOR"
    CADENA = "CADENA"
    OPERADOR = "OPERADOR"
    NEGACION = "NEGACION"
    PARENTESIS = "PARENTESIS"
    LLAVES = "LLAVES"
    DOS_PUNTOS = "DOS_PUNTOS"
    EOF = "EOF"


ACCIONES = {
    "activar_incubadora",
    "especie_posible_ornitorrinco",
    "activar_riego",
    "clasificar_como_ornitorrinco_perry",
    "prender_incubadora",
    "dar_alerta_venenoso",
    "apagar_incubadora",
    "desactivar_riego",
    "encender_ventilacion",
    "apagar_ventilacion",
    "iniciar_humidificacion",
    "activar_calefaccion",
    "emitir_alerta_temperatura",
    "emitir_alerta_humedad",
    "notificar_peligro_nido",
    "alertar_especie_peligrosa",
    "clasificar_como_ave",
    "clasificar_como_reptil",
    "clasificar_como_monotrema",
    "clasificar_como_equidna",
    "registrar_eclosion",
    "marcar_huevo_fertil",
    "solicitar_revision_manual",
}

PALABRAS_RESERVADAS = {
    "Q_booleano": TipoToken.TIPO_BOOLEANO,
    "Q_texto": TipoToken.TIPO_TEXTO,
    "Q_numerico": TipoToken.TIPO_NUMERICO,
    "verdadero": TipoToken.BOOLEANO,
    "falso": TipoToken.BOOLEANO,
    "kukukuku": TipoToken.CONSOLA,
    "kirikiki": TipoToken.COMENTARIO,
    "Y": TipoToken.CONECTOR_Y,
    "O": TipoToken.CONECTOR_O,
    "SI": TipoToken.CONECTOR_SI,
    "ENTONCES": TipoToken.CONECTOR_ENTONCES,
    "SINO": TipoToken.CONECTOR_SINO,
    "CLOK": TipoToken.CONECTOR_CLOK,
    **{accion: TipoToken.ACCION for accion in ACCIONES},
}


@dataclass
class Token:
    tipo: TipoToken
    valor: str
    linea: int
    columna: int

    def __repr__(self):
        return f"{self.tipo}({self.valor!r}) en {self.linea}:{self.columna}"


class ErrorDeLenguaje(Exception):
    """Error base del lenguaje: guarda el mensaje, la línea y la columna."""

    fase = "Error"

    def __init__(self, mensaje, linea, columna):
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna
        super().__init__(f"{self.fase} en línea {linea}, columna {columna}: {mensaje}")


class ErrorLexico(ErrorDeLenguaje):
    """Error propio del lexer: guarda el mensaje, la línea y la columna."""

    fase = "Error léxico"


class ErrorSintactico(ErrorDeLenguaje):
    """Error propio del parser: guarda el mensaje, la línea y la columna."""

    fase = "Error sintáctico"


class ErrorSemantico(ErrorDeLenguaje):
    """Error propio del intérprete: guarda el mensaje, la línea y la columna."""

    fase = "Error semántico"
