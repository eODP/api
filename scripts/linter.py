import subprocess
import sys


def lint():
    command = "black ./app"
    process = subprocess.Popen(command.split())
    output, error = process.communicate()

    command = "black ./tests"
    process = subprocess.Popen(command.split())
    output, error = process.communicate()

    command = "flake8 ./app"
    process = subprocess.Popen(command.split())
    output, error = process.communicate()


if __name__ == "__main__":
    lint()
