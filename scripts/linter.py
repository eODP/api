import subprocess


def lint():
    _exec("black ./app")
    _exec("black ./scripts")
    _exec("black ./tests")
    _exec("flake8 ./app")
    _exec("flake8 ./scripts")
    _exec("flake8 ./tests")


def _exec(command):
    process = subprocess.Popen(command.split())
    output, error = process.communicate()


if __name__ == "__main__":
    lint()
