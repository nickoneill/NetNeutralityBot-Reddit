"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        NetNeutralityBot
Date Created:       08/03/2017
Date Last Edited:   08/03/2017
Version:            v1.0
==========================================
"""

import sqlite3
import time
import traceback
from os import path

CREATE_TABLE = 'CREATE TABLE IF NOT EXISTS posts (' + \
               'permalink TEXT NOT NULL, ' + \
               'timestamp REAL NOT NULL, ' + \
               'PRIMARY KEY( permalink ));'
INSERT_ROW = 'INSERT INTO posts VALUES (?,?);'
GET_POST = 'SELECT * FROM posts WHERE permalink=?;'
COUNT = 'SELECT COUNT(*) FROM posts;'


class DatabaseHandler:
    def __init__(self, db_location):
        self.db_location = db_location
        self.connection = self.connect()

    def connect(self):
        try:
            # Create db file if it doesn't exist
            if not path.isfile(self.db_location):
                with open(self.db_location, 'w+') as f:
                    f.close()

            connection = sqlite3.connect(self.db_location)
            connection.text_factory = str
            connection.execute('PRAGMA foreign_keys = ON;')
            cursor = connection.cursor()
            cursor.execute(CREATE_TABLE)
            return connection
        except:
            raise DatabaseHandlerException('Error Connecting to Database\n\n' + traceback.format_exc())

    def disconnect(self):
        try:
            if self.connection:
                self.connection.rollback()
                self.connection.close()
            self.connection = None
        except:
            raise DatabaseHandlerException('Error Disconnecting from Database\n\n' + traceback.format_exc())

    def reset(self):
        try:
            self.disconnect()
            self.connection = self.connect()
        except:
            DatabaseHandlerException('Error resetting connection to database\n\n' + traceback.format_exc())

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def insert_comment(self, permalink):
        timestamp = time.time()
        print('Inserting new row: [' + permalink + ', ' + str(timestamp) + ']')
        try:
            values = [permalink, timestamp]
            self.connection.cursor().execute(INSERT_ROW, values)
        except:
            raise DatabaseHandlerException('ERROR - Inserting new row')

    def match_exists(self, permalink):
        try:
            return len(self.connection.cursor().execute(GET_POST, [permalink]).fetchall()) >= 1
        except:
            print('ERROR - Couldn\'t figure out if post existed')
            return True

    def count_posts(self):
        try:
            return len(self.connection.cursor().execute(COUNT).fetchall())
        except:
            print('ERROR - Counting posts')
            return -1


class DatabaseHandlerException(Exception):
    INTEGRITY_ERROR = 'Integrity Error - Row already exists'

    def __init__(self, error_args):
        Exception.__init__(self, 'DBHelper Exception: {0}'.format(error_args))
        self.errorArgs = error_args
