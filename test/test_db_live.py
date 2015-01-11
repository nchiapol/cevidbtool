# -*- coding: utf-8 -*-
""" cevidbtool - manage lists on CeviDB groups

Copyright 2014, Nicola Chiapolini v/o Carbon, carbon@cevi.ch

License: GNU General Public License version 3,
         or (at your option) any later version.


test_db_live.py -- test cases for cevidblib.db connecting to the live DB

"""
# ensure path is set correctly
from  path_helper import add_path
add_path()

import unittest
import cevidblib.db as cdb

class TestsUsingLiveDB(unittest.TestCase):
    """ Test real connection to the CeviDB, needs a user account """
    url = "https://db.cevi.ch"
    user = "cevidb-tests@cevi-zhshgl.ch"

    @classmethod
    def setUpClass(self):
        # read the password from a separate file
        # to prevent the password ending up in git
        try:
            with open("pw_file.txt", "r") as pw_file:
                self.pw = pw_file.readline().strip()
        except IOError:
            message = """
Skipping Tests with Live DB as password file is missing!\n\
    Create the file 'pw_file.txt' containing\n\
    the password for cevidb-tests@cevi-zhshghl.ch.
"""
            print(message)
            raise unittest.SkipTest("Password file is missing.")

    def setUp(self):
        self.db = cdb.CeviDB(self.user, self.url, "../cacert.pem")

    def tearDown(self):
        del self.db

    def test_cert_error(self):
        """ missing certificat file raises error """
        self.db.set_cert_file("inexistent_file")
        with self.assertRaises(cdb.RequestsError):
            self.db.connect(self.pw)

    def test_login(self):
        """ connecting works and returns token with correct length """
        self.db.connect(self.pw)
        self.assertIsNotNone(self.db._auth_token)
        self.assertEqual(len(self.db._auth_token), 20)

    def test_token_manager(self):
        """ token can be obtained, changed and deleted """
        self.assertIsNone(self.db._auth_token)
        self.db.get_token(self.pw)
        self.assertIsNotNone(self.db._auth_token)
        token = self.db._auth_token
        self.db.get_token(self.pw)
        self.assertEqual(self.db._auth_token, token)
        self.db.generate_token(self.pw)
        self.assertNotEqual(self.db._auth_token, token)
        self.db.delete_token(self.pw)
        self.assertIsNone(self.db._auth_token)


if __name__ == "__main__":
    unittest.main()

