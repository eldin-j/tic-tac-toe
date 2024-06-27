import tkinter as tk

from ui import TicTacToeApp

root = tk.Tk()
app = TicTacToeApp(root)
app.create_welcome_screen()
root.mainloop()
