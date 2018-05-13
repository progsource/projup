# This project is licensed under the {license} license. For more information
# see the LICENSE file.

import os
import unittest

import colour_runner.runner

import tests


def suite():
  suite = unittest.TestSuite()
  loader = unittest.TestLoader()

  suite.addTests(loader.loadTestsFromModule(tests))

  return suite


if __name__ == '__main__':
  runner = colour_runner.runner.ColourTextTestRunner(verbosity = 1)
  runner.run(suite())
