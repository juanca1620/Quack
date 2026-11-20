from tokens import Token, TipoToken, PALABRAS_RESERVADAS, ErrorLexico


def tokenizar(texto):
    tokens = []
    columna = 1
    fila = 1
    ciclos = 0

    while ciclos < len(texto):
        c = texto[ciclos]

        if c == "\n":
            columna = 1
            fila += 1
            ciclos += 1
            continue

        if c in (" ", "\t", "\r"):
            columna += 1
            ciclos += 1
            continue

        if c.isdigit():
            inicio = ciclos
            inicio_token_columna = columna
            puntos = 0

            while ciclos < len(texto) and (texto[ciclos].isdigit() or texto[ciclos] == '.'):
                if texto[ciclos] == '.':
                    puntos += 1
                    if puntos > 1:
                        raise ErrorLexico("numero no valido", fila, columna)
                columna += 1
                ciclos += 1

            if texto[ciclos - 1] == '.':
                raise ErrorLexico("numero no valido", fila, columna)

            tokens.append(Token(TipoToken.NUMERO, texto[inicio:ciclos], fila, inicio_token_columna))

        elif c.isalpha() or c == "_":
            inicio = ciclos
            inicio_token_columna = columna

            while ciclos < len(texto) and (texto[ciclos].isalpha() or texto[ciclos] == "_"):
                columna += 1
                ciclos += 1
            palabra = texto[inicio:ciclos]

            tipo = PALABRAS_RESERVADAS.get(palabra, TipoToken.IDENTIFICADOR)
            tokens.append(Token(tipo, palabra, fila, inicio_token_columna))

        elif c == '"':
            inicio = ciclos
            inicio_token_columna = columna
            inicio_fila = fila
            ciclos += 1
            columna += 1

            while ciclos < len(texto) and texto[ciclos] != '"':
                if texto[ciclos] == '\n':
                    fila += 1
                    columna = 1
                else:
                    columna += 1
                ciclos += 1

            if ciclos >= len(texto):
                raise ErrorLexico("cadena sin cerrar", inicio_fila, inicio_token_columna)

            tokens.append(Token(TipoToken.CADENA, texto[inicio + 1:ciclos], inicio_fila, inicio_token_columna))
            ciclos += 1
            columna += 1

        elif c == '/' and ciclos + 1 < len(texto) and texto[ciclos + 1] == '*':
            inicio = ciclos
            inicio_token_columna = columna
            inicio_fila = fila
            ciclos += 2
            columna += 2

            while ciclos < len(texto) and texto[ciclos:ciclos + 2] != '*/':
                if texto[ciclos] == '\n':
                    fila += 1
                    columna = 1
                else:
                    columna += 1
                ciclos += 1

            if ciclos >= len(texto):
                raise ErrorLexico("comentario sin cerrar", inicio_fila, inicio_token_columna)

            ciclos += 2
            columna += 2
            continue

        elif c in "+-*/":
            tokens.append(Token(TipoToken.OPERADOR, c, fila, columna))
            ciclos += 1
            columna += 1

        elif c == "=":
            if ciclos + 1 < len(texto) and texto[ciclos + 1] == "=":
                tokens.append(Token(TipoToken.OPERADOR, "==", fila, columna))
                ciclos += 2
                columna += 2
            else:
                tokens.append(Token(TipoToken.OPERADOR, "=", fila, columna))
                ciclos += 1
                columna += 1

        elif c in "><":
            if ciclos + 1 < len(texto) and texto[ciclos + 1] == "=":
                tokens.append(Token(TipoToken.OPERADOR, f"{c}=", fila, columna))
                ciclos += 2
                columna += 2
            else:
                tokens.append(Token(TipoToken.OPERADOR, c, fila, columna))
                ciclos += 1
                columna += 1

        elif c == "!":
            if ciclos + 1 < len(texto) and texto[ciclos + 1] == "=":
                tokens.append(Token(TipoToken.OPERADOR, "!=", fila, columna))
                ciclos += 2
                columna += 2
            else:
                tokens.append(Token(TipoToken.NEGACION, "!", fila, columna))
                ciclos += 1
                columna += 1

        elif c in "()":
            tokens.append(Token(TipoToken.PARENTESIS, c, fila, columna))
            ciclos += 1
            columna += 1

        elif c in "{}":
            tokens.append(Token(TipoToken.LLAVES, c, fila, columna))
            ciclos += 1
            columna += 1

        elif c == ":":
            tokens.append(Token(TipoToken.DOS_PUNTOS, c, fila, columna))
            ciclos += 1
            columna += 1

        else:
            raise ErrorLexico(f"carácter inesperado '{c}'", fila, columna)

    tokens.append(Token(TipoToken.EOF, "", fila, columna))
    return tokens
