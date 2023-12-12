import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from Signal.plotting import plot_constellation
from Signal.signal import Signal
from Signal.constellation import Constellation
from Multipath.rayleigh_channel import AWGNChannel, SingleRayleighChannel, MultipleRayleighChannels

def update_plot():
    axs[0].clear()
    axs[1].clear()
    channel_left = channel_map[values[f'-CHANNEL LEFT-']](values["-SNR-"], num_channels=values['-N_CHANNELS LEFT-'], equalize=values['-EQUALIZE LEFT-'])
    channel_right = channel_map[values[f'-CHANNEL RIGHT-']](values["-SNR-"], num_channels=values['-N_CHANNELS RIGHT-'], equalize=values['-EQUALIZE RIGHT-'])
    rx_signal_left = plot_constellation(channel_left, signal_left, axs[0])
    rx_signal_right = plot_constellation(channel_right, signal_right, axs[1])
    bit_error_rate_left = np.sum(np.abs(rx_signal_left.bit_stream - signal_left.bit_stream))/len(bit_stream)
    bit_error_rate_right = np.sum(np.abs(rx_signal_right.bit_stream - signal_right.bit_stream))/len(bit_stream)
    axs[0].set_title(f"BER: {bit_error_rate_left:.4f}", fontsize=10)
    axs[0].axis('on')
    axs[1].set_title(f"BER: {bit_error_rate_right:.4f}", fontsize=10)
    axs[1].axis('on')
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

def get_parts(side: str = 'LEFT') -> (sg.Column, sg.Column):
    control_col = [
        [sg.Text('Simulation', font='Any 25')],
        [sg.Text('Number of Bits', font='Any 15')],
        [sg.InputText('1000', key=f'-N_BITS-', size=(20, 1))],
        [sg.Text('SNR (dB)', font='Any 15')],
        [sg.Slider(range=(-10, 50), default_value=0, size=(20, 15), orientation='horizontal', key=f'-SNR-', enable_events=True)],
        [sg.Text(f'Transmission Channel {side}', font='Any 15')],
        [sg.DropDown(['AWGN', 'Single Rayleigh', 'Multi Rayleigh'], default_value='AWGN', key=f'-CHANNEL {side}-', size=(20, 1))],
        [sg.Checkbox('Equalize (Only affects Rayleigh channels)', default=False, key=f'-EQUALIZE {side}-', size=(50, 1))],
        [sg.Text('Number of Channels (Only affects Multi Rayleigh)', font='Any 15')],
        [sg.InputText('5', key=f'-N_CHANNELS {side}-', size=(20, 1))],
        [sg.Text(f'Modulation Type {side}', font='Any 15')],
        [sg.DropDown(['BPSK', '4-QAM', '8-PSK', '16-PSK'], default_value='8-PSK', key=f'-MODULATION {side}-', size=(20, 1))],
    ]
    if side == 'RIGHT':
        control_col = control_col[5:]
    else:
        control_col += [
            [sg.Button('Generate Signal', key='-NEW SIGNAL-', size=(15, 1))],  #, sg.Button('Plot BER Comparison', size=(15, 1))],
            [sg.Button('Exit', size=(10, 1))]
        ]

    plot_col = [
        [sg.Text('Plot', font='Any 15')],
        [sg.Canvas(size=(300, 300), key=f'-CANVAS-')],
    ]

    return sg.Column(control_col), sg.Column(plot_col)

channel_map = {
    'AWGN': AWGNChannel,
    'Single Rayleigh': SingleRayleighChannel,
    'Multi Rayleigh': MultipleRayleighChannels,
}

control_col, plot_col = get_parts('LEFT')
control_col2, plot_col2 = get_parts('RIGHT')

layout = [[control_col, plot_col, control_col2]]

window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI',
                     layout, location=(0,0), finalize=True)
fig, axs = plt.subplots(1, 2, figsize=(5, 3))
figure_canvas_agg = FigureCanvasTkAgg(fig, window['-CANVAS-'].TKCanvas)
figure_canvas_agg.draw()
figure_canvas_agg.get_tk_widget().pack()
axs[0].axis('off')
axs[1].axis('off')

bit_stream = None
while True:
    event, values = window.read(timeout=100)
    if event in ('Exit', None):
        break
    elif event == '-SNR-':
        if bit_stream is not None:
            update_plot()
    elif event == '-NEW SIGNAL-':
        bit_stream = np.random.randint(0, 2, int(values['-N_BITS-']))
        signal_left = Signal(bit_stream, Constellation(int(values['-MODULATION LEFT-'].split("-")[0])))
        signal_right = Signal(bit_stream, Constellation(int(values['-MODULATION RIGHT-'].split("-")[0])))
        update_plot()
    elif event == 'Plot BER Comparison':
        plt.figure()
        bit_stream = np.random.randint(0, 2, int(values['-N_BITS-']))
        signal_left = Signal(bit_stream, Constellation(int(values['-MODULATION LEFT-'][0])))
        signal_right = Signal(bit_stream, Constellation(int(values['-MODULATION RIGHT-'][0])))
        snr_range = np.arange(-10, 50, 1)
        bit_error_rates = np.zeros((len(snr_range), 2))
        for snr in snr_range:
            channel_left = channel_map[values[f'-CHANNEL LEFT-']](snr, values['-N_CHANNELS LEFT-'], equalize=values['-EQUALIZE LEFT-'])
            channel_right = channel_map[values[f'-CHANNEL RIGHT-']](snr, values['-N_CHANNELS RIGHT-'], equalize=values['-EQUALIZE RIGHT-'])
            rx_signal_left = plot_constellation(channel_left, signal_left, axs[0])
            rx_signal_right = plot_constellation(channel_right, signal_right, axs[1])
            bit_error_rate_left = np.sum(np.abs(rx_signal_left.bit_stream - signal_left.bit_stream))/len(bit_stream)
            bit_error_rate_right = np.sum(np.abs(rx_signal_right.bit_stream - signal_right.bit_stream))/len(bit_stream)
            bit_error_rates[snr, 0] = bit_error_rate_left
            bit_error_rates[snr, 1] = bit_error_rate_right

        plt.plot(snr_range, bit_error_rates[:, 0], label=values["-CHANNEL LEFT-"])
        plt.plot(snr_range, bit_error_rates[:, 1], label=values["-CHANNEL RIGHT-"])
        plt.yscale('log')
        plt.xlabel("SNR (dB)")
        plt.ylabel("Bit Error Rate")
        plt.title(f"Bit Error Rate vs SNR for {values['-MODULATION-']}")
        plt.show()

    elif event == 'stop':
        pass
window.close()
