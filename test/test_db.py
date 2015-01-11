# -*- coding: utf-8 -*-
""" cevidbtool - manage lists on CeviDB groups

Copyright 2014, Nicola Chiapolini v/o Carbon, carbon@cevi.ch

License: GNU General Public License version 3,
         or (at your option) any later version.


test_db.py -- test cases for cevidblib.db that work offline

"""
# ensure path is set correctly
from path_helper import add_path
add_path()

import unittest
import cevidblib.db as cdb
from mock_requests import MockRequests, MockRequestsResult

class TestsWithoutDB(unittest.TestCase):
    """ test init and general functionality of CeviDB object """

    url = "https://test.example.com"
    user = "tester@example.com"
    pw = "password"
    cert = "mycert.pem"

    @classmethod
    def setUpClass(self):
        # safe original requests module before monkeypatching
        # cevidblib.db for connection tests
        self.orig_requests = cdb.requests

    @classmethod
    def tearDownClass(self):
        # restore original requests module
        cdb.requests = self.orig_requests

    def setUp(self):
        self.db = cdb.CeviDB(self.user, self.url, self.cert)
        self.mock = MockRequests()
        cdb.requests = self.mock

    def tearDown(self):
        del self.db

    def test_cevidb_object(self):
        """ check initialsation of CeviDB object """
        # create a local db instance to be independet of test order
        self.assertIsInstance(self.db, cdb.CeviDB)
        self.assertEqual(self.db._db_root[:len(self.url)], self.url)
        # url ends with a /
        self.assertEqual(self.db._db_root[-1], "/")
        self.assertEqual(self.db._email, self.user)
        self.assertIsNone(self.db._auth_token)
        self.assertIsNone(self.db._id)
        self.assertEqual(self.db._cert_file, self.cert)

    def test_connect(self):
        """ check the call to request by connect() """
        ret_json = {
                "people": [ {"authentication_token":"123", "id":"1"} ]
                }
        self.mock.results.append(MockRequestsResult(ret_json))
        self.db.connect(self.pw)
        expect_url = "https://test.example.com/users/token.json?person[email]=tester@example.com&person[password]=password"
        self.assertEqual(self.mock.calls[0].args[0], expect_url)
        self.assertEqual(self.db._auth_token, "123")
        self.assertEqual(self.db._id, "1")

    def test_get_group_members(self):
        """ check the call to request by get_group_members() """
        expect_people = [{ "id": "1" }, {"id": "2"}]
        ret_json = {"people": expect_people}
        # ensure _auth_token is set
        self.db.set_auth_token("abc")
        self.mock.results.append(MockRequestsResult(ret_json))
        res = self.db.get_group_members(42)
        expect_url = "https://test.example.com/groups/42/people.json?user_email=tester@example.com&user_token=abc"
        self.assertEqual(self.mock.calls[0].args[0], expect_url)
        self.assertListEqual(res, expect_people)

    def test_certificate(self):
        """ check get_request() passes the certificate file correctly """
        self.db.set_auth_token("abc")
        calls = self.mock.calls
        # test default cert file
        self.db.get_request("")
        self.assertEqual(calls[0].kwargs["verify"], self.cert)
        # test changing to None
        self.db.set_cert_file(None)
        self.db.get_request("")
        self.assertIsNone(calls[1].kwargs["verify"])
        # test changing to other string
        self.db.set_cert_file("../test.pem")
        self.db.get_request("")
        self.assertEqual(calls[2].kwargs["verify"], "../test.pem")

    def test_get_request_token(self):
        """ ensure RuntimeError gets raised if no auth-token is set """
        with self.assertRaises(RuntimeError):
            self.db.get_request("")

    def test_get_request_redirect(self):
        """ check redirection works for get_request() """
        self.db.set_auth_token("abc")
        query_string = "?user_email=tester@example.com&user_token=abc"
        # configure mock object to return different url on first call
        ret_url = self.url+"/second.json"
        self.mock.results.append(MockRequestsResult(url = ret_url))
        # run
        res = self.db.get_request("first.json")
        # asssert result
        self.assertEqual(len(self.mock.calls), 2)
        self.assertEqual(res.url, ret_url+query_string)

    def test_get_request_loop(self):
        """ assert that get_request does not end in infinit loop """
        self.db.set_auth_token("abc")
        # configure mock object to return empty url twice
        # (the called url will be domain+query_string)
        mock_result = MockRequestsResult(url = "")
        self.mock.results.extend([mock_result, mock_result])
        # run & assert result
        with self.assertRaises(RuntimeError):
            res = self.db.get_request("groups.json")
        self.assertEqual(len(self.mock.calls), 2)

if __name__ == "__main__":
    unittest.main()

