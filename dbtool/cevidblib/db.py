# -*- coding: utf-8 -*-
""" cevidbtool - manage lists on CeviDB groups

Copyright 2014, Nicola Chiapolini v/o Carbon, carbon@cevi.ch

License: GNU General Public License version 3,
         or (at your option) any later version.


db.py -- class to handel connection to CeviDB

"""

import requests
import os

class RequestsError(Exception):
    """ Calls to handel exceptions raised inside requests """
    pass


class TokenAction(object):
    """ struct to store action configuration """

    def __init__(self, function, endpoint):
        """ define function and endpoint for action """
        self.func = function
        self.end = endpoint


class CeviDB(object):
    """ object to handel connection

    the object stores:
        - url of database
        - certificate file to use for SSL verification
        - main email of user (login email)
        - authentication token generated for user
        - id of user in database

    and handles the login process as well as the other requests

    """

    def __init__(self,
                 token,
                 db_root="https://db.cevi.ch",
                 cert_file=None
                 ):
        """ initialise basic connection settings

        Parameters
        ----------
        email : string
            email adress used for login
        db_root : string
            base url for database (default: https://db.cevi.ch)
        cert_file : string
            certificate file used for SSL verification including path
            see set_cert_file() for details

        """
        # ensure one trailing slash for db url
        self._db_root    = db_root.strip("/")+"/"
        self._token      = token
        self._id         = None
        self._cert_file  = None
        self.set_cert_file(cert_file)

    def set_cert_file(self, filename=None):
        """ set the certificate file used

        By default or if file does not exists, the root certificates
        trusted by the system are used

        Parameters
        ----------
        filename : string, bool, None
            certificate file to use, possibliy including path
            instead of a file, False and None can be specified:
                False -- switch of SSL verification
                None -- use certificates installed on system

        """
        if filename and os.path.isfile(filename):
            self._cert_file = filename
        #TODO:
        # - functionality should probably be exposed via config
        # - a missing file should at least trigger a warning
        # - updat tests

    def get_group_members(self, group_id):
        """ get list with all members of given group

        Parameters
        ----------
        group_id : int
            id of group to retrieve

        """
        endpoint = "groups/{gid}/people.json".format(gid=group_id)
        json = self.get_request(endpoint).json()
        return json['people']

    def get_person(self, pers_id):
        """ get details for a given person

        Parameters
        ----------
        pers_id : int
            id of person to retrieve

        Returns
        -------
        json : dict
            dictionary representing result json

        """
        endpoint = "people/{pid}.json".format(pid=pers_id)
        return self.get_request(endpoint).json()

    def get_group(self, group_id):
        """ get info on a given group

        this function does not return the members of a group

        Parameters
        ----------
        group_id : int
            id of group to retrieve

        Returns
        -------
        json : dict
            dictionary representing result json

        """
        endpoint = "groups/{gid}.json".format(gid=group_id)
        return self.get_request(endpoint).json()

    def get_request(self, endpoint, query_string=None, redirect=1):
        """ general get request

        Parameters
        ----------
        endpoint : string
            part of request url between domain (db_root) and query string
            or url including domain but without query string
        query_string : string
            query_string without preceding '?' or '&'
            (this will be combined with the authentication variables
            to form the final query string)
        redirect : int
            counter to limit number of redirects

        Returns
        -------
        res : result object
            result of request

        Raises
        ------
        RequestsError
            if certificate file is missing
            or anything else goes wrong with the SSL connection
        HTTPError
            if a http error occured
        RuntimeError
            if the authentication token is missing
            or the get request gets redirected too often

        """
        if endpoint[:len(self._db_root)] == self._db_root:
            url = endpoint
        else:
            url = self._db_root+endpoint
        url += "?token={token}".format(
                    token=self._token
                    )
        if query_string is not None:
            url += "&"+query_string
        res = requests.get(url, verify=self._cert_file)
        # internal redirects
        #   e.g. people/{pid}.json -> groups/{gid}/people/{pid}.json
        # do not pass the query string on and therefore result in
        # a "401 Authorization Required" error.
        if res.url != url:
            if redirect > 0:
                res = self.get_request(res.url, redirect=redirect-1)
            else:
                raise RuntimeError("Too many redirects")
        res.raise_for_status()
        return res

