#!/bin/python3

# docstring
'''
parking_manager.py - A Management Interface for the Parking Enforcer Database Application.

Copyright (c) 2026 Jason Wu. All rights reserved.
'''

# imports
import sqlite3

# constants and variables
DATABASE = "parking.db"

# functions


# main
# (mostly just boilerplate database testing for now)
db = sqlite3.connect(DATABASE)
cursor = db.cursor()

statement = "SELECT * FROM sessions;"
cursor.execute(statement)
results = cursor.fetchall()
print(results)
