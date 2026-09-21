import tkinter as tk
from tkinter import ttk, messagebox

import threading
import time

from hoppers import (
    SIZE,
    EMPTY,
    P1,
    P2,
    CAMP_P1,
    CAMP_P2,
    initial_state,
    player,
    actions,
    result,
    winner,
    format_action
)

from minimax_agent import MinimaxAgent


class HoppersGUI:

    CELL_SIZE = 55
    MARGIN = 35

    BOARD_PIXELS = (
        SIZE * CELL_SIZE
        + MARGIN * 2
    )


    def __init__(self, root):
        self.root = root

        self.root.title(
            "Hoppers - Inteligencia Artificial"
        )

        self.root.geometry(
            "1050x720"
        )

        self.root.minsize(
            950,
            680
        )

        self.state = initial_state()

        self.selected_piece = None
        self.selected_actions = []

        self.agent_thinking = False
        self.game_token = 0

        self.mode_var = tk.StringVar(
            value="Humano vs Agente"
        )

        self.depth_var = tk.IntVar(
            value=2
        )

        self.status_var = tk.StringVar()
        self.objective_var = tk.StringVar()

        self.selected_var = tk.StringVar(
            value="Ninguna ficha seleccionada"
        )

        self.create_interface()

        self.update_interface()

        self.root.after(
            300,
            self.check_agent_turn
        )


    def create_interface(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        main_frame = ttk.Frame(
            self.root,
            padding=15
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        title = ttk.Label(
            main_frame,
            text="HOPPERS",
            font=("Arial", 24, "bold")
        )

        title.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(0, 5)
        )

        subtitle = ttk.Label(
            main_frame,
            text=(
                "Selecciona una ficha y después "
                "haz clic en uno de los espacios disponibles."
            ),
            font=("Arial", 11)
        )

        subtitle.grid(
            row=1,
            column=0,
            columnspan=2,
            pady=(0, 15)
        )

        board_frame = ttk.Frame(
            main_frame
        )

        board_frame.grid(
            row=2,
            column=0,
            sticky="n"
        )

        self.canvas = tk.Canvas(
            board_frame,
            width=self.BOARD_PIXELS,
            height=self.BOARD_PIXELS,
            background="#f4f4f4",
            highlightthickness=0
        )

        self.canvas.pack()

        self.canvas.bind(
            "<Button-1>",
            self.on_board_click
        )

        side = ttk.Frame(
            main_frame,
            padding=(20, 0)
        )

        side.grid(
            row=2,
            column=1,
            sticky="nsew"
        )

        main_frame.columnconfigure(
            1,
            weight=1
        )

        self.create_config_panel(side)
        self.create_turn_panel(side)
        self.create_selection_panel(side)
        self.create_help_panel(side)
        self.create_history_panel(side)


    def create_config_panel(self, parent):
        frame = ttk.LabelFrame(
            parent,
            text="Configuración",
            padding=12
        )

        frame.pack(
            fill="x",
            pady=(0, 12)
        )

        ttk.Label(
            frame,
            text="Modo de juego:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=5
        )

        mode_box = ttk.Combobox(
            frame,
            textvariable=self.mode_var,
            state="readonly",
            width=22
        )

        mode_box["values"] = (
            "Humano vs Agente",
            "Agente vs Humano",
            "Agente vs Agente",
            "Humano vs Humano"
        )

        mode_box.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        ttk.Label(
            frame,
            text="Profundidad del agente:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=5
        )

        depth_box = ttk.Combobox(
            frame,
            textvariable=self.depth_var,
            state="readonly",
            width=10
        )

        depth_box["values"] = (
            1,
            2,
            3,
            4,
            5
        )

        depth_box.grid(
            row=3,
            column=0,
            sticky="w",
            pady=(0, 10)
        )

        new_button = ttk.Button(
            frame,
            text="Nueva partida",
            command=self.new_game
        )

        new_button.grid(
            row=4,
            column=0,
            sticky="ew",
            pady=5
        )

        frame.columnconfigure(
            0,
            weight=1
        )


    def create_turn_panel(self, parent):
        frame = ttk.LabelFrame(
            parent,
            text="Turno actual",
            padding=12
        )

        frame.pack(
            fill="x",
            pady=(0, 12)
        )

        ttk.Label(
            frame,
            textvariable=self.status_var,
            font=("Arial", 13, "bold"),
            wraplength=320
        ).pack(
            anchor="w"
        )

        ttk.Label(
            frame,
            textvariable=self.objective_var,
            wraplength=320
        ).pack(
            anchor="w",
            pady=(8, 0)
        )


    def create_selection_panel(self, parent):
        frame = ttk.LabelFrame(
            parent,
            text="Ficha seleccionada",
            padding=12
        )

        frame.pack(
            fill="x",
            pady=(0, 12)
        )

        ttk.Label(
            frame,
            textvariable=self.selected_var,
            wraplength=320
        ).pack(
            anchor="w"
        )

        self.moves_text = tk.Text(
            frame,
            height=7,
            width=38,
            state="disabled",
            wrap="word",
            font=("Consolas", 9)
        )

        self.moves_text.pack(
            fill="x",
            pady=(8, 0)
        )


    def create_help_panel(self, parent):
        frame = ttk.LabelFrame(
            parent,
            text="¿Cómo se juega?",
            padding=12
        )

        frame.pack(
            fill="x",
            pady=(0, 12)
        )

        text = (
            "1. Haz clic en una de tus fichas.\n\n"
            "2. Los espacios disponibles aparecerán resaltados.\n\n"
            "3. Haz clic en uno de esos espacios para mover la ficha.\n\n"
            "4. X (verde) debe llegar a la esquina inferior derecha ↘.\n\n"
            "5. O (morado) debe llegar a la esquina superior izquierda ↖.\n\n"
            "6. También puedes realizar saltos sobre otras fichas."
        )

        ttk.Label(
            frame,
            text=text,
            justify="left",
            wraplength=320
        ).pack(
            anchor="w"
        )


    def create_history_panel(self, parent):
        frame = ttk.LabelFrame(
            parent,
            text="Historial de movimientos",
            padding=10
        )

        frame.pack(
            fill="both",
            expand=True
        )

        self.history_text = tk.Text(
            frame,
            height=8,
            width=38,
            state="disabled",
            wrap="word",
            font=("Consolas", 9)
        )

        self.history_text.pack(
            fill="both",
            expand=True
        )


    def new_game(self):
        self.game_token += 1

        self.state = initial_state()

        self.selected_piece = None
        self.selected_actions = []

        self.agent_thinking = False

        self.clear_history()
        self.clear_move_information()

        self.update_interface()

        self.root.after(
            300,
            self.check_agent_turn
        )


    def is_human_turn(self):
        current = player(
            self.state
        )

        mode = self.mode_var.get()

        if mode == "Humano vs Humano":
            return True

        if mode == "Agente vs Agente":
            return False

        if mode == "Humano vs Agente":
            return current == P1

        if mode == "Agente vs Humano":
            return current == P2

        return True


    def update_interface(self):
        self.draw_board()

        current = player(
            self.state
        )

        if self.agent_thinking:
            self.status_var.set(
                f"Jugador {current}: "
                "el agente está pensando..."
            )

        else:
            symbol = (
                "X"
                if current == P1
                else "O"
            )

            actor = (
                "Humano"
                if self.is_human_turn()
                else "Agente"
            )

            self.status_var.set(
                f"Turno del Jugador {current} "
                f"({symbol}) - {actor}"
            )

        if current == P1:
            self.objective_var.set(
                "X (verde) debe llevar sus fichas "
                "hacia la esquina inferior derecha ↘"
            )

        else:
            self.objective_var.set(
                "O (morado) debe llevar sus fichas "
                "hacia la esquina superior izquierda ↖"
            )


    def draw_board(self):
        self.canvas.delete("all")

        margin = self.MARGIN
        cell = self.CELL_SIZE

        # Números de columnas
        for col in range(SIZE):
            x = (
                margin
                + col * cell
                + cell / 2
            )

            self.canvas.create_text(
                x,
                margin / 2,
                text=str(col),
                font=("Arial", 10, "bold")
            )

        # Números de filas
        for row in range(SIZE):
            y = (
                margin
                + row * cell
                + cell / 2
            )

            self.canvas.create_text(
                margin / 2,
                y,
                text=str(row),
                font=("Arial", 10, "bold")
            )

        destinations = {
            action[-1]
            for action in self.selected_actions
        }

        for row in range(SIZE):
            for col in range(SIZE):
                x1 = margin + col * cell
                y1 = margin + row * cell

                x2 = x1 + cell
                y2 = y1 + cell

                position = (
                    row,
                    col
                )

                fill = "#ffffff"

                # Campamento verde
                if position in CAMP_P1:
                    fill = "#E5F4E9"

                # Campamento morado
                elif position in CAMP_P2:
                    fill = "#EEE5F5"

                # Lugar disponible
                if position in destinations:
                    fill = "#CDEBFF"

                # Ficha seleccionada
                if position == self.selected_piece:
                    fill = "#FFF1A8"

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=fill,
                    outline="#777777",
                    width=1
                )

        # Dibujar fichas
        for row in range(SIZE):
            for col in range(SIZE):
                value = (
                    self.state.board[row][col]
                )

                if value == EMPTY:
                    continue

                x1 = margin + col * cell + 7
                y1 = margin + row * cell + 7

                x2 = (
                    margin
                    + (col + 1) * cell
                    - 7
                )

                y2 = (
                    margin
                    + (row + 1) * cell
                    - 7
                )

                if value == P1:
                    color = "#2E8B57"
                    symbol = "X"

                else:
                    color = "#7B2CBF"
                    symbol = "O"

                self.canvas.create_oval(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline="#222222",
                    width=2
                )

                self.canvas.create_text(
                    (x1 + x2) / 2,
                    (y1 + y2) / 2,
                    text=symbol,
                    fill="white",
                    font=("Arial", 16, "bold")
                )

        bottom = (
            margin
            + SIZE * cell
            + 18
        )

        self.canvas.create_text(
            margin,
            bottom,
            text=(
                "X = Jugador 1 (verde)     "
                "O = Jugador 2 (morado)     "
                "Celeste = movimiento disponible"
            ),
            anchor="w",
            font=("Arial", 9)
        )


    def on_board_click(self, event):
        if self.agent_thinking:
            return

        if not self.is_human_turn():
            return

        margin = self.MARGIN
        cell = self.CELL_SIZE

        board_x = event.x - margin
        board_y = event.y - margin

        if board_x < 0 or board_y < 0:
            return

        col = int(
            board_x // cell
        )

        row = int(
            board_y // cell
        )

        if not (
            0 <= row < SIZE
            and 0 <= col < SIZE
        ):
            return

        position = (
            row,
            col
        )

        current = player(
            self.state
        )

        clicked_value = (
            self.state.board[row][col]
        )

        # Si selecciona una ficha propia
        if clicked_value == current:
            if position == self.selected_piece:
                self.selected_piece = None
                self.selected_actions = []

                self.clear_move_information()
                self.update_interface()

                return

            self.select_piece(
                position
            )

            return

        # Si selecciona un destino válido
        if self.selected_piece is not None:
            possible = [
                action
                for action in self.selected_actions
                if action[-1] == position
            ]

            if possible:
                self.make_move(
                    possible[0]
                )

                return

            self.status_var.set(
                "Ese espacio no es válido. "
                "Selecciona una casilla celeste."
            )


    def select_piece(self, position):
        legal_actions = actions(
            self.state
        )

        piece_actions = [
            action
            for action in legal_actions
            if action[0] == position
        ]

        self.selected_piece = position
        self.selected_actions = piece_actions

        if not piece_actions:
            self.selected_var.set(
                f"Ficha {position}: "
                "no tiene movimientos disponibles."
            )

            self.clear_moves_text()

        else:
            self.selected_var.set(
                f"Ficha seleccionada: {position}\n"
                f"Movimientos disponibles: "
                f"{len(piece_actions)}"
            )

            self.show_piece_moves(
                piece_actions
            )

        self.update_interface()


    def show_piece_moves(self, piece_actions):
        self.moves_text.configure(
            state="normal"
        )

        self.moves_text.delete(
            "1.0",
            tk.END
        )

        for action in piece_actions:
            destination = action[-1]

            if len(action) == 2:
                sr, sc = action[0]
                er, ec = action[-1]

                distance = max(
                    abs(er - sr),
                    abs(ec - sc)
                )

                if distance == 1:
                    move_type = "Paso"
                else:
                    move_type = "Salto"

            else:
                move_type = (
                    f"Salto múltiple "
                    f"({len(action) - 1} saltos)"
                )

            self.moves_text.insert(
                tk.END,
                f"→ {destination}   "
                f"{move_type}\n"
            )

        self.moves_text.configure(
            state="disabled"
        )


    def make_move(self, action):
        moving_player = player(
            self.state
        )

        self.state = result(
            self.state,
            action
        )

        self.add_history(
            moving_player,
            action,
            "Humano"
        )

        self.selected_piece = None
        self.selected_actions = []

        self.clear_move_information()

        self.update_interface()

        if self.check_game_over():
            return

        self.root.after(
            300,
            self.check_agent_turn
        )


    def check_agent_turn(self):
        if self.check_game_over():
            return

        if self.is_human_turn():
            self.agent_thinking = False
            self.update_interface()

            return

        self.start_agent_turn()


    def start_agent_turn(self):
        if self.agent_thinking:
            return

        self.agent_thinking = True

        self.selected_piece = None
        self.selected_actions = []

        self.clear_move_information()
        self.update_interface()

        depth = int(
            self.depth_var.get()
        )

        current_player = player(
            self.state
        )

        agent = MinimaxAgent(
            depth=depth,
            time_limit=28.0
        )

        state_snapshot = self.state
        token = self.game_token

        thread = threading.Thread(
            target=self.agent_worker,
            args=(
                state_snapshot,
                current_player,
                agent,
                token
            ),
            daemon=True
        )

        thread.start()


    def agent_worker(
        self,
        state_snapshot,
        current_player,
        agent,
        token
    ):
        start_time = (
            time.perf_counter()
        )

        action = agent.choose_action(
            state_snapshot
        )

        elapsed = (
            time.perf_counter()
            - start_time
        )

        nodes = agent.nodes

        self.root.after(
            0,
            lambda: self.finish_agent_move(
                state_snapshot,
                current_player,
                action,
                elapsed,
                nodes,
                token
            )
        )


    def finish_agent_move(
        self,
        old_state,
        moving_player,
        action,
        elapsed,
        nodes,
        token
    ):
        # Evita usar una respuesta de una partida anterior
        if token != self.game_token:
            return

        if old_state != self.state:
            return

        self.agent_thinking = False

        if action is None:
            self.update_interface()
            self.check_game_over()

            return

        self.state = result(
            self.state,
            action
        )

        self.add_history(
            moving_player,
            action,
            (
                f"Agente | "
                f"{elapsed:.2f}s | "
                f"{nodes} nodos"
            )
        )

        self.update_interface()

        if self.check_game_over():
            return

        self.root.after(
            500,
            self.check_agent_turn
        )


    def add_history(
        self,
        player_id,
        action,
        actor
    ):
        symbol = (
            "X"
            if player_id == P1
            else "O"
        )

        route = format_action(
            action
        )

        text = (
            f"{symbol} | {actor}\n"
            f"{route}\n\n"
        )

        self.history_text.configure(
            state="normal"
        )

        self.history_text.insert(
            tk.END,
            text
        )

        self.history_text.see(
            tk.END
        )

        self.history_text.configure(
            state="disabled"
        )


    def clear_history(self):
        self.history_text.configure(
            state="normal"
        )

        self.history_text.delete(
            "1.0",
            tk.END
        )

        self.history_text.configure(
            state="disabled"
        )


    def clear_move_information(self):
        self.selected_var.set(
            "Ninguna ficha seleccionada"
        )

        self.clear_moves_text()


    def clear_moves_text(self):
        self.moves_text.configure(
            state="normal"
        )

        self.moves_text.delete(
            "1.0",
            tk.END
        )

        self.moves_text.configure(
            state="disabled"
        )


    def check_game_over(self):
        game_winner = winner(
            self.state
        )

        if game_winner is None:
            return False

        self.agent_thinking = False
        self.update_interface()

        symbol = (
            "X"
            if game_winner == P1
            else "O"
        )

        self.status_var.set(
            f"¡Ganó el Jugador "
            f"{game_winner} ({symbol})!"
        )

        messagebox.showinfo(
            "Fin de la partida",
            (
                f"¡Ganó el Jugador "
                f"{game_winner} ({symbol})!"
            )
        )

        return True


def main():
    root = tk.Tk()

    HoppersGUI(
        root
    )

    root.mainloop()


if __name__ == "__main__":
    main()