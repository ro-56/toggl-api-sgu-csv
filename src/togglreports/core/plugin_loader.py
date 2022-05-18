import importlib
import os
import json

from togglreports.core import report_factory


PLUGIN_FILEPATH = os.path.normpath(os.path.join(os.path.dirname(__file__),"../../../data","reports.json"))


class PluginInterface:
    """
    Represents a plugin interface
    """

    @staticmethod
    def register(name: str) -> None:
        """Register plugin"""


def import_plugin(name: str) -> PluginInterface:
    """Imports a module given a name."""
    return importlib.import_module(f"togglreports.plugins.{name}")


def get_plugins() -> list[dict[str, str]]:
    """Returns a list of plugins."""
    with open(PLUGIN_FILEPATH) as file:
        data = json.load(file)

        return data["plugins"]


def load_plugins() -> None:
    """Loads the plugins defined in the plugins list."""
    plugin_list = get_plugins()

    for plugin_name in plugin_list:
        plugin = import_plugin(plugin_name)
        plugin.register(report_factory.register, plugin_name)
