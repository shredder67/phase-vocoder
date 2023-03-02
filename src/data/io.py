import numpy as np
import scipy.io.wavfile as spiowf


def read_file(file: str) -> np.ndarray:
    """reads a .wav file and returns the data as a numpy array"""
    sr, data = spiowf.read(file)
    return sr, data


def write_file(output_file: str, data: np.ndarray, sr: int):
    """writes a .wav file from a numpy array"""
    spiowf.write(output_file, sr, data)
