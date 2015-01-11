# -*- coding: utf-8 -*-
""" cevidbtool - manage lists on CeviDB groups

Copyright 2014, Nicola Chiapolini v/o Carbon, carbon@cevi.ch

License: GNU General Public License version 3,
         or (at your option) any later version.


mock_requests.py -- Mock Objects to test without connecting to the DB

"""

class MockRequestsCall(object):
    """ structure to store info on function calls """

    def __init__(self, args, kwargs):
        self.args=args
        self.kwargs = kwargs


class MockRequestsResult(object):
    """ mock object for the results returned by requests """

    def __init__(self, json=None, url=None):
        """ initialise result object

        Parameter
        ---------
        json : dict
            dictionary representing result json
        url : string
            content of url attribute

        """
        self._json = json
        self.url = url

    def raise_for_status(self):
        """ mock function """
        pass

    def json(self):
        """ mock function """
        return self._json


class MockRequests(object):
    """ mock object for the requests module

    The mock object provides post and get functions that
    collect the arguments passed and return a configurable result
    object.

    Attributes
    ----------
    calls : list
        list with objects representing calls to get/post
    results : list
        list with result objects to be returned on calls

    """

    def __init__(self):
        self.calls = []
        self.results = []

    def _process_call(self, *args, **kwargs):
        """ helper implementing main logic

        This function stores the arguments from the function
        call and prepares the result object. If no result
        object is configured, a default object is created.

        """
        self.calls.append(MockRequestsCall(args, kwargs))
        try:
            ret = self.results.pop(0)
        except IndexError:
            ret = MockRequestsResult()
        if ret.url == None:
            ret.url = args[0]
        return ret

    def post(self, *args, **kwargs):
        """ mock function """
        return self._process_call(*args, **kwargs)

    def get(self, *args, **kwargs):
        """ mock function """
        return self._process_call(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """ mock function """
        return self._process_call(*args, **kwargs)

