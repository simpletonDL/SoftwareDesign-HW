"""
Модуль с интерпретатором для баша
"""

from typing import IO

from src.commands.basic_commands import WcCommand, GrepCommand
from src.commands.basic_commands import EchoCommand, CatCommand, PwdCommand
from src.interpreter.base_interpreter import BaseInterpreter
from src.lexer.lexer import SimpleLexer
from src.parser.simple_parser import SimpleParser


class BashInterpreter(BaseInterpreter):
    """
    Данный интерпретатор баша является наследником
    базого интрпретатора, и просто регистриует набор
    утилит.
    """
    _registered_commands = [
        EchoCommand,
        CatCommand,
        PwdCommand,
        WcCommand,
        GrepCommand
    ]

    def __init__(self, inp: IO, out: IO, err: IO):
        super().__init__(inp, out, err, SimpleLexer(), SimpleParser())

        for cmd in BashInterpreter._registered_commands:
            self.register_cmd(cmd())
