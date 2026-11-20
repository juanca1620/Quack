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

