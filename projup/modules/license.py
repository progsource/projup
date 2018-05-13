# This project is licensed under the MIT license. For more information
# see the LICENSE file.

import npyscreen

from projup.modules.module import Module


class License(Module):

  def __init__(self, pathToProjup, execPath):
    super().__init__(pathToProjup, execPath)
    self.__tplPath = self._pathToProjup + '/templates/license/'
    self.__formData = None

  def createForm(self, form, beginEntryAt):
    self.__formData = form.add(
      npyscreen.TitleSelectOne,
      max_height = 6,
      value = [
        0,
      ],
      name = 'License:',
      values = ['Apache 2.0', 'BSD 2-clause', 'BSD 3-clause', 'MIT'],
      scroll_exit = True,
      begin_entry_at = beginEntryAt
    )

  def getModuleData(self, data):
    data.license = self.__formData.get_selected_objects()[0]

    return data

  def _process(self):
    licenseTemplateFile = ''
    licenseFile = self._projectPath + '/LICENSE'

    if self._data.license == 'Apache 2.0':
      licenseTemplateFile = 'apache-2.0-short.tpl'
    elif self._data.license == 'BSD 2-clause':
      licenseTemplateFile = 'bsd2.tpl'
    elif self._data.license == 'BSD 3-clause':
      licenseTemplateFile = 'bsd3.tpl'
    elif self._data.license == 'MIT':
      licenseTemplateFile = 'mit.tpl'

    self._tplToFile(self.__tplPath + licenseTemplateFile, licenseFile)
