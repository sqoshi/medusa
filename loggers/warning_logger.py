from termcolor import colored


class WarningLogger:
    def __init__(self):
        self.warning_prefix = colored('[WARNING] ', 'yellow')
        self.logged_content = ""

    def warn(self, message):
        msg = self.warning_prefix + colored(message, 'yellow')
        self.logged_content += msg
        print(msg)
