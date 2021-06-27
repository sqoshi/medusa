import time

import termcolor


class TimeLogger:
    def __init__(self):
        self.last_measurement = time.time()

    def measure_time(self):
        now = time.time()
        diff = now - self.last_measurement
        self.last_measurement = now
        return diff

    def beautify(self, diff):
        return round(diff / 60, 2)

    def log_time(self, name=None):
        seconds = self.beautify(self.measure_time())
        color = 'red' if seconds > 60 else "green"  # longer than one minute
        print(
            termcolor.colored(f"[{name}] Executed in " if name else "Executed in ", "yellow") +
            termcolor.colored(str(seconds), color) +
            termcolor.colored(f" seconds.", "yellow")
        )
