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


class TestProject(TestCase):

  def setUp(self):
    fakeTpl = tests.fakeTemplates.FakeTemplates(PATH_TO_PROJUP + '/templates')
    self.setUpPyfakefs()
    fakeTpl.copyContentToVirtualFS()

    self.execPath = '/test'
    self.fs.create_dir(self.execPath)

  def test_itShouldGenerateAnApacheLicenseFile(self):
    data = ModuleData()
    data.technicalTitle = 'testing'
    data.projectTitle = 'Test Project'
    data.projectDescription = 'This is a test project'
    data.version = '1.0.0'
    data.author = 'Testa'
    data.year = 2018
    data.license = 'MIT'

    project = projup.modules.Project(
      PATH_TO_PROJUP,
      self.execPath,
    )
    project.process(data)

    self.assertTrue(os.path.exists(self.execPath + '/testing'))
    self.assertTrue(os.path.exists(self.execPath + '/testing/README.md'))

    readmeFile = open(self.execPath + '/testing/README.md', 'r')
    readme = readmeFile.read()
    readmeFile.close()

    self.assertTrue('# Test Project' in readme)
    self.assertTrue('[License: MIT]' in readme)
    self.assertTrue('[Version: 1.0.0]' in readme)
    self.assertTrue(data.projectDescription in readme)
