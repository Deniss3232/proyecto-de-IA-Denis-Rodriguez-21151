# Proyecto Hoppers con Minimax

## Descripción general

Para este proyecto se implementó el juego Hoppers utilizando un
tablero de 10x10 y dos jugadores con 15 piezas cada uno. El objetivo
principal del juego es mover las piezas desde el campamento inicial
hasta el campamento ubicado en la esquina contraria.

Las piezas pueden realizar movimientos de un espacio hacia cualquiera
de las ocho direcciones disponibles, siempre que la posición esté
vacía. También pueden realizar saltos sobre otras piezas. Una de las
características importantes del juego es que los saltos pueden
encadenarse durante un mismo turno.

## Representación del juego

El tablero se representa mediante una matriz de 10x10. Se utilizó el
valor 0 para los espacios vacíos, 1 para las piezas del jugador 1 y 2
para las piezas del jugador 2.

Los estados se manejan de manera inmutable utilizando tuplas. De esta
forma, al ejecutar una acción se crea un estado nuevo y no se modifica
directamente el estado anterior.

## Minimax y poda alfa-beta

Para el agente inteligente se utilizó el algoritmo Minimax con poda
alfa-beta. El jugador que está tomando la decisión intenta maximizar
el valor de la posición, mientras que el rival intenta minimizarlo.

La poda alfa-beta permite evitar la evaluación de ramas del árbol que
ya se sabe que no pueden mejorar la decisión final. Esto permite
alcanzar mayores profundidades utilizando menos tiempo.

## Profundidad

La profundidad máxima puede ser configurada al iniciar el programa.
Cuando el algoritmo alcanza dicha profundidad sin encontrar un estado
terminal, se utiliza la función heurística para estimar qué tan
favorable es la posición.

También se utilizó iterative deepening. Esto significa que primero se
realiza una búsqueda a profundidad 1, después a profundidad 2 y así
sucesivamente hasta llegar al límite configurado.

## Función heurística

La función heurística toma en cuenta tres aspectos principales.

El primero es la cantidad de piezas que ya se encuentran dentro del
campamento objetivo. Este factor recibe el peso más alto debido a que
representa directamente el objetivo del juego.

El segundo factor es la distancia de las piezas hacia el campamento
contrario. Se utiliza distancia de Chebyshev debido a que las piezas
pueden desplazarse en ocho direcciones, incluyendo diagonales.

Finalmente se toma en cuenta la cantidad de piezas que todavía se
encuentran dentro del campamento inicial. Se busca favorecer estados
donde las piezas ya han comenzado a desplazarse hacia el lado
contrario.

Todos estos valores también se comparan contra la situación del rival,
permitiendo que la evaluación tome en cuenta tanto el progreso propio
como el progreso del oponente.

## Manejo del tiempo

El proyecto establece un máximo interno de 29 segundos para la
búsqueda. Se utilizó este valor en lugar de los 30 segundos exactos
para mantener un margen de seguridad.

Durante la búsqueda se revisa constantemente el tiempo transcurrido.
Si se alcanza el límite, se detiene la búsqueda y se retorna la mejor
jugada encontrada en la última profundidad terminada. Además, antes de
comenzar la búsqueda se guarda una jugada legal, garantizando que el
agente siempre pueda devolver un movimiento válido.

## Modos de juego

El programa permite jugar en cuatro modalidades:

- Humano contra agente.
- Agente contra humano.
- Agente contra agente.
- Humano contra humano.

Esto también permite realizar pruebas del funcionamiento de las reglas
sin necesidad de ejecutar siempre el algoritmo de inteligencia
artificial.

## Observaciones

Durante las pruebas se observó que aumentar la profundidad mejora la
capacidad del agente para anticipar movimientos, pero también aumenta
considerablemente la cantidad de estados que deben ser explorados.

Por este motivo, profundidades entre 2 y 3 son adecuadas para comenzar
las pruebas y posteriormente se puede evaluar si el equipo permite
utilizar valores mayores sin superar el límite de tiempo.