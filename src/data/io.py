from typing import Tuple

import numpy as np
import soundfile as sf

def read_file(file: str) -> Tuple[int, np.ndarray]:
    """reads a .wav file and returns the data as a numpy array"""
    data, sr = sf.read(file)
    return sr, data


def write_file(output_file: str, data: np.ndarray, sr: int) -> None:
    """writes a .wav file from a numpy array"""
    sf.write(output_file, data, sr)
