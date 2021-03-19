"""
Модуль для окружения.
Окружает только словарь.
"""


class Environment:
    def __init__(self):
        self._vars = {}

    @property
    def vars(self):
        return self._vars
