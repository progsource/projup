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


class TestVcs(TestCase):

  def setUp(self):
    fakeTpl = tests.fakeTemplates.FakeTemplates(PATH_TO_PROJUP + '/templates')
    self.setUpPyfakefs()
    fakeTpl.copyContentToVirtualFS()

    self.execPath = '/test'
    self.gitignorePath = self.execPath + '/.gitignore'
    self.fs.create_dir(self.execPath)

    self.vcs = projup.modules.Vcs(
      PATH_TO_PROJUP,
      self.execPath,
    )

    self.data = ModuleData()

  def test_itShouldGenerateAGitIgnoreFile(self):
    self.vcs.process(self.data)

    self.assertTrue(os.path.exists(self.gitignorePath))

  def test_itShouldGenerateAGitignoreWithPython(self):
    self.data.codeLanguages.append('python')

    self.vcs.process(self.data)

    self.assertTrue(os.path.exists(self.gitignorePath))
    gitignore = open(self.gitignorePath, 'r')
    self.assertEquals('venv\n__pycache__\n', gitignore.read())
    gitignore.close()

  def test_itShouldGenerateAGitignoreWithCpp(self):
    self.data.codeLanguages.append('cpp')

    self.vcs.process(self.data)

    self.assertTrue(os.path.exists(self.gitignorePath))
    gitignore = open(self.gitignorePath, 'r')
    self.assertEquals('*.o\n*.obj\n', gitignore.read())
    gitignore.close()

  def test_itShouldGenerateAGitignoreWithMacOSX(self):
    self.data.operatingSystems.append('MacOSX')

    self.vcs.process(self.data)

    self.assertTrue(os.path.exists(self.gitignorePath))
    gitignore = open(self.gitignorePath, 'r')
    self.assertEquals('.DS_Store\n', gitignore.read())
    gitignore.close()

  def test_itShouldGenerateAGitignoreWithWindows(self):
    self.data.operatingSystems.append('Windows')

    self.vcs.process(self.data)

    self.assertTrue(os.path.exists(self.gitignorePath))
    gitignore = open(self.gitignorePath, 'r')
    self.assertEquals('Thumbs.db\n', gitignore.read())
    gitignore.close()

  def test_itShouldGenerateGithubIssueTemplateForCpp(self):
    self.data.codeLanguages.append('cpp')
    self.data.projectTitle = 'Testing'
    issueTplFile = self.execPath + '/ISSUE_TEMPLATE.md'

    self.vcs.process(self.data)

    self.assertTrue(os.path.exists(issueTplFile))

    tplFile = open(issueTplFile, 'r')
    issueTpl = tplFile.read()
    tplFile.close()

    self.assertTrue('**Compiler:**         | ?' in issueTpl)
    self.assertTrue('**Testing version:** | ?' in issueTpl)

  def test_itShouldGenerateGithubIssueTemplateForPython(self):
    self.data.codeLanguages.append('python')
    self.data.projectTitle = 'Testing'
    issueTplFile = self.execPath + '/ISSUE_TEMPLATE.md'

    self.vcs.process(self.data)

    self.assertTrue(os.path.exists(issueTplFile))

    tplFile = open(issueTplFile, 'r')
    issueTpl = tplFile.read()
    tplFile.close()

    self.assertTrue('**python version:**   | ?' in issueTpl)
    self.assertTrue('**Testing version:** | ?' in issueTpl)
