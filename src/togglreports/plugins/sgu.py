from typing import Callable

class SGUReport():
    """
    Sgu report
    """

    _base_data: dict
    _config: dict
    _file_format: str = 'csv'

    def __init__(self, data: dict, config: dict):
        self._base_data = data
        self._config = config
        print(self._config)

    def export(self) -> None:
        print('export')


def register(register_function: Callable, name: str) -> None:
    """ Register plugin """
    register_function(name, SGUReport)
