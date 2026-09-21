# Proyecto Hoppers con Inteligencia Artificial

Este proyecto implementa el juego Hoppers en Python, incluyendo una interfaz gráfica y un agente inteligente basado en Minimax con poda alfa-beta.

El objetivo del juego es mover las 15 fichas de cada jugador desde su campamento inicial hasta el campamento contrario. Las fichas pueden moverse una casilla en cualquiera de las ocho direcciones o realizar saltos simples y múltiples sobre otras fichas.

## Características

- Tablero de 10x10.
- 15 fichas por jugador.
- Movimientos en 8 direcciones.
- Saltos simples y saltos múltiples.
- Interfaz gráfica usando Tkinter.
- Modo Humano vs Agente.
- Modo Agente vs Humano.
- Modo Agente vs Agente.
- Modo Humano vs Humano.
- Algoritmo Minimax.
- Poda alfa-beta.
- Profundidad configurable.
- Función heurística.
- Límite de tiempo por jugada del agente.

## Archivos principales

- `hoppers.py`: contiene las reglas y la lógica del juego.
- `minimax_agent.py`: contiene el agente inteligente y el algoritmo Minimax.
- `main.py`: contiene la interfaz gráfica y los modos de juego.
- `informe.md`: explicación técnica del proyecto.

## Cómo ejecutar el proyecto

Se necesita tener Python instalado.

Desde la carpeta del proyecto ejecutar:

```bash
python main.py
