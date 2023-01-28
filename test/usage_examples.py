# -*- coding: utf-8 -*-
""" cevidbtool - manage lists on CeviDB groups

Copyright 2014, Nicola Chiapolini v/o Carbon, carbon@cevi.ch

License: GNU General Public License version 3,
         or (at your option) any later version.

"""


from path_helper import add_path
add_path()
add_path("../dbtool")

from cevidblib.config import Settings
TEST_CFG = Settings("../examples/config.ini")
TEST_CFG.group_id     = None # add id of group (int)
USER                  = None # add your login-email (string)
PASS                  = None # add your password (string)

def copy_file():
    """ copy content of example file to new test file

    opens file examples/spender.xls and copys cells configured in
    examples/config.ini to test/example.xlsx.

    """
    from cevidblib.filedict import XlsxReader, XlsxWriter
    old_file   = XlsxReader(TEST_CFG, "../examples/spender.xlsx")
    out_writer = XlsxWriter(TEST_CFG, "example.xlsx", old_file)
    out_writer.fill(old_file.persons)
    out_writer.save()

def get_group():
    """ connect to the CeviDB and retrieve all persons

    connect to the DB with the credentials given in USER and PASS
    and retrieve persons from group specified by TEST_CFG.group_id.

    """
    from cevidblib.db import CeviDB
    db = CeviDB(USER, TEST_CFG.db_url, "../cacert.pem")
    db.connect(PASS)
    group = db.get_group_members(TEST_CFG.group_id)
    print(group)

def master_run():
    """ run a full update on test_example.xlsx

    update the file test/example.xlsx created by copy_file()
    with the data as retrieved in get_group().
    creates backup file test/YYYY-MM-DD_example.xlsx and

    """
    from cevidblib.master import Master
    master = Master(TEST_CFG)
    master.run(USER, PASS, "example.xlsx", "../cacert.pem")

if __name__== "__main__":
    """ run all three examples

    creates the following files:
        * YYYY-MM-DD_example.xlsx
        * example.xlsx

    """
    if TEST_CFG.group_id == None or USER == None or PASS == None:
        print("Please set correct values on lines 18-20 of usage_example.py")
        import sys; sys.exit(1)
    copy_file()
    get_group()
    master_run()
