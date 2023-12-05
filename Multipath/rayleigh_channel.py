import numpy as np

class AWGNChannel:
    def __init__(self, snr: float):
        self.snr = snr
        self.noise = None

    def __call__(self, symbols: np.ndarray) -> np.ndarray:
        self.noise = np.random.randn(len(symbols)) + 1j*np.random.randn(len(symbols)) # Random Complex Noise
        self.noise *= 10**(-self.snr/20)/np.sqrt(2) # DB to linear
        return symbols + self.noise

class SingleRayleighChannel:
    def __init__(self, snr: float):
        self.snr = snr

    def __call__(self, symbols: np.ndarray) -> np.ndarray:
        noise = np.random.randn(len(symbols)) + 1j*np.random.randn(len(symbols))
        noise *= 10**(-self.snr/20)/np.sqrt(2)
        h = 1/np.sqrt(2) * (np.random.randn(len(symbols)) + 1j*np.random.randn(len(symbols)))

        unequalized = symbols * h + noise
        equalized = unequalized * np.conj(h) / np.abs(h)**2
        return equalized 
    
class N_RayleighChannels:
    def __init__(self, num_channels: int, doppler_spread: float):
        self.num_channels = num_channels
        self.doppler_spread = doppler_spread

    def __call__(self, symbols: np.ndarray) -> np.ndarray:
        alpha = np.random.rand(self.num_channels) * 2*np.pi
        phi = np.random.rand(self.num_channels) * 2*np.pi

        d_alpha = np.random.randn(self.num_channels) * np.cos(2 * np.pi * self.doppler_spread * np.cos(alpha) + phi)
        d_phi = np.random.randn(self.num_channels) * np.sin(2 * np.pi * self.doppler_spread * np.cos(alpha) + phi)

        out = symbols.copy()




