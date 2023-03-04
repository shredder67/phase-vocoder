from src import *

import time

import numpy as np
import click


class TestPerformance:
    def __init__(self):
        self.sr, self.x = io.read_file('data/test_1.wav')
        self.N = 2048
        self.hs = 512
        self.stretch_ratio = 1.5

    def test_stretch_audio(self):
        time1 = time.time()
        stretch_audio(self.x, self.sr, self.stretch_ratio, self.N, self.hs)
        time2 = time.time()
        dt = time2 - time1
        return dt

    def mean_and_std_time(self, n=50):
        times = []
        for _ in range(n):
            dt = self.test_stretch_audio()
            times.append(dt)
        return np.mean(times), np.std(times)


@click.command()
@click.option('--n', default=10, help='number of test runs')
def test_performance(n):
    test = TestPerformance()
    print("phase vocoder avg exec time: {:.3f} +- {:.3f}ms".format(*test.mean_and_std_time(n)))


if __name__ == '__main__':
    test_performance()
