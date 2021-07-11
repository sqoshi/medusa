from abc import ABC, abstractmethod


class Runner(ABC):
    @abstractmethod
    def main(self):
        pass

    @abstractmethod
    def run(self):
        pass
