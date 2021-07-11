import shutil

from termcolor import cprint


def print_welcome():
    limit = shutil.get_terminal_size().columns
    welcome_msg = "Welcome in medusa. 🐍️"
    spacer = int((limit - len(welcome_msg)) / 2) * " "
    cprint(limit * "=", "blue")
    cprint(spacer + welcome_msg, "green")
    cprint(limit * "=", "blue")
