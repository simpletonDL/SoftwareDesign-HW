"""
Модуль, где задаются регулярки для токенов.
Используется библиотека Lex.
"""

from enum import Enum
import ply.lex as lex

from src.exceptions.exceptions import ParseError


class TokenType(Enum):
    """
    Класс перечисления токенов.
    STR: обычная строка
    SINGLE: строка в одинарных кавычках
    DOUBLE: строка в двойных кавычках
    VAR_DER: обяъвление переменной вида var=expr.
    """
    STR = 'STR'
    SINGLE = 'SINGLE'
    DOUBLE = 'DOUBLE'
    PIPE = 'PIPE'
    VAR_DEF = 'VAR_DEF'


class Token:
    """
    Класс, представляющий токен. У токена есть тип
    и подлежащая строка. От типа зависит, будет ли
    как будет происходить дальнейшая подстановка
    переменных.
    """
    def __init__(self, kind: TokenType, token: str):
        self._kind = kind
        self._token = token

    @property
    def kind(self) -> TokenType:
        return self._kind

    @property
    def string(self) -> str:
        return self._token

    def __str__(self):
        return f'({self._kind}, {self._token})'

    def __eq__(self, other):
        return isinstance(other, Token) and self.kind == other.kind and self.string == other.string

tokens = (
    'VAR_DEF',
    'STR',
    'SINGLE',
    'DOUBLE',
    'PIPE',
)


def tokenize(t: lex.LexToken, tp: TokenType):
    t.value = Token(tp, t.value)
    return t


def t_VAR_DEF(t):
    r'\w+=([^\s\t\r\'\"\|=]+|\'[^\']*\'|\"[^\"]*\")'
    return tokenize(t, TokenType.VAR_DEF)


def t_STR(t):
    r'[^\s\t\r\'\"\|=]+'
    return tokenize(t, TokenType.STR)


def t_SINGLE(t):
    r'\'[^\']*\''
    return tokenize(t, TokenType.SINGLE)


def t_DOUBLE(t):
    r'\"[^\"]*\"'
    return tokenize(t, TokenType.DOUBLE)


def t_PIPE(t):
    r'\|'
    return tokenize(t, TokenType.PIPE)


t_ignore = ' \t\n'


def t_error(t):
    raise ParseError(f'Illegal token near \'{t.value.strip()}\'')

lexer = lex.lex()
