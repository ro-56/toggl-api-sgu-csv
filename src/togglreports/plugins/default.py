from typing import Callable

class DefaultReport():
    """
    Default report
    """
    def __init__(self, data: dict):
        pass

    def export(self) -> None:
        print('export')


def register(register_function: Callable, name: str) -> None:
    """ Register plugin """
    register_function(name, DefaultReport)
