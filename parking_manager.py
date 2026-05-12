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
def log_entry(plate, entry_time):
    # connects to the database
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # executes the statement to insert a new session entry into the database
    statement = f"INSERT INTO sessions (plate, entry_time) VALUES ('{plate}', '{entry_time}');"
    cursor.execute(statement)

    # tells the user when the command executes successfully
    print(f"Added car '{plate}' with entry time {entry_time} to parking session list.")

# main

# testing
log_entry("ABC123", "2026-01-01 12:00:00")