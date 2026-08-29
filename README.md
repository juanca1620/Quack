Quack

Integrantes

- Laura Valeria Valencia
- Juan Camilo Soto Soto
- Luis Miguel Sepulveda Quintero
- Jhovanny Quiceno

Introduccion

Quack es un lenguaje de reglas en español para el dominio de animales
que ponen huevos (aves, reptiles y monotremas), incluyendo el caso de
Perry, el ornitorrinco.

Sintaxis

SI <condicion> ENTONCES <accion>

La condicion puede ser simple (una comparacion) o compuesta, uniendo
varias comparaciones con Y o con O (no se mezclan Y y O en la misma
regla).

Variables del dominio

- especie (texto): nombre de la especie, ejemplo "Perry"
- pone_huevos (booleano): si pone huevos
- tiene_pico (booleano): si tiene pico
- tiene_pelo (booleano): si tiene pelo
- tiene_plumas (booleano): si tiene plumas
- es_mamifero (booleano): si es mamifero
- es_acuatico (booleano): si es acuatico
- veneno (booleano): si produce veneno
- cantidad_huevos (numerico): numero de huevos por puesta
- dias_incubacion (numerico): dias de incubacion
- temperatura (numerico): temperatura del ambiente o del nido
- humedad (numerico): humedad del ambiente o del nido

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

