# -*- coding: utf-8 -*-
""" cevidbtool - manage lists on CeviDB groups

Copyright 2014, Nicola Chiapolini v/o Carbon, carbon@cevi.ch

License: GNU General Public License version 3,
         or (at your option) any later version.


constants.py -- constants usefull for tests

"""

# data from test file
PERSONS = {
    "1": {1: "Jemand", 2: "Irgend", 3: 1,
        4: 10, 5: 20, 6: 30, 7: '=SUM(D6:F6)'},
    "2": {1: "Jemand", 2: "Noch", 3: 2,
         4:  5, 5: 25, 6: 20, 7: '=SUM(D7:F7)'},
    "3": {1: "Anders", 2: "Jemand", 3: 3,
         4: 14, 5: 12, 6: 16, 7: '=SUM(D5:F5)'},
}

# example for DB
RESULT_DB = [
   {"id": "1", "last_name": "Jemand", "first_name": "Irgend"},
   {"id": "3", "last_name": "Anders", "first_name": "Jemand"},
   {"id": "4", "last_name": "Neue", "first_name": "Eine"},
]


