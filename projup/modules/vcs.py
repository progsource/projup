# This project is licensed under the MIT license. For more information
# see the LICENSE file.

import os, subprocess

from projup.modules.module import Module


class VcsGit(Module):

  def __init__(self, pathToProjup, execPath):
    super().__init__(pathToProjup, execPath)
    self.__tplPath = self._pathToProjup + '/templates/gitignore/'

  def getVcsName(self):
    return 'Git'

  def _process(self):
    self.__generateGitIgnore()
    self.__generateIssueTemplate()
    self.__initGit()

    if 'cpp' in self._data.codeLanguages:
      self.__addSubmoduleGtest()

    self.__initialGitCommit()

  def __generateGitIgnore(self):
    gitignore = ''
    gitignore = self.__generateGitIgnoreForOperatingSystems(gitignore)
    gitignore = self.__generateGitIgnoreForCodeLanguages(gitignore)

    gitignoreFile = open(self._projectPath + '/.gitignore', 'w')
    gitignoreFile.write(gitignore)
    gitignoreFile.close()

  def __generateGitIgnoreForOperatingSystems(self, gitignore):
    if 'MacOSX' in self._data.operatingSystems:
      tplApple = open(self.__tplPath + 'apple.tpl')
      gitignore += tplApple.read()
      tplApple.close()

    if 'Windows' in self._data.operatingSystems:
      tplWindows = open(self.__tplPath + 'windows.tpl')
      gitignore += tplWindows.read()
      tplWindows.close()

    return gitignore

  def __generateGitIgnoreForCodeLanguages(self, gitignore):
    if 'cpp' in self._data.codeLanguages:
      tplCpp = open(self.__tplPath + 'cpp.tpl')
      gitignore += tplCpp.read()
      tplCpp.close()

    if 'python' in self._data.codeLanguages:
      tplPython = open(self.__tplPath + 'python.tpl')
      gitignore += tplPython.read()
      tplPython.close()

    return gitignore

  def __generateIssueTemplate(self):
    if 'cpp' in self._data.codeLanguages:
      self._tplToFile(
        self._pathToProjup + '/templates/git/cpp_issue_template.tpl',
        self._projectPath + '/ISSUE_TEMPLATE.md',
      )
    elif 'python' in self._data.codeLanguages:
      self._tplToFile(
        self._pathToProjup + '/templates/git/python_issue_template.tpl',
        self._projectPath + '/ISSUE_TEMPLATE.md',
      )

  def __initGit(self):
    os.chdir(self._projectPath)

    subprocess.call(['git', 'init'])
    subprocess.call(['git', 'config', 'user.name', self._data.author])
    subprocess.call(['git', 'config', 'user.email', self._data.email])

    os.chdir(self._execPath)

  def __addSubmoduleGtest(self):
    os.chdir(self._projectPath)

    subprocess.call(
      [
        'git',
        'submodule',
        'add',
        'https://github.com/google/googletest.git',
        'libs/gtest',
      ]
    )

    os.chdir(self._execPath)

  def __initialGitCommit(self):
    os.chdir(self._projectPath)

    subprocess.call(['git', 'add', '.'])
    subprocess.call(
      [
        'git', 'commit', '-m',
        '[projup] initial commit\n\nwith config:\n\n' + str(self._data)
      ]
    )

    os.chdir(self._execPath)


class Vcs(Module):

  def __init__(self, pathToProjup, execPath):
    super().__init__(pathToProjup, execPath)
    self.addSubmodule(VcsGit(pathToProjup, execPath))

  def _process(self):
    pass
