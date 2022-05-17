### testes
import json
import os

from togglreports.core import plugin_loader, report_factory

def main():
    FILE = os.path.normpath(os.path.join(os.path.dirname(__file__),"../../data","reports.json"))
    with open(FILE) as file:
        data = json.load(file)

        # load the plugins
        plugin_loader.load_plugins(data["plugins"])


        report = report_factory.create_report('default').run()


if __name__ == '__main__':
    main()
