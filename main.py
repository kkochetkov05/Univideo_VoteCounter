import tkinter as tk
from gui import VoteCounterGUI


def main():
    root = tk.Tk()
    root.state('zoomed')  # сразу на весь экран, можно убрать если не нужно
    app = VoteCounterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
