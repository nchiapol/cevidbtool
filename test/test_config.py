# -*- coding: utf-8 -*-
""" cevidbtool - manage lists on CeviDB groups

Copyright 2014, Nicola Chiapolini v/o Carbon, carbon@cevi.ch

License: GNU General Public License version 3,
         or (at your option) any later version.


test_config.py -- test cases for cevidblib.config

"""
# ensure path is set correctly
from  path_helper import add_path
add_path()
add_path("../dbtool")

import unittest
import cevidblib.config as cfg

class ConfigTesterNoFixture(unittest.TestCase):

    def test_file_open(self):
        with self.assertRaises(IOError):
            settings = cfg.Settings("not_exisiting_file.ini")

class ConfigTesterFixture(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.settings = cfg.Settings("test.ini")

    def test_simple_config(self):
        self.assertEqual(self.settings.db_url, "http://cevi.puzzle.ch/")
        self.assertEqual(self.settings.default_mail, "tester@example.com")
        self.assertEqual(self.settings.group_id, 42)
        self.assertEqual(self.settings.header_lines, 4)
        self.assertEqual(self.settings.footer_lines, 0)
        self.assertEqual(self.settings.freeze_column, "D")

    def test_column_config(self):
        keys_expected = [1, 2, 3, 4, 5, 6, 7]
        group_expected = {1: "person", 2: "person", 3: "person",
                          4: "data", 5: "data", 6: "data", 7: "formula"}
        value_expected = {1: "last_name", 2: "first_name", 3: "id",
                4: "", 5: "", 6: "", 7: "=SUM(D{row}:F{row})"}
        self.assertCountEqual(list(self.settings.columns.keys()), keys_expected)
        for key in keys_expected:
            col = self.settings.columns[key]
            self.assertIsInstance(col, cfg.ColConfig)
            self.assertEqual(col.group, group_expected[key])
            self.assertEqual(col.value, value_expected[key])
        self.assertListEqual(self.settings.column_keys, keys_expected )
        self.assertEqual(len(self.settings.pers_cols), 3)
        for pair in self.settings.pers_cols:
            self.assertEqual(pair[1], value_expected[pair[0]])

    def test_get_column_key(self):
        self.assertEqual(self.settings.get_column_key("id"), 3)
        with self.assertRaises(ValueError):
            self.settings.get_column_key("town")

if __name__ == "__main__":
    unittest.main()
