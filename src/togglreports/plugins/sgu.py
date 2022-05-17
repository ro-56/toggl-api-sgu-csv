from togglreports.core import report_factory

class SGUReport():
    """
    Sgu report
    """
    def __init__(self):
        pass

    def run(self) -> None:
        print('run')

    def export(self) -> None:
        print('export')


def register(name: str) -> None:
    """
    Register plugin
    """
    report_factory.register_report(name, SGUReport)
