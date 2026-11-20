# Gramática en EBNF del lenguaje Quack:
# programa             ::= instruccion* EOF
# instruccion          ::= declaracion | asignacion | regla_si | bucle_clok | consola | comentario | ACCION
# declaracion          ::= declaracion_booleano | declaracion_texto | declaracion_numerico
# declaracion_booleano ::= "Q_booleano" IDENTIFICADOR ( "=" expresion_booleana )?
# declaracion_texto    ::= "Q_texto" IDENTIFICADOR ( "=" expresion_texto )?
# declaracion_numerico ::= "Q_numerico" IDENTIFICADOR ( "=" expresion_numerica )?
# asignacion           ::= IDENTIFICADOR "=" expresion
# regla_si             ::= "SI" expresion_booleana "ENTONCES" bloque_si ( "SINO" bloque_si )?
# bucle_clok           ::= "CLOK" expresion_booleana ":" INDENT instruccion+ DEDENT
# consola              ::= "kukukuku" expresion
# comentario           ::= "kirikiki" expresion_texto
# expresion_booleana   ::= termino_booleano ( "O" termino_booleano )*
# termino_booleano     ::= factor_booleano ( "Y" factor_booleano )*
# factor_booleano      ::= "!" factor_booleano | condicion
# condicion            ::= expresion ( ( ">" | "<" | "=" | ">=" | "<=" | "==" | "!=" ) expresion )?
# expresion_texto      ::= expresion
# expresion_numerica   ::= expresion
# expresion            ::= termino ( ( "+" | "-" ) termino )*
# termino              ::= factor ( ( "*" | "/" ) factor )*
# factor               ::= "-" factor | NUMERO | CADENA | BOOLEANO | IDENTIFICADOR | "(" expresion ")"

from tokens import Token, TipoToken, ErrorSintactico
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

