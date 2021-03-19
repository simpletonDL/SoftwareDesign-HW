"""
Модуль с встроенными командами, которые содержаться
в интерпретаторе по дефолту.
"""

import io
import subprocess
from typing import List

from src.commands.command_api import IBasicCommand
from src.commands.command_api import ICommand
from src.exceptions.exceptions import ExitInterpreter


class BuiltInCmdNames:
    SetVar = 'SetVar'
    ListVars = 'printenv'
    Exit = 'exit'


class SetVarCommand(IBasicCommand):
    def get_name(self) -> str:
        return BuiltInCmdNames.SetVar

    def run(self, args, inp, out, err, env) -> int:
        name, value = args
        env.vars[name] = value
        return 0


class ListVarsCommand(IBasicCommand):
    def get_name(self) -> str:
        return BuiltInCmdNames.ListVars

    def run(self, args, inp, out, err, env) -> int:
        print('\n'.join([f'{k}={v}' for k, v in env.vars.items()]),
              file=out)
        return 0


class ExitCommand(IBasicCommand):
    def get_name(self) -> str:
        return BuiltInCmdNames.Exit

    def run(self, args, inp, out, err, env) -> int:
        raise ExitInterpreter('By-by!')


class PipeAggregationCommand(ICommand):
    def __init__(self, cmd_1: ICommand, args_1: List[str],
                 cmd_2: ICommand, args_2: List[str]):
        self.cmd_1 = cmd_1
        self.cmd_2 = cmd_2
        self.args_1 = args_1
        self.args_2 = args_2

    def run(self, args, inp, out, err, env):
        if len(args) != 0:
            raise RuntimeError('PipeAggregation expected 0 arguments')

        out_cmd_1 = io.StringIO()
        ret = self.cmd_1.run(self.args_1, inp, out_cmd_1, err, env)

        if ret != 0:
            return ret

        inp_cmd_2 = io.StringIO(out_cmd_1.getvalue())
        return self.cmd_2.run(self.args_2, inp_cmd_2, out, err, env)


class ExternalCommand(ICommand):
    def __init__(self, name):
        self._name = name

    def run(self, args, inp, out, err, env) -> int:
        if isinstance(inp, io.StringIO):
            proc_inp = subprocess.PIPE
            communicate_args = [inp.getvalue()]
        else:
            proc_inp = inp
            communicate_args = []

        proc = subprocess.Popen(" ".join([self._name, *args]),
                                stdin=proc_inp,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding='utf8',
                                shell=True)

        s_out, s_err = proc.communicate(*communicate_args)
        out.write(s_out)
        err.write(s_err)
        return proc.poll()
