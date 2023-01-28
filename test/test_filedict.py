# -*- coding: utf-8 -*-
""" cevidbtool - manage lists on CeviDB groups

Copyright 2014, Nicola Chiapolini v/o Carbon, carbon@cevi.ch

License: GNU General Public License version 3,
         or (at your option) any later version.


test_filedict.py -- test cases for cevidblib.filedict

"""
# ensure path is set correctly
from  path_helper import add_path
add_path()
add_path("../dbtool")

import unittest
import cevidblib.filedict as fd
from cevidblib.config import Settings
from random import randint
from constants import PERSONS

""" Mock objects and functions """
class MockOpenpyxl(object):

    def Workbook(self):
        return self


class MockReader(object):
    start_footer = 2


def mock_copy(src, dst):
    global copy_calls
    copy_calls.append((src,dst))


class MockCell(object):

    def __init__(self, col, val, style=None):
        self.column = col
        self.value = val
        self.style = style


class HelperTests(unittest.TestCase):
    """ test helper functions from filedict module """

    def test_to_coord(self):
        """ coordinate strings are built correctly """
        self.assertEqual(fd.to_coord("A", "1"), "A1")
        self.assertEqual(fd.to_coord("B", 2), "B2")
        self.assertEqual(fd.to_coord("ABC", "12345"), "ABC12345")
        self.assertEqual(fd.to_coord(4,6), "D6")

    def test_row2person(self):
        """ row of mock cells is correclty paresed into dict """
        value = [MockCell("A", "Eins"), MockCell("B", "Zwei"),
                 MockCell("C", 3), MockCell("D", "Vier")]
        expect = {"A": "Eins", "B": "Zwei", "C": 3, "D": "Vier"}
        self.assertDictEqual(fd.row2person(value), expect)


class TestReader(unittest.TestCase):
    """ test loading test.xlsx """

    @classmethod
    def setUpClass(self):
        self.cfg = Settings("test.ini")
        self.reader = fd.XlsxReader(self.cfg, "test.xlsx")

    def test_init_attributes(self):
        """ initialising the general attributes works """
        self.assertEqual(self.reader._cfg, self.cfg)
        wb_type = fd.openpyxl.workbook.workbook.Workbook
        self.assertEqual(type(self.reader._wb), wb_type)
        self.assertEqual(self.reader.start_persons, 5)
        self.assertEqual(self.reader.start_footer, 8)

    def test_init_persons2(self):
        """ person data is read correctly """
        self.assertDictEqual(self.reader.persons, PERSONS)

    def test_cellaccess(self):
        """ cells can be accessed correctly """
        # pairs: (value, expect)
        tests = [("A1", "Testdatei für cevidblib"),
                 ("F4", "Posten 3"),
                 ("D6", 10)
                 ]
        for val, exp in tests:
            self.assertEqual(self.reader.cell(val), exp)


class TestCopyWriter(unittest.TestCase):
    """ create copy of test.xlsx

    copy header from test.xlsx and take person data from  PERSONS-dict

    """

    @classmethod
    def setUpClass(self):
        self.cfg = Settings("test.ini")
        self.reader = fd.XlsxReader(self.cfg, "test.xlsx")
        self.writer = fd.XlsxWriter(self.cfg, "test_new.xlsx", self.reader)
        self.writer.fill(PERSONS)

    @classmethod
    def tearDownClass(self):
        self.writer.save()

    def test_attributes(self):
        """ general attributes correct after filling """
        self.assertEqual(self.writer._cfg, self.cfg)
        wb_type = fd.openpyxl.workbook.workbook.Workbook
        self.assertEqual(type(self.writer._wb), wb_type)
        self.assertEqual(self.writer._filename, "test_new.xlsx")
        self.assertEqual(self.writer._old_file, self.reader)
        self.assertEqual(self.writer._start_persons, 5)
        self.assertEqual(self.writer._start_footer, 8)

    def compare_cell(self, cell):
        wcell = self.writer._wb.active[cell]
        rcell = self.reader.cell(cell)
        self.assertEqual(wcell.value, rcell,
                "Difference in cell {cell}: {wv} != {rv}".format(
                    cell=cell, wv=wcell.value, rv=rcell
                ))

    def test_random(self):
        """ random selection of fields is created correctly """
        for i in range(20):
            cell = fd.to_coord(randint(1,10), randint(1,10))
            self.compare_cell(cell)

    def test_column(self):
        """ column A is written correctly """
        for i in range(1,11):
            cell = fd.to_coord("A", i)
            self.compare_cell(cell)

    def test_row(self):
        """ row 6 is written correctly """
        for i in range(1,11):
            cell = fd.to_coord(i, 6)
            self.compare_cell(cell)


class TestWriterSimple(unittest.TestCase):
    """ tests for XlsxWriter using mock objects

    used to test:
      * copy_footer
    """

    @classmethod
    def setUpClass(self):
        self.cfg = Settings("test.ini")
        self.orig_openpyxl = fd.openpyxl
        fd.openpyxl = MockOpenpyxl()
        fd.openpyxl.utils = self.orig_openpyxl.utils

    @classmethod
    def tearDownClass(self):
        fd.openpyxl = self.orig_openpyxl

    def setUp(self):
        global copy_calls
        copy_calls = []
        self.writer = fd.XlsxWriter(self.cfg, "new.xlsx", MockReader())
        self.writer.copy_cell = mock_copy

    def test_copyfooter_raises(self):
        """ copy_footer rises exception when start_footer is not set """
        with self.assertRaises(RuntimeError):
            self.writer.copy_footer()

    def test_copyfooter(self):
        """ copy_footer copies correct cells """
        self.writer._start_footer = 8
        self.writer._cfg.footer_lines = 2
        self.writer.copy_footer()
        self.assertEqual(len(copy_calls), 14)
        self.assertEqual(copy_calls[0], ("A2", "A8"))
        self.assertEqual(copy_calls[-1], ("G3", "G9"))

    def test_copyfooter_negative(self):
        """ copy_footer handles negativ numnber of footer lines correctly """
        self.writer._start_footer = 8
        self.writer._cfg.footer_lines = -2
        self.writer.copy_footer()
        self.assertEqual(len(copy_calls), 0)

if __name__ == "__main__":
    unittest.main()

