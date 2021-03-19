from typing import Dict

from src.expander.expander import Expander
from src.lexer.rules import Token, TokenType


def check(t: Token, mapper: Dict[str, str], expected: str):
    assert Expander.substitute(t, mapper) == expected


def test_1():
    t = Token(TokenType.STR, """abc$xy$cv""")
    m = {
        'xy': '12',
        'cv': '34'
    }
    check(t, m, 'abc1234')


def test_2():
    t = Token(TokenType.DOUBLE, """\"abc$empty$x$y\"""")
    m = {
        'x': '29',
        'y': '42'
    }
    check(t, m, 'abc2942')


def test_3():
    t = Token(TokenType.SINGLE, """\'123$x$y$z\'""")
    m = {
        'x': '29',
        'y': '42',
        'z': '61',
    }
    check(t, m, '123$x$y$z')
