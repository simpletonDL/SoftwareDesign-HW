from subprocess import Popen, PIPE
from typing import List

import pytest
from termcolor import colored

from testing.common import *


@pytest.fixture
def bash_subprocess():
    return Popen(f'python3 {root_dir / "bash.py"}',
                 shell=True,
                 stdin=PIPE,
                 stderr=PIPE,
                 stdout=PIPE,
                 encoding='utf8')


@pytest.fixture
def check(bash_subprocess):
    def check(inp: List[str], expected_out, expected_err):
        out, err = bash_subprocess.communicate('\n'.join(inp))
        out, err = (x.strip('\n').split('\n') if x else []
                    for x in (out, err))
        assert out == expected_out
        assert err == expected_err

    return check


def test_1(check):
    check(
        [
            'echo 123',
            'cat',
            'Some text here',
            'another line of text',
        ],
        [
            '123',
            'Some text here',
            'another line of text'
        ],
        []
    )


def test_2(check):
    check(
        [
            'echo how many cats? | cat | cat | cat | cat',
        ],
        [
            'how many cats?'
        ],
        []
    )


def test_vars(check):
    check(
        [
            'x="nt"',
            'y=" wa"',
            "z=eep",
            'a=I',
            'b="sl"',
            'echo "$a$y$x to $b$z"'
        ],
        ['I want to sleep'],
        []
    )


def test_grep_1(check):
    check(
        [
            f'cat {test_input / "file_2.txt"} | grep "Я сижу"'
        ],
        [
            f'{colored("Я сижу", "red")} у окна. За окном осина.',
            f'{colored("Я сижу", "red")} у окна. Я помыл посуду.',
            f'{colored("Я сижу", "red")} у окна. Вспоминаю юность.',
            f'{colored("Я сижу", "red")} у окна, обхватив колени,',
            f'{colored("Я сижу", "red")} у окна в темноте; как скорый,',
            f'{colored("Я сижу", "red")} в темноте. И она не хуже'
        ],
        []
    )


def test_grep_2(check):
    check(
        [
            "reg=,.+,",
            f'cat {test_input / "file_2.txt"} | grep $reg -A 2',
        ],
        [
            f'Что готический стиль победит{colored(", как школа,", "red")}',
            f'как способность торчать, избежав укола.',
            f'Я сижу у окна. За окном осина.',
            f'{colored("--", "blue")}',
            f'Что{colored(", устав от поднятой веком пыли,", "red")}',
            f'русский глаз отдохнет на эстонском шпиле.',
            f'Я сижу у окна. Я помыл посуду.',
            f'{colored("--", "blue")}',
            f'Что любовь{colored(", как акт,", "red")} лишена глагола.',
            f'Что не знал Эвклид{colored(", что, сходя на конус,", "red")}',
            f'вещь обретает не ноль, но Хронос.',
            f'Я сижу у окна. Вспоминаю юность.',
            f'{colored("--", "blue")}',
            f'И что семя{colored(", упавши в дурную почву,", "red")}',
            f'не дает побега; что луг с поляной',
            f'есть пример рукоблудья, в Природе данный.',
            f'{colored("--", "blue")}',
            f'Я сижу у окна{colored(", обхватив колени,", "red")}',
            f'в обществе собственной грузной тени.',
        ],
        [],
    )


def test_wc(check):
    check(
        [
            f'cat {test_input / "file_1.txt"} | wc'
        ],
        [
            '3 4 18'
        ],
        []
    )
