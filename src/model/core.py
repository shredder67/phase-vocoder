from typing import Union
from math import pi

import numpy as np
import scipy.fft as spft


def get_stretched_params(n: int, N: int, hs: int, stretch_ratio: Union[int, float]):
    """Returns stretched audio length and sampling hop size"""
    new_n = int(n * stretch_ratio)
    new_hs = hs * (new_n - N) // (n - N)
    return new_n, new_hs


def hanning_window(n, N):
    w = 0.5 * (1 - np.cos(2*pi*n / N))
    return w


def get_hann_values(N):
    """Returns array of hanning window values for each n in range(N)"""
    return np.array([hanning_window(n, N) for n in range(N)])


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
    w = get_hann_values(N)
    for i in range(frames):
        frame = x[i*hop_size:i*hop_size + N] * w
        X[:, i] = spft.fft(frame, N)[:freq_bins]
    return X


def processing(X: np.ndarray, sr: int, hs_a: int, hs_s: int) -> np.ndarray:
    """Obtaining true frequencies
    ## Parameters:
    - `X: np.ndarray` - freq_bins/frames matrix
    - `sr: int` - sampling rate of original signal
    - `hs_a: int` - hop size of original signal
    - `hs_s: int` - hop size of stretched signal

    ## Returns:
    `X_s: np.ndarray` - freq_bins/frames matrix
    """
    w_bin = (np.arange(X.shape[0]) * sr / X.shape[0]) # freqs per each bin
    dt_a = hs_a / sr
    dt_s = hs_s / sr
    ph_a = np.angle(X)
    ph_s = np.zeros_like(ph_a)
    for i in range(1, X.shape[1]):
        ph_delta = ph_a[:, i] - ph_a[:, i-1]
        ph_delta = ph_delta / dt_a - w_bin
        ph_delta = np.mod(ph_delta + pi, 2*pi) - pi
        fr_true = ph_delta + w_bin
        ph_s[:, i] = ph_a[:, i-1] + dt_s * fr_true
    X_s = np.abs(X) * np.exp(1j * ph_s)       
    return X_s


def synthesis(X: np.ndarray, n: int, new_n: int, sr: int, N: int, hs_a: int, hs_s: int) -> np.ndarray:
    """Apply ifft to each frame with hanning window and add overlapping windows
    
    ## Parameters:
    - `X: np.ndarray` - freq_bins/frames matrix
    - `n: int` - number of samples in original signal
    - `sr: int` - sampling rate of original signal
    - `N: int` - size of Hanning window
    - `hs_a: int` - size of hop between frames during analysis phase
    - `r: Union[float, int]` - stretch ratio 

    ## Returns:
    `y: np.ndarray` - synthesized signal (stretched or compressed without changed pitch)
    """

    q = np.zeros((X.shape[1], new_n))
    y = np.zeros(new_n)
    w = get_hann_values(N)
    for i in range(X.shape[1]):
        q[i, i*hs_s:i*hs_s + N] = np.real(spft.ifft(X[:, i] * np.sqrt(2), N)) * w
    
    # add overlapping windows
    for i in range(X.shape[1]):
        y[i*hs_s:i*hs_s + N] += q[i, i*hs_s:i*hs_s + N]
    return y


def stretch_audio(x, sr, stretch_ratio, N=2048, hs=512):
    """Stretch audio signal by given stretch ratio
    ## Parameters:
    - `x: np.ndarray` - source digital signal
    - `sr: int` - sampling rate of signal
    - `stretch_ratio: Union[int, float]` - stretch ratio
    - `N: int` (optional) - size of Hanning window, default=2048
    - `hs: int` (optional) - size of hop between frames, default=512
    """
    n = len(x)
    new_n, new_hs = get_stretched_params(n, N, hs, stretch_ratio)
    X = stft(x, sr, N, hs)
    X_s = processing(X, sr, hs, new_hs)
    y = synthesis(X_s, n, new_n, sr, N, hs, new_hs)
    return y
    