OPERADORES_COMPARACION = (">", "<", "=", ">=", "<=", "==", "!=")


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def actual(self):
        if self.pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.pos]

    def siguiente(self):
        if self.pos + 1 >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.pos + 1]

    def avanzar(self):
        token = self.actual()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token

    def imprimir(self):
        for t in self.tokens:
            print(t)

    def esperar(self, tipo, valor=None):
        t = self.actual()
        if t.tipo != tipo or (valor is not None and t.valor != valor):
            quiero = f"'{valor}'" if valor else f"un {tipo}"
            llego = "el fin del archivo" if t.tipo == TipoToken.EOF else f"'{t.valor}'"
            raise ErrorSintactico(
                f"se esperaba {quiero} y llegó {llego}", t.linea, t.columna
            )
        return self.avanzar()

    # <valor> ::= <numero> | <booleano> | <texto> | <identificador>
    def valor(self):
        return self.expresion()

    # <condicion> ::= expresion ( OPERADOR_COMPARACION expresion )?
    def condicion(self):
        izq = self.expresion()
        t = self.actual()
        if t.tipo == TipoToken.OPERADOR and t.valor in OPERADORES_COMPARACION:
            operador = self.avanzar()
            der = self.expresion()
            return Condicion(izq, operador, der)
        return izq

    # factor_booleano ::= '!' factor_booleano | condicion
    def factor_booleano(self):
        t = self.actual()
        if t.tipo == TipoToken.NEGACION:
            operador = self.avanzar()
            return OperacionUnaria(operador, self.factor_booleano())
        return self.condicion()

    # termino_booleano ::= factor_booleano ( 'Y' factor_booleano )*
    def termino_booleano(self):
        izq = self.factor_booleano()
        while self.actual().tipo == TipoToken.CONECTOR_Y:
            conector = self.avanzar()
            der = self.factor_booleano()
            izq = OperacionBinaria(izq, conector, der)
        return izq

    # expresion_booleana ::= termino_booleano ( 'O' termino_booleano )*
    def expresion_booleana(self):
        izq = self.termino_booleano()
        while self.actual().tipo == TipoToken.CONECTOR_O:
            conector = self.avanzar()
            der = self.termino_booleano()
            izq = OperacionBinaria(izq, conector, der)
        return izq

    def expresion_texto(self):
        return self.expresion()

    def expresion_numerica(self):
        return self.expresion()

    # factor ::= '-' factor | NUMERO | CADENA | BOOLEANO | IDENTIFICADOR | '(' expresion ')'
    def factor(self):
        t = self.actual()
        if t.tipo == TipoToken.OPERADOR and t.valor == "-":
            operador = self.avanzar()
            return OperacionUnaria(operador, self.factor())
        if t.tipo == TipoToken.NUMERO:
            return Numero(self.avanzar())
        if t.tipo == TipoToken.CADENA:
            return Cadena(self.avanzar())
        if t.tipo == TipoToken.BOOLEANO:
            return Booleano(self.avanzar())
        if t.tipo == TipoToken.IDENTIFICADOR:
            return Variable(self.avanzar())
        if t.tipo == TipoToken.PARENTESIS and t.valor == "(":
            self.avanzar()  # '('
            dentro = self.expresion_booleana()  # soporta expresiones aritméticas y lógicas entre ()
            self.esperar(TipoToken.PARENTESIS, ")")  # ')'
            return dentro
        raise ErrorSintactico(
            f"se esperaba un número, una variable o '(' y llegó '{t.valor}'",
            t.linea,
            t.columna,
        )

    # termino ::= factor (('*' | '/') factor)*
    def termino(self):
        izq = self.factor()
        while self.actual().tipo == TipoToken.OPERADOR and self.actual().valor in ("*", "/"):
            operador = self.avanzar()
            der = self.factor()
            izq = OperacionBinaria(izq, operador, der)
        return izq

    # expresion ::= termino (('+' | '-') termino)*
    def expresion(self):
        izq = self.termino()
        while self.actual().tipo == TipoToken.OPERADOR and self.actual().valor in ("+", "-"):
            operador = self.avanzar()
            der = self.termino()
            izq = OperacionBinaria(izq, operador, der)
        return izq

    # <declaracion_booleano> ::= "Q_booleano" <identificador> [ "=" <expresion_booleana> ]
    def declaracion_booleano(self):
        tipo = self.esperar(TipoToken.TIPO_BOOLEANO)
        nombre = self.esperar(TipoToken.IDENTIFICADOR)
        valor = None
        if self.actual().tipo == TipoToken.OPERADOR and self.actual().valor == "=":
            self.avanzar()
            valor = self.expresion_booleana()
        return Declaracion(tipo, nombre, valor)

    # <declaracion_texto> ::= "Q_texto" <identificador> [ "=" <expresion_texto> ]
    def declaracion_texto(self):
        tipo = self.esperar(TipoToken.TIPO_TEXTO)
        nombre = self.esperar(TipoToken.IDENTIFICADOR)
        valor = None
        if self.actual().tipo == TipoToken.OPERADOR and self.actual().valor == "=":
            self.avanzar()
            valor = self.expresion_texto()
        return Declaracion(tipo, nombre, valor)

    # <declaracion_numerico> ::= "Q_numerico" <identificador> [ "=" <expresion_numerica> ]
    def declaracion_numerico(self):
        tipo = self.esperar(TipoToken.TIPO_NUMERICO)
        nombre = self.esperar(TipoToken.IDENTIFICADOR)
        valor = None
        if self.actual().tipo == TipoToken.OPERADOR and self.actual().valor == "=":
            self.avanzar()
            valor = self.expresion_numerica()
        return Declaracion(tipo, nombre, valor)

    # <declaracion> ::= <declaracion_booleano> | <declaracion_texto> | <declaracion_numerico>
    def declaracion(self):
        t = self.actual()
        if t.tipo == TipoToken.TIPO_BOOLEANO:
            return self.declaracion_booleano()
        if t.tipo == TipoToken.TIPO_TEXTO:
            return self.declaracion_texto()
        if t.tipo == TipoToken.TIPO_NUMERICO:
            return self.declaracion_numerico()
        raise ErrorSintactico(
            f"se esperaba un tipo de declaración y llegó '{t.valor}'",
            t.linea,
            t.columna,
        )

    def asignacion(self):
        nombre = self.esperar(TipoToken.IDENTIFICADOR)
        self.esperar(TipoToken.OPERADOR, "=")
        valor = self.expresion_booleana()
        return Asignacion(nombre, valor)

    def bloque_llaves(self):
        llave = self.esperar(TipoToken.LLAVES, "{")
        instrucciones = []
        while not (self.actual().tipo == TipoToken.LLAVES and self.actual().valor == "}"):
            if self.actual().tipo == TipoToken.EOF:
                t = self.actual()
                raise ErrorSintactico(
                    f"falta '}}' para cerrar el bloque abierto en la línea {llave.linea}",
                    t.linea,
                    t.columna,
                )
            instrucciones.append(self.instruccion())
        self.avanzar()  # '}'
        return instrucciones

    def bloque_cuerpo(self, tok_referencia, tok_cierre_cabecera):
        if self.actual().tipo == TipoToken.LLAVES and self.actual().valor == "{":
            return self.bloque_llaves()

        instrucciones = []
        linea_previa = tok_cierre_cabecera.linea

        while (
            self.actual().tipo != TipoToken.EOF
            and self.actual().tipo != TipoToken.CONECTOR_SINO
            and self.actual().linea > linea_previa
            and self.actual().columna > tok_referencia.columna
        ):
            inst = self.instruccion()
            instrucciones.append(inst)
            linea_previa = self.tokens[self.pos - 1].linea

        if instrucciones:
            return instrucciones[0] if len(instrucciones) == 1 else instrucciones

        # Si está en la misma línea (ej. SI x < 18 ENTONCES activar_incubadora)
        return self.instruccion()

    def regla_si(self):
        tok_si = self.esperar(TipoToken.CONECTOR_SI)
        cond = self.expresion_booleana()
        tok_entonces = self.esperar(TipoToken.CONECTOR_ENTONCES)
        entonces = self.bloque_cuerpo(tok_si, tok_entonces)

        sino = None
        if self.actual().tipo == TipoToken.CONECTOR_SINO:
            tok_sino = self.avanzar()
            sino = self.bloque_cuerpo(tok_sino, tok_sino)

        return ReglaSi(cond, entonces, sino)

    def consola(self):
        self.esperar(TipoToken.CONSOLA)
        val = self.expresion_booleana()
        return Consola(val)

    def comentario(self):
        self.esperar(TipoToken.COMENTARIO)
        val = self.expresion_texto()
        return Comentario(val)

    # <bucle_clok> ::= "CLOK" <condicion> ":" <nueva_linea> <bloque_indentado>
    def bucle_clok(self):
        tok_clok = self.esperar(TipoToken.CONECTOR_CLOK)
        cond = self.expresion_booleana()

        if self.actual().tipo == TipoToken.LLAVES and self.actual().valor == "{":
            acciones = self.bloque_llaves()
            return BucleClok(cond, acciones)

        dos_puntos = self.esperar(TipoToken.DOS_PUNTOS, ":")

        acciones = []
        linea_previa = dos_puntos.linea

        while (
            self.actual().tipo != TipoToken.EOF
            and self.actual().linea > linea_previa
            and self.actual().columna > tok_clok.columna
        ):
            acciones.append(self.instruccion())
            linea_previa = self.tokens[self.pos - 1].linea

        if not acciones:
            t = self.actual()
            raise ErrorSintactico(
                f"se esperaba un bloque indentado con al menos una acción después de ':' y llegó '{t.valor}'",
                t.linea,
                t.columna,
            )

        return BucleClok(cond, acciones)

    def instruccion(self):
        t = self.actual()
        if t.tipo in (
            TipoToken.TIPO_BOOLEANO,
            TipoToken.TIPO_TEXTO,
            TipoToken.TIPO_NUMERICO,
        ):
            return self.declaracion()
        if t.tipo == TipoToken.ACCION:
            return Accion(self.avanzar())
        if t.tipo == TipoToken.IDENTIFICADOR:
            if self.siguiente().tipo == TipoToken.OPERADOR and self.siguiente().valor == "=":
                return self.asignacion()
            return Accion(self.avanzar())
        if t.tipo == TipoToken.CONECTOR_SI:
            return self.regla_si()
        if t.tipo == TipoToken.CONSOLA:
            return self.consola()
        if t.tipo == TipoToken.COMENTARIO:
            return self.comentario()
        if t.tipo == TipoToken.CONECTOR_CLOK:
            return self.bucle_clok()
        raise ErrorSintactico(
            f"se esperaba el inicio de una instrucción y llegó '{t.valor}'",
            t.linea,
            t.columna,
        )

    def programa(self):
        instrucciones = []
        while self.actual().tipo != TipoToken.EOF:
            instrucciones.append(self.instruccion())
        return Programa(instrucciones)
