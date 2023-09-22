from app.printer_interface import Printer

class TestPrinter(Printer):
    def __init__(self, output: callable) -> None:
        self.output = output
        self.content = ''

    def print(self, *objects: list[str], sep: str=' ', end: str='\n', file=None, flush: bool=False) -> None:
        self.content += sep.join(objects) + end

    def clear(self) -> None:
        self.content = ''

    def update(self) -> None:
        self.output(self.content)
        self.clear()


def test_init_pinter() -> None:
    printer = TestPrinter(print)
    assert printer.content == ''
    assert printer.output is print


def test_pinter_print() -> None:
    printer = TestPrinter(print)
    printer.print('test')
    assert printer.content == 'test\n'


def test_pinter_print_end() -> None:
    printer = TestPrinter(print)
    printer.print('test', end='\t')
    assert printer.content == 'test\t'


def test_pinter_print_args() -> None:
    printer = TestPrinter(print)
    printer.print('test', 'test2')
    assert printer.content == 'test test2\n'


def test_pinter_print_args_sep() -> None:
    printer = TestPrinter(print)
    printer.print('test', 'test2', sep='-')
    assert printer.content == 'test-test2\n'


def test_pinter_clear() -> None:
    printer = TestPrinter(print)
    printer.content = 'test'
    printer.clear()
    assert printer.content == ''


def test_pinter_update(capsys) -> None:
    printer = TestPrinter(print)
    printer.content = 'test'
    printer.update()
    captured = capsys.readouterr()
    assert captured.out.strip() == 'test'