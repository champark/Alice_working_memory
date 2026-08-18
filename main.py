# -*- coding: utf-8 -*-
import tkinter as tk

from app import AliceMemoryGame


def main() -> None:
    root = tk.Tk()
    AliceMemoryGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
