language: python
python:
  - "3.4"
  - "3.5"
  - "3.6"
  - "pypy3.5"
install:
  - pip install pipenv
  - pipenv sync --dev --system

script:
  - python test.py
  - yapf --diff --recursive . || exit;
