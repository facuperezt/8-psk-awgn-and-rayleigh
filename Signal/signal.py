import numpy as np
from numba import njit
from .constellation import Constellation

# Numba function to calculate pairwise distance between two arrays
@njit("float64[:,:](complex128[:], complex128[:])", fastmath=True)
def _pairwise_distance(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    dist = np.zeros((len(a), len(b)))
    for i in range(len(a)):
        for j in range(len(b)):
            dist[i, j] = np.abs(a[i] - b[j])**2
    return dist

class Signal:
    def __init__(self, bit_stream: np.ndarray, constellation: Constellation):
        self.bit_stream = bit_stream
        self.constellation = constellation
        self.symbols = self._bits_to_symbols()

    def _bits_to_symbols(self) -> np.ndarray:
        n = int(np.log2(len(self.constellation.constellation)))
        symbols = np.zeros(int(len(self.bit_stream)//n), dtype=complex)
        for i in range(0, len(self.bit_stream), n):
            _i = min(i//n, len(symbols) - 1)
            _bits = "".join([str(a) for a in self.bit_stream[i:i+n]])
            symbols[_i] = self.constellation.constellation[int(_bits, 2)]
        self.bit_stream = self.bit_stream[:_i*n + 1]
        return symbols

    def encode(self, bit_stream: np.ndarray) -> np.ndarray:
        _store_bit_stream = self.bit_stream.copy()
        self.bit_stream = bit_stream
        out = self._bits_to_symbols()
        self.bit_stream = _store_bit_stream
        return out

    def _symbols_to_bits(self) -> np.ndarray:
        dist = _pairwise_distance(self.symbols, self.constellation.constellation)
        min_dist = np.argmin(dist, axis=1)
        rx_bits = np.concatenate([np.array([int(_bit) for _bit in self.constellation.constellation_map[i]]) for i in min_dist])
        return rx_bits
    
    def decode(self, symbols: np.ndarray) -> np.ndarray:
        _store_symbols = self.symbols.copy()
        self.symbols = symbols
        out = self._symbols_to_bits()
        self.symbols = _store_symbols
        return out