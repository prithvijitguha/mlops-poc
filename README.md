# MLOps Proof of Concept (POC)

This repository contains a Proof of Concept (POC) for a self-service reporting assistant using MLOps principles. The assistant leverages the OpenAI API to provide an interactive and user-friendly interface for generating reports.


[![codecov](https://codecov.io/gh/prithvijitguha/mlops-poc/graph/badge.svg?token=HFNPEOC9NS)](https://codecov.io/gh/prithvijitguha/mlops-poc)&nbsp;
![build and test](https://github.com/prithvijitguha/mlops-poc/actions/workflows/build.yml/badge.svg?branch=main)&nbsp;
![documentation](https://readthedocs.org/projects/mlops-poc/badge/?version=latest)&nbsp;
[![Documentation Status](https://readthedocs.org/projects/mlops/badge/?version=latest)](https://flowrunner.readthedocs.io/en/latest/?badge=latest)&nbsp;
[![Python 3.11](https://img.shields.io/badge/python-3.11-%2334D058.svg)](https://www.python.org/downloads/release/python-390/)&nbsp;
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)&nbsp;
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)&nbsp;
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

# Demo Screenshot:

![Hei Screenshot](docs/source/static/hei_screenshot.png)

## Technical Documentation

For more detailed information about the project, please refer to our [technical documentation on ReadTheDocs](https://mlops-poc.readthedocs.io/en/latest/).

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip

### Installation

You can install the necessary dependencies by running one of the following commands:

```shell
pip install .[dev] .
```
## Instructions to run:
```shell
pip install .[dev] .
```
OR

```shell
pip install -r requirements-dev.txt -r requirements.txt -r requirements-docs.txt

```

### Configuration

Create a .env file in the root directory of the project and add your OpenAI API Key:

Your file contents should look like

```yaml
# environment variables defined inside a .env file
OPENAI_API_KEY=my-open-ai-api-key
```

Replace my-open-ai-api-key with your actual OpenAI API key.

### Running the application

After installing the dependencies and setting up the configuration, you can run the application with the following command:
```shell
streamlit run src/web/app.py
```

Some reference reading:
- [open-ai-documentation](https://platform.openai.com/docs/introduction)
- [openai-python](https://github.com/openai/openai-python/tree/main)
- [open-ai-cookbook](https://github.com/openai/openai-cookbook/tree/main)
