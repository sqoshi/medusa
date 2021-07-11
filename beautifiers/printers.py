import shutil

from termcolor import cprint


def print_header(message="Welcome in medusa.", emoji="🐍️"):
    limit = shutil.get_terminal_size().columns
    welcome_msg = f"{message} {emoji}"
    spacer = int((limit - len(welcome_msg)) / 2) * " "
    cprint(limit * "=", "blue")
    cprint(spacer + welcome_msg, "green")
    cprint(limit * "=", "blue")
