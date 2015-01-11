# -*- coding: utf-8 -*-
""" cevidbtool - manage lists on CeviDB groups

Copyright 2014, Nicola Chiapolini v/o Carbon, carbon@cevi.ch

License: GNU General Public License version 3,
         or (at your option) any later version.


test_master.py -- test cases for cevidblib.master

"""
# ensure path is set correctly
from  path_helper import add_path
add_path()
add_path("../imports")

import unittest
import os
import time
from cevidblib.master import Master
from constants import PERSONS, RESULT_DB

class MockCfg(object):
      column_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
      pers_cols = [("A", "last_name"), ("B", "first_name"), ("C", "id")]

class ConfigTesterFixture(unittest.TestCase):

    def setUp(self):
        self.master = Master(MockCfg())

    def test_backup(self):
        """ handling backup file works """
        filename = "backup_test.txt"
        backupname = time.strftime("%Y-%m-%d_")+filename
        # moving original file to backup works
        self.assertTrue(os.path.isfile(filename))
        self.master.backup_file(filename)
        self.assertFalse(os.path.isfile(filename))
        self.assertTrue(os.path.isfile(backupname))
        # error raised if backup file exists
        with self.assertRaises(RuntimeError):
            self.master.backup_file(filename)
        # restoring backup works
        self.master.restore_backup()
        self.assertTrue(os.path.isfile(filename))
        self.assertFalse(os.path.isfile(backupname))

    def test_updatepersons(self):
        """ update_persons joins test lists correctly """
        values = dict(PERSONS)
        expect = dict(PERSONS)
        expect["4"] = {"A": u"Neue", "B": u"Eine", "C": "4",
         "D": "", "E": "", "F": "", "G": u''}
        self.master.update_persons(values, RESULT_DB)
        self.assertDictEqual(values, expect)


if __name__ == "__main__":
    unittest.main()
