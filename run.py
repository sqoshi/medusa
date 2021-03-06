import argparse
import sys

from medusa.beautifiers.printers import print_header
from medusa.commands import Command
from medusa.commands import converter, face_detector
from medusa.loggers.logger import Logger


def main():
    parser = argparse.ArgumentParser(description="Python ML/DL package help in images preprocessing.")
    parser.add_argument("command", type=Command, choices=list(Command), help="Command option.")

    args = parser.parse_args(sys.argv[1:2])

    print_header()
    logger = Logger()
    if args.command is Command.convert:
        converter.CommandRunner().run(logger)
    elif args.command is Command.detect:
        face_detector.CommandRunner().run(logger)

    print_header("See you soon in medusa!")
