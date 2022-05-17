from typing import Protocol


class ReportPlugin(Protocol):
    def __init__(self):
        pass

    def run(self) -> None:
        pass

    def export(self) -> None:
        pass
