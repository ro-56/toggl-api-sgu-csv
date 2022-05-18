from typing import Protocol


class ReportPlugin(Protocol):

    def __init__(self, data: dict):
        pass

    def export(self) -> None:
        pass
