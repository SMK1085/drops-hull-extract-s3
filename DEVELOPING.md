# Developing Guidelines

## Virtualenv

This project uses [Virtualenv](http://www.virtualenv.org/) to create an isolated development environment. This ensures a consistent development experience. Please do not inherit globally installed packages.

### Installation

To install `virtualenv` run:

``` bash
pip install virtualenv
```

### Usage

Initialize `virtualenv` by running in the project root folder:

```bash
virtualenv venv
```

These commands create a `venv/` directory in the project where all dependencies are installed. You need to **activate** it first though (in every terminal instance where you are working on your project):

```bash
source venv/bin/activate
```

You should see a `(venv)` appear at the beginning of your terminal prompt indicating that you are working inside the `virtualenv`.

To leave the virtual environment run:

```bash
deactivate
```

### Dependencies

The project currently has the following dependencies which should be installed in `venv`:

```bash
pip install boto3
pip install requests
pip install moto
pip install pytest
pip install python-dotenv
pip install pylint
pip install coverage
```

## Testing

Collect coverage and run test suites

```bash
coverage run --source=src -m pytest -vv -s tests/
```

Generate HTML report for coverage

```bash
coverage html
```
