"""Simple GUI to run backtests and display results."""
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from strategies import STRATEGIES
from main import generate_prices


def run(strategy_name, figure):
    prices = generate_prices()
    result = STRATEGIES[strategy_name](prices)
    figure.clf()
    ax = figure.add_subplot(111)
    result.equity_curve.plot(ax=ax)
    ax.set_title(strategy_name)
    ax.set_xlabel("Time")
    ax.set_ylabel("Equity")
    canvas.draw()


def start_gui():
    root = tk.Tk()
    root.title("Backtesting GUI")

    strategy_var = tk.StringVar(value=list(STRATEGIES.keys())[0])

    ttk.Label(root, text="Strategy:").pack(side=tk.LEFT, padx=5, pady=5)
    strategy_menu = ttk.OptionMenu(root, strategy_var, strategy_var.get(), *STRATEGIES.keys())
    strategy_menu.pack(side=tk.LEFT, padx=5, pady=5)

    fig = plt.Figure(figsize=(6,4))
    global canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    run_button = ttk.Button(root, text="Run", command=lambda: run(strategy_var.get(), fig))
    run_button.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()


if __name__ == "__main__":
    start_gui()
