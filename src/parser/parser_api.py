"""
Модуль с интерфейсом для парсеров.
Предполагается, что возможно в будущем
появится альтернативная реализация
парсера. Вообщем, оверинжинеринг.
"""

from abc import ABC, abstractmethod
from typing import List
from typing import TypeVar, Generic

from src.lexer.lexer import Token

T = TypeVar('T')


class CommandInfo(Generic[T]):
    """
    Объекты данного класса хранят распаршеную
    информацию об утилитах (echo/cat). Данная
    информация включает название команды и её
    аргументы.
    """
    def __init__(self, name: T, args: List[T]):
        self._name = name
        self._args = args

    @property
    def name(self) -> T:
        return self._name

    @property
    def args(self) -> List[T]:
        return self._args

    def __str__(self):
        return f'(name={self.name}, args={[str(x) for x in self.args]})'


class PipeInfo(Generic[T]):
    """
    Объекты данного класса на текущий
    момент представляют корень разбора
    парсера, то есть парсер выдаёт
    именно объект данного класса.
    Представляет из себя просто массив
    из утилит, которые были связаны
    пайпами.
    """
    def __init__(self, utils: List[CommandInfo[T]]):
        self._utils = utils

    @property
    def utils(self) -> List[CommandInfo[T]]:
        return self._utils

    def __str__(self):
        return f'{[str(x) for x in self.utils]}'


class IParser(ABC):
    """Интерфейс парсера"""
    @abstractmethod
    def parse(self, s: List[Token]) -> PipeInfo[Token]:
        pass
