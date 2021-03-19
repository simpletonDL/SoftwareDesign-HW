from typing import IO

from termcolor import colored

from src.exceptions.exceptions import InterpreterException
from src.interpreter.base_interpreter import BaseInterpreter


class BashRunner:
    """
    Класс для запуска интерпретатора.
    """

    def __init__(self, interpreter: BaseInterpreter):
        """
        :param interpreter: инстанс интерпретатора, который
        запускается в методе run.
        """
        self.interpreter = interpreter

    def run(self, inp: IO = None, out: IO = None, err: IO = None):
        """
        Метод, который запускает интерпретатор до окончания
        потока ввода. Все потоки inp, out, err могут быть
        отличными от соответствующих потоков ввода/вывода/ошибок
        в интерпретаторе. По дефолту эти потоки берутся из
        интерпретаторы.
        :param inp: Поток ввода, откуда читаются команды
        :param out: Поток вывода, куда пишутся вспомогательные
        сообщения.
        :param err: Поток ошибок, куда пишуться сообщения из
        перехваченных исключений InterpreterException.
        :return:
        """
        inp = inp if inp else self.interpreter.inp
        out = out if out else self.interpreter.out
        err = err if err else self.interpreter.err

        try:
            for cmd_line in inp:
                try:
                    self.interpreter.execute_cmd_line(cmd_line)
                except InterpreterException as e:
                    print(colored(f'Error: {e}', 'red'), file=err)
        except KeyboardInterrupt:
            print('\nClosing bash. Please donate to developer.', file=out)
            return 0
        return 0
