# This project is licensed under the MIT license. For more information
# see the LICENSE file.

import npyscreen

from projup.modules.module import Module


class OperatingSystems(Module):

  def __init__(self, pathToProjup, execPath):
    super().__init__(pathToProjup, execPath)
    self.__formData = None

  def createForm(self, form, beginEntryAt):
    self.__formData = form.add(
      npyscreen.TitleMultiSelect,
      max_height = 7,
      value = [2, 3, 4],
      name = 'Operating Systems:',
      values = ['Android', 'iOS', 'Linux', 'MacOSX', 'Windows'],
      scroll_exit = True,
      begin_entry_at = beginEntryAt,
    )

  def getModuleData(self, data):
    data.operatingSystems = self.__formData.get_selected_objects()
    return data

  def _process(self):
    pass
