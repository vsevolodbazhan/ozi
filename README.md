# Ozi

[![Build Status](https://travis-ci.com/vsevolodbazhan/ozi.svg?branch=master)](https://travis-ci.com/vsevolodbazhan/ozi)
[![codecov](https://codecov.io/gh/vsevolodbazhan/ozi/branch/master/graph/badge.svg)](https://codecov.io/gh/vsevolodbazhan/ozi)
[![CodeFactor](https://www.codefactor.io/repository/github/vsevolodbazhan/ozi/badge)](https://www.codefactor.io/repository/github/vsevolodbazhan/ozi)
[![Requirements Status](https://requires.io/github/vsevolodbazhan/ozi/requirements.svg?branch=master)](https://requires.io/github/vsevolodbazhan/ozi/requirements/?branch=master)

Mailings management microservice for [Tomoru](https://tomoru.ru).

## Installation

Install dependencies using [pip](https://pip.pypa.io/en/stable/):

```bash
pip install -r requirements.txt
```

or [Poetry](https://python-poetry.org):

```bash
poetry install
```

Poetry will install dev-dependencies as well. So use that if you are planning to contribute.

## Setup

1. `SECRET_KEY`. You might want to use something like [Djecrety](https://djecrety.ir) or Python's `secrets` module to generate a secret key.
2. `DEBUG`. A boolean value. Defaults to `False`.

## Usage

Run the server:

```bash
gunicorn config.wsgi
```

and run task processing:

```bash
python manage.py process_tasks
```

You might want to activate shell first with:

```bash
poetry shell
```

## Tests

Run tests using `pytest`:

```
pytest --cov=.
```

## Notes

Note that for the build to be successful it has to have no `flake8` errors and have >= 90% test coverage.

## License

[GNU GPLv3](https://github.com/vsevolodbazhan/ozi/blob/master/COPYING)
