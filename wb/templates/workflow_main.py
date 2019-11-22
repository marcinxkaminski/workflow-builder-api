from os import listdir
from json import loads
from argparse import ArgumentParser
# IMPORTS - DO NOT REMOVE THIS COMMENT!


def main(input: str, output: str, delimiter: str, kwargs: dict):
    # MAIN - DO NOT REMOVE THIS COMMENT!

    return


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        '-d', '--directory',
        help='Directory containing csv files with data',
        type=str
    )

    parser.add_argument(
        '-i', '--input',
        help='Input file with data',
        type=str,
        default='data.csv'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output file for results',
        type=str,
        default='results.csv'
    )

    parser.add_argument(
        '-s', '--delimiter',
        help='Delimiter/Seperator sign used in your files',
        type=str,
        default=','
    )

    parser.add_argument(
        '-k', '--kwargs',
        help="Any other arguments that could be used by any of the Workflow Elements. Should be JSON dumped to string.",
        type=str,
        default='{}'
    )

    args = parser.parse_args()

    if args.directory:
        out = args.output
        delimiter = args.delimiter
        kwargs = loads(args.kwargs)
        for f in listdir(args.directory):
            main(input=f, output=out, delimiter=delimiter, kwargs=kwargs)
    else:
        main(input=args.input, output=args.output,
             delimiter=args.delimiter, kwargs=loads(args.kwargs))
