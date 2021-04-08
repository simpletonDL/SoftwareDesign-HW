from termcolor import colored

from src.commands.basic_commands import *
from src.commands.builtin_commands import *
from src.commands.command_api import ICommand
from src.enviroment.enviroment import Environment
from testing.common import *


def check(cmd: ICommand, args: List[str], inp: str, expected: str):
    output_stream = exec_command(cmd, args, inp)
    print(output_stream.getvalue())
    assert output_stream.getvalue() == expected


def exec_command(cmd: ICommand, args: List[str], inp: str):
    inp_stream = io.StringIO(inp)
    output_stream = io.StringIO()
    err_stream = io.StringIO()
    env = Environment()
    cmd.run(args, inp_stream, output_stream, err_stream, env)
    return output_stream


def test_echo1():
    echo = EchoCommand()
    check(echo, ['123', '456'], '', '123 456\n')


def test_echo2():
    echo = EchoCommand()
    check(echo, [], '', '\n')


def test_cat3():
    path = test_input / 'file_1.txt'
    cat = CatCommand()
    with open(path, 'r') as f:
        expected = f.read()
    check(cat, [str(path)], '', expected)


def test_echo_pipe_cat():
    echo = EchoCommand()
    cat = CatCommand()
    pipe = PipeAggregationCommand(echo, ['hello'], cat, [])

    check(pipe, [], '', 'hello\n')


def test_ls1():
    ls = LsCommand()
    dir_content = ['.pylintrc', colored('testing', 'blue'), colored('.git', 'blue'),
                   'architecture_review.md', 'bash.py', colored('.pytest_cache', 'blue'),
                   colored('__pycache__', 'blue'), 'README.md', 'Makefile', 'conftest.py',
                   colored('src', 'blue'), colored('.idea', 'blue'), colored('.github', 'blue')]
    check(ls, [], '', '\n'.join(dir_content) + '\n')


def test_ls2():
    ls = LsCommand()
    dir_content = [colored('parser', 'blue'), colored('bash_runner', 'blue'),
                   colored('commands', 'blue'), colored('interpreter', 'blue'),
                   colored('expander', 'blue'), 'requirements.txt', colored('enviroment', 'blue'),
                   colored('exceptions', 'blue'), colored('lexer', 'blue')]
    check(ls, ['src'], '', '\n'.join(dir_content) + '\n')


def test_ls3():
    ls = LsCommand()
    check(ls, ['testing/test_input/file_1.txt'], '', 'file_1.txt\n')


def test_ls4():
    ls = LsCommand()
    try:
        exec_command(ls, ['file3.txt'], '')
        assert False
    except InterpreterException:
        assert True


def test_echo_pipe_ls():
    echo = EchoCommand()
    ls = LsCommand()
    pipe = PipeAggregationCommand(echo, ['src/enviroment'], ls, [])
    dir_content = ['.pylintrc', colored('testing', 'blue'), colored('.git', 'blue'),
                   'architecture_review.md', 'bash.py', colored('.pytest_cache', 'blue'),
                   colored('__pycache__', 'blue'), 'README.md', 'Makefile', 'conftest.py',
                   colored('src', 'blue'), colored('.idea', 'blue'), colored('.github', 'blue')]
    check(pipe, [], '', '\n'.join(dir_content) + '\n')


def test_cd1():
    cd = CdCommand()
    pwd = PwdCommand()
    exec_command(cd, ['src/commands'], '')
    check(pwd, [], '', '/home/user/Desktop/SoftwareDesign-HW/src/commands\n')


def test_cd2():
    cd = CdCommand()
    pwd = PwdCommand()
    exec_command(cd, ['..'], '')
    check(pwd, [], '', '/home/user/Desktop/SoftwareDesign-HW/src\n')


def test_cd3():
    cd = CdCommand()
    try:
        exec_command(cd, ['bash_runner_incorrect_directory'], '')
        assert False
    except InterpreterException:
        assert True


def test_cd4():
    cd = CdCommand()
    pwd = PwdCommand()
    exec_command(cd, [], '')
    check(pwd, [], '', f'{Path.home()}\n')
