# -*- coding: utf-8 -*-
""" cevidbtool - manage lists on CeviDB groups

Copyright 2014, Nicola Chiapolini v/o Carbon, carbon@cevi.ch

License: GNU General Public License version 3,
         or (at your option) any later version.

master.py -- main class coordinating db-query and file update

"""
from __future__ import division, print_function, unicode_literals
from filedict import XlsxReader, XlsxWriter
from db import CeviDB
import os, time
from config import Settings

class Master(object):
    """ object to handle backups, and calls to other objects """

    def __init__(self, settings=None):
        """ initilise settings and attributes

        Parameters
        ----------
        settings : cevidblib.config.Settings object
            configuration for file to process
            if None, default settings are used (default: None)

        """
        if settings==None:
            self._cfg    = Settings()
        else:
            self._cfg    = settings
        self._reader = None
        self._writer = None
        self._db     = None
        self._filename   = None
        self._backupname = None

    @property
    def cfg(self):
        """ object representing loaded configuration """
        return self._cfg

    def backup_file(self, filename):
        """ move existing data file to backup

        the passed file will be moved to a new name
        with a YYYY-MM-DD_ prefix in the same directory

        Parameters
        ----------
        filename : string
            filename of data file (including path)

        Raises
        ------
        RuntimeError
            if the backup-filename exists already

        """
        self._filename = filename
        dirname  = os.path.dirname(filename)
        basename = os.path.basename(filename)
        backup_base = time.strftime("%Y-%m-%d_")+basename
        backupname  = os.path.join(dirname, backup_base)
        if os.path.exists(backupname):
            raise RuntimeError("Backup file exists already")
        os.rename(filename, backupname)
        self._backupname = backupname

    def restore_backup(self):
        """ restore backup file

        move backup file back to its original name
        the names of the backup file and its original
        name are stored in the object properties by
        backup_file()

        """
        os.rename(self._backupname, self._filename)

    def update_persons(self, list_file, list_db):
        """ merge person data from file and db

        updates the data in list_file:
            * update person-fields with latest values from DB
            * do not change other fields of existing persons
            * add new rows for new persons in DB list_db
            * keep all data on persons not in  list_db anymore

        Parameters
        ----------
        list_file : dict of dicts
            dictionary with data from file
        list_db : list of dicts
            list with data from DB query

        Returns
        -------
        Nothing, the list_file object is modified

        """
        for row_db in list_db:
            pers_id = row_db['id']
            try:
                row_file = list_file[pers_id]
            except KeyError:
                row_file = {}
                for key in self._cfg.column_keys:
                    row_file[key] = ""
                list_file[pers_id] = row_file
            for key, field in self.cfg.pers_cols:
                row_file[key] = row_db[field]

    def run(self, user, password, filename, cert="cacert.pem"):
        """ main function for update

        Parameters
        ----------
        user: string
            username for db
        password: string
            password for user
        filename: string
            file to update (including path)
        cert_file : string
            certificate file used for SSL verification including path
            (default: 'cacert.pem' in the present working directory.)

        """
        self.backup_file(filename)
        try:
            self._reader = XlsxReader(self.cfg, self._backupname)
            persons_file = self._reader.persons

            self._db     = CeviDB(user, self._cfg.db_url, cert)
            self._db.connect(password)
            persons_db   = self._db.get_group_members(self._cfg.group_id)

            self.update_persons(persons_file, persons_db)

            self._writer = XlsxWriter(self.cfg, filename, self._reader)
            self._writer.fill(persons_file)
            self._writer.save()
        except Exception as e:
            self.restore_backup()
            raise e

