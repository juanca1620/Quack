from dataclasses import dataclass
from tokens import Token


@dataclass
class Numero:
    token: Token


@dataclass
class Variable:
    token: Token


@dataclass
class Cadena:
    token: Token


@dataclass
class Booleano:
    token: Token


@dataclass
class Accion:
    token: Token


@dataclass
class OperacionUnaria:
    operador: Token
    operando: object


@dataclass
class Condicion:
    variable: object
    operador: Token
    valor: object


@dataclass
class OperacionBinaria:
    izq: object
    operador: Token
    der: object


@dataclass
class Declaracion:
    tipo: Token
    nombre: Token
    valor: object = None


@dataclass
class Asignacion:
    nombre: Token
    valor: object


@dataclass
class ReglaSi:
    condicion: object
    entonces: object
    sino: object = None


@dataclass
class BucleClok:
    condicion: object
    acciones: list


@dataclass
class Consola:
    valor: object


@dataclass
class Comentario:
    valor: object


@dataclass
class Programa:
    instrucciones: list


def mostrar_arbol(nodo, nivel=0):
    sangria = "  " * nivel

    if isinstance(nodo, Programa):
        print(f"{sangria}Programa")
        for instruccion in nodo.instrucciones:
            mostrar_arbol(instruccion, nivel + 1)

    elif isinstance(nodo, Declaracion):
        print(f"{sangria}Declaracion {nodo.tipo.valor} {nodo.nombre.valor}")
        if nodo.valor is not None:
            mostrar_arbol(nodo.valor, nivel + 1)

    elif isinstance(nodo, Asignacion):
        print(f"{sangria}Asignacion {nodo.nombre.valor}")
        mostrar_arbol(nodo.valor, nivel + 1)

    elif isinstance(nodo, ReglaSi):
        print(f"{sangria}ReglaSi")
        mostrar_arbol(nodo.condicion, nivel + 1)
        if isinstance(nodo.entonces, list):
            for inst in nodo.entonces:
                mostrar_arbol(inst, nivel + 1)
        else:
            mostrar_arbol(nodo.entonces, nivel + 1)
        if nodo.sino is not None:
            print(f"{sangria}  Sino")
            if isinstance(nodo.sino, list):
                for inst in nodo.sino:
                    mostrar_arbol(inst, nivel + 2)
            else:
                mostrar_arbol(nodo.sino, nivel + 2)

    elif isinstance(nodo, BucleClok):
        print(f"{sangria}BucleClok")
        mostrar_arbol(nodo.condicion, nivel + 1)
        for accion in nodo.acciones:
            mostrar_arbol(accion, nivel + 1)

    elif isinstance(nodo, Condicion):
        print(f"{sangria}Condicion {nodo.operador.valor}")
        mostrar_arbol(nodo.variable, nivel + 1)
        mostrar_arbol(nodo.valor, nivel + 1)

    elif isinstance(nodo, OperacionUnaria):
        print(f"{sangria}OperacionUnaria {nodo.operador.valor}")
        mostrar_arbol(nodo.operando, nivel + 1)

    elif isinstance(nodo, OperacionBinaria):
        print(f"{sangria}OperacionBinaria {nodo.operador.valor}")
        mostrar_arbol(nodo.izq, nivel + 1)
        mostrar_arbol(nodo.der, nivel + 1)

    elif isinstance(nodo, Consola):
        print(f"{sangria}Consola")
        mostrar_arbol(nodo.valor, nivel + 1)

    elif isinstance(nodo, Comentario):
        print(f"{sangria}Comentario")
        mostrar_arbol(nodo.valor, nivel + 1)

    elif isinstance(nodo, Accion):
        print(f"{sangria}Accion {nodo.token.valor}")

    elif isinstance(nodo, Numero):
        print(f"{sangria}Numero {nodo.token.valor}")

    elif isinstance(nodo, Variable):
        print(f"{sangria}Variable {nodo.token.valor}")

    elif isinstance(nodo, Cadena):
        print(f'{sangria}Cadena "{nodo.token.valor}"')

    elif isinstance(nodo, Booleano):
        print(f"{sangria}Booleano {nodo.token.valor}")

    else:
        print(f"{sangria}Nodo desconocido: {nodo}")
