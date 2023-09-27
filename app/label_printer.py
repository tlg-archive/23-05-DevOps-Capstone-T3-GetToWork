

from tkinter import Label
from app.printer_interface import Printer


class LabelPrinter(Printer):
    def __init__(self, label: Label):
        self.content = ""
        self.label = label

    def print(self, *objects: list[str], sep: str = ' ', end: str = '\n', file=None, flush: bool = False) -> None:
        printed_text = sep.join(objects) + end
        self.content += printed_text
        self.update()

    def clear(self) -> None:
        self.content = ""
        self.update()

    def update(self) -> None:
        self.label.config(text=self.content)
