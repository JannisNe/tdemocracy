[![Release](https://img.shields.io/github/v/release/JannisNe/tdemocracy)](https://img.shields.io/github/v/release/JannisNe/tdemocracy)
[![Build status](https://img.shields.io/github/actions/workflow/status/JannisNe/tdemocracy/main.yml?branch=main)](https://github.com/JannisNe/tdemocracy/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/JannisNe/tdemocracy/branch/main/graph/badge.svg)](https://codecov.io/gh/JannisNe/tdemocracy)
[![Commit activity](https://img.shields.io/github/commit-activity/m/JannisNe/tdemocracy)](https://img.shields.io/github/commit-activity/m/JannisNe/tdemocracy)
[![License](https://img.shields.io/github/license/JannisNe/tdemocracy)](https://img.shields.io/github/license/JannisNe/tdemocracy)
[![Deploy Docs](https://github.com/JannisNe/tdemocracy/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/JannisNe/tdemocracy/actions/workflows/deploy-docs.yml)

# Listen to TDEmocracy!

This repository contains the data model used in the stream of candidate nuclear transients for the TDEmocracy project.

## Prerequisites

You need an account at the [SCIMMA Hopskotch service](https://scimma.org/hopskotch). Please contact the TDEmocracy lead to have your account added to the Ampel-TDEmocracy group. You can store your username and password in your environment variables `TDEMOCRACY_USERNAME` and `TDEMOCRACY_PASSWORD` or in a `.env` file in the root of the repository.

## Installation

Pull the repository and install the dependencies with [`poetry`](https://python-poetry.org/):

```bash
git clone https://github.com/JannisNe/tdemocracy.git
cd tdemocracy
poetry install
```

In the future, you will be able to install the package via `pip`:

```bash
pip install tdemocracy
```

## Usage:

```python
from tdemocracy.listen import listen_to_nuclear_stream

for report in listen_to_nuclear_stream():
    # do something with the report
    ...
```

The report is an instance of `tdemocracy.model.LSSTReport`. There you can find more documentation on the contents.

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
