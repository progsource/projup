# This project is licensed under the MIT license. For more information
# see the LICENSE file.

from projup.modules.module import Module


class ContinousIntegration(Module):

  def __init__(self, pathToProjup, execPath):
    super().__init__(pathToProjup, execPath)

  def _process(self):
    if 'cpp' in self._data.codeLanguages:
      self._tplToFile(
        self._pathToProjup + '/templates/ci/travis/cpp.tpl',
        self._projectPath + '/.travis.yml'
      )
    elif 'python' in self._data.codeLanguages:
      self._tplToFile(
        self._pathToProjup + '/templates/ci/travis/python.tpl',
        self._projectPath + '/.travis.yml'
      )
