# This project is licensed under the MIT license. For more information
# see the LICENSE file.

import os
import unittest
from unittest import mock

# ------------------------------------------------------------------------------

from pyfakefs.fake_filesystem_unittest import TestCase
from pyfakefs.fake_filesystem_unittest import Patcher

# ------------------------------------------------------------------------------

import tests.fakeTemplates

# ------------------------------------------------------------------------------

import projup
from projup.modules.module import ModuleData

# ------------------------------------------------------------------------------

PATH_TO_PROJUP = os.path.dirname(os.path.realpath(__file__ + '/..'))

# ------------------------------------------------------------------------------


class TestCI(TestCase):

  def setUp(self):
    fakeTpl = tests.fakeTemplates.FakeTemplates(PATH_TO_PROJUP + '/templates')
    self.setUpPyfakefs()
    fakeTpl.copyContentToVirtualFS()

    self.execPath = '/test'
    self.fs.create_dir(self.execPath)
    self.fs.create_dir(self.execPath + '/testing')

    self.travisFilePath = self.execPath + '/testing/.travis.yml'

    self.ci = projup.modules.ContinousIntegration(
      PATH_TO_PROJUP,
      self.execPath,
    )

    self.data = ModuleData()
    self.data.technicalTitle = 'testing'
    self.data.author = 'Testa'
    self.data.year = 2018
    self.data.license = 'MIT'

  def test_itShouldGenerateCppTravisFile(self):
    self.data.codeLanguages.append('cpp')

    self.ci.process(self.data)

    self.assertTrue(os.path.exists(self.travisFilePath))

    travisFile = open(self.travisFilePath, 'r')
    travisConfig = travisFile.read()
    travisFile.close()

    self.assertTrue('language: cpp' in travisConfig)
    self.assertTrue('- ../build/testingTests' in travisConfig)

  def test_itShouldGeneratePythonTravisFile(self):
    self.data.codeLanguages.append('python')

    self.ci.process(self.data)

    self.assertTrue(os.path.exists(self.travisFilePath))

    travisFile = open(self.travisFilePath, 'r')
    travisConfig = travisFile.read()
    travisFile.close()

    self.assertTrue('language: python' in travisConfig)
