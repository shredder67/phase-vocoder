from math import cos, pi

import numpy as np
import scipy.fft as spft


def hanning_window(n, N):
    w = 0.5 * (1 - cos(2*pi*n / N))
    return w


def stft(x: np.ndarray, sr:int,  N: int, hop_size: int) -> np.ndarray:
    """Performs STFT by applying Hanning window
    
    ## Parameters:
    - `x: np.ndarray` - source digital signal
    - `sr: int` - sampling rate of signal
    - `frame_size: int` - size of single frame (frame_size assumed to be equal to window_size)
    - `hop_size: int` - size of hop between frames, 1/hop_size = overlap
    - `N: int` - size of Hammon window

    ## Returns:
    - `X: np.ndarray` - freq_bins/frames matrix
    - `freqs: np.ndarray` - array of frequencies per each freq_bin
    """
    freq_bins = int(N // 2 + 1) # -> (0, sr/2)Hz range
    frames = (len(x) - N) // hop_size + 1 
    X = np.zeros((freq_bins, frames), dtype='complex_')
    w = np.array([hanning_window(n, N) for n in range(N)]) # precalculated hanning window function values
    for i in range(frames):
        frame = x[i*hop_size:i*hop_size + N] * w
        X[:, i] = spft.fft(frame, N)[:freq_bins]
    return X


def stretch_audio(x, sr, stretch_ratio):
    raise NotImplementedError