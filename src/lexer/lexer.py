"""
Модуль лексера. Пока просто один класс
со статическим методом.
"""
from abc import ABC, abstractmethod
from typing import List

from src.lexer.rules import Token, lexer


class ILexer(ABC):
    @abstractmethod
    def split(self, s: str) -> List[Token]:
        pass


class SimpleLexer(ILexer):
    """
    Класс лексера, нужен для разделения
    исходной строки на разные токены.
    """

    def split(self, s: str) -> List[Token]:
        """
        Разделяет строку и преобразует её
        в список токенов.
        :param s: входная строка
        :return: список токенов
        """
        lexer.input(s)
        return [x.value for x in lexer]
