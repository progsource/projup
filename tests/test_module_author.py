# This project is licensed under the MIT license. For more information
# see the LICENSE file.

import os
import unittest
from unittest import mock

# ------------------------------------------------------------------------------

from pyfakefs.fake_filesystem_unittest import TestCase

# ------------------------------------------------------------------------------

import tests.fakeTemplates

# ------------------------------------------------------------------------------

import projup
from projup.modules.module import ModuleData

# ------------------------------------------------------------------------------

PATH_TO_PROJUP = os.path.dirname(os.path.realpath(__file__ + '/..'))

# ------------------------------------------------------------------------------


class TestAuthor(TestCase):

  def setUp(self):
    fakeTpl = tests.fakeTemplates.FakeTemplates(PATH_TO_PROJUP + '/templates')
    self.setUpPyfakefs()
    fakeTpl.copyContentToVirtualFS()

    self.execPath = '/test'
    self.fs.create_dir(self.execPath)
    self.fs.create_dir(self.execPath + '/testing')
    self.authorsPath = self.execPath + '/testing/AUTHORS'

    self.author = projup.modules.Author(
      PATH_TO_PROJUP,
      self.execPath,
    )

    self.data = ModuleData()
    self.data.technicalTitle = 'testing'

  def test_itShouldGenerateAnAuthorsFile(self):
    self.data.author = 'Testa'
    self.data.email = 'info@example.com'

    self.author.process(self.data)

    self.assertTrue(os.path.exists(self.authorsPath))

    authorsFile = open(self.authorsPath, 'r')
    authorsData = authorsFile.read()
    authorsFile.close()

    self.assertTrue('Testa (info@example.com)' in authorsData)
