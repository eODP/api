# eODP API

Flask app fot the eODP API.

## Setup

We are using Python 3.6.8 on the production server.

For the dev environment, we are using [pyenv](https://github.com/pyenv/pyenv) to run Python 3.6.8, and [Poetry](https://python-poetry.org) to manage packages and virtual environments.

(1) Install pyenv and Poetry.

(2) Start virtual environment
```bash
poetry shell
```

(3) Install packages.

```bash
poetry install
```

(4) Config .env file

Copy `.env-example` and rename it `.env`.

Fill in the missing environmental variables.

## Run App

Start Flask app. The app is set to run in debug mode for development.

```bash
python eodp_api/app.py
```

## Testing

Run tests

```bash
poetry run pytest
```

Run linter (flake8) and code formatter(Black).

```bash
poetry run lint
```
