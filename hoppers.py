from dataclasses import dataclass
from typing import Tuple, List, Optional


SIZE = 10

EMPTY = 0
P1 = 1
P2 = 2

Position = Tuple[int, int]
Action = Tuple[Position, ...]


DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]


# Campamento inicial del jugador 1
CAMP_P1 = {
    (0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
    (1, 0), (1, 1), (1, 2), (1, 3),
    (2, 0), (2, 1), (2, 2),
    (3, 0), (3, 1),
    (4, 0)
}


# Campamento inicial del jugador 2
CAMP_P2 = {
    (5, 9),
    (6, 8), (6, 9),
    (7, 7), (7, 8), (7, 9),
    (8, 6), (8, 7), (8, 8), (8, 9),
    (9, 5), (9, 6), (9, 7), (9, 8), (9, 9)
}


@dataclass(frozen=True)
class State:
    board: Tuple[Tuple[int, ...], ...]
    turn: int


def initial_state() -> State:
    board = [
        [EMPTY for _ in range(SIZE)]
        for _ in range(SIZE)
    ]

    for row, col in CAMP_P1:
        board[row][col] = P1

    for row, col in CAMP_P2:
        board[row][col] = P2

    return State(
        board=tuple(tuple(row) for row in board),
        turn=P1
    )


def player(state: State) -> int:
    return state.turn


def inside(row: int, col: int) -> bool:
    return 0 <= row < SIZE and 0 <= col < SIZE


def hop_paths_from(state: State, start: Position) -> List[Action]:
    board = state.board
    occupied = set()

    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] != EMPTY and (row, col) != start:
                occupied.add((row, col))

    paths = {}

    def search(current, path, visited):
        row, col = current

        for dr, dc in DIRECTIONS:
            middle = (row + dr, col + dc)
            landing = (row + 2 * dr, col + 2 * dc)

            mr, mc = middle
            lr, lc = landing

            if not inside(mr, mc) or not inside(lr, lc):
                continue

            # Para saltar debe haber una ficha en medio
            if middle not in occupied:
                continue

            # El lugar donde cae debe estar vacío
            if landing in occupied:
                continue

            if landing in visited:
                continue

            new_path = path + [landing]

            # Una sola ruta por destino es suficiente
            if landing not in paths:
                paths[landing] = tuple(new_path)

            search(
                landing,
                new_path,
                visited | {landing}
            )

    search(start, [start], {start})

    return list(paths.values())


def actions(state: State) -> List[Action]:
    moves = []
    current_player = player(state)

    for row in range(SIZE):
        for col in range(SIZE):
            if state.board[row][col] != current_player:
                continue

            start = (row, col)

            # Movimiento normal de una casilla
            for dr, dc in DIRECTIONS:
                nr = row + dr
                nc = col + dc

                if inside(nr, nc) and state.board[nr][nc] == EMPTY:
                    moves.append(
                        (start, (nr, nc))
                    )

            # Saltos simples o múltiples
            moves.extend(
                hop_paths_from(state, start)
            )

    return moves


def result(state: State, action: Action) -> State:
    if len(action) < 2:
        raise ValueError("Movimiento inválido.")

    start = action[0]
    end = action[-1]

    sr, sc = start
    er, ec = end

    current_player = player(state)

    if state.board[sr][sc] != current_player:
        raise ValueError("Esa ficha no pertenece al jugador actual.")

    board = [list(row) for row in state.board]

    board[sr][sc] = EMPTY
    board[er][ec] = current_player

    next_player = P2 if current_player == P1 else P1

    return State(
        board=tuple(tuple(row) for row in board),
        turn=next_player
    )


def camp_winner(state: State) -> Optional[int]:
    board = state.board

    # Jugador 1 intenta ocupar el campamento del jugador 2
    camp2_full = all(
        board[row][col] != EMPTY
        for row, col in CAMP_P2
    )

    p1_in_camp = any(
        board[row][col] == P1
        for row, col in CAMP_P2
    )

    if camp2_full and p1_in_camp:
        return P1

    # Jugador 2 intenta ocupar el campamento del jugador 1
    camp1_full = all(
        board[row][col] != EMPTY
        for row, col in CAMP_P1
    )

    p2_in_camp = any(
        board[row][col] == P2
        for row, col in CAMP_P1
    )

    if camp1_full and p2_in_camp:
        return P2

    return None


def winner(state: State) -> Optional[int]:
    win = camp_winner(state)

    if win is not None:
        return win

    # Si un jugador se queda sin movimientos gana el otro
    if len(actions(state)) == 0:
        return P2 if player(state) == P1 else P1

    return None


def terminal(state: State) -> bool:
    return winner(state) is not None


def utility(state: State, perspective: int) -> int:
    win = winner(state)

    if win is None:
        return 0

    return 1 if win == perspective else -1


def pieces_of(state: State, player_id: int) -> List[Position]:
    pieces = []

    for row in range(SIZE):
        for col in range(SIZE):
            if state.board[row][col] == player_id:
                pieces.append((row, col))

    return pieces


def target_camp(player_id: int):
    return CAMP_P2 if player_id == P1 else CAMP_P1


def home_camp(player_id: int):
    return CAMP_P1 if player_id == P1 else CAMP_P2


def distance_to_target(position: Position, player_id: int) -> int:
    row, col = position
    target = target_camp(player_id)

    # Se usa Chebyshev porque el juego permite movimientos diagonales
    return min(
        max(
            abs(row - target_row),
            abs(col - target_col)
        )
        for target_row, target_col in target
    )


def heuristic(state: State, perspective: int) -> float:
    opponent = P2 if perspective == P1 else P1

    own_pieces = pieces_of(state, perspective)
    enemy_pieces = pieces_of(state, opponent)

    own_target = target_camp(perspective)
    enemy_target = target_camp(opponent)

    own_home = home_camp(perspective)
    enemy_home = home_camp(opponent)

    own_in_target = sum(
        1 for piece in own_pieces
        if piece in own_target
    )

    enemy_in_target = sum(
        1 for piece in enemy_pieces
        if piece in enemy_target
    )

    own_in_home = sum(
        1 for piece in own_pieces
        if piece in own_home
    )

    enemy_in_home = sum(
        1 for piece in enemy_pieces
        if piece in enemy_home
    )

    own_distance = sum(
        distance_to_target(piece, perspective)
        for piece in own_pieces
    )

    enemy_distance = sum(
        distance_to_target(piece, opponent)
        for piece in enemy_pieces
    )

    score = 0

    # Llegar al campamento rival tiene el peso más importante
    score += 150 * (own_in_target - enemy_in_target)

    # También se recompensa acercarse a la meta
    score += 8 * (enemy_distance - own_distance)

    # Y salir del campamento inicial
    score += 15 * (enemy_in_home - own_in_home)

    return float(score)


def format_action(action: Action) -> str:
    return " → ".join(
        f"({row},{col})"
        for row, col in action
    )