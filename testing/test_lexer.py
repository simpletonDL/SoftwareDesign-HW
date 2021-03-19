from typing import List

from src.lexer.lexer import SimpleLexer
from src.lexer.rules import Token, TokenType


def list_to_str(xs: List):
    return [str(s) for s in xs]


def check(s: str, expected: List[Token]):
    a, b = list_to_str(SimpleLexer().split(s)), list_to_str(expected)
    assert a == b


def test_1():
    expected = [Token(TokenType.VAR_DEF, "x=5")]
    assert SimpleLexer().split("""x=5""") == expected


def test_2():
    cmd = """  echo  "123"  x """
    expected = [
        Token(TokenType.STR, 'echo'),
        Token(TokenType.DOUBLE, '"123"'),
        Token(TokenType.STR, 'x')
    ]
    check(cmd, expected)


def test_3():
    cmd = """ cat ' 123  ' x | echo """
    expected = [
        Token(TokenType.STR, 'cat'),
        Token(TokenType.SINGLE, "' 123  '"),
        Token(TokenType.STR, 'x'),
        Token(TokenType.PIPE, '|'),
        Token(TokenType.STR, 'echo')
    ]
    check(cmd, expected)
