# -*- coding: utf-8 -*-
""" cevidbtool - manage lists on CeviDB groups

Copyright 2014, Nicola Chiapolini v/o Carbon, carbon@cevi.ch

License: GNU General Public License version 3,
         or (at your option) any later version.


db.py -- class to handel connection to CeviDB

"""
from __future__ import division, print_function, unicode_literals
import requests


class RequestsError(Exception):
    """ Calls to handel exceptions raised inside requests """
    pass


class TokenAction(object):
    """ struct to store action configuration """

    def __init__(self, function, endpoint):
        """ define function and endpoint for action """
        self.func = function
        self.end = endpoint


def _handle_requests_error(error):
    """ raise RequestsError with helpful message """
    # check for signature of missing certificate file
    cert_error = False
    try:
        if type(error.args[0].args[0]) == IOError:
            cert_error = True
    except Exception:
        pass
    if cert_error:
        raise RequestsError("SSLError: Zertifikat-Datei nicht gefunden.")
    # raise with general message, if signature not known
    raise RequestsError(repr(error))


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
                 email,
                 db_root="https://db.cevi.ch",
                 cert_file="cacert.pem"
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
            (default: 'cacert.pem')
            see set_cert_file() for details

        """
        # ensure one trailing slash for db url
        self._db_root    = db_root.strip("/")+"/"
        self._email      = email
        self._auth_token = None
        self._id         = None
        self._cert_file  = str(cert_file)

    def set_cert_file(self, filename):
        """ set a new certificate file used

        No check is performed to assert that the file exists.

        Parameters
        ----------
        filename : string, bool, None
            certificate file to use, possibliy including path
            instead of a file, False and None can be specified:
                False -- switch of SSL verification
                None -- use certificates installed on system

        """
        self._cert_file = filename

    def set_auth_token(self, auth_token):
        """ set the authentication token

        Useful if the token is known, no password is needed then.
        No check is performed to ensure the token is valid.

        Parameters
        ----------
        auth_token : string
            authentication token

        """
        self._auth_token = auth_token

    def _token_manager(self, action, password):
        """ login to database and store authentication token

        Parameters
        ----------
        action : TokenAction
            configuration for requested action
        password : string
            password to use for login

        Raises
        ------
        RequestsError
            if certificate file is missing
            or anything else goes wrong with the SSL connection
        HTTPError
            if a http error occured

        """
        url = self._db_root+action.end+".json"
        url += "?person[email]={mail}&person[password]={pw}".format(
                    mail=self._email,
                    pw=password,
                    )
        try:
            res = action.func(url, verify=self._cert_file)
        except requests.exceptions.SSLError as e:
            _handle_requests_error(e)
        res.raise_for_status()
        user = res.json()["people"][0]
        self._auth_token = user["authentication_token"]
        self._id = user["id"]

    def connect(self, password):
        """ alias for the default methode to obtain a token

        use this function if your code does not require a specific
        behaviour for token generation.

        Parameters
        ----------
        password : string
            password to use for login

        """
        self.generate_token(password)

    def get_token(self, password):
        """ get existing token or generate new one

        Parameters
        ----------
        password : string
            password to use for login

        """
        action = TokenAction(requests.post, "users/sign_in")
        self._token_manager(action, password)

    def delete_token(self, password):
        """ delete existing token

        Parameters
        ----------
        password : string
            password to use for login

        """
        action = TokenAction(requests.delete, "users/token")
        self._token_manager(action, password)

    def generate_token(self, password):
        """ generate new token, replacing an existing one

        Parameters
        ----------
        password : string
            password to use for login

        """
        action = TokenAction(requests.post, "users/token")
        self._token_manager(action, password)

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

    def get_request(self, endpoint, redirect=0):
        """ general get request

        Parameters
        ----------
        endpoint : string
            part of request url between domain (db_root) and query string
            or url including domain but without query string
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
        if self._auth_token is None:
            raise RuntimeError("Authentication token fehlt.")
        if endpoint[:len(self._db_root)] == self._db_root:
            url = endpoint
        else:
            url = self._db_root+endpoint
        url += "?user_email={mail}&user_token={token}".format(
                    mail=self._email,
                    token=self._auth_token
                    )
        try:
            res = requests.get(url, verify=self._cert_file)
        except requests.exceptions.SSLError as e:
            _handle_requests_error(e)
        # internal redirects
        #   e.g. people/{pid}.json -> groups/{gid}/people/{pid}.json
        # do not pass the query string on and therefore result in
        # a "401 Authorization Required" error.
        if res.url != url:
            if redirect == 0:
                res = self.get_request(res.url, redirect+1)
            else:
                raise RuntimeError("Too many redirects")
        res.raise_for_status()
        return res

