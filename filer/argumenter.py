import argparse
import pathlib

class Argumenter:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="Y Programming Language Compiler v0.0.1",
            description="Compiles Y programming language.",
            epilog="Created by Nousad in 2024",
        )

        self.parser.add_argument(
            "filename",
            help="Path to the Y source file.",
            type=str,
            metavar="FILE",
        )

        self.parser.add_argument(
            "--output",
            "-o",
            help="Specify the output file name.",
            type=str,
            required=False,
            metavar="FILE",
        )

        self.parser.add_argument(
            "--encoding",
            "-e",
            help="Specify the encoding of the input file.",
            type=str,
            required=False,
            metavar="ENCODING",
            default="utf-8",
        )

        self.args = self.parser.parse_args()

        input_path = pathlib.Path(self.args.filename).absolute()
        output_path = pathlib.Path(self.args.filename).absolute()

        self.input = input_path
        self.output = self.args.output or output_path
        self.encoding = self.args.encoding

        print(self.input, self.output, self.encoding)
        exit(0)