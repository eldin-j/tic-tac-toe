import tkinter as tk

from controller import Controller

# colors
bg_color = '#EDF4FA'
light_color = '#FBFFFA'
dark_color = '#112034'
not_focused_color = '#535657'
cross_color = '#2F292D'
circle_color = '#3F0631'
lined_color = '#FFB703'
black_color = '#000000'


class TicTacToeApp:
    def __init__(self, master):
        self.controller = Controller()

        self.window = master
        self.window.title("Tic-Tac-Toe")

        # sizes and position
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window_size = int(self.screen_height * 0.5)
        self.window_pos_x = (self.screen_width - self.window_size) // 2
        self.window_pos_y = (self.screen_height - self.window_size) // 2

        self.canvas = tk.Canvas(
            width=self.window_size,
            height=self.window_size,
            background=dark_color
        )

        # window config
        self.window.geometry('{win_size}x{win_size}+{x}+{y}'.format(
            win_size=self.window_size,
            x=self.window_pos_x,
            y=self.window_pos_y
        ))
        self.window.resizable(False, False)
        self.window.configure(bg=bg_color)

    def destroy_all_widgets(self) -> None:
        for widget in self.window.winfo_children():
            if widget != self.canvas:
                widget.destroy()

    # region welcome_screen
    def create_welcome_screen(self) -> None:
        heading_label = tk.Label(
            self.window,
            text="Tic-Tac-Toe",
            bg=bg_color,
            fg=black_color,
            font=(
                "Trebuchet MS", int(self.window_size * 0.06),
                "bold"),
            pady=int(self.window_size * 0.13),
        )

        prompt_label = tk.Label(
            self.window,
            text="Enter nicknames",
            bg=bg_color,
            fg=dark_color,
            font=("Trebuchet MS", int(self.window_size * 0.0375), "bold")
        )

        entries = []
        for symbol in ['X', 'O']:
            entry = tk.Entry(
                self.window,
                bg=light_color,
                fg=not_focused_color,
                font=("Trebuchet MS", int(self.window_size * 0.03), "bold"),
                justify="center",
                disabledbackground=dark_color,
                disabledforeground='white',
                width=int(self.window_size * 0.035)
            )
            entry.bind(
                '<Return>',
                lambda event, ent=entry: self.on_enter_press(event, ent))
            entry.insert(0, symbol)
            entry.bind(
                "<FocusIn>",
                lambda event, ent=entry, sym=symbol: self.on_entry_click(event,
                                                                         ent,
                                                                         sym)
            )
            entry.bind(
                "<FocusOut>",
                lambda event, ent=entry, sym=symbol: self.on_entry_leave(event,
                                                                         ent,
                                                                         sym)
            )
            entries.append(entry)

        button = tk.Button(
            self.window,
            text='Start Game',
            command=lambda: self.on_start_button_press(entries, prompt_label),
            bg=dark_color,
            fg=light_color,
            font=("Trebuchet MS", int(self.window_size * 0.03), "bold"),
            width=int(self.window_size * 0.035),
            height=int(self.window_size * 0.001),
            cursor='hand2',
            borderwidth=0
        )

        heading_label.pack()
        prompt_label.pack()
        for entry in entries:
            entry.pack(pady=int(self.window_size * 0.0067))
        button.pack(pady=int(self.window_size * 0.01))

    def on_start_button_press(self,
                              entries: list[tk.Entry],
                              label: tk.Label
                              ) -> None:
        # when Start Game button pressed, check if all entries are not empty
        for i_entry in entries:
            if not i_entry.get() or \
                    i_entry.get() == 'X' or i_entry.get() == 'O':
                label.config(text="Nicknames cannot be empty")
                return
        # if so create board screen
        [self.controller.add_player(i_entry.get()) for i_entry in entries]
        self.destroy_all_widgets()
        self.create_board_screen()

    def on_enter_press(self, event, entry: tk.Entry) -> None:
        if entry.get().strip() != '':
            self.window.unbind('<Return>')
            entry.bind(
                '<Return>', lambda evt: self.disable_entry(evt, entry)
            )
            entry.config(state='disabled')

    def disable_entry(self, event, entry: tk.Entry) -> None:
        entry.config(state='disabled')

    def on_entry_click(self, event, entry: tk.Entry, placeholder: str) -> None:
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=black_color)

    def on_entry_leave(self, event, entry: tk.Entry, placeholder: str) -> None:
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg=not_focused_color)

    # endregion

    # region restart_screen
    def restart_game(self) -> None:
        self.controller.restart_game()
        self.destroy_all_widgets()
        self.create_welcome_screen()

    def create_restart_screen(self, message: str) -> None:
        self.destroy_all_widgets()
        self.canvas.delete('all')
        self.canvas.pack_forget()

        restart_label = tk.Label(
            self.window,
            text=message,
            bg=bg_color,
            font=(
                "Trebuchet MS", int(self.window_size * 0.06),
                "bold"),
            pady=int(self.window_size * 0.16),
        )
        restart_label.pack()

        button_data = [
            {
                'text': 'Restart',
                'command': self.restart_game,
            },
            {
                'text': 'Exit',
                'command': self.window.destroy,
            }
        ]
        for num, data in enumerate(button_data):
            button = tk.Button(
                self.window,
                text=data['text'],
                command=data['command'],
                bg=dark_color,
                fg=light_color,
                font=("Trebuchet MS", int(self.window_size * 0.03), "bold"),
                width=int(self.window_size * 0.035),
                height=int(self.window_size * 0.001),
                cursor='hand2',
                borderwidth=0
            )
            button.pack(pady=self.window_size * 0.01 * num)

    # endregion

    # region board_screen
    def create_board_screen(self) -> None:
        padding = int(self.window_size * 0.01)
        button_size = self.window_size // self.controller.board.dimension

        for row in range(self.controller.board.dimension):
            for col in range(self.controller.board.dimension):
                x0 = col * (button_size + padding)
                y0 = row * (button_size + padding)
                x1 = x0 + button_size
                y1 = y0 + button_size
                cell_num = row * 3 + col
                rectangle = self.canvas.create_rectangle(
                    x0, y0, x1, y1,
                    fill=light_color
                )

                self.canvas.tag_bind(
                    rectangle,
                    '<Button-1>',
                    lambda event, num=cell_num: self.on_cell_click(event, num)
                )

        self.canvas.pack()
        self.window.mainloop()

    def on_cell_click(self, event, cell_num) -> None:
        if self.controller.is_game_over():
            return

        self.controller.make_move(cell_num)
        game_state: str = self.controller.get_game_state()

        if game_state == 'continue':
            self.mark_cell(cell_num)
        else:
            if game_state == 'win':
                message = f'{self.controller.get_winner()} won!'
                self.mark_cells_sequence(
                    self.controller.get_lined_cells()
                )
            elif game_state == 'draw':
                message = 'Draw!'
                self.mark_cells_sequence(
                    range(self.controller.board.dimension ** 2)
                )
            self.window.after(1500,
                              lambda: self.create_restart_screen(message))

    def mark_cell(self, cell_num, in_line=False) -> None:
        row = cell_num // self.controller.board.dimension
        col = cell_num % self.controller.board.dimension
        button_size = self.window_size // self.controller.board.dimension
        text_x = col * button_size + button_size // 2
        text_y = row * button_size + button_size // 2

        mark_color = lined_color if in_line else \
            [cross_color, circle_color][self.controller.board.moves_num % 2]
        self.canvas.create_text(
            text_x,
            text_y,
            text=self.controller.board.cells[cell_num].marking,
            fill=mark_color,
            font=("Trebuchet MS", int(self.window_size * 0.12), "bold")
        )

    def mark_cells_sequence(self, cell_nums) -> None:
        for i_cell_num in cell_nums:
            self.mark_cell(i_cell_num, True)
    # endregion
