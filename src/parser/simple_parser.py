"""
Реализация парсера
"""

from itertools import groupby
from typing import List

from src.commands.builtin_commands import BuiltInCmdNames
from src.exceptions.exceptions import ParseError
from src.lexer.lexer import Token
from src.lexer.rules import TokenType
from src.parser.parser_api import IParser, PipeInfo, CommandInfo


class SimpleParser(IParser):
    """
    Класс, реализующий парсер.
    """

    def parse(self, tokens: List[Token]) -> PipeInfo[Token]:
        """
        Принимает список токенов, разобраный результат.
        Пока просто идёт разделение по пайпам, и то, что
        оказалось внутри пайпов, считается базовой командой.
        :param tokens:
        :return:
        """
        if len(tokens) == 1 and tokens[0].kind == TokenType.VAR_DEF:
            token = tokens[0]
            var_name, value = [arg.strip() for arg in token.string.split("=")]
            cmd_name = Token(TokenType.STR, BuiltInCmdNames.SetVar)
            arg1 = Token(TokenType.STR, var_name)
            arg2 = Token(TokenType.STR, value.strip('\"').strip('\''))
            return PipeInfo([CommandInfo(cmd_name, [arg1, arg2])])

        if TokenType.VAR_DEF in [t.kind for t in tokens]:
            raise ParseError("Var definition must be the only command")

        split_tokens = [list(y) for x, y in groupby(tokens, lambda z: z.kind == TokenType.PIPE)
                        if not x]
        cmds = [CommandInfo(tokens[0], tokens[1:]) for tokens in split_tokens]
        return PipeInfo(cmds)
