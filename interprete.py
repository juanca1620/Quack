from tokens import ErrorSemantico
from arbol import (
    Numero,
    Variable,
    Cadena,
    Booleano,
    Accion,
    OperacionUnaria,
    BucleClok,
    Condicion,
    OperacionBinaria,
    Declaracion,
    Asignacion,
    ReglaSi,
    Consola,
    Comentario,
    Programa,
)

# Qué tipos de Python acepta cada tipo de dato de Quack.
# Se usa type(valor) y no isinstance() porque en Python isinstance(True, int) es True.
ACEPTA = {
    "Q_numerico": (int, float),
    "Q_texto": (str,),
    "Q_booleano": (bool,),
}

VALORES_POR_DEFECTO = {
    "Q_numerico": 0,
    "Q_texto": "",
    "Q_booleano": False,
}

MAX_ITERACIONES_CLOK = 100000


class Entorno:
    """Entorno anidado con referencia a su padre para manejar alcance de bloques."""

    def __init__(self, padre=None):
        self.valores = {}
        self.padre = padre

    def declarar(self, nombre, tipo, valor, linea, columna):
        if nombre in self.valores:
            linea_previa = self.valores[nombre]["linea"]
            raise ErrorSemantico(
                f"la variable '{nombre}' ya fue declarada en la línea {linea_previa}",
                linea,
                columna,
            )
        self.valores[nombre] = {
            "tipo": tipo,
            "valor": valor,
            "linea": linea,
        }

    def buscar(self, nombre, linea, columna):
        if nombre in self.valores:
            return self.valores[nombre]
        if self.padre is not None:
            return self.padre.buscar(nombre, linea, columna)
        raise ErrorSemantico(
            f"la variable '{nombre}' no ha sido declarada",
            linea,
            columna,
        )


