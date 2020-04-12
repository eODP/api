import subprocess


def lint():
    command = "poetry run black ./eodp_api"
    process = subprocess.Popen(command.split())
    output, error = process.communicate()

    command = "poetry run black ./tests"
    process = subprocess.Popen(command.split())
    output, error = process.communicate()

    command = "poetry run flake8 ./eodp_api"
    process = subprocess.Popen(command.split())
    output, error = process.communicate()
