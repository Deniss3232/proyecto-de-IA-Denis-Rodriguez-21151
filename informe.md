
---

## `informe.md`

```markdown
# Informe - Proyecto Hoppers con Minimax

## Introducción

Para este proyecto se implementó el juego Hoppers junto con un agente inteligente capaz de seleccionar movimientos utilizando el algoritmo Minimax con poda alfa-beta.

El juego se desarrolla en un tablero de 10x10 y cada jugador comienza con 15 fichas colocadas en una de las esquinas del tablero.

El objetivo principal es mover las fichas desde el campamento inicial hasta el campamento contrario antes que el otro jugador.

Además de implementar las reglas del juego, se agregó una interfaz gráfica para facilitar las pruebas y hacer más sencillo entender los movimientos disponibles.

## Representación del juego

El tablero se representa internamente mediante una matriz de 10x10.

Se utilizan los siguientes valores:

- `0` representa una posición vacía.
- `1` representa una ficha del Jugador 1.
- `2` representa una ficha del Jugador 2.

El estado del juego contiene dos elementos principales:

- El contenido actual del tablero.
- El jugador al que le corresponde el turno.

Los estados se manejan utilizando tuplas para evitar modificar directamente estados anteriores durante la búsqueda de Minimax.

Esto permite que el algoritmo pueda generar diferentes posibilidades sin alterar accidentalmente el estado original del juego.

## Estado inicial

El Jugador 1 comienza en la esquina superior izquierda y el Jugador 2 comienza en la esquina inferior derecha.

Cada jugador cuenta con 15 fichas.

El campamento inicial del Jugador 1 está formado por las siguientes posiciones:

- Fila 0: cinco fichas.
- Fila 1: cuatro fichas.
- Fila 2: tres fichas.
- Fila 3: dos fichas.
- Fila 4: una ficha.

El campamento del Jugador 2 utiliza la misma forma, pero ubicada en la esquina opuesta.

## Movimientos

Las fichas pueden realizar dos tipos principales de movimiento.

### Movimiento normal

Una ficha puede desplazarse una casilla en cualquiera de las ocho direcciones:

- Arriba.
- Abajo.
- Izquierda.
- Derecha.
- Diagonal superior izquierda.
- Diagonal superior derecha.
- Diagonal inferior izquierda.
- Diagonal inferior derecha.

El movimiento únicamente puede realizarse si la casilla de destino se encuentra vacía.

### Saltos

Una ficha también puede saltar sobre otra ficha cuando existe una ficha en la posición adyacente y la casilla que se encuentra inmediatamente después está vacía.

La ficha que se salta no se elimina del tablero.

Esto significa que una ficha puede saltar sobre fichas propias o fichas del rival.

También se implementaron saltos múltiples. Después de realizar un salto, si existe otro salto disponible desde la nueva posición, el movimiento puede continuar dentro del mismo turno.

## Funciones principales del juego

Se implementaron las funciones necesarias para representar el problema de forma independiente del agente.

### `initial_state()`

Genera el estado inicial del tablero con las 15 fichas de cada jugador.

### `player(state)`

Retorna el jugador al que le corresponde realizar el siguiente movimiento.

### `actions(state)`

Genera todas las acciones legales disponibles para el jugador actual.

Incluye movimientos normales, saltos simples y saltos múltiples.

### `result(state, action)`

Genera un nuevo estado después de aplicar una acción.

El estado recibido no se modifica directamente.

### `terminal(state)`

Indica si la partida ya terminó.

### `winner(state)`

Retorna el jugador que ganó la partida.

### `utility(state, perspective)`

Asigna un valor a los estados terminales desde la perspectiva del jugador que se encuentra evaluando la posición.

Una victoria tiene valor positivo y una derrota tiene valor negativo.

## Condición de victoria

El objetivo es ocupar el campamento contrario.

También se tomó en cuenta la regla que evita que un jugador pueda bloquear permanentemente la partida dejando una ficha dentro de su propio campamento.

Por esta razón, el campamento se considera ocupado cuando todas sus posiciones contienen fichas y existe por lo menos una ficha del jugador que intenta conquistar dicho campamento.

## Algoritmo Minimax

Para controlar al agente se utilizó el algoritmo Minimax.

El algoritmo considera que existen dos jugadores con objetivos opuestos.

El jugador controlado por el agente intenta maximizar el valor de la posición mientras que el jugador contrario intenta minimizarlo.

El algoritmo genera diferentes movimientos posibles y analiza los estados que se producen después de cada uno.

De esta manera puede tomar una decisión considerando posibles respuestas del rival.

## Poda alfa-beta

Se implementó poda alfa-beta para reducir la cantidad de estados evaluados.

Durante Minimax se mantienen dos valores:

- Alfa representa el mejor valor encontrado hasta el momento para el jugador que maximiza.
- Beta representa el mejor valor encontrado para el jugador que minimiza.

Cuando se detecta que una rama ya no puede mejorar el resultado de una decisión, esa rama deja de evaluarse.

La poda alfa-beta no cambia la decisión final de Minimax, pero permite reducir la cantidad de estados que deben analizarse.

## Profundidad de búsqueda

La búsqueda tiene una profundidad configurable.

La profundidad representa cuántos niveles del árbol de juego se analizan antes de utilizar la función heurística.

Por ejemplo:

- Profundidad 1 analiza únicamente las posibles jugadas inmediatas.
- Profundidad 2 también considera posibles respuestas del rival.
- Profundidad 3 permite analizar una jugada adicional del agente.

Una profundidad mayor permite considerar más situaciones futuras, pero también aumenta considerablemente la cantidad de estados que deben analizarse.

Por esta razón, para pruebas rápidas se pueden utilizar profundidades de 2 o 3.

## Iterative Deepening

También se utiliza una estrategia de profundización progresiva.

El agente comienza realizando una búsqueda a profundidad 1.

Después intenta profundidad 2, luego profundidad 3 y así sucesivamente hasta alcanzar la profundidad configurada.

Esto permite que el programa siempre tenga una jugada válida disponible aunque se alcance el límite de tiempo antes de completar la búsqueda más profunda.

## Función heurística

Cuando Minimax alcanza el límite de profundidad y el estado todavía no es terminal, utiliza una función heurística para estimar qué tan favorable es la posición.

La heurística utiliza principalmente tres factores.

### Fichas dentro del campamento objetivo

Se recompensa a un jugador cuando logra colocar fichas dentro del campamento contrario.

Este factor recibe un peso alto porque representa directamente el objetivo principal del juego.

### Distancia hacia el objetivo

También se calcula qué tan lejos se encuentran las fichas del campamento objetivo.

Para esta parte se utiliza distancia de Chebyshev, ya que las fichas pueden desplazarse tanto horizontal y verticalmente como de forma diagonal.

Mientras menor sea la distancia total hacia el objetivo, mejor se considera la posición.

### Fichas que todavía se encuentran en el campamento inicial

Se penalizan los estados en los cuales muchas fichas todavía permanecen dentro del campamento inicial.

Esto permite motivar al agente a sacar sus fichas y avanzar hacia el otro lado del tablero.

La evaluación final compara estos factores tanto para el jugador actual como para el rival.

De esta manera, el agente no solamente intenta avanzar sus propias fichas, sino que también toma en cuenta el progreso del oponente.

## Manejo del límite de tiempo

El proyecto establece un máximo de 30 segundos para que el agente decida una jugada.

Para evitar superar este límite se utiliza internamente un máximo de 28 segundos.

Durante la ejecución de Minimax se revisa periódicamente el tiempo transcurrido.

Si se alcanza el límite, la búsqueda se detiene y se utiliza la mejor jugada obtenida en la última profundidad terminada.

Además, antes de iniciar la búsqueda se guarda una jugada legal.

Esto permite garantizar que el agente siempre pueda devolver una acción válida incluso si no logra completar toda la búsqueda.

## Interfaz gráfica

Se implementó una interfaz gráfica utilizando Tkinter.

La intención fue que el juego pudiera entenderse y probarse de una manera más sencilla.

El Jugador 1 utiliza fichas verdes identificadas con la letra X.

El Jugador 2 utiliza fichas moradas identificadas con la letra O.

Cuando una persona selecciona una ficha, el programa muestra visualmente las posiciones a las que puede moverse.

También se muestra información como:

- Jugador actual.
- Objetivo del jugador.
- Ficha seleccionada.
- Movimientos disponibles.
- Tipo de movimiento.
- Historial de movimientos.
- Tiempo utilizado por el agente.
- Cantidad de nodos evaluados.

## Modos de juego

Se implementaron cuatro modos diferentes.

### Humano vs Agente

El Jugador 1 es controlado por una persona y el Jugador 2 por Minimax.

### Agente vs Humano

El Jugador 1 es controlado por Minimax y el Jugador 2 por una persona.

### Agente vs Agente

Ambos jugadores utilizan Minimax.

Este modo permite observar directamente el comportamiento de los agentes.

### Humano vs Humano

Ambos jugadores son controlados manualmente.

Este modo también fue útil para probar las reglas del juego sin depender del agente.

## Observaciones

Durante el desarrollo se observó que la cantidad de movimientos posibles puede aumentar bastante durante una partida.

Esto hace que el árbol de búsqueda crezca rápidamente cuando se aumenta la profundidad.

La poda alfa-beta y el ordenamiento de movimientos ayudan a disminuir la cantidad de ramas que deben explorarse.

También se observó que profundidades pequeñas permiten respuestas prácticamente inmediatas, mientras que profundidades mayores pueden acercarse al límite de tiempo.

Por esta razón se agregó el control del tiempo y la profundización progresiva.

La interfaz gráfica también fue útil para verificar que las acciones generadas fueran válidas, ya que permite observar directamente qué posiciones se encuentran disponibles para cada ficha.

## Conclusión

El proyecto permitió aplicar conceptos de inteligencia artificial dentro de un juego de dos jugadores.

Se implementó la lógica completa de Hoppers, incluyendo movimientos normales, saltos simples, saltos múltiples y condiciones de victoria.

El agente utiliza Minimax con poda alfa-beta, profundidad configurable y una función heurística para evaluar posiciones no terminales.

Finalmente, se implementó un control de tiempo para respetar el límite máximo por jugada y una interfaz gráfica para facilitar el uso y las pruebas del programa.
