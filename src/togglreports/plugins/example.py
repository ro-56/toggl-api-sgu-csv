from typing import Callable


class ExampleReport():
    """ Example report """

    _base_data: list[dict]
    _base_config: dict
    _config: dict

    def __init__(self, data: list[dict], base_config: dict, config: dict):
        self._base_data = data
        self._base_config = base_config
        self._config = config

    def export(self) -> None:
        print('export')


def register(register_function: Callable, name: str) -> None:
    """ Register plugin """
    register_function(name, ExampleReport)
