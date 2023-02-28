import argparse

parser = argparse.ArgumentParser(description='Training and testing vocoder model')
parser.add_argument('--train', type=bool, defult=False, help='train model')
parser.add_argument('--input_file', type=str, help='input file')
parser.add_argument('--output_file', type=str, help='output file')
parser.add_argument('--stretch_ratio', type=float, help='stretch ratio')


def get_arguments():
    args = parser.parse_args()
    return args