# 🦆 Quack — un lenguaje de programación en español

**Quack** es un lenguaje de programación escrito en Python, pensado para
controlar (de forma simulada) un **nido / incubadora de ornitorrincos** —de ahí nombres
como `clasificar_como_ornitorrinco_perry` o `activar_incubadora`—.

El proyecto implementa un **intérprete completo** con las tres fases clásicas de un
compilador/intérprete:

1. **Análisis léxico** (`lexer.py`): convierte el texto en una lista de *tokens*.
2. **Análisis sintáctico** (`parser.py`): convierte los tokens en un **árbol de sintaxis abstracta (AST)**.
3. **Análisis semántico + ejecución** (`interprete.py`): recorre el árbol, revisa los tipos y ejecuta el programa.

Todo está escrito a mano, sin librerías externas (no usa PLY, ANTLR, Lark, etc.).

---

## Índice

- [Requisitos y cómo ejecutarlo](#requisitos-y-cómo-ejecutarlo)
- [Estructura del proyecto](#estructura-del-proyecto)
- [El lenguaje Quack en 5 minutos](#el-lenguaje-quack-en-5-minutos)
- [Cómo funciona por dentro (visión general)](#cómo-funciona-por-dentro-visión-general)
- [Paso 1 — `tokens.py`: el vocabulario](#paso-1--tokenspy-el-vocabulario)
- [Paso 2 — `lexer.py`: de texto a tokens](#paso-2--lexerpy-de-texto-a-tokens)
- [Paso 3 — `arbol.py`: los nodos del árbol](#paso-3--arbolpy-los-nodos-del-árbol)
- [Paso 4 — `parser.py`: de tokens a árbol](#paso-4--parserpy-de-tokens-a-árbol)
- [Paso 5 — `interprete.py`: ejecutar el árbol](#paso-5--interpretepy-ejecutar-el-árbol)
- [Paso 6 — `main.py`: el punto de entrada](#paso-6--mainpy-el-punto-de-entrada)
- [Ejemplo completo de principio a fin](#ejemplo-completo-de-principio-a-fin)
- [Manejo de errores](#manejo-de-errores)
- [Archivos de ejemplo](#archivos-de-ejemplo)
- [Detalles, limitaciones y cosas a tener en cuenta](#detalles-limitaciones-y-cosas-a-tener-en-cuenta)

---

## Requisitos y cómo ejecutarlo

- **Python 3.11 o superior** (el código usa `enum.StrEnum`, que apareció en Python 3.11).
- No necesita instalar nada más.

Hay que ejecutarlo **desde la carpeta del proyecto**, porque los módulos se importan entre sí
por nombre (`from tokens import ...`, `from lexer import ...`).

```bash
cd Quack-main

# 1) Ejecutar un programa escrito en un archivo
python main.py programa.txt

# 2) Ver el árbol de sintaxis (AST) en lugar de ejecutar el programa
python main.py programa.txt --arbol

# 3) Modo interactivo (REPL): escribe instrucciones línea por línea
python main.py
> Q_numerico x = 10
> kukukuku x * 2
20
> salir
```

En el modo interactivo se sale con `salir`, `exit`, `Ctrl+D` o `Ctrl+C`. Las variables se
conservan entre líneas porque se reutiliza el mismo intérprete.

---

## Estructura del proyecto

| Archivo | Qué contiene | Fase |
|---|---|---|
| `tokens.py` | Tipos de token, palabras reservadas, lista de acciones, clase `Token` y clases de error | Base compartida |
| `lexer.py` | Función `tokenizar(texto)` | Análisis léxico |
| `arbol.py` | Clases de los nodos del AST y `mostrar_arbol()` para imprimirlo | Representación |
| `parser.py` | Clase `Parser` (descendente recursivo) + la gramática EBNF en comentarios | Análisis sintáctico |
| `interprete.py` | Clases `Entorno` (tabla de símbolos) e `Interprete` | Semántica y ejecución |
| `main.py` | Lee el archivo o abre el REPL, conecta todas las fases y muestra errores | Punto de entrada |
| `error_lexico.py` | Copia antigua de las clases de error (**no se usa**, ver limitaciones) | — |
| `programa.txt` | Programa de demostración completo | Ejemplo |
| `programa_valido.txt` | Ejemplo con comentarios `/* */` y `kirikiki` | Ejemplo |
| `programa_invalido.txt` | Ejemplo con un carácter ilegal (`@`) | Ejemplo |

---

## El lenguaje Quack en 5 minutos

### Tipos de datos y declaración de variables

| Palabra | Tipo | Valor por defecto | Ejemplo |
|---|---|---|---|
| `Q_numerico` | Número (entero o decimal) | `0` | `Q_numerico temperatura = 17.5` |
| `Q_texto` | Texto entre comillas dobles | `""` | `Q_texto especie = "Perry"` |
| `Q_booleano` | `verdadero` / `falso` | `falso` | `Q_booleano pone_huevos = verdadero` |

```quack
Q_numerico humedad          /* sin valor: queda en 0 */
humedad = 45                /* asignación a una variable ya declarada */
```

### Operadores

| Categoría | Operadores | Notas |
|---|---|---|
| Aritméticos | `+  -  *  /` | `+` también concatena dos textos |
| Unarios | `-x` (negativo), `!x` (negación) | `!` solo con booleanos |
| Comparación | `<  >  <=  >=  ==  !=  =` | `=` dentro de una condición funciona como `==` |
| Lógicos | `Y` (and), `O` (or) | Solo con booleanos |
| Agrupación | `( ... )` | |

Precedencia (de mayor a menor): `()` y `-` unario → `*  /` → `+  -` → comparaciones → `!` → `Y` → `O`.

### Instrucciones

| Instrucción | Sintaxis | Qué hace |
|---|---|---|
| Imprimir | `kukukuku <expresión>` | Muestra el valor en consola (los booleanos salen como `verdadero`/`falso`) |
| Comentario de línea | `kirikiki "texto"` | Se ignora al ejecutar (pero sí aparece en el árbol) |
| Comentario de bloque | `/* ... */` | Lo descarta el lexer; puede ocupar varias líneas |
| Acción | `activar_incubadora` | Simula una acción del sistema: imprime su nombre |
| Condicional | `SI <cond> ENTONCES ... SINO ...` | Ejecuta un bloque u otro |
| Ciclo | `CLOK <cond> : ...` o `CLOK <cond> { ... }` | Repite mientras la condición sea verdadera |

### Bloques: por indentación o con llaves

Los cuerpos de `SI`, `SINO` y `CLOK` se pueden escribir de dos formas:

```quack
/* 1) Por indentación (las instrucciones van más a la derecha que SI / CLOK) */
SI temperatura < 18 ENTONCES
    activar_incubadora
    kukukuku "hace frío"
SINO
    apagar_incubadora

CLOK temperatura < 18 :
    temperatura = temperatura + 1

/* 2) Con llaves */
SI temperatura < 18 ENTONCES {
    activar_incubadora
} SINO {
    apagar_incubadora
}

CLOK huevos < 3 {
    huevos = huevos + 1
}

/* 3) SI de una sola instrucción en la misma línea */
SI humedad <= 20 ENTONCES activar_riego
```

### Acciones predefinidas

Están en `tokens.py` (conjunto `ACCIONES`). Al ejecutarse, simplemente se imprime su nombre:

`activar_incubadora`, `prender_incubadora`, `apagar_incubadora`, `activar_riego`,
`desactivar_riego`, `encender_ventilacion`, `apagar_ventilacion`, `iniciar_humidificacion`,
`activar_calefaccion`, `emitir_alerta_temperatura`, `emitir_alerta_humedad`,
`notificar_peligro_nido`, `alertar_especie_peligrosa`, `dar_alerta_venenoso`,
`especie_posible_ornitorrinco`, `clasificar_como_ornitorrinco_perry`, `clasificar_como_ave`,
`clasificar_como_reptil`, `clasificar_como_monotrema`, `clasificar_como_equidna`,
`registrar_eclosion`, `marcar_huevo_fertil`, `solicitar_revision_manual`.

---

## Cómo funciona por dentro (visión general)

```
 programa.txt (texto)
        │
        ▼
 ┌──────────────┐   lista de Token     ┌──────────────┐   árbol (AST)   ┌────────────────┐
 │  lexer.py    │ ───────────────────▶ │  parser.py   │ ──────────────▶ │ interprete.py  │ ──▶ salida
 │ tokenizar()  │                      │ Parser       │                 │ Interprete     │    en consola
 └──────────────┘                      └──────────────┘                 └────────────────┘
        │                                     │                                │
   ErrorLexico                         ErrorSintactico                   ErrorSemantico
        └─────────────────────────────────────┴────────────────────────────────┘
                                              │
                                   main.py: mostrar_error()
```

`main.py` hace literalmente esto:

```python
tokens   = tokenizar(contenido)          # fase 1
programa = Parser(tokens).programa()     # fase 2
Interprete().ejecutar_programa(programa) # fase 3  (o mostrar_arbol(programa) con --arbol)
```

Las tres clases de error heredan de una misma clase base (`ErrorDeLenguaje`), así que
`main.py` puede capturarlas todas con un único `except` y mostrarlas igual.

---

## Paso 1 — `tokens.py`: el vocabulario

Este archivo no "hace" nada por sí solo; define las piezas que usan los demás.

### 1.1 `TipoToken`
Un `StrEnum` con todas las categorías de token posibles:

| Tipo | Ejemplos |
|---|---|
| `NUMERO` | `17.5`, `45` |
| `CADENA` | `"Perry"` (se guarda sin comillas) |
| `BOOLEANO` | `verdadero`, `falso` |
| `TIPO_NUMERICO`, `TIPO_TEXTO`, `TIPO_BOOLEANO` | `Q_numerico`, `Q_texto`, `Q_booleano` |
| `CONSOLA` | `kukukuku` |
| `COMENTARIO` | `kirikiki` |
| `CONECTOR_Y`, `CONECTOR_O` | `Y`, `O` |
| `CONECTOR_SI`, `CONECTOR_ENTONCES`, `CONECTOR_SINO` | `SI`, `ENTONCES`, `SINO` |
| `CONECTOR_CLOK` | `CLOK` |
| `ACCION` | `activar_riego`, ... |
| `IDENTIFICADOR` | nombres de variables: `temperatura` |
| `OPERADOR` | `+ - * / = == != < > <= >=` |
| `NEGACION` | `!` |
| `PARENTESIS`, `LLAVES`, `DOS_PUNTOS` | `( )`, `{ }`, `:` |
| `EOF` | marca el final del archivo |

### 1.2 `ACCIONES` y `PALABRAS_RESERVADAS`
- `ACCIONES` es un conjunto con los nombres de las acciones del nido.
- `PALABRAS_RESERVADAS` es un diccionario `palabra → TipoToken`. Incluye las palabras clave
  y, con `**{accion: TipoToken.ACCION for accion in ACCIONES}`, también todas las acciones.
  El lexer lo consulta para decidir si una palabra es reservada o un identificador.

### 1.3 `Token`
Un `dataclass` con cuatro campos: `tipo`, `valor` (el texto original), `linea` y `columna`.
Guardar la posición es lo que permite luego mostrar errores con `^` apuntando al lugar exacto.
Su `__repr__` lo imprime así: `NUMERO('20.5') en 1:38`.

### 1.4 Las clases de error
```
Exception
 └── ErrorDeLenguaje      (guarda mensaje, línea y columna)
      ├── ErrorLexico     fase = "Error léxico"
      ├── ErrorSintactico fase = "Error sintáctico"
      └── ErrorSemantico  fase = "Error semántico"
```
El constructor arma el mensaje con el formato:
`"<fase> en línea <L>, columna <C>: <mensaje>"`.

---

## Paso 2 — `lexer.py`: de texto a tokens

La función `tokenizar(texto)` recorre el texto **carácter por carácter** con un índice
(`ciclos`) y lleva la cuenta de la posición (`fila`, `columna`). En cada vuelta mira el
carácter actual `c` y decide qué hacer:

| Si `c` es... | Qué hace |
|---|---|
| `\n` | Sube `fila`, reinicia `columna = 1`. No genera token. |
| espacio, `\t`, `\r` | Avanza una columna. No genera token. |
| un dígito | Lee dígitos y puntos seguidos → token `NUMERO`. Da error si hay **dos puntos** (`1.2.3`) o si **termina en punto** (`5.`). |
| letra o `_` | Lee letras y `_` seguidos → busca la palabra en `PALABRAS_RESERVADAS`; si no está, es `IDENTIFICADOR`. |
| `"` | Lee hasta la siguiente `"` (puede cruzar líneas) → token `CADENA` sin las comillas. Si se acaba el archivo: error `cadena sin cerrar`. |
| `/` seguido de `*` | Comentario de bloque: salta todo hasta `*/`. **No genera token.** Si no se cierra: error `comentario sin cerrar`. |
| `+ - * /` | Token `OPERADOR`. |
| `=` | Mira el siguiente carácter: `==` o `=`. |
| `<` o `>` | Mira el siguiente: `<=`, `>=`, o solo `<` / `>`. |
| `!` | Si sigue `=` es el operador `!=`; si no, es `NEGACION`. |
| `(` `)` | Token `PARENTESIS`. |
| `{` `}` | Token `LLAVES`. |
| `:` | Token `DOS_PUNTOS`. |
| cualquier otra cosa | `ErrorLexico("carácter inesperado ...")` |

Al final agrega un token `EOF` para que el parser sepa dónde termina todo.

> 💡 La técnica de mirar el carácter siguiente para distinguir `=` de `==` se llama
> *lookahead* (mirar adelante) de un carácter.

**Ejemplo real** — esta entrada:

```quack
Q_numerico promedio = (temperatura + 20.5) / 2
SI temperatura < 18 ENTONCES
    activar_incubadora
```

produce estos tokens:

```
TIPO_NUMERICO('Q_numerico') en 1:1
IDENTIFICADOR('promedio') en 1:12
OPERADOR('=') en 1:21
PARENTESIS('(') en 1:23
IDENTIFICADOR('temperatura') en 1:24
OPERADOR('+') en 1:36
NUMERO('20.5') en 1:38
PARENTESIS(')') en 1:42
OPERADOR('/') en 1:44
NUMERO('2') en 1:46
CONECTOR_SI('SI') en 2:1
IDENTIFICADOR('temperatura') en 2:4
OPERADOR('<') en 2:16
NUMERO('18') en 2:18
CONECTOR_ENTONCES('ENTONCES') en 2:21
ACCION('activar_incubadora') en 3:5
EOF('') en 3:23
```

Fíjate que el lexer **no genera tokens de salto de línea ni de indentación**; solo guarda la
línea y la columna de cada token. El parser usará esas posiciones para detectar los bloques
indentados.

---

## Paso 3 — `arbol.py`: los nodos del árbol

Define, con `@dataclass`, un tipo de nodo para cada construcción del lenguaje:

| Nodo | Campos | Representa |
|---|---|---|
| `Programa` | `instrucciones` | La raíz: lista de todas las instrucciones |
| `Declaracion` | `tipo`, `nombre`, `valor` (opcional) | `Q_numerico x = 5` |
| `Asignacion` | `nombre`, `valor` | `x = x + 1` |
| `ReglaSi` | `condicion`, `entonces`, `sino` (opcional) | `SI ... ENTONCES ... SINO ...` |
| `BucleClok` | `condicion`, `acciones` | `CLOK ... :` |
| `Consola` | `valor` | `kukukuku ...` |
| `Comentario` | `valor` | `kirikiki ...` |
| `Accion` | `token` | `activar_riego` |
| `Condicion` | `variable` (lado izq.), `operador`, `valor` (lado der.) | `a < b`, `a == b` |
| `OperacionBinaria` | `izq`, `operador`, `der` | `a + b`, `a Y b`, `a O b` |
| `OperacionUnaria` | `operador`, `operando` | `-a`, `!a` |
| `Numero`, `Cadena`, `Booleano`, `Variable` | `token` | Las hojas del árbol |

Los nodos guardan el **token original** (no solo el valor), para poder reportar la línea y
columna si algo falla en la ejecución.

La función `mostrar_arbol(nodo, nivel)` recorre el árbol recursivamente y lo imprime con dos
espacios de sangría por nivel. Es lo que se ve al usar `--arbol`.

---

## Paso 4 — `parser.py`: de tokens a árbol

### 4.1 La gramática

Al inicio del archivo está la gramática en notación **EBNF**. Resumida:

```
programa           ::= instruccion* EOF
instruccion        ::= declaracion | asignacion | regla_si | bucle_clok | consola | comentario | ACCION
declaracion        ::= ("Q_booleano" | "Q_texto" | "Q_numerico") IDENTIFICADOR ( "=" expresion )?
asignacion         ::= IDENTIFICADOR "=" expresion
regla_si           ::= "SI" expresion_booleana "ENTONCES" bloque ( "SINO" bloque )?
bucle_clok         ::= "CLOK" expresion_booleana ( ":" bloque_indentado | "{" instruccion* "}" )
consola            ::= "kukukuku" expresion
comentario         ::= "kirikiki" expresion

expresion_booleana ::= termino_booleano ( "O" termino_booleano )*
termino_booleano   ::= factor_booleano ( "Y" factor_booleano )*
factor_booleano    ::= "!" factor_booleano | condicion
condicion          ::= expresion ( COMPARADOR expresion )?
expresion          ::= termino ( ("+" | "-") termino )*
termino            ::= factor ( ("*" | "/") factor )*
factor             ::= "-" factor | NUMERO | CADENA | BOOLEANO | IDENTIFICADOR | "(" expresion_booleana ")"
```

(La versión del archivo menciona `INDENT/DEDENT`; en la práctica el parser no recibe esos
tokens, sino que compara columnas, como se explica abajo. Tampoco menciona los bloques con
llaves, que sí están implementados.)

### 4.2 Técnica: descenso recursivo

El `Parser` es un **parser descendente recursivo**: hay **un método por cada regla** de la
gramática, y cada método llama a los métodos de las reglas que contiene. Por ejemplo,
`expresion()` llama a `termino()`, que llama a `factor()`.

La **precedencia de operadores sale sola de esta jerarquía**: lo que está más abajo en la
cadena de llamadas se agrupa primero. Por eso `2 + 3 * 4` se agrupa como `2 + (3 * 4)`.

### 4.3 Métodos auxiliares

| Método | Qué hace |
|---|---|
| `actual()` | Devuelve el token en la posición `pos` (o `EOF` si se pasó). |
| `siguiente()` | Mira el token de después **sin avanzar** (lookahead de 1 token). |
| `avanzar()` | Devuelve el token actual y mueve `pos` uno adelante. |
| `esperar(tipo, valor)` | Exige que el token actual sea de ese tipo/valor; si no, lanza `ErrorSintactico("se esperaba X y llegó Y")`. Si sí, avanza. |
| `imprimir()` | Utilidad de depuración: imprime todos los tokens. |

### 4.4 Paso a paso: cómo se reconoce cada instrucción

**`programa()`** — repite `instruccion()` hasta encontrar `EOF` y devuelve `Programa(lista)`.

**`instruccion()`** — mira el token actual y decide qué regla usar:

| Token actual | Llama a |
|---|---|
| `Q_numerico` / `Q_texto` / `Q_booleano` | `declaracion()` |
| `ACCION` | crea `Accion(token)` |
| `IDENTIFICADOR` seguido de `=` | `asignacion()` (usa `siguiente()` para decidirlo) |
| `IDENTIFICADOR` sin `=` | lo trata como `Accion` |
| `SI` | `regla_si()` |
| `kukukuku` | `consola()` |
| `kirikiki` | `comentario()` |
| `CLOK` | `bucle_clok()` |
| otro | `ErrorSintactico("se esperaba el inicio de una instrucción...")` |

**`declaracion()`** — según el tipo llama a `declaracion_numerico/texto/booleano()`. Cada una:
1. `esperar` el tipo (`Q_numerico`...),
2. `esperar` un `IDENTIFICADOR`,
3. si viene `=`, avanza y lee la expresión,
4. devuelve `Declaracion(tipo, nombre, valor)`.

> El parser **no revisa tipos** aquí: `Q_numerico x = "hola"` es sintácticamente válido. El
> error de tipos lo detecta el intérprete.

**`asignacion()`** — `IDENTIFICADOR`, `=`, expresión → `Asignacion(nombre, valor)`.

**`consola()` / `comentario()`** — consumen la palabra clave y leen una expresión.

**`regla_si()`**:
1. `esperar("SI")` y guardar ese token (su columna sirve de referencia),
2. leer la condición con `expresion_booleana()`,
3. `esperar("ENTONCES")`,
4. leer el cuerpo con `bloque_cuerpo()`,
5. si el siguiente token es `SINO`, leer otro cuerpo,
6. devolver `ReglaSi(cond, entonces, sino)`.

**`bloque_cuerpo(tok_referencia, tok_cierre_cabecera)`** — esta es la parte más ingeniosa,
porque decide **dónde termina un bloque por indentación**:

1. Si el siguiente token es `{`, delega en `bloque_llaves()`.
2. Si no, va leyendo instrucciones **mientras** el token actual:
   - no sea `EOF` ni `SINO`,
   - esté en una **línea posterior** a la última instrucción leída, y
   - esté en una **columna mayor** que la de `SI` (o `SINO`).
3. Cuando una instrucción aparece en una columna igual o menor, el bloque terminó.
4. Si no encontró ninguna instrucción en líneas siguientes, asume la forma en la **misma
   línea** (`SI x < 18 ENTONCES activar_incubadora`) y lee una sola instrucción.
5. Si el bloque tiene una sola instrucción devuelve ese nodo; si tiene varias, una lista.

```
SI temperatura < 18 ENTONCES      ← SI está en la columna 1
    activar_incubadora             ← columna 5 > 1 → dentro del bloque
    kukukuku "frío"                ← columna 5 > 1 → dentro del bloque
kukukuku "fin"                     ← columna 1, no es > 1 → fuera del bloque
```

**`bloque_llaves()`** — espera `{`, lee instrucciones hasta `}`. Si llega a `EOF` sin cerrar,
lanza `falta '}' para cerrar el bloque abierto en la línea N`.

**`bucle_clok()`**:
1. `esperar("CLOK")`, leer la condición,
2. si viene `{` → bloque con llaves,
3. si no → `esperar(":")` y leer instrucciones con la misma regla de columnas que `SI`
   (deben estar en líneas siguientes y más a la derecha que `CLOK`),
4. si el bloque quedó vacío → error `se esperaba un bloque indentado...`,
5. devuelve `BucleClok(cond, acciones)`.

### 4.5 Paso a paso: cómo se reconocen las expresiones

Cada nivel lee un "operando" del nivel inferior y, mientras vea su operador, sigue
construyendo `OperacionBinaria` hacia la izquierda (asociatividad izquierda):

1. **`expresion_booleana()`** — `termino_booleano` separados por `O`.
2. **`termino_booleano()`** — `factor_booleano` separados por `Y` (por eso `Y` tiene más
   prioridad que `O`).
3. **`factor_booleano()`** — si ve `!`, crea `OperacionUnaria("!", ...)`; si no, va a `condicion()`.
4. **`condicion()`** — lee una `expresion`; si después viene un comparador
   (`> < = >= <= == !=`), lee otra y crea `Condicion(izq, op, der)`. Si no viene comparador,
   devuelve la expresión tal cual.
5. **`expresion()`** — `termino` separados por `+` o `-`.
6. **`termino()`** — `factor` separados por `*` o `/`.
7. **`factor()`** — el nivel más bajo:
   - `-` → `OperacionUnaria("-", factor())`
   - `NUMERO` → `Numero`, `CADENA` → `Cadena`, `BOOLEANO` → `Booleano`, `IDENTIFICADOR` → `Variable`
   - `(` → lee una `expresion_booleana()` completa y espera `)`
   - otra cosa → `ErrorSintactico`

**Ejemplo**: `(temperatura + 20.5) / 2` queda así:

```
OperacionBinaria /
  OperacionBinaria +
    Variable temperatura
    Numero 20.5
  Numero 2
```

---

## Paso 5 — `interprete.py`: ejecutar el árbol

### 5.1 `Entorno`: la tabla de símbolos

Guarda las variables en un diccionario `nombre → {"tipo", "valor", "linea"}` y tiene una
referencia a su **entorno padre**. Así se implementan los **alcances (scopes)**:

- `declarar(...)` — registra una variable en el entorno actual. Si ya existe **en ese mismo
  entorno**, lanza `la variable 'x' ya fue declarada en la línea N`.
- `buscar(...)` — busca la variable en el entorno actual; si no está, sube al padre, y así
  hasta la raíz. Si no la encuentra, lanza `la variable 'x' no ha sido declarada`.

```
Entorno global       { temperatura, especie, humedad }
   └── Entorno del SI  { variable_local }     ← puede leer las globales
```

### 5.2 Tablas de apoyo

- `ACEPTA`: qué tipos de Python acepta cada tipo de Quack
  (`Q_numerico → int/float`, `Q_texto → str`, `Q_booleano → bool`).
  Se compara con `type(valor)` y no con `isinstance` porque en Python `True` también es un `int`.
- `VALORES_POR_DEFECTO`: `0`, `""`, `False`.
- `MAX_ITERACIONES_CLOK = 100000`: límite de seguridad contra ciclos infinitos.

### 5.3 `ejecutar(nodo)`: las instrucciones

| Nodo | Qué hace paso a paso |
|---|---|
| `Declaracion` | 1) Evalúa el valor (o usa el valor por defecto). 2) Verifica que el tipo coincida con `ACEPTA`. 3) Lo registra con `entorno.declarar`. |
| `Asignacion` | 1) Busca la variable (debe existir). 2) Evalúa el nuevo valor. 3) Verifica que sea del mismo tipo con que se declaró. 4) Actualiza el valor. |
| `Consola` | Evalúa la expresión y la imprime; los booleanos se imprimen como `verdadero`/`falso`. |
| `Comentario` | No hace nada. |
| `Accion` | Imprime el nombre de la acción (simula que se ejecutó). |
| `ReglaSi` | Evalúa la condición; si es verdadera ejecuta `entonces`, si no y hay `sino`, ejecuta `sino`. Cada rama corre en un **entorno nuevo**. |
| `BucleClok` | Mientras la condición sea verdadera, ejecuta el cuerpo en un **entorno nuevo en cada vuelta**. Si pasa de 100 000 vueltas lanza `el ciclo superó 100000 vueltas; ¿falta actualizar la variable de la condición?`. |

`_ejecutar_bloque(cuerpo)` es quien crea el entorno hijo, ejecuta las instrucciones y, en un
`finally`, restaura el entorno anterior (aunque ocurra un error). Por eso una variable
declarada dentro de un `SI` **no existe fuera** de él.

### 5.4 `evaluar(nodo)`: las expresiones

| Nodo | Resultado |
|---|---|
| `Numero` | `float` si el texto tiene punto, si no `int` |
| `Cadena` | el texto |
| `Booleano` | `True` si es `verdadero` |
| `Variable` | busca la variable en el entorno y devuelve su valor |
| `OperacionUnaria` | `-` solo con números; `!` solo con booleanos |
| `OperacionBinaria` | evalúa ambos lados y llama a `operar()` |
| `Condicion` | evalúa ambos lados y llama a `comparar()` |

### 5.5 `operar()`: reglas de tipos para `+ - * / Y O`

1. `Y` / `O` → ambos lados deben ser booleanos.
2. Si algún lado es texto → solo se permite `texto + texto` (concatenación).
3. Si algún lado es booleano → error (no hay aritmética con booleanos).
4. Números → `+ - * /`.
   - División entre cero → error `división por cero`.
   - Si se dividen dos enteros y la división es exacta, el resultado es entero (`6/3 → 2`);
     si no, es decimal (`7/2 → 3.5`).

### 5.6 `comparar()`: reglas de tipos para comparaciones

- `==`, `=` y `!=` → los dos lados deben ser del mismo tipo (se permite comparar `int` con
  `float`). Comparar texto con número da error.
- `< > <= >=` → solo entre números.

---

## Paso 6 — `main.py`: el punto de entrada

1. **Sin argumentos** → `modo_interactivo()`:
   - Crea **un solo** `Interprete` (así las variables persisten entre líneas).
   - En un ciclo: lee una línea con `input("> ")`, la tokeniza, la parsea y la ejecuta.
   - Si hay error, lo muestra y sigue pidiendo líneas (no se cierra).
2. **Con un archivo** → lo lee en UTF-8 (si no existe: `Error: No se encontró el archivo`).
   - Tokeniza y parsea.
   - Con `--arbol` imprime el AST; sin él, ejecuta el programa.
   - Si ocurre un error del lenguaje, lo muestra y termina con código de salida `1`.
3. **`mostrar_error(error, codigo)`** imprime el mensaje, la línea de código donde ocurrió y
   un `^` debajo de la columna exacta.

---

## Ejemplo completo de principio a fin

`programa.txt`:

```quack
/* Programa de demostracion Quack
: revisa el nido de Perry */
Q_numerico temperatura = 17.5
Q_texto especie = "Perry"
Q_numerico humedad = 45
Q_booleano pone_huevos = verdadero
Q_numerico promedio = (temperatura + 20.5) / 2
/* reglas que revisan
   el estado del nido */
SI temperatura < 18 ENTONCES
    activar_incubadora
SI humedad <= 20 O temperatura >= 32.8 ENTONCES
    activar_riego
SI especie == "Perry" Y pone_huevos != falso ENTONCES
    clasificar_como_ornitorrinco_perry
CLOK temperatura < 18 :
    activar_incubadora
    temperatura = temperatura + 1
kukukuku "Revision del nido terminada"
```

Qué pasa en la ejecución, instrucción por instrucción:

| # | Instrucción | Efecto |
|---|---|---|
| 1 | Comentario `/* ... */` | El lexer lo descarta. |
| 2 | `Q_numerico temperatura = 17.5` | `temperatura = 17.5` |
| 3 | `Q_texto especie = "Perry"` | `especie = "Perry"` |
| 4 | `Q_numerico humedad = 45` | `humedad = 45` |
| 5 | `Q_booleano pone_huevos = verdadero` | `pone_huevos = True` |
| 6 | `Q_numerico promedio = (17.5 + 20.5) / 2` | `promedio = 19.0` |
| 7 | `SI 17.5 < 18` → verdadero | imprime `activar_incubadora` |
| 8 | `SI 45 <= 20 O 17.5 >= 32.8` → falso O falso | no hace nada |
| 9 | `SI "Perry" == "Perry" Y verdadero != falso` → verdadero | imprime `clasificar_como_ornitorrinco_perry` |
| 10 | `CLOK 17.5 < 18` | 1.ª vuelta: imprime `activar_incubadora`, `temperatura = 18.5`. 2.ª revisión: `18.5 < 18` es falso → sale. |
| 11 | `kukukuku "..."` | imprime el texto |

Salida:

```
$ python main.py programa.txt
activar_incubadora
clasificar_como_ornitorrinco_perry
activar_incubadora
Revision del nido terminada
```

Y con `--arbol` se ve el AST (fragmento):

```
Programa
  Declaracion Q_numerico temperatura
    Numero 17.5
  ...
  ReglaSi
    OperacionBinaria Y
      Condicion ==
        Variable especie
        Cadena "Perry"
      Condicion !=
        Variable pone_huevos
        Booleano falso
    Accion clasificar_como_ornitorrinco_perry
  BucleClok
    Condicion <
      Variable temperatura
      Numero 18
    Accion activar_incubadora
    Asignacion temperatura
      OperacionBinaria +
        Variable temperatura
        Numero 1
  Consola
    Cadena "Revision del nido terminada"
```

---

## Manejo de errores

Cada fase detecta su propio tipo de error y todos se muestran con el mismo formato:

```
<Tipo de error> en línea L, columna C: <mensaje>
    <línea del código>
    <espacios>^
```

| Fase | Ejemplos de error |
|---|---|
| **Léxico** | `carácter inesperado '@'`, `numero no valido` (`5.` o `1.2.3`), `cadena sin cerrar`, `comentario sin cerrar` |
| **Sintáctico** | `se esperaba 'ENTONCES' y llegó ...`, `se esperaba el inicio de una instrucción y llegó '+'`, `falta '}' para cerrar el bloque...`, `se esperaba un bloque indentado...` |
| **Semántico** | variable no declarada, variable ya declarada, tipo incorrecto en declaración/asignación, `no se puede usar '+' con textos`, operadores con booleanos, comparar tipos incompatibles, `división por cero`, ciclo de más de 100 000 vueltas |

Ejemplo real con `programa_invalido.txt`:

```
$ python main.py programa_invalido.txt
Error léxico en línea 1, columna 19: carácter inesperado '@'
    Q_numerico x = 42 @ 10
                      ^
```

Ejemplos en el modo interactivo:

```
> Q_texto s = "x" + 1
Error semántico en línea 1, columna 17: no se puede usar '+' con textos
    Q_texto s = "x" + 1
                    ^
> kukukuku b
Error semántico en línea 1, columna 10: la variable 'b' no ha sido declarada
    kukukuku b
             ^
```

---

## Archivos de ejemplo

| Archivo | Resultado al ejecutarlo |
|---|---|
| `programa.txt` | Se ejecuta correctamente (ver salida arriba). |
| `programa_invalido.txt` | Error léxico por el carácter `@`. |
| `programa_valido.txt` | Sirve para ver que los comentarios `/* */` multilínea se ignoran, **pero en realidad produce un error sintáctico**: `X + 5` no es una instrucción válida (una expresión suelta no puede ir sola). Si se quita esa parte, o se cambia por `kukukuku X + 5` con `X` declarada, funciona. |

```
$ python main.py programa_valido.txt
Error sintáctico en línea 1, columna 3: se esperaba el inicio de una instrucción y llegó '+'
    X + 5 /* esto
      ^
```

---

## Detalles, limitaciones y cosas a tener en cuenta

Cosas que se observan al leer y probar el código, útiles si vas a seguir desarrollándolo:

1. **`error_lexico.py` no se usa.** Es una copia antigua de las clases de error (ni siquiera
   tiene `ErrorSemantico`). Las clases que realmente se usan están en `tokens.py`. Se puede borrar.
2. **Los identificadores no pueden tener números.** El lexer solo acepta letras y `_`, así que
   `sensor1` se parte en `sensor` + `1`.
3. **Cualquier palabra suelta se ejecuta como acción.** Si un `IDENTIFICADOR` no va seguido de
   `=`, el parser lo convierte en `Accion` y el intérprete imprime su nombre. Es decir,
   `hola` imprime `hola` aunque no esté en la lista `ACCIONES`; esa lista solo sirve para
   clasificar el token como `ACCION`.
4. **Las condiciones de `SI` y `CLOK` no exigen un booleano.** Se usa la "veracidad" de Python,
   así que `SI 5 ENTONCES ...` se ejecuta (porque 5 es "verdadero" en Python) y
   `SI 0 ENTONCES ...` no.
5. **`=` funciona como comparación dentro de condiciones.** `SI x = 5 ENTONCES` es lo mismo que
   `SI x == 5 ENTONCES`.
6. **Indentación por columnas.** Un tabulador cuenta como una sola columna, así que mezclar
   tabs y espacios puede cambiar qué instrucciones quedan dentro de un bloque.
7. **El `SINO` siempre se une al `SI` más cercano** que lo esté esperando (el clásico
   "dangling else"). Si se anidan `SI`, conviene usar llaves.
8. **Cada vuelta de `CLOK` tiene su propio alcance.** Una variable declarada dentro del ciclo
   se crea de nuevo en cada vuelta y no existe fuera de él.
9. **El modo interactivo procesa una línea a la vez**, así que los bloques por indentación
   (varias líneas) no se pueden escribir ahí; se pueden usar llaves en una sola línea:
   `SI verdadero ENTONCES { kukukuku 1 }`.
10. **`kirikiki` no evalúa su contenido**, así que `kirikiki x` no falla aunque `x` no exista.
11. **El `-` unario se une al factor más cercano**: `-a * 2` es `(-a) * 2`.
12. **No se puede ejecutar con `python -I`** (modo aislado) ni desde otra carpeta, porque los
    módulos se importan por nombre relativo a la carpeta del proyecto.
13. **La gramática EBNF en el comentario de `parser.py` está un poco desactualizada**: menciona
    `INDENT/DEDENT` (que no existen como tokens) y no incluye los bloques con llaves.
