# This project is licensed under the MIT license. For more information
# see the LICENSE file.

import os, shutil, subprocess

import npyscreen

from projup.modules.module import Module
from projup.modules.module import TemplateFileValue


class CodeLanguages(Module):

  def __init__(self, pathToProjup, execPath):
    super().__init__(pathToProjup, execPath)
    self.__formData = None

  def createForm(self, form, beginEntryAt):
    self.__formData = form.add(
      npyscreen.TitleMultiSelect,
      max_height = 4,
      value = [],
      name = 'Languages:',
      values = ['cpp', 'python'],
      scroll_exit = True,
      begin_entry_at = beginEntryAt
    )

  def getModuleData(self, data):
    data.codeLanguages = self.__formData.get_selected_objects()
    return data

  def _process(self):
    if 'cpp' in self._data.codeLanguages:
      self.__generateBaseCppFiles()
      self.__generateCmakeFiles()
    elif 'python' in self._data.codeLanguages:
      self.__generateBasePythonFiles()
      self.__generatePipenvFiles()

  def __generateBaseCppFiles(self):
    os.mkdir(self._projectPath + '/include', mode = 0o777, dir_fd = None)
    os.mkdir(
      self._projectPath + '/include/' + self._data.technicalTitle,
      mode = 0o777,
      dir_fd = None,
    )
    os.mkdir(self._projectPath + '/src', mode = 0o777, dir_fd = None)
    os.mkdir(
      self._projectPath + '/src/' + self._data.technicalTitle,
      mode = 0o777,
      dir_fd = None,
    )
    self._tplToFile(
      self._pathToProjup + '/templates/cpp/projectheader.tpl',
      self._projectPath + '/include/' + self._data.technicalTitle + '/' +
      self._data.technicalTitle + '.h',
    )

    fileValues = []
    fileValues.append(
      TemplateFileValue(
        'cppheader',
        self._data.technicalTitle + '/' + self._data.technicalTitle + '.h'
      )
    )

    self._tplToFile(
      self._pathToProjup + '/templates/cpp/projectsource.tpl',
      self._projectPath + '/src/' + self._data.technicalTitle + '/' +
      self._data.technicalTitle + '.cpp',
      fileValues,
    )

  def __generateCmakeFiles(self):
    os.mkdir(self._projectPath + '/cmake', mode = 0o777, dir_fd = None)
    shutil.copyfile(
      self._pathToProjup + '/templates/cpp/cmake/colorize.cmake',
      self._projectPath + '/cmake/colorize.cmake'
    )
    shutil.copyfile(
      self._pathToProjup + '/templates/cpp/cmake/change_include_dir.cmake',
      self._projectPath + '/cmake/change_include_dir.cmake'
    )
    shutil.copyfile(
      self._pathToProjup + '/templates/cpp/cmake/cotire.cmake',
      self._projectPath + '/cmake/cotire.cmake'
    )

    self._tplToFile(
      self._pathToProjup + '/templates/cpp/cmake/main_cmake.tpl',
      self._projectPath + '/CMakeLists.txt',
    )
    os.mkdir(self._projectPath + '/libs', mode = 0o777, dir_fd = None)
    self._tplToFile(
      self._pathToProjup + '/templates/cpp/cmake/libs_cmake.tpl',
      self._projectPath + '/libs/CMakeLists.txt',
    )

  def __generateBasePythonFiles(self):
    self._tplToFile(
      self._pathToProjup + '/templates/python/app.tpl',
      self._projectPath + '/app.py',
    )
    self._tplToFile(
      self._pathToProjup + '/templates/python/test.tpl',
      self._projectPath + '/test.py'
    )
    os.mkdir(self._projectPath + '/tests', mode = 0o777, dir_fd = None)
    self._tplToFile(
      self._pathToProjup + '/templates/python/__init__.tpl',
      self._projectPath + '/tests/__init__.py'
    )

  def __generatePipenvFiles(self):
    shutil.copyfile(
      self._pathToProjup + '/templates/python/Pipfile.tpl',
      self._projectPath + '/Pipfile'
    )

    os.chdir(self._projectPath)
    subprocess.call(['pipenv', 'install'])
    os.chdir(self._execPath)
