# This project is licensed under the MIT license. For more information
# see the LICENSE file.

from projup.modules.module import Module


class CodeStyle(Module):

  def __init__(self, pathToProjup, execPath):
    super().__init__(pathToProjup, execPath)

  def _process(self):
    self.__generateEditorConfig()

    if 'python' in self._data.codeLanguages:
      self._tplToFile(
        self._pathToProjup + '/templates/python/yapf.tpl',
        self._projectPath + '/.style.yapf'
      )

  def __generateEditorConfig(self):
    editorconfig = ''
    baseFile = open(
      self._pathToProjup + '/templates/editorconfig/base.tpl', 'r'
    )
    editorconfig += baseFile.read()
    baseFile.close()

    if 'cpp' in self._data.codeLanguages:
      cppFile = open(
        self._pathToProjup + '/templates/editorconfig/cpp.tpl', 'r'
      )
      editorconfig += '\n' + cppFile.read()
      cppFile.close()

    if 'python' in self._data.codeLanguages:
      pythonFile = open(
        self._pathToProjup + '/templates/editorconfig/python.tpl', 'r'
      )
      editorconfig += '\n' + pythonFile.read()
      pythonFile.close()

    editorConfigFile = open(self._projectPath + '/.editorconfig', 'w')
    editorConfigFile.write(editorconfig)
    editorConfigFile.close()
