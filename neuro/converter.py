import argparse

from music21 import converter


def main(in_path, out_path):
    abc = converter.parse(str(in_path))
    abc.write('midi', fp=str(out_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert .abc files to .mid')

    parser.add_argument('--into', default='', help='input file (in abc notation)')
    parser.add_argument('--out', default='', help='output file (midi format)')

    args = parser.parse_args()
    print(args.into, args.out)

    main(args.into, args.out)
