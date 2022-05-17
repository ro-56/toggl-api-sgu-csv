import importlib


class PluginInterface:
    """
    Represents a plugin interface
    """

    @staticmethod
    def register(name: str) -> None:
        """Register plugin"""


def import_plugin(name: str) -> PluginInterface:
    """Imports a module given a name."""
    return importlib.import_module(name)


def load_plugins(plugin_list: list[dict[str, str]]) -> None:
    """Loads the plugins defined in the plugins list."""
    for plugin_item in plugin_list:
        try:
            plugin_name = plugin_item.get("name")
            plugin_module = plugin_item.get("module")
        except KeyError as err:
            raise KeyError(f"Plugin {plugin_item} does not have a name or module") from err
        
        plugin = import_plugin(plugin_module)
        plugin.register(name=plugin_name)
