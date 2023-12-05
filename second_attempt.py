#%%
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.cm as cm

from Multipath.rayleigh_channel import AWGNChannel, SingleRayleighChannel, EqualizedSingleRayleighChannel
from Signal.signal import Signal, _pairwise_distance
from Signal.constellation import Constellation

const = Constellation(8)
# const.plot()

n_bits = 3000
bit_stream = np.random.randint(0, 2, n_bits)
signal = Signal(bit_stream, const)

snr_incre  = 6  # SNR increment factor
all_snr = np.arange(-6, 60, snr_incre)  # Signal to noise ratio (dB)

# Simulate AWGN channel with variable SNR
channel_classes = [AWGNChannel, SingleRayleighChannel, EqualizedSingleRayleighChannel]
fig, axs = plt.subplots(len(all_snr) + 1, len(channel_classes), figsize=(7, 12), sharex=False, sharey="row")
axs[0, 0].set_title("AWGN Channel")
axs[0, 1].set_title("Unequalized Single Rayleigh Channel")
axs[0, 2].set_title("Equalized Single Rayleigh Channel")

for j, channel_class in enumerate(channel_classes):
    bit_error_rate = np.zeros(len(all_snr))
    for i, (snr, ax) in enumerate(zip(all_snr, axs[:, j])):
        channel = channel_class(snr)
        rx_symbols = channel(signal.symbols)
        rx_bits = signal.decode(rx_symbols)
        recieved_signal = Signal(rx_bits, const)
        bit_error_rate[i] = np.sum(np.abs(rx_bits - bit_stream))/n_bits
        color = ["tab:green" if bit else "tab:red" for bit in recieved_signal.symbols == signal.symbols]
        min_distance = _pairwise_distance(rx_symbols, const.constellation).min(axis=1)
        ax.scatter(rx_symbols.real, rx_symbols.imag, color=color, cmap=cm.get_cmap('coolwarm'))
        ax.set_ylabel(f"SNR = {snr} dB")
        const.plot(ax=axs[i, j])
    axs[-1, j].plot(all_snr, bit_error_rate, color="tab:blue")
    axs[-1, j].plot(all_snr, bit_error_rate, 'x', color="tab:orange")    
    axs[-1, j].set_xlabel("SNR (dB)")
    axs[-1, j].set_ylabel("Bit Error Rate")
    axs[-1, j].spines[["right", "top"]].set_visible(False)
plt.tight_layout()
plt.show()
# %%
