"""
Модуль со всеми исключениями, которые бросаются
по ходу работы.
"""


class InterpreterException(RuntimeError):
    """
    Базовый класс для всех исключений, которые
    перехватываются в интерпретаторе. То есть
    выброс всех наследников данного класса не
    приводит к остановке интерпретатора, а
    просто к сообщению в поток ошибок.
    """


class CommandNotRegistered(InterpreterException):
    pass


class ParseError(InterpreterException):
    pass


class ExitInterpreter(SystemExit):
    pass
