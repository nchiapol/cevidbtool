# -*- coding: utf-8 -*-
""" cevidbtool - manage lists on CeviDB groups

Copyright 2014, Nicola Chiapolini v/o Carbon, carbon@cevi.ch

License: GNU General Public License version 3,
         or (at your option) any later version.


constants.py -- constants usefull for tests

"""

# data from test file
PERSONS = {
    "1": {"A": "Jemand", "B": "Irgend", "C": 1,
        "D": 10, "E": 20, "F": 30, "G": '=SUM(D6:F6)'},
    "2": {"A": "Jemand", "B": "Noch", "C": 2,
         "D":  5, "E": 25, "F": 20, "G": '=SUM(D7:F7)'},
    "3": {"A": "Anders", "B": "Jemand", "C": 3,
         "D": 14, "E": 12, "F": 16, "G": '=SUM(D5:F5)'},
}

# example for DB
RESULT_DB = [
   {"id": "1", "last_name": "Jemand", "first_name": "Irgend"},
   {"id": "3", "last_name": "Anders", "first_name": "Jemand"},
   {"id": "4", "last_name": "Neue", "first_name": "Eine"},
]


