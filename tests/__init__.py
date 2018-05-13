# This project is licensed under the MIT license. For more information
# see the LICENSE file.

import subprocess
from unittest import mock

import tests.fakeTemplates

# we have to mock `call` here, because of git initialization and pipenv
subprocess.call = mock.create_autospec(
  subprocess.call, return_value = 'mocked!'
)

from tests.test_module_author import TestAuthor
from tests.test_module_license import TestLicense
from tests.test_module_codeLanguages import TestCodeLanguages
from tests.test_module_codeStyle import TestCodeStyle
from tests.test_module_continousIntegration import TestCI
from tests.test_module_project import TestProject
from tests.test_module_vcs import TestVcs
