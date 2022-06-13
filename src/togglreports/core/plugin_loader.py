import importlib
import os
import json
from typing import Callable

from togglreports.core import report_factory


PLUGIN_FILEPATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "./data", "reports.json"))


class PluginInterface:
    """
    Represents a plugin interface
    """

    @staticmethod
    def register(register_function: Callable, name: str) -> None:
        """Register plugin"""


def import_plugin(name: str) -> PluginInterface:
    """Imports a module given a name."""
    return importlib.import_module(f"togglreports.plugins.{name}")  # type: ignore


def get_plugins() -> list[str]:
    """Returns a list of plugins."""
    with open(PLUGIN_FILEPATH) as file:
        data = json.load(file)
        return data["plugins"]


def get_plugins_required_configuration() -> dict[dict[str, str]]:
    """ Returns a list of all plugins required configuration """
    with open(PLUGIN_FILEPATH) as file:
        data = json.load(file)
        return data["config"]


def load_plugins() -> None:
    """Loads the plugins defined in the plugins list."""
    plugin_list = get_plugins()

    for plugin_name in plugin_list:
        plugin = import_plugin(plugin_name)
        plugin.register(report_factory.register, plugin_name)


if __name__ == '__main__':
    get_plugins_required_configuration()
