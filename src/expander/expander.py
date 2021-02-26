import re
from typing import Dict, Match

from src.lexer.rules import *
from src.parser.parser_api import *


class Expander:
    @staticmethod
    def _substitute(s: str, mapper: Dict[str, str]) -> str:
        def replace(x: Match[str]) -> str:
            var_name = x.group(1)
            var_value = mapper.get(var_name, '')
            return var_value

        return re.sub(r'\$(\w+)', replace, s)

    @staticmethod
    def substitute(t: Token, mapper: Dict[str, str]) -> str:
        if t.kind == TokenType.SINGLE:
            return t.string[1:-1]
        if t.kind == TokenType.DOUBLE:
            return Expander._substitute(t.string[1:-1], mapper)
        if t.kind == TokenType.STR:
            return Expander._substitute(t.string, mapper)

        raise RuntimeError(f'Unsupported token kind: {t.kind}')

    @staticmethod
    def substitute_utility(cmd_info: CommandInfo[Token], mapper: Dict[str, str]) -> CommandInfo[str]:
        # TODO: mapper
        return CommandInfo(
            Expander.substitute(cmd_info.name, mapper),
            [Expander.substitute(x, mapper) for x in cmd_info.args]
        )

    @staticmethod
    def substitute_pipe(pipe_info: PipeInfo[Token], mapper: Dict[str, str]) -> PipeInfo[str]:
        return PipeInfo(
            [Expander.substitute_utility(x, mapper) for x in pipe_info.utils]
        )