class Interprete:

    def __init__(self):
        self.entorno = Entorno()

    def ejecutar_programa(self, programa: Programa):
        for instruccion in programa.instrucciones:
            self.ejecutar(instruccion)

    def _ejecutar_bloque(self, cuerpo):
        entorno_anterior = self.entorno
        self.entorno = Entorno(padre=entorno_anterior)
        try:
            if isinstance(cuerpo, list):
                for instruccion in cuerpo:
                    self.ejecutar(instruccion)
            else:
                self.ejecutar(cuerpo)
        finally:
            self.entorno = entorno_anterior

    def evaluar(self, nodo):
        if isinstance(nodo, Numero):
            texto = nodo.token.valor
            return float(texto) if "." in texto else int(texto)

        if isinstance(nodo, Cadena):
            return nodo.token.valor

        if isinstance(nodo, Booleano):
            return nodo.token.valor == "verdadero"

        if isinstance(nodo, Variable):
            nombre = nodo.token.valor
            info = self.entorno.buscar(nombre, nodo.token.linea, nodo.token.columna)
            return info["valor"]

        if isinstance(nodo, OperacionUnaria):
            val = self.evaluar(nodo.operando)
            op = nodo.operador.valor
            if op == "-":
                if type(val) not in (int, float):
                    raise ErrorSemantico(
                        "no se puede usar '-' unario con un valor no numérico",
                        nodo.operador.linea,
                        nodo.operador.columna,
                    )
                return -val
            if op == "!":
                if type(val) is not bool:
                    raise ErrorSemantico(
                        "el operador '!' solo se puede usar con valores booleanos",
                        nodo.operador.linea,
                        nodo.operador.columna,
                    )
                return not val

        if isinstance(nodo, OperacionBinaria):
            izq = self.evaluar(nodo.izq)
            der = self.evaluar(nodo.der)
            return self.operar(izq, nodo.operador, der)

        if isinstance(nodo, Condicion):
            izq = self.evaluar(nodo.variable)
            der = self.evaluar(nodo.valor)
            return self.comparar(izq, nodo.operador, der)

        raise ErrorSemantico(f"no se puede evaluar el nodo {nodo}", 1, 1)

    def operar(self, izq, operador, der):
        op = operador.valor

        # Conectores lógicos: Y, O
        if op in ("Y", "O"):
            if type(izq) is not bool or type(der) is not bool:
                raise ErrorSemantico(
                    f"el conector '{op}' solo se puede usar con valores booleanos",
                    operador.linea,
                    operador.columna,
                )
            return (izq and der) if op == "Y" else (izq or der)

        # Operaciones con textos (str)
        if type(izq) is str or type(der) is str:
            if op == "+" and type(izq) is str and type(der) is str:
                return izq + der
            raise ErrorSemantico(
                f"no se puede usar '{op}' con textos",
                operador.linea,
                operador.columna,
            )

        # No permitir aritmética con booleanos
        if type(izq) is bool or type(der) is bool:
            raise ErrorSemantico(
                f"no se puede usar '{op}' con booleanos",
                operador.linea,
                operador.columna,
            )

        # Operaciones numéricas: +, -, *, /
        if op == "+":
            return izq + der
        if op == "-":
            return izq - der
        if op == "*":
            return izq * der
        if op == "/":
            if der == 0:
                raise ErrorSemantico(
                    "división por cero",
                    operador.linea,
                    operador.columna,
                )
            if type(izq) is int and type(der) is int and izq % der == 0:
                return izq // der
            return izq / der

        raise ErrorSemantico(
            f"operador desconocido '{op}'",
            operador.linea,
            operador.columna,
        )

    def comparar(self, izq, operador, der):
        op = operador.valor

        if op in ("==", "="):
            if type(izq) is not type(der) and not (
                type(izq) in (int, float) and type(der) in (int, float)
            ):
                raise ErrorSemantico(
                    f"no se pueden comparar tipos incompatibles con '{op}'",
                    operador.linea,
                    operador.columna,
                )
            return izq == der

        if op == "!=":
            if type(izq) is not type(der) and not (
                type(izq) in (int, float) and type(der) in (int, float)
            ):
                raise ErrorSemantico(
                    f"no se pueden comparar tipos incompatibles con '{op}'",
                    operador.linea,
                    operador.columna,
                )
            return izq != der

        if type(izq) not in (int, float) or type(der) not in (int, float):
            raise ErrorSemantico(
                f"el comparador '{op}' solo se puede usar entre números",
                operador.linea,
                operador.columna,
            )

        if op == "<":
            return izq < der
        if op == ">":
            return izq > der
        if op == "<=":
            return izq <= der
        if op == ">=":
            return izq >= der

        raise ErrorSemantico(
            f"comparador desconocido '{op}'",
            operador.linea,
            operador.columna,
        )

    def ejecutar(self, nodo):
        if isinstance(nodo, Declaracion):
            nombre = nodo.nombre.valor
            tipo = nodo.tipo.valor

            valor = (
                self.evaluar(nodo.valor)
                if nodo.valor is not None
                else VALORES_POR_DEFECTO[tipo]
            )

            if type(valor) not in ACEPTA[tipo]:
                raise ErrorSemantico(
                    f"no se puede guardar ese valor en la variable '{nombre}' de tipo {tipo}",
                    nodo.nombre.linea,
                    nodo.nombre.columna,
                )

            self.entorno.declarar(
                nombre, tipo, valor, nodo.nombre.linea, nodo.nombre.columna
            )

        elif isinstance(nodo, Asignacion):
            nombre = nodo.nombre.valor
            info = self.entorno.buscar(
                nombre, nodo.nombre.linea, nodo.nombre.columna
            )

            valor = self.evaluar(nodo.valor)
            tipo = info["tipo"]

            if type(valor) not in ACEPTA[tipo]:
                raise ErrorSemantico(
                    f"no se puede guardar ese valor en la variable '{nombre}' de tipo {tipo}",
                    nodo.nombre.linea,
                    nodo.nombre.columna,
                )

            info["valor"] = valor

        elif isinstance(nodo, Consola):
            valor = self.evaluar(nodo.valor)
            if type(valor) is bool:
                print("verdadero" if valor else "falso")
            else:
                print(valor)

        elif isinstance(nodo, Comentario):
            pass

        elif isinstance(nodo, Accion):
            print(nodo.token.valor)

        elif isinstance(nodo, ReglaSi):
            if self.evaluar(nodo.condicion):
                self._ejecutar_bloque(nodo.entonces)
            elif nodo.sino is not None:
                self._ejecutar_bloque(nodo.sino)

        elif isinstance(nodo, BucleClok):
            vueltas = 0
            while self.evaluar(nodo.condicion):
                vueltas += 1
                if vueltas > MAX_ITERACIONES_CLOK:
                    linea_err = (
                        nodo.condicion.operador.linea
                        if hasattr(nodo.condicion, "operador")
                        else 1
                    )
                    raise ErrorSemantico(
                        f"el ciclo superó {MAX_ITERACIONES_CLOK} vueltas; ¿falta actualizar la variable de la condición?",
                        linea_err,
                        1,
                    )
                self._ejecutar_bloque(nodo.acciones)
