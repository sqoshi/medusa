import shutil
import termcolor


def print_welcome():
    limit = shutil.get_terminal_size().columns
    welcome_msg = "Welcome in medusa. 🐍️"
    spacer = int((limit - len(welcome_msg)) / 2) * " "
    print(limit * "=")
    termcolor.cprint(spacer + welcome_msg, "green")
    print(limit * "=")
