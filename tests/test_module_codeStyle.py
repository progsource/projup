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


class TestCodeStyle(TestCase):

  def setUp(self):
    fakeTpl = tests.fakeTemplates.FakeTemplates(PATH_TO_PROJUP + '/templates')
    self.setUpPyfakefs()
    fakeTpl.copyContentToVirtualFS()

    self.execPath = '/test'
    self.fs.create_dir(self.execPath)
    self.fs.create_dir(self.execPath + '/testing')

    self.editorConfigPath = self.execPath + '/testing/.editorconfig'

    self.codeStyle = projup.modules.CodeStyle(
      PATH_TO_PROJUP,
      self.execPath,
    )

    self.data = ModuleData()
    self.data.technicalTitle = 'testing'
    self.data.author = 'Testa'
    self.data.year = 2018
    self.data.license = 'MIT'

  def test_itShouldGenerateEditorConfigWithCpp(self):
    self.data.codeLanguages.append('cpp')

    self.codeStyle.process(self.data)

    self.assertTrue(os.path.exists(self.editorConfigPath))

    editorConfigFile = open(self.editorConfigPath, 'r')
    editorConfig = editorConfigFile.read()
    editorConfigFile.close()

    self.assertTrue('root = true' in editorConfig)
    self.assertTrue('[*.{h,hh,hpp,c,cc,cpp,cxx}]' in editorConfig)

  def test_itShouldGenerateEditorConfigWithPython(self):
    self.data.codeLanguages.append('python')

    self.codeStyle.process(self.data)

    self.assertTrue(os.path.exists(self.editorConfigPath))

    editorConfigFile = open(self.editorConfigPath, 'r')
    editorConfig = editorConfigFile.read()
    editorConfigFile.close()

    self.assertTrue('root = true' in editorConfig)
    self.assertTrue('[*.py]' in editorConfig)

  def test_itShouldGenerateYapfFileForPython(self):
    self.data.codeLanguages.append('python')

    self.codeStyle.process(self.data)

    self.assertTrue(os.path.exists(self.execPath + '/testing/.style.yapf'))
