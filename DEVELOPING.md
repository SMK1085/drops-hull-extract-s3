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

## Git Flow

This project follows [Vincent Driessen's branching model](https://nvie.com/posts/a-successful-git-branching-model/) and uses Git Flow.
Please make sure that you understand the model and commit to the proper branch.
If you have any questions, [open a ticket](https://github.com/SMK1085/drops-hull-extract-s3/issues/new) and discuss it with the maintainers.

## Terraform

DROPS are built by providing examples for Terraform. This ensures that scenarios are almost instantly deployable to AWS with a few tweaks in the variables. If you want to add a new scenario, please make sure to follow the steps below:

1. [Open a ticket](https://github.com/SMK1085/drops-hull-extract-s3/issues/new) to discuss the new scenario.
2. Create a new folder with the scenario slug under `tf/examples/`
3. Make sure that you have some best practice code splitting in Terraform files. If you are unsure, please ask in the ticket.
4. Test your Terraform code and make sure that it actually works.

**Important**: All Terraform code needs to target version 0.12 or higher. If you submit code targeting an older version, the PR will be rejected.
