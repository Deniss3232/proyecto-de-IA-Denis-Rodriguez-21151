import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
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


class HoppersApp:

    CELL = 54
    MARGIN = 34

    GREEN = "#2E8B57"
    PURPLE = "#7B2CBF"

    BG = "#171A21"
    CARD = "#232730"
    BOARD_BG = "#F4F1EA"

    TEXT = "#F5F5F5"
    MUTED = "#A9AFBA"

    BLUE = "#38A9D1"
    GOLD = "#E8B647"

    def __init__(self, root):
        self.root = root
        self.root.title("Hoppers")
        self.root.geometry("1050x820")
        self.root.minsize(980, 760)
        self.root.configure(bg=self.BG)

        self.state = initial_state()

        self.selected_piece = None
        self.selected_actions = []

        self.agent_thinking = False
        self.agent_queue = queue.Queue()

        self.game_id = 0

        self.mode = None
        self.depth = 2

        self.history = []

        self.main_frame = None
        self.canvas = None

        self.show_start_screen()




    def show_start_screen(self):
        if self.main_frame is not None:
            self.main_frame.destroy()

        self.main_frame = tk.Frame(
            self.root,
            bg=self.BG
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        center = tk.Frame(
            self.main_frame,
            bg=self.BG
        )

        center.place(
            relx=0.5,
            rely=0.48,
            anchor="center"
        )

        tk.Label(
            center,
            text="HOPPERS",
            font=("Segoe UI", 38, "bold"),
            fg="white",
            bg=self.BG
        ).pack()

        tk.Label(
            center,
            text="Proyecto de Inteligencia Artificial",
            font=("Segoe UI", 12),
            fg=self.MUTED,
            bg=self.BG
        ).pack(
            pady=(0, 30)
        )

        tk.Label(
            center,
            text="Selecciona un modo de juego",
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg=self.BG
        ).pack(
            pady=(0, 15)
        )

        modes = [
            ("Humano vs Agente", "Tú juegas primero"),
            ("Agente vs Humano", "El agente juega primero"),
            ("Agente vs Agente", "Observa a los dos agentes"),
            ("Humano vs Humano", "Dos jugadores manuales")
        ]

        for name, description in modes:
            button = tk.Button(
                center,
                text=f"{name}\n{description}",
                command=lambda m=name: self.select_mode(m),
                width=32,
                height=3,
                font=("Segoe UI", 11, "bold"),
                bg=self.CARD,
                fg="white",
                activebackground="#313642",
                activeforeground="white",
                relief="flat",
                cursor="hand2"
            )

            button.pack(
                pady=6
            )

        depth_frame = tk.Frame(
            center,
            bg=self.BG
        )

        depth_frame.pack(
            pady=(25, 0)
        )

        tk.Label(
            depth_frame,
            text="Profundidad del agente:",
            font=("Segoe UI", 10),
            fg=self.MUTED,
            bg=self.BG
        ).pack(
            side="left",
            padx=(0, 10)
        )

        self.depth_var = tk.IntVar(
            value=2
        )

        depth_box = ttk.Combobox(
            depth_frame,
            textvariable=self.depth_var,
            state="readonly",
            values=(1, 2, 3, 4, 5),
            width=5
        )

        depth_box.pack(
            side="left"
        )


    def select_mode(self, mode):
        self.mode = mode
        self.depth = int(
            self.depth_var.get()
        )

        self.start_game()




    def start_game(self):
        self.game_id += 1

        self.state = initial_state()

        self.selected_piece = None
        self.selected_actions = []

        self.agent_thinking = False

        self.history = []

        self.create_game_screen()
        self.update_game()

        self.root.after(
            400,
            self.check_agent_turn
        )


    def create_game_screen(self):
        self.main_frame.destroy()

        self.main_frame = tk.Frame(
            self.root,
            bg=self.BG
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        # Barra superior
        top = tk.Frame(
            self.main_frame,
            bg=self.BG
        )

        top.pack(
            fill="x",
            padx=28,
            pady=(20, 10)
        )

        tk.Button(
            top,
            text="← Menú",
            command=self.show_start_screen,
            bg=self.CARD,
            fg="white",
            activebackground="#343944",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 10),
            cursor="hand2"
        ).pack(
            side="left",
            ipadx=12,
            ipady=5
        )

        tk.Label(
            top,
            text="HOPPERS",
            font=("Segoe UI", 22, "bold"),
            bg=self.BG,
            fg="white"
        ).pack(
            side="left",
            padx=20
        )

        tk.Label(
            top,
            text=self.mode,
            font=("Segoe UI", 10),
            bg=self.BG,
            fg=self.MUTED
        ).pack(
            side="left"
        )

        tk.Button(
            top,
            text="Cómo jugar",
            command=self.show_help,
            bg=self.CARD,
            fg="white",
            activebackground="#343944",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        ).pack(
            side="right",
            padx=(8, 0),
            ipadx=10,
            ipady=5
        )

        tk.Button(
            top,
            text="Historial",
            command=self.show_history,
            bg=self.CARD,
            fg="white",
            activebackground="#343944",
            activeforeground="white",
            relief="flat",
            cursor="hand2"
        ).pack(
            side="right",
            ipadx=10,
            ipady=5
        )


        # Tarjetas de jugadores
        player_area = tk.Frame(
            self.main_frame,
            bg=self.BG
        )

        player_area.pack(
            pady=(5, 10)
        )

        self.p1_card = tk.Frame(
            player_area,
            bg=self.CARD,
            width=280,
            height=80
        )

        self.p1_card.pack(
            side="left",
            padx=10
        )

        self.p1_card.pack_propagate(False)

        self.p1_title = tk.Label(
            self.p1_card,
            text="X   JUGADOR 1",
            font=("Segoe UI", 14, "bold"),
            bg=self.CARD,
            fg=self.GREEN
        )

        self.p1_title.pack(
            pady=(12, 2)
        )

        self.p1_info = tk.Label(
            self.p1_card,
            text="Meta: esquina inferior derecha ↘",
            font=("Segoe UI", 9),
            bg=self.CARD,
            fg=self.MUTED
        )

        self.p1_info.pack()


        self.p2_card = tk.Frame(
            player_area,
            bg=self.CARD,
            width=280,
            height=80
        )

        self.p2_card.pack(
            side="left",
            padx=10
        )

        self.p2_card.pack_propagate(False)

        self.p2_title = tk.Label(
            self.p2_card,
            text="O   JUGADOR 2",
            font=("Segoe UI", 14, "bold"),
            bg=self.CARD,
            fg=self.PURPLE
        )

        self.p2_title.pack(
            pady=(12, 2)
        )

        self.p2_info = tk.Label(
            self.p2_card,
            text="Meta: esquina superior izquierda ↖",
            font=("Segoe UI", 9),
            bg=self.CARD,
            fg=self.MUTED
        )

        self.p2_info.pack()


        # Texto central de turno
        self.turn_label = tk.Label(
            self.main_frame,
            text="",
            font=("Segoe UI", 13, "bold"),
            fg="white",
            bg=self.BG
        )

        self.turn_label.pack(
            pady=(5, 3)
        )

        self.status_label = tk.Label(
            self.main_frame,
            text="",
            font=("Segoe UI", 9),
            fg=self.MUTED,
            bg=self.BG
        )

        self.status_label.pack(
            pady=(0, 5)
        )


        # Tablero
        board_container = tk.Frame(
            self.main_frame,
            bg=self.BOARD_BG,
            padx=15,
            pady=15
        )

        board_container.pack(
            pady=10
        )

        canvas_size = (
            SIZE * self.CELL
            + self.MARGIN * 2
        )

        self.canvas = tk.Canvas(
            board_container,
            width=canvas_size,
            height=canvas_size,
            bg=self.BOARD_BG,
            highlightthickness=0
        )

        self.canvas.pack()

        self.canvas.bind(
            "<Button-1>",
            self.board_click
        )


        # Información inferior
        bottom = tk.Frame(
            self.main_frame,
            bg=self.BG
        )

        bottom.pack(
            fill="x",
            padx=100,
            pady=(5, 20)
        )

        self.selection_label = tk.Label(
            bottom,
            text="Selecciona una ficha",
            font=("Segoe UI", 10),
            fg="white",
            bg=self.BG
        )

        self.selection_label.pack(
            side="left"
        )

        self.last_move_label = tk.Label(
            bottom,
            text="",
            font=("Segoe UI", 9),
            fg=self.MUTED,
            bg=self.BG
        )

        self.last_move_label.pack(
            side="right"
        )




    def human_turn(self):
        current = player(self.state)

        if self.mode == "Humano vs Humano":
            return True

        if self.mode == "Agente vs Agente":
            return False

        if self.mode == "Humano vs Agente":
            return current == P1

        if self.mode == "Agente vs Humano":
            return current == P2

        return True


    def update_game(self):
        self.draw_board()

        current = player(
            self.state
        )

        normal = self.CARD
        active = "#343A46"

        if current == P1:
            self.p1_card.configure(
                bg=active
            )

            self.p1_title.configure(
                bg=active
            )

            self.p1_info.configure(
                bg=active
            )

            self.p2_card.configure(
                bg=normal
            )

            self.p2_title.configure(
                bg=normal
            )

            self.p2_info.configure(
                bg=normal
            )

            name = "Jugador 1 · Verde"

        else:
            self.p2_card.configure(
                bg=active
            )

            self.p2_title.configure(
                bg=active
            )

            self.p2_info.configure(
                bg=active
            )

            self.p1_card.configure(
                bg=normal
            )

            self.p1_title.configure(
                bg=normal
            )

            self.p1_info.configure(
                bg=normal
            )

            name = "Jugador 2 · Morado"

        if self.agent_thinking:
            self.turn_label.config(
                text=f"{name} está pensando..."
            )

            self.status_label.config(
                text="Minimax está calculando el movimiento."
            )

        else:
            actor = (
                "Humano"
                if self.human_turn()
                else "Agente"
            )

            self.turn_label.config(
                text=f"Turno de {name}"
            )

            self.status_label.config(
                text=actor
            )




    def draw_board(self):
        self.canvas.delete("all")

        destinations = {
            action[-1]
            for action in self.selected_actions
        }

        for i in range(SIZE):
            x = (
                self.MARGIN
                + i * self.CELL
                + self.CELL / 2
            )

            y = (
                self.MARGIN
                + i * self.CELL
                + self.CELL / 2
            )

            self.canvas.create_text(
                x,
                self.MARGIN / 2,
                text=str(i),
                fill="#777777",
                font=("Segoe UI", 9, "bold")
            )

            self.canvas.create_text(
                self.MARGIN / 2,
                y,
                text=str(i),
                fill="#777777",
                font=("Segoe UI", 9, "bold")
            )


        for row in range(SIZE):
            for col in range(SIZE):
                position = (
                    row,
                    col
                )

                x1 = (
                    self.MARGIN
                    + col * self.CELL
                )

                y1 = (
                    self.MARGIN
                    + row * self.CELL
                )

                x2 = x1 + self.CELL
                y2 = y1 + self.CELL

                if (row + col) % 2 == 0:
                    color = "#F7F4ED"
                else:
                    color = "#E8E4DA"

                if position in CAMP_P1:
                    color = "#DDEFE4"

                elif position in CAMP_P2:
                    color = "#EDE1F5"

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline="#C9C5BC"
                )


        # Destinos posibles
        for row, col in destinations:
            x = (
                self.MARGIN
                + col * self.CELL
                + self.CELL / 2
            )

            y = (
                self.MARGIN
                + row * self.CELL
                + self.CELL / 2
            )

            self.canvas.create_oval(
                x - 10,
                y - 10,
                x + 10,
                y + 10,
                outline=self.BLUE,
                width=3
            )

            self.canvas.create_oval(
                x - 3,
                y - 3,
                x + 3,
                y + 3,
                fill=self.BLUE,
                outline=""
            )


        # Fichas
        for row in range(SIZE):
            for col in range(SIZE):
                piece = (
                    self.state.board[row][col]
                )

                if piece == EMPTY:
                    continue

                x = (
                    self.MARGIN
                    + col * self.CELL
                    + self.CELL / 2
                )

                y = (
                    self.MARGIN
                    + row * self.CELL
                    + self.CELL / 2
                )

                if piece == P1:
                    color = self.GREEN
                    letter = "X"
                else:
                    color = self.PURPLE
                    letter = "O"

                if (row, col) == self.selected_piece:
                    self.canvas.create_oval(
                        x - 25,
                        y - 25,
                        x + 25,
                        y + 25,
                        outline=self.GOLD,
                        width=4
                    )

                self.canvas.create_oval(
                    x - 19,
                    y - 19,
                    x + 19,
                    y + 19,
                    fill=color,
                    outline="#2A2A2A",
                    width=2
                )

                self.canvas.create_text(
                    x,
                    y,
                    text=letter,
                    fill="white",
                    font=("Segoe UI", 14, "bold")
                )




    def board_click(self, event):
        if self.agent_thinking:
            return

        if not self.human_turn():
            return

        x = event.x - self.MARGIN
        y = event.y - self.MARGIN

        if x < 0 or y < 0:
            return

        col = int(
            x // self.CELL
        )

        row = int(
            y // self.CELL
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

        clicked = (
            self.state.board[row][col]
        )

        if clicked == current:
            self.select_piece(
                position
            )

            return

        if self.selected_piece is not None:
            possible = [
                move
                for move in self.selected_actions
                if move[-1] == position
            ]

            if possible:
                self.make_move(
                    possible[0]
                )

            else:
                self.selection_label.config(
                    text="Selecciona uno de los destinos azules."
                )


    def select_piece(self, position):
        if position == self.selected_piece:
            self.selected_piece = None
            self.selected_actions = []

            self.selection_label.config(
                text="Selecciona una ficha"
            )

            self.update_game()
            return

        all_moves = actions(
            self.state
        )

        piece_moves = [
            move
            for move in all_moves
            if move[0] == position
        ]

        self.selected_piece = position
        self.selected_actions = piece_moves

        if len(piece_moves) == 0:
            self.selection_label.config(
                text=f"La ficha {position} no puede moverse."
            )

        else:
            self.selection_label.config(
                text=(
                    f"Ficha {position} · "
                    f"{len(piece_moves)} movimientos disponibles"
                )
            )

        self.update_game()


    def make_move(self, move):
        current_player = player(
            self.state
        )

        self.state = result(
            self.state,
            move
        )

        self.save_history(
            current_player,
            move,
            "Humano"
        )

        self.selected_piece = None
        self.selected_actions = []

        self.last_move_label.config(
            text=f"Última jugada: {format_action(move)}"
        )

        self.selection_label.config(
            text="Selecciona una ficha"
        )

        self.update_game()

        if self.check_winner():
            return

        self.root.after(
            300,
            self.check_agent_turn
        )




    def check_agent_turn(self):
        if self.check_winner():
            return

        if self.human_turn():
            self.agent_thinking = False
            self.update_game()
            return

        self.start_agent()


    def start_agent(self):
        if self.agent_thinking:
            return

        self.agent_thinking = True

        self.selected_piece = None
        self.selected_actions = []

        self.update_game()

        agent = MinimaxAgent(
            depth=self.depth,
            time_limit=28.0
        )

        old_state = self.state
        current_player = player(
            self.state
        )

        current_game = self.game_id

        thread = threading.Thread(
            target=self.agent_worker,
            args=(
                current_game,
                old_state,
                current_player,
                agent
            ),
            daemon=True
        )

        thread.start()

        self.root.after(
            100,
            self.check_agent_result
        )


    def agent_worker(
        self,
        game_id,
        old_state,
        current_player,
        agent
    ):
        start = time.perf_counter()

        move = agent.choose_action(
            old_state
        )

        elapsed = (
            time.perf_counter()
            - start
        )

        self.agent_queue.put(
            (
                game_id,
                old_state,
                current_player,
                move,
                elapsed,
                agent.nodes
            )
        )


    def check_agent_result(self):
        data = None

        while not self.agent_queue.empty():
            item = self.agent_queue.get()

            if item[0] == self.game_id:
                data = item

        if data is None:
            if self.agent_thinking:
                self.root.after(
                    100,
                    self.check_agent_result
                )

            return

        (
            game_id,
            old_state,
            current_player,
            move,
            elapsed,
            nodes
        ) = data

        if game_id != self.game_id:
            return

        if old_state != self.state:
            return

        self.agent_thinking = False

        if move is None:
            self.check_winner()
            return

        self.state = result(
            self.state,
            move
        )

        description = (
            f"Agente · {elapsed:.2f}s · {nodes} nodos"
        )

        self.save_history(
            current_player,
            move,
            description
        )

        self.last_move_label.config(
            text=f"Última jugada: {format_action(move)}"
        )

        self.update_game()

        if self.check_winner():
            return

        self.root.after(
            500,
            self.check_agent_turn
        )



    def save_history(
        self,
        player_id,
        move,
        description
    ):
        symbol = (
            "X"
            if player_id == P1
            else "O"
        )

        self.history.append(
            (
                symbol,
                description,
                format_action(move)
            )
        )


    def show_history(self):
        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Historial de movimientos"
        )

        window.geometry(
            "520x500"
        )

        window.configure(
            bg=self.BG
        )

        tk.Label(
            window,
            text="Historial de la partida",
            font=("Segoe UI", 18, "bold"),
            bg=self.BG,
            fg="white"
        ).pack(
            pady=(20, 10)
        )

        text = tk.Text(
            window,
            bg=self.CARD,
            fg="white",
            relief="flat",
            font=("Consolas", 10),
            padx=15,
            pady=15
        )

        text.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        if not self.history:
            text.insert(
                tk.END,
                "Todavía no se han realizado movimientos."
            )

        else:
            for number, item in enumerate(
                self.history,
                start=1
            ):
                symbol, description, move = item

                text.insert(
                    tk.END,
                    f"{number}. {symbol} - {description}\n"
                    f"   {move}\n\n"
                )

        text.config(
            state="disabled"
        )




    def show_help(self):
        messagebox.showinfo(
            "Cómo jugar Hoppers",
            (
                "OBJETIVO\n\n"
                "El jugador verde (X) debe llegar a la esquina "
                "inferior derecha.\n\n"
                "El jugador morado (O) debe llegar a la esquina "
                "superior izquierda.\n\n"
                "MOVIMIENTOS\n\n"
                "Haz clic sobre una de tus fichas. "
                "Los círculos azules indican los lugares disponibles.\n\n"
                "Las fichas pueden moverse una casilla en cualquiera "
                "de las ocho direcciones.\n\n"
                "También pueden saltar sobre otras fichas y realizar "
                "varios saltos en un mismo turno."
            )
        )



    def check_winner(self):
        game_winner = winner(
            self.state
        )

        if game_winner is None:
            return False

        self.agent_thinking = False

        if game_winner == P1:
            name = "Jugador 1 · Verde"
        else:
            name = "Jugador 2 · Morado"

        messagebox.showinfo(
            "Fin de la partida",
            f"¡Ganó {name}!"
        )

        return True


def main():
    root = tk.Tk()

    HoppersApp(
        root
    )

    root.mainloop()


if __name__ == "__main__":
    main()
