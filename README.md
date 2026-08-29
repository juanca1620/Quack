Quack

Integrantes

- Valencia
- Soto
- Quintero
- Quiceno

Introduccion

Para este proyecto escogimos como dominio los animales que ponen huevos,
es decir aves, reptiles y los monotremas (como el ornitorrinco). A este
lenguaje de reglas lo llamamos Quack. La idea es que a partir de unas
reglas escritas en español se pueda clasificar una especie, revisar
condiciones del nido o del ambiente donde estan los huevos, y activar
ciertas acciones como prender una incubadora o dar una alerta si el
animal es venenoso. Incluimos tambien el caso especial de Perry, el
ornitorrinco, porque es un mamifero que pone huevos y no encaja del todo
en las categorias normales de ave o reptil.

Sintaxis de las reglas

Cada regla la escribimos siempre igual: empieza con SI, luego va una
condicion (o varias condiciones unidas con Y o con O), y despues de la
palabra ENTONCES va la accion que se ejecuta si se cumple la condicion.

Algo importante es que en una misma regla no se pueden mezclar los
conectores Y y O. Si una regla tiene varias condiciones, todas van
unidas por Y, o todas van unidas por O, pero no revueltas.

Cada condicion tiene tres partes: una variable, un operador de
comparacion y un valor. Los operadores que usamos son >, <, =, >= y <=.
Los nombres de variables van siempre en minusculas, y si el nombre tiene
varias palabras las separamos con guion bajo, por ejemplo
cantidad_huevos. El valor puede ser un numero, puede ser verdadero o
falso si la variable es booleana, o puede ser un texto entre comillas
si la variable es de tipo texto, como especie = "Perry". La accion que
va despues de ENTONCES tambien se escribe en minusculas.

Convencion que seguimos para escribir las reglas

- SI, ENTONCES, Y y O siempre en mayuscula.
- Si se va declarar una variable Se empieza nombrando el tipo de variable con un prefijo "Q_" y el tipo del dato separado de un espacio el nombre de la variable: Ejemplo: Q_booleano pone_huevos
- Variables y acciones en minuscula, separando palabras con guion bajo.
- Los booleanos se escriben como verdadero o falso.
- Los textos van entre comillas dobles.
- Dejamos un espacio entre la variable, el operador y el valor (por
  ejemplo temperatura >= 25, no temperatura>=25).
- Cada regla va en un solo renglon.

Palabras reservadas

| Palabra o simbolo | Que significa | Categoria |
|--------------------|----------------|-----------|
| SI | Con esto empieza la condicion de una regla | Palabra clave |
| ENTONCES | Separa la condicion de la accion | Palabra clave |
| CLOK |Empieza la sintaxis para un bucle definido | Palabra clave |
| Y | Une condiciones, y todas tienen que cumplirse | Operador logico |
| O | Une condiciones, y basta con que una se cumpla | Operador logico |
| > | Mayor que | Operador relacional |
| < | Menor que | Operador relacional |
| = | Igual a | Operador relacional |
| >= | Mayor o igual que | Operador relacional |
| <= | Menor o igual que | Operador relacional |
| verdadero | Valor booleano verdadero (true en Java) | Literal |
| falso | Valor booleano falso (false en Java) | Literal |
| "texto" | Un valor de tipo texto, entre comillas | Literal |
| numero | Un valor numerico, entero o decimal | Literal |

Las palabras reservadas no se pueden usar como nombre de variable ni de
accion, y como ya dijimos, en una misma regla no se mezclan Y y O.

Variables que usamos

- especie (texto): nombre de la especie, por ejemplo "Perry".
- pone_huevos (booleano): si pone huevos o no.
- tiene_pico (booleano): si tiene pico.
- tiene_pelo (booleano): si tiene pelo.
- tiene_plumas (booleano): si tiene plumas.
- es_mamifero (booleano): si es mamifero.
- es_acuatico (booleano): si vive en el agua.
- veneno (booleano): si produce veneno.
- cantidad_huevos (numerico): cuantos huevos pone por puesta.
- dias_incubacion (numerico): cuantos dias dura la incubacion.
- temperatura (numerico): temperatura del ambiente o del nido.
- humedad (numerico): humedad del ambiente o del nido.

Tabla de tipos de datos

| Variable | Tipo en Java | Ejemplo |
|----------|--------------|---------|
| especie | String | "Perry" |
| pone_huevos | boolean | true |
| tiene_pico | boolean | true |
| tiene_pelo | boolean | false |
| tiene_plumas | boolean | false |
| es_mamifero | boolean | true |
| es_acuatico | boolean | true |
| veneno | boolean | true |
| cantidad_huevos | int | 2 |
| dias_incubacion | int | 65 |
| temperatura | double | 28.5 |
| humedad | double | 45.0 |

Reglas

1. SI pone_huevos = verdadero ENTONCES es_oviparo
2. SI temperatura < 18 ENTONCES activar_incubadora
3. SI veneno = verdadero ENTONCES alerta_manejo_cuidadoso
4. SI cantidad_huevos > 5 ENTONCES nido_grande
5. SI tiene_pico = verdadero Y tiene_pelo = verdadero ENTONCES especie_posible_ornitorrinco
6. SI es_acuatico = verdadero O tiene_pico = verdadero ENTONCES habitat_posible_humedal
7. SI tiene_plumas = verdadero Y pone_huevos = verdadero ENTONCES clasificar_como_ave
8. SI cantidad_huevos >= 1 Y cantidad_huevos <= 3 ENTONCES nido_pequeno
9. SI cantidad_huevos > 5 Y tiene_pico = verdadero ENTONCES nido_grande_de_ave
10. SI temperatura >= 25 Y es_acuatico = verdadero ENTONCES riesgo_moho_humedal
11. SI dias_incubacion > 60 Y es_mamifero = verdadero ENTONCES incubacion_prolongada_monotrema
12. SI especie = "Perry" Y pone_huevos = verdadero ENTONCES clasificar_como_ornitorrinco_perry
13. SI temperatura > 30 ENTONCES riesgo_sobrecalentamiento
14. SI humedad < 20 O temperatura > 32 ENTONCES activar_riego
15. SI cantidad_huevos > 3 Y es_mamifero = verdadero ENTONCES caso_especial_monotrema

sintaxis general de las reglas

SI <condicion> { (Y | O) <condicion> } ENTONCES <accion>

<condicion> ::= <variable> <operador> <valor>

<declaracion> ::= <tipo> <variable> = <valor>

<operador> ::= > | < | = | >= | <=

<valor> ::= numero | true | false | "texto"

--Trabajo Futuro--

CLOK <Q_int variable = numero> [operador] <condicion>{
  <EJECUCION>
}