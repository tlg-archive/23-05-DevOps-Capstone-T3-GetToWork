
from typing import Protocol

class Printer(Protocol):
    output: any
    content: str

    def print(self, *objects: list[str], sep: str=' ', end: str='\n', file=None, flush: bool=False) -> None:
        pass

    def clear(self) -> None:
        pass

    def update(self) -> None:
        pass
