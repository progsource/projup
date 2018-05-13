# This project is licensed under the MIT license. For more information
# see the LICENSE file.

import os
import unittest
from unittest import mock

# ------------------------------------------------------------------------------

from pyfakefs.fake_filesystem_unittest import TestCase
from pyfakefs.fake_filesystem_unittest import Patcher

# ------------------------------------------------------------------------------

import tests.fakeTemplates

# ------------------------------------------------------------------------------

import projup
from projup.modules.module import ModuleData

# ------------------------------------------------------------------------------

PATH_TO_PROJUP = os.path.dirname(os.path.realpath(__file__ + '/..'))

# ------------------------------------------------------------------------------


class TestLicense(TestCase):

  def setUp(self):
    fakeTpl = tests.fakeTemplates.FakeTemplates(PATH_TO_PROJUP + '/templates')
    self.setUpPyfakefs()
    fakeTpl.copyContentToVirtualFS()

    self.execPath = '/test'
    self.fs.create_dir(self.execPath)
    self.fs.create_dir(self.execPath + '/testing')
    self.licensePath = self.execPath + '/testing/LICENSE'

    self.license = projup.modules.License(
      PATH_TO_PROJUP,
      self.execPath,
    )

    self.data = ModuleData()
    self.data.technicalTitle = 'testing'
    self.data.author = 'Testa'
    self.data.year = 2018

  def test_itShouldGenerateAnApacheLicenseFile(self):
    self.data.license = 'Apache 2.0'

    self.license.process(self.data)

    self.assertTrue(os.path.exists(self.licensePath))

    licenseFile = open(self.licensePath, 'r')
    licenseData = licenseFile.read()
    licenseFile.close()

    self.assertTrue('Copyright 2018 Testa' in licenseData)
    self.assertTrue('Apache License, Version 2.0' in licenseData)

  def test_itShouldGenerateABSD2ClauseLicenseFile(self):
    self.data.license = 'BSD 2-clause'

    self.license.process(self.data)

    self.assertTrue(os.path.exists(self.licensePath))

    licenseFile = open(self.licensePath, 'r')
    licenseData = licenseFile.read()
    licenseFile.close()

    self.assertTrue('Copyright 2018 Testa' in licenseData)
    self.assertTrue('1. Redistributions' in licenseData)
    self.assertTrue('2. Redistributions' in licenseData)
    self.assertFalse('3. Neither' in licenseData)

  def test_itShouldGenerateABSD3ClauseLicenseFile(self):
    self.data.license = 'BSD 3-clause'

    self.license.process(self.data)

    self.assertTrue(os.path.exists(self.licensePath))

    licenseFile = open(self.licensePath, 'r')
    licenseData = licenseFile.read()
    licenseFile.close()

    self.assertTrue('Copyright 2018 Testa' in licenseData)
    self.assertTrue('1. Redistributions' in licenseData)
    self.assertTrue('2. Redistributions' in licenseData)
    self.assertTrue('3. Neither' in licenseData)

  def test_itShouldGenerateAMITLicenseFile(self):
    self.data.license = 'MIT'

    self.license.process(self.data)

    self.assertTrue(os.path.exists(self.licensePath))

    licenseFile = open(self.licensePath, 'r')
    licenseData = licenseFile.read()
    licenseFile.close()

    self.assertTrue('Copyright 2018 Testa' in licenseData)
    self.assertTrue(
      ''.join(
        [
          'Permission is hereby granted, free of charge, to any person obtaining a copy of\n',
          'this software and associated documentation files (the "Software"), to deal in'
        ]
      ) in licenseData
    )
