# This project is licensed under the MIT license. For more information
# see the LICENSE file.

import os
import unittest

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


class TestCodeLanguages(TestCase):

  def setUp(self):
    fakeTpl = tests.fakeTemplates.FakeTemplates(PATH_TO_PROJUP + '/templates')
    self.setUpPyfakefs()
    fakeTpl.copyContentToVirtualFS()

    self.execPath = '/test'
    self.fs.create_dir(self.execPath)
    self.fs.create_dir(self.execPath + '/testing')
    self.includePath = self.execPath + '/testing/include/testing'
    self.srcPath = self.execPath + '/testing/src/testing'

    self.codeLanguages = projup.modules.CodeLanguages(
      PATH_TO_PROJUP,
      self.execPath,
    )

    self.data = ModuleData()
    self.data.technicalTitle = 'testing'

  def test_itShouldGenerateAHeaderAndSrcFileForCpp(self):
    self.data.codeLanguages.append('cpp')
    self.data.license = 'MIT'

    self.codeLanguages.process(self.data)

    self.assertTrue(os.path.exists(self.includePath))
    self.assertTrue(os.path.exists(self.srcPath))

    includeFile = open(self.includePath + '/testing.h', 'r')
    includeData = includeFile.read()
    includeFile.close()

    self.assertTrue('under the MIT license' in includeData)
    self.assertTrue('#pragma once' in includeData)

    srcFile = open(self.srcPath + '/testing.cpp', 'r')
    srcData = srcFile.read()
    srcFile.close()

    self.assertTrue('under the MIT license' in srcData)
    self.assertTrue('#include "testing/testing.h"' in srcData)

  def test_itShouldGenerateCmakeFilesForCpp(self):
    self.data.codeLanguages.append('cpp')
    self.data.license = 'MIT'

    self.codeLanguages.process(self.data)

    self.assertTrue(os.path.exists(self.execPath + '/testing/cmake'))
    self.assertTrue(os.path.exists(self.execPath + '/testing/libs'))

    self.assertTrue(
      os.path.exists(self.execPath + '/testing/cmake/colorize.cmake')
    )
    self.assertTrue(
      os.path.exists(self.execPath + '/testing/cmake/change_include_dir.cmake')
    )
    self.assertTrue(
      os.path.exists(self.execPath + '/testing/cmake/cotire.cmake')
    )

    self.assertTrue(os.path.exists(self.execPath + '/testing/CMakeLists.txt'))
    self.assertTrue(
      os.path.exists(self.execPath + '/testing/libs/CMakeLists.txt')
    )

    mainCmakeFile = open(self.execPath + '/testing/CMakeLists.txt')
    mainCmakeFileContents = mainCmakeFile.read()
    mainCmakeFile.close()

    self.assertTrue('project(testing)' in mainCmakeFileContents)

  def test_itShouldGenerateBasicPythonFiles(self):
    self.data.codeLanguages.append('python')
    self.data.license = 'MIT'

    self.codeLanguages.process(self.data)

    self.assertTrue(os.path.exists(self.execPath + '/testing/app.py'))
    self.assertTrue(os.path.exists(self.execPath + '/testing/test.py'))
    self.assertTrue(os.path.exists(self.execPath + '/testing/tests'))
    self.assertTrue(
      os.path.exists(self.execPath + '/testing/tests/__init__.py')
    )

  def test_itShouldGeneratePipenvFileForPython(self):
    self.data.codeLanguages.append('python')
    self.data.license = 'MIT'

    self.codeLanguages.process(self.data)

    self.assertTrue(os.path.exists(self.execPath + '/testing/Pipfile'))
