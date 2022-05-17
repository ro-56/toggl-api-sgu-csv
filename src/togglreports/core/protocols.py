from typing import Protocol


class ReportPlugin(Protocol):
    def __init__(self):
        pass

    def run(self, args: dict) -> None:
        pass

    def export_report(self, args: dict) -> None:
        pass
