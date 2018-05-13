# This project is licensed under the MIT license. For more information
# see the LICENSE file.

import os
import datetime
import npyscreen
from pathlib import Path
from os.path import expanduser

import toml

import projup.modules
from projup.modules.module import ModuleData

PATH_TO_PROJUP = os.path.dirname(os.path.realpath(__file__))
PROJUP_VERSION = '0.2.0'

# ------------------------------------------------------------------------------


class projupForm(npyscreen.ActionFormMinimal):

  def on_ok(self):
    self.editing = False


# ------------------------------------------------------------------------------


class ProjupApp(npyscreen.NPSAppManaged):

  def main(self):
    beginEntryAt = 30

    execPath = os.getcwd()

    self.__modules = []
    self.__modules.append(projup.modules.Project(PATH_TO_PROJUP, execPath))
    self.__modules.append(projup.modules.Author(PATH_TO_PROJUP, execPath))
    self.__modules.append(projup.modules.License(PATH_TO_PROJUP, execPath))
    self.__modules.append(
      projup.modules.CodeLanguages(PATH_TO_PROJUP, execPath)
    )
    self.__modules.append(projup.modules.OperatingSystems(PATH_TO_PROJUP, execPath))
    self.__modules.append(
      projup.modules.ContinousIntegration(PATH_TO_PROJUP, execPath)
    )
    self.__modules.append(projup.modules.CodeStyle(PATH_TO_PROJUP, execPath))
    # vcs has to be the last one
    self.__modules.append(projup.modules.Vcs(PATH_TO_PROJUP, execPath))

    form = projupForm(
      name = 'projup ' + PROJUP_VERSION,
      minimum_columns = 120,
    )

    data = self.__parseDefaultConfig()

    for m in self.__modules:
      m.setData(data)
      m.createForm(form, beginEntryAt)

    form.edit()  # This lets the user interact with the Form.

    # --------------------------------------------------------------------------

    now = datetime.datetime.now()
    data.year = now.year

    for m in self.__modules:
      data = m.getModuleData(data)

    # This has to stay in a separate step and cannot be performed in the loop
    # that is handling the module data
    for m in self.__modules:
      m.process(data)

  # ----------------------------------------------------------------------------

  def __parseDefaultConfig(self):
    data = ModuleData()
    cfgData = {'author': '', 'email': ''}

    configFilename = expanduser('~') + '/.projup'
    configFile = Path(configFilename)
    if configFile.is_file():
      cfgData = toml.load(configFilename)

    if cfgData['author']:
      data.author = cfgData['author']
    if cfgData['email']:
      data.email = cfgData['email']

    return data


# ------------------------------------------------------------------------------

if __name__ == '__main__':
  app = ProjupApp()
  app.run()
