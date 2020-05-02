# eODP API

Flask app fot the eODP API.

## Setup

We are using Python 3.6.8 on the production server.

For the dev environment, we are using [pyenv](https://github.com/pyenv/pyenv) to run Python 3.6.8, pip to manage packages, and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) to manage virtual environments.

(1) Install pyenv, pyenv-virtualenv

(2) Install Python 3.6.8

```bash
pyenv install 3.6.8
```

set this directory to use Python 3.6.8

```bash
pyenv local 3.6.8
```

(3) Start virtual environment

create virtual environment

```bash
pyenv virtualenv 3.6.8 <venv-name>
```

set this directory to use `<venv-name>` virtual environment

```bash
pyenv local <venv-name>
```

(4) Install packages.

```bash
pip install -r requirements.txt
```

(5) Config .env file

Copy `.env-example` and rename it `.env`.

Fill in the missing environmental variables.

(6) Install additional packages

```bash
pip install <package>

pip freeze > requirements.txt
```

(7) Database migrations

We are using [flask-migrate](https://github.com/miguelgrinberg/Flask-Migrate) to handle SQLAchemy migrations.

Make `flask` available to the command line.

```bash
export FLASK_APP=app/app.py
```

Migration commands.

```bash
# create migration
flask db migrate -m 'name of migration'

# run migration
flask db upgrade
```

**NOTE:** Running flask from the command using Python 3.6 might result in an [ASCII encoding error with Click](https://click.palletsprojects.com/en/5.x/python3/#python-3-surrogate-handling).

You can try:

```bash
# option 1
export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8

# option 2
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# option 3
unset LC_ALL
```

## Run App

Start Flask app. The app is set to run in debug mode for development.

```bash
python app/app.py
```

## Testing

Run tests

```bash
pytest
```

Run linter (flake8) and code formatter (Black).

```bash
python scripts/linter.py
```
