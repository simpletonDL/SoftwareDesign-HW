"""
Модуль с реализацией базого интерпретатора.
"""

from functools import reduce
from typing import Dict, IO, List

from src.commands.builtin_commands import SetVarCommand, ListVarsCommand
from src.commands.builtin_commands import ExitCommand, ExternalCommand
from src.commands.builtin_commands import PipeAggregationCommand
from src.commands.command_api import ICommand, IBasicCommand
from src.enviroment.enviroment import Environment
from src.expander.expander import Expander
from src.lexer.lexer import ILexer
from src.parser.parser_api import CommandInfo, IParser


class BaseInterpreter:
    """
    Базовый интерпретатор. Реализует основной движок
    запуска команд. Предоставляет дефолтные команды
    и механизм регистрации новых команд.
    """
    _registered_cmds = [
        SetVarCommand,
        ListVarsCommand,
        ExitCommand
    ]

    def __init__(self, inp: IO, out: IO, err: IO, lexer: ILexer, parser: IParser):
        """
        Конструктор, который фиксирует потоки, с которыми
        будет работать интерпретатор (не обязательно sys.stdin/...)
        :param inp: Поток ввода (например, StringIO)
        :param out: Поток вывода
        :param err: Поток ошибок
        """
        self.inp = inp
        self.out = out
        self.err = err

        self.lexer = lexer
        self.parser = parser

        self._cmds: Dict[str, IBasicCommand] = {
            cmd.get_name(): cmd
            for cmd in [cmdType() for cmdType in BaseInterpreter._registered_cmds]
        }
        self._env = Environment()

    def register_cmd(self, cmd: IBasicCommand):
        name = cmd.get_name()
        self._cmds[name] = cmd

    def _run_cmd(self, cmd: ICommand, args: List[str]) -> int:
        return cmd.run(args, self.inp, self.out, self.err, self._env)

    def _get_cmd(self, name: str) -> ICommand:
        if name in self._cmds:
            return self._cmds[name]
        return ExternalCommand(name)

    def _make_pipe(self, acc: PipeAggregationCommand, cmd_info: CommandInfo[str]):
        cmd = self._get_cmd(cmd_info.name)
        return PipeAggregationCommand(acc, [], cmd, cmd_info.args)

    def execute_cmd_line(self, cmd_line: str) -> int:
        """
        Основной метод, который выполняет одну командную
        строку. Работает примерно в таком порядке:
        Лексер -> Парсер -> Подстановка переменных ->
        Поиск команд -> Собирание пайплайнов -> Запуск
        :param cmd_line:
        :return:
        """
        tokens = self.lexer.split(cmd_line)
        pipe_token_info = self.parser.parse(tokens)
        pipe_str_info = Expander.substitute_pipe(pipe_token_info, self._env.vars)
        cmd_infos = pipe_str_info.utils

        if len(cmd_infos) > 1:
            ini = PipeAggregationCommand(
                    self._get_cmd(cmd_infos[0].name),
                    cmd_infos[0].args,
                    self._get_cmd(cmd_infos[1].name),
                    cmd_infos[1].args
                  )
            cmd = reduce(self._make_pipe, cmd_infos[2:], ini)
            return self._run_cmd(cmd, [])
        if len(cmd_infos) == 1:
            cmd_info = cmd_infos[0]
            cmd = self._get_cmd(cmd_info.name)
            return self._run_cmd(cmd, cmd_info.args)
        return 0
