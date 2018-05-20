# projup

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version: 0.2.0](https://img.shields.io/badge/Version-0.2.0-brightgreen.svg)](https://semver.org/)
[![Build Status](https://travis-ci.org/progsource/projup.svg?branch=master)](https://travis-ci.org/progsource/projup)

projup is a project setup tool written in python. It will generate typical
files and folders for you, after you entered the project configuration.
You can easily modify it to fit your needs.

## goals

* easy & fast project setup
* easy to modify
* easy to setup itself

## how to run with python (pipenv)

projup requires python 3.4+ and pipenv

1. If you do not have python installed yet, install it.
2. If you do not have pipenv installed yet, run `pip install pipenv`
3. Clone the repository
4. Run `pipenv sync` in the projup folder
5. Go to a folder, in which you want to create your projects and run
  `pipenv run python path/to/projup/app.py`
  *Do not run it inside of a pipenv enviroment if you want to set up a python
  project, else the pipenv commands will be executed on the wrong project.*

### how to run tests

1. Setup with `pipenv sync --dev`
2. Run `pipenv run python test.py` in the projup folder

## how it works

projup takes your input and puts that on some templates. Those you can find in
the `templates` folder. You can change them to fit your needs.

### default config

To not have to type your name and email again and again on one system, you can
instead create a projup config file in your home directory with the following
content: (`~/.projup `)

```toml
author = "My Name"
email = "info@example.com"
```

## how to contribute

* [Create a GitHub issue](https://github.com/progsource/projup/issues/new)
* Create a pull request with an own branch
  * Add yourself to the AUTHORS file.
  * Run `pipenv sync --dev` if you didn't do it yet.
  * Make sure, that you run `pipenv run yapf -i -r *.py` before you commit.

## alternatives

* [cookiecutter](https://github.com/audreyr/cookiecutter)
