from music21 import converter


def main(in_path, out_path):
    abc = converter.parse(str(in_path))
    abc.write('midi', fp=str(out_path))
