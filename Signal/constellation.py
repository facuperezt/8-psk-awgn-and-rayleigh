import numpy as np
from matplotlib import pyplot as plt

class Constellation:
    def __init__(self, modulation: int):
        self.modulation = modulation
        self.mod_delta = 2*np.pi/modulation
        if modulation == 2:
            self.constellation = np.array([-1+0j, 1+0j])
        else:
            self.constellation = np.array([np.exp((self.mod_delta/2)*1j + 1j * self.mod_delta * i) for i in range(modulation)])
        self.constellation_map = np.array([np.binary_repr(i, width=int(np.log2(modulation))) for i in range(modulation)])


    def plot(self, ax: plt.Axes = None):
        flag = False
        # Plotting of N-PSK constellation
        if ax is None:
            fig, ax = plt.subplots(figsize=(5, 5))
            flag = True
        ax.plot(np.real(self.constellation), np.imag(self.constellation), 'k*')
        for _i in range(len(self.constellation_map)):
            ax.text(np.real(self.constellation[_i]), np.imag(self.constellation[_i]), self.constellation_map[_i])
        if flag:
            ax.grid()
            ax.legend(['8-PSK constellation'])
            ax.set_xlabel('In-phase Component')
            ax.set_ylabel('Quadrature Component')
            ax.set_title(f'Constellation Plot for {self.modulation}-PSK')
        else:
            ax.set_xlim([-2, 2])
            ax.set_ylim([-2, 2])
            ax.spines[["left", "right", "top", "bottom"]].set_visible(False)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.axvline(0, color='k', linestyle='--')
            ax.axhline(0, color='k', linestyle='--')