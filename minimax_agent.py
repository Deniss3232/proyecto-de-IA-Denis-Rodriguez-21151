import time
from math import inf

from hoppers import (
    actions,
    result,
    terminal,
    utility,
    heuristic,
    player
)


WIN_SCORE = 1_000_000


class SearchTimeout(Exception):
    pass


class MinimaxAgent:

    def __init__(self, depth=3, time_limit=28.0):
        self.depth = depth
        self.time_limit = time_limit

        self.start_time = 0
        self.root_player = None
        self.nodes = 0


    # Revisa constantemente que no se pase del tiempo
    def check_time(self):
        elapsed = time.perf_counter() - self.start_time

        if elapsed >= self.time_limit:
            raise SearchTimeout()


    def choose_action(self, state):
        legal_actions = actions(state)

        if not legal_actions:
            return None

        # Se guarda una jugada desde el principio por seguridad
        best_action = legal_actions[0]

        self.root_player = player(state)
        self.start_time = time.perf_counter()
        self.nodes = 0

        # Se va aumentando la profundidad poco a poco
        for current_depth in range(1, self.depth + 1):
            try:
                action, _ = self.search_root(
                    state,
                    current_depth
                )

                if action is not None:
                    best_action = action

            except SearchTimeout:
                break

        return best_action


    def search_root(self, state, depth):
        self.check_time()

        legal_actions = actions(state)

        best_action = legal_actions[0]
        best_value = -inf

        alpha = -inf
        beta = inf

        children = []

        # Ordenar primero los movimientos que parecen mejores
        for action in legal_actions:
            self.check_time()

            child = result(state, action)

            value = heuristic(
                child,
                self.root_player
            )

            children.append(
                (value, action, child)
            )

        children.sort(
            key=lambda item: item[0],
            reverse=True
        )

        for _, action, child in children:
            self.check_time()

            value = self.alpha_beta(
                child,
                depth - 1,
                alpha,
                beta
            )

            if value > best_value:
                best_value = value
                best_action = action

            alpha = max(alpha, best_value)

        return best_action, best_value


    def alpha_beta(self, state, depth, alpha, beta):
        self.check_time()
        self.nodes += 1

        if terminal(state):
            return (
                utility(
                    state,
                    self.root_player
                )
                * WIN_SCORE
            )

        if depth == 0:
            return heuristic(
                state,
                self.root_player
            )

        legal_actions = actions(state)

        maximizing = (
            player(state)
            == self.root_player
        )

        children = []

        for action in legal_actions:
            self.check_time()

            child = result(
                state,
                action
            )

            value = heuristic(
                child,
                self.root_player
            )

            children.append(
                (value, child)
            )

        children.sort(
            key=lambda item: item[0],
            reverse=maximizing
        )

        if maximizing:
            value = -inf

            for _, child in children:
                self.check_time()

                value = max(
                    value,
                    self.alpha_beta(
                        child,
                        depth - 1,
                        alpha,
                        beta
                    )
                )

                alpha = max(alpha, value)

                if alpha >= beta:
                    break

            return value

        else:
            value = inf

            for _, child in children:
                self.check_time()

                value = min(
                    value,
                    self.alpha_beta(
                        child,
                        depth - 1,
                        alpha,
                        beta
                    )
                )

                beta = min(beta, value)

                if beta <= alpha:
                    break

            return value