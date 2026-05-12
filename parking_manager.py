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
    print(f"Created session for '{plate}' with entry time {entry_time}.")

    # saves the new data and closes connection to the database
    db.commit()
    db.close()

def log_exit(plate, exit_time):
    # connects to the database
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # executes the statement to update the current session's entry with an exit time
    statement = f"UPDATE sessions SET exit_time = '{exit_time}' WHERE plate = '{plate}' AND exit_time IS NULL;"
    cursor.execute(statement)

    # tells the user when the command executes successfully
    print(f"Updated session for '{plate}' with exit time {exit_time}.")

    # saves the new data and closes connection to the database
    db.commit()
    db.close()

# main

# testing
log_entry("ABC123", "2026-01-01 12:00:00")
log_exit("ABC123", "2026-01-01 12:30:00")