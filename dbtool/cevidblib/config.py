# -*- coding: utf-8 -*-
""" cevidbtool - manage lists on CeviDB groups

Copyright 2014, Nicola Chiapolini v/o Carbon, carbon@cevi.ch

License: GNU General Public License version 3,
         or (at your option) any later version.


config.py - classes to manage configuration

"""
import configparser
import openpyxl

class ColConfig(object):
    """ object to represent column configuration

    each column belongs to a groupd and has an optional value
    the group is defined based on the optional value.
    Possible groups are:
        data: columns with no pre-defined value,
              the content of these cells should be conserved on updates
        formula: columns with a pre-defined value starting with '='
                 the content of these cells is set to the formula
                   on each update
        person: columns with a pre-defined value NOT starting with '='
                the value stored must correpond to the attribute of
                  a person in the DB
                the content of these cells is filled with the
                  corresponding attribute from the database
    """

    def __init__(self, _group, _value=""):
        """ initialise column object

        Parameters
        ----------
        _group : string
            one of ["data", "formula", "person"] (see docs for class)

        """
        self.group = _group
        self.value = _value

class Settings(object):
    """ object representing the config file

    The object is initialised from a file. If no filename is given
    'default.ini' is used.

    """

    def __init__(self, filename = None):
        """ read config file and initialise object

        Parameters
        ----------
        filename : string
            path and name of the config file to read
            (default: default.ini)

        Raises
        ------
        RuntimeError
            if config file could not be read

        """
        # open and read file
        if filename == None:
            filename = "config.ini"
        self._parser = configparser.RawConfigParser()
        loaded = self._parser.read(filename, encoding="utf-8")
        if len(loaded) == 0:
            raise IOError("Failed to load config file")

        # parse simple config values
        self.db_url       = self._parser.get("db", "url")
        self.default_mail = self._parser.get("db", "defaultmail")
        self.group_id     = self._parser.getint("file", "groupid")
        self.header_lines = self._parser.getint("file", "headerlines")
        self.footer_lines = self._parser.getint("file", "footerlines")
        self.freeze_column = self._parser.get("file", "freezecolumn")

        # parse row config
        #   create dictionary with column objects
        #   {'A' : <<ColConfig Object>>, 'B' : <<...}
        col_def = {}
        for row in self._parser.items("rows"):
            group = "data"
            if len(row[1]) > 0:
                if row[1][0] == "=":
                    group = "formula"
                else:
                    group = "person"
            col_def[openpyxl.utils.column_index_from_string(row[0])] = ColConfig(group, row[1])
        self.columns = col_def

        #   create list of column keys: ['A', 'B', ...]
        self.column_keys = list(self.columns.keys())
        self.column_keys.sort()

        #   create list with pairs containing (key, name)
        #   for all person columns: [('A', 'id'), ('B', 'last_name'), ...]
        self.pers_cols = []
        for key, item in self.columns.items():
            if item.group == "person":
                self.pers_cols.append((key, item.value))

    def get_column_key(self, value):
        """ find key for column with given pre-defined value

        Parameters
        ----------
        value : string
            pre-defined value to look for (usually attribute from DB)

        Raises
        ------
        ValueError
            if no column has the pre-defined value searched for

        """
        for key, item in self.columns.items():
            if item.value == value:
                return key
        raise ValueError(value+" not found in configuration")

