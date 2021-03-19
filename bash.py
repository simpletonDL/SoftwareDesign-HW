import sys

from src.bash_runner.runner import BashRunner
from src.interpreter.bash import BashInterpreter

interpreter = BashRunner(BashInterpreter(sys.stdin, sys.stdout, sys.stderr))
sys.exit(interpreter.run())
