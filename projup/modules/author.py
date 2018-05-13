# This project is licensed under the MIT license. For more information
# see the LICENSE file.

import npyscreen

from projup.modules.module import Module


class Author(Module):

  def __init__(self, pathToProjup, execPath):
    super().__init__(pathToProjup, execPath)
    self.__formDataAuthor = None
    self.__formDataEmail = None

  def createForm(self, form, beginEntryAt):
    self.__formDataAuthor = form.add(
      npyscreen.TitleText,
      name = 'Author Name:',
      begin_entry_at = beginEntryAt,
      value = self._data.author,
    )
    self.__formDataEmail = form.add(
      npyscreen.TitleText,
      name = 'Author E-Mail:',
      begin_entry_at = beginEntryAt,
      value = self._data.email,
    )

  def getModuleData(self, data):
    data.author = self.__formDataAuthor.value
    data.email = self.__formDataEmail.value

    return data

  def _process(self):
    self._tplToFile(
      self._pathToProjup + '/templates/authors.tpl',
      self._projectPath + '/AUTHORS'
    )
