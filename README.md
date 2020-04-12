# eODP API

Flask app fot the eODP API.

## Setup

We are using Python 3.6.8 on the production server.

For the dev environment, we are using [pyenv](https://github.com/pyenv/pyenv) to run Python 3.6.8, pip to manage packages, and Python venv to manage virtual environments.

(1) Install pyenv

(2) Start virtual environment

create virtual environment

```bash
python -m venv venv
```
start virtual environment

```bash
source venv/bin/activate
```

(3) Install packages.

```bash
pip install -r requirements.txt
```

(4) Config .env file

Copy `.env-example` and rename it `.env`.

Fill in the missing environmental variables.

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
