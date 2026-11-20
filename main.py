import sys
from tokens import ErrorDeLenguaje
from lexer import tokenizar
from parser import Parser
from arbol import mostrar_arbol
from interprete import Interprete


def mostrar_error(error: ErrorDeLenguaje, codigo: str):
    print(error)
    lineas = codigo.splitlines()
    if 1 <= error.linea <= len(lineas):
        linea_codigo = lineas[error.linea - 1]
        print(f"    {linea_codigo}")
        espacios = " " * max(error.columna - 1, 0)
        print(f"    {espacios}^")


def modo_interactivo():
    interprete = Interprete()
    while True:
        try:
            linea = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not linea.strip():
            continue
        if linea.strip() in ("salir", "exit"):
            break

        try:
            programa = Parser(tokenizar(linea)).programa()
            interprete.ejecutar_programa(programa)
        except ErrorDeLenguaje as e:
            mostrar_error(e, linea)


def main():
    if len(sys.argv) < 2:
        modo_interactivo()
        return

    ruta = sys.argv[1]
    ver_arbol = "--arbol" in sys.argv[2:]

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta}'")
        sys.exit(1)

    try:
        tokens = tokenizar(contenido)
        programa = Parser(tokens).programa()
        if ver_arbol:
            mostrar_arbol(programa)
        else:
            Interprete().ejecutar_programa(programa)
    except ErrorDeLenguaje as e:
        mostrar_error(e, contenido)
        sys.exit(1)


if __name__ == "__main__":
    main()
