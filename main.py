import click
from src import *


@click.command()
@click.argument("input_file", type=click.Path(exists=True), default="./data/test_mono.wav")
@click.argument("output_file", type=click.Path(exists=False), default="./test_mono_r05.wav")
@click.argument("stretch_ratio", type=float, default=2.0)
def stretch_audio(input_file, output_file, stretch_ratio):
    sampling_rate, original_audio = io.read_file(input_file)
    stretched_audio = stretch_audio(original_audio, sampling_rate, stretch_ratio)
    io.write_file(output_file, stretched_audio, sampling_rate)


if __name__ == '__main__':
    stretch_audio()
