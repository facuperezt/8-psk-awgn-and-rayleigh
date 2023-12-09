#%%
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.cm as cm

import collections

from Multipath.rayleigh_channel import AWGNChannel, SingleRayleighChannel, EqualizedSingleRayleighChannel, MultipleRayleighChannels
from Signal.signal import Signal, _pairwise_distance
from Signal.constellation import Constellation


bit_error_rate_for_all_constellations = {}
rx_sym = collections.defaultdict(dict)
for modulation in [2, 4, 8, 16]:
    const = Constellation(modulation)
    # const.plot()

    n_bits = 1500
    bit_stream = np.random.randint(0, 2, n_bits)
    signal = Signal(bit_stream, const)

    snr_start = -3  # Starting SNR (dB)
    snr_incre  = 3  # SNR increment factor
    snr_end   = 44  # Ending SNR (dB)
    skip_n_plots = 4 # Skip every n plots
    all_snr = np.arange(snr_start, snr_end, snr_incre)  # Signal to noise ratio (dB)

    # Simulate AWGN channel with variable SNR
    channel_classes = [AWGNChannel, SingleRayleighChannel, EqualizedSingleRayleighChannel]
    fig, axs = plt.subplots(len(all_snr) + 1, len(channel_classes), figsize=(7, 12), sharex=False, sharey="row")
    fig.suptitle(f'Channels {modulation}-PSK Constellation\n', size=13 )
    axs[0, 0].set_title("AWGN", fontsize=10)
    axs[0, 1].set_title("Unequalized Single Rayleigh", fontsize=10)
    axs[0, 2].set_title("Equalized Single Rayleigh", fontsize=10)
    bit_error_rate = np.zeros((len(all_snr), len(channel_classes)))
    for j, channel_class in enumerate(channel_classes):
        # bit_error_rate = np.zeros(len(all_snr))
        for i, (snr, ax) in enumerate(zip(all_snr, axs[:, j])):
            channel = channel_class(snr)
            rx_symbols = channel(signal.symbols)
            rx_bits = signal.decode(rx_symbols)
            recieved_signal = Signal(rx_bits, const)
            bit_error_rate[i, j] = np.sum(np.abs(rx_bits - bit_stream))/n_bits
            color = ["tab:green" if bit else "tab:red" for bit in recieved_signal.symbols == signal.symbols]
            min_distance = _pairwise_distance(rx_symbols, const.constellation).min(axis=1)
            ax.scatter(rx_symbols.real, rx_symbols.imag, color=color, alpha=0.5)
            ax.set_ylabel(f"SNR {snr}dB", fontsize=8)
            const.plot(ax=axs[i, j], flag = 2)
            if not (const.modulation in rx_sym and channel.name in rx_sym[const.modulation]):
                rx_sym[const.modulation][channel.name] = rx_symbols.reshape(1, -1)
            else:
                rx_data = rx_sym[const.modulation][channel.name]
                rx_sym[const.modulation][channel.name] = np.concatenate((rx_data, rx_symbols.reshape(1,-1)))
        axs[-1, j].plot(all_snr, bit_error_rate[:,j], color="tab:blue")
        axs[-1, j].plot(all_snr, bit_error_rate[:,j], 'x', color="tab:orange")    
        axs[-1, j].set_xlabel("SNR (dB)")
        axs[-1, j].set_ylabel("BER")
        axs[-1, j].spines[["right", "top"]].set_visible(False)

    bit_error_rate_for_all_constellations[const.modulation] = bit_error_rate
    fig.tight_layout()
    plt.savefig(f"{modulation}-PSK_all.pdf",bbox_inches='tight' )
#%%
import matplotlib as mpl
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=["tab:blue", "tab:orange", "tab:green"]) 
fig2 = plt.figure()
styles = {2: '-D', 4: '--o', 8: ':s', 16: '-^'}
for key, value in bit_error_rate_for_all_constellations.items():
    color = ""
    plt.plot(all_snr, value, styles[key])
    plt.yscale('log')
    plt.xlabel("SNR (dB)")
    plt.ylabel("Bit Error Rate")
    plt.title(f"Bit Error Rate vs SNR for {key}-PSK")
    plt.legend(["AWGN", "Single Rayleigh", "Equalized Single Rayleigh"])
    plt.tight_layout()
    plt.savefig(f"{key}-PSK_BER.pdf",bbox_inches='tight' )
    plt.show()
# %%
plt.close('all')

for constel, chann in rx_sym.items():
    const = Constellation(int(constel))
    for idx in range(0, len(all_snr), 4):
        fig3 = plt.figure(figsize=(7, 12), layout='constrained')
        fig3.suptitle(f'Channels {constel}-PSK Constellation', size=13, weight='heavy' )
        subfigs = fig3.subfigures(1,len(chann))
        subfigs[0].suptitle(AWGNChannel.name,size=10, weight ="bold"  )
        subfigs[1].suptitle(SingleRayleighChannel.name,size=10,weight="bold" )
        subfigs[2].suptitle(EqualizedSingleRayleighChannel.name,size=10,weight="bold" )
        for index, (key, val) in enumerate(chann.items()):
            ax = subfigs[index].subplots(4,1)
            for i in range(4):
                ax[i].scatter(val[idx+i].real, val[idx+i].imag, cmap=cm.get_cmap('coolwarm'))
                ax[i].set_title(f"SNR = {all_snr[idx+i]} dB")
                const.plot(ax=ax[i],flag = 2)
        plt.savefig(f"{constel}-PSK_SNR_{all_snr[idx]}-{all_snr[idx+3]}_dB.pdf",bbox_inches='tight' )
        plt.close()
        #plt.show()
