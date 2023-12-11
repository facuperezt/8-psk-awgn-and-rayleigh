import matplotlib.pyplot as plt

from .signal import Signal


def plot_constellation(channel, signal: Signal, ax: plt.Axes):
    rx_symbols = channel(signal.symbols)
    rx_bits = signal.decode(rx_symbols)
    recieved_signal = Signal(rx_bits, signal.constellation)
    color = ["tab:green" if bit else "tab:red" for bit in recieved_signal.symbols == signal.symbols]
    ax.scatter(rx_symbols.real, rx_symbols.imag, color=color, alpha=0.5)
    signal.constellation.plot(ax=ax, flag = 2)

    return recieved_signal