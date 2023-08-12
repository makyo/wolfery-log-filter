# Wolfery Log Filter

Filters lines from Wolfery logs by setting `display: none` using a config file.

## Usage

Requires [poetry](https://github.com/python-poetry/poetry)

Install the dependencies:

    poetry install

Run the command with the config file and log:

    poetry run wolfery_log_filter/__init__.py config.yaml log.html

You can output the results to an output HTML file. Statistics are printed to STDERR.
