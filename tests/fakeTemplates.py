# This project is licensed under the MIT license. For more information
# see the LICENSE file.

import os


class DirectoryNotFound(LookupError):
  '''raise this when a directory was not found'''


class FakeFile:

  def __init__(self, filename, contents):
    self.filename = filename
    self.contents = contents


class FakeTemplates:
  """ Intention of this class is to make the template folder available while the
  rest of the filesystem is faked during the tests.
  """

  def __init__(self, templateRealPath):
    if not os.path.exists(templateRealPath):
      raise DirectoryNotFound(
        'The templateRealPath "' + templateRealPath + '" was not found!'
      )

    self.__templateRealPath = templateRealPath
    self.__directory = []

    for entry in os.listdir(self.__templateRealPath):
      self.__copyContentToTemporary(self.__templateRealPath, entry)

  def __copyContentToTemporary(self, directory, entry):
    fullPath = directory + '/' + entry

    if os.path.isfile(fullPath):
      tmpContentFile = open(fullPath, 'r')
      tmpFile = FakeFile(fullPath, tmpContentFile.read())
      self.__directory.append(tmpFile)
    elif os.path.isdir(fullPath):
      for subentry in os.listdir(fullPath):
        self.__copyContentToTemporary(fullPath, subentry)

  def copyContentToVirtualFS(self):
    """ this method should be called AFTER the filesystem is faked
    """

    for fakeFile in self.__directory:
      os.makedirs(os.path.dirname(fakeFile.filename), exist_ok = True)
      virtualFile = open(fakeFile.filename, 'w')
      virtualFile.write(fakeFile.contents)
      virtualFile.close()
