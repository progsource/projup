# This project is licensed under the MIT license. For more information
# see the LICENSE file.

import os

import npyscreen

from projup.modules.module import Module


class TitleMultiLineEdit(npyscreen.BoxTitle):
  _contained_widget = npyscreen.MultiLineEdit


class Project(Module):

  def __init__(self, pathToProjup, execPath):
    super().__init__(pathToProjup, execPath)
    self.__formDataTechnicalTitle = None
    self.__formDataProjectTitle = None
    self.__formDataDescription = None
    self.__formDataVersion = None

  def createForm(self, form, beginEntryAt):
    self.__formDataTechnicalTitle = form.add(
      npyscreen.TitleText,
      name = 'Technical Working Title\n(will be used as folder name):',
      begin_entry_at = beginEntryAt
    )
    self.__formDataProjectTitle = form.add(
      npyscreen.TitleText,
      name = 'Project Title:',
      begin_entry_at = beginEntryAt
    )
    self.__formDataDescription = form.add(
      TitleMultiLineEdit,
      name = 'Project Description:',
      max_height = 11,
      begin_entry_at = beginEntryAt
    )
    self.__formDataVersion = form.add(
      npyscreen.TitleText,
      name = 'Version:',
      begin_entry_at = beginEntryAt,
    )

  def getModuleData(self, data):
    data.technicalTitle = self.__formDataTechnicalTitle.value
    data.projectTitle = self.__formDataProjectTitle.value
    data.projectDescription = self.__formDataDescription.value
    data.version = self.__formDataVersion.value

    return data

  def _process(self):
    os.mkdir(
      self._execPath + '/' + self._data.technicalTitle,
      mode = 0o777,
      dir_fd = None
    )
    self.__generateReadme()

  def __generateReadme(self):
    self._tplToFile(
      self._pathToProjup + '/templates/readme.tpl',
      self._projectPath + '/README.md'
    )
