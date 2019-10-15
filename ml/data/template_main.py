from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-d', '--directory',
        help='Directory containing csv files with data',
        type=str,
        default='*.csv'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output file for results',
        type=str,
        default='ecg-preprocessing.txt'
    )

    parser.add_argument(
        '-s', '--samplingRate',
        help='sampling rate in seconds',
        type=float,
        default=1000.0
        )

    parser.add_argument(
        '-w', '--segmentWidth',
        help='segment width in seconds',
        type=int,
        default=120
        )

    parser.add_argument(
        '-b', '--bits',
        help='the number of bits for each channel',
        type=int,
        default=6
        )

    args = parser.parse_args()