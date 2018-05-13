# This project is licensed under the MIT license. For more information
# see the LICENSE file.

import os, shutil, fileinput


class ModuleImplementationError(LookupError):
  '''raise this when there's a wrong implementation of a module'''


class ModuleError(LookupError):
  '''raise this when there's an error'''


class ModuleData:

  def __init__(self):
    self.technicalTitle = ''
    self.projectTitle = ''
    self.projectDescription = ''
    self.version = ''
    self.author = ''
    self.email = ''
    self.license = ''
    self.codeLanguages = []
    self.operatingSystems = []
    self.year = 0

  def __str__(self):
    return ''.join(
      [
        'technicalTitle=',
        self.technicalTitle,
        '\n',
        'projectTitle=',
        self.projectTitle,
        '\n',
        'version=',
        self.version,
        '\n',
        'author=',
        self.author,
        '\n',
        'license=',
        self.license,
        '\n',
        'codeLanguages=',
        str(self.codeLanguages),
        '\n',
        'operatingSystems=',
        str(self.operatingSystems),
        '\n',
        'year=',
        str(self.year),
        '\n',
      ]
    )


class TemplateFileValue:

  def __init__(self, title, value):
    self.title = title
    self.value = value


class Module:

  def __init__(self, pathToProjup, execPath):
    if not os.path.exists(pathToProjup):
      raise ModuleError('pathToProjup "' + pathToProjup + '" does not exist')

    if not os.path.exists(execPath):
      raise ModuleError('execPath "' + execPath + '" does not exist')

    self._pathToProjup = pathToProjup
    self._execPath = execPath
    self._projectPath = ''
    self._submodules = []
    self._data = []

  def addSubmodule(self, module):
    self._submodules.append(module)

  def setData(self, data):
    self._data = data

  def createForm(self, form, beginEntryAt):
    pass

  def getModuleData(self, data):
    return data

  def process(self, data):
    self._projectPath = os.path.join(self._execPath, data.technicalTitle)

    self._data = data
    self._process()

    for submodule in self._submodules:
      submodule.process(data)

  def _process(self):
    raise ModuleImplementationError('_process has to be overriden in module')

  def _tplToFile(self, tplFile, outFile, additionalVariables = []):
    shutil.copyfile(tplFile, outFile)
    with fileinput.FileInput(outFile, inplace = True) as file:
      for line in file:
        newFileLine = line.replace(
          '{technicalTitle}', self._data.technicalTitle
        )
        newFileLine = newFileLine.replace('{username}', self._data.author)
        newFileLine = newFileLine.replace('{usermail}', self._data.email)
        newFileLine = newFileLine.replace(
          '{projectname}', self._data.projectTitle
        )
        newFileLine = newFileLine.replace(
          '{projectdescription}', self._data.projectDescription
        )
        newFileLine = newFileLine.replace('{year}', str(self._data.year))
        newFileLine = newFileLine.replace('{license}', self._data.license)
        newFileLine = newFileLine.replace('{version}', self._data.version)
        for additionalVariable in additionalVariables:
          newFileLine = newFileLine.replace(
            '{' + additionalVariable.title + '}', additionalVariable.value
          )
        print(newFileLine, end = '')
