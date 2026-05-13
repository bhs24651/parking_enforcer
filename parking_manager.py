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
TIME_LIMIT = 60

# functions
def log_entry(plate, entry_time):
    # TODO: Add input sanitization to prevent breaking the software

    # connects to the database
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # executes the statement to insert a new session entry into the database
    statement = f"INSERT INTO sessions (plate, entry_time) VALUES ('{plate}', '{entry_time}');"
    cursor.execute(statement)

    # executes another statement to exempt the vehicle's session if applicable
    statement = "UPDATE sessions SET is_exempted = 1, exemption_id = exemptions.id FROM exemptions WHERE sessions.plate = exemptions.plate AND exit_time IS NULL;"
    cursor.execute(statement)

    # tells the user when the statements execute successfully
    print(f"Created session for '{plate}' with entry time {entry_time}.")

    # saves the new data and closes connection to the database
    db.commit()
    db.close()

def log_exit(plate, exit_time):
    # TODO: Add input sanitization to prevent breaking the software

    # connects to the database
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # executes the statement to update the current session's entry with an exit time
    statement = f"UPDATE sessions SET exit_time = '{exit_time}' WHERE plate = '{plate}' AND exit_time IS NULL;"
    cursor.execute(statement)

    # executes another statement to determine if that session was in breach of the parking time limit
    statement = F"UPDATE sessions SET breach_status = 'unpaid' WHERE (unixepoch(exit_time) - unixepoch(entry_time)) / 60.0 > {TIME_LIMIT} AND is_exempted = 0 AND breach_status IS NULL;"
    cursor.execute(statement)

    # tells the user when the command executes successfully
    print(f"Updated session for '{plate}' with exit time {exit_time}.")

    # saves the new data and closes connection to the database
    db.commit()
    db.close()

# main

# testing
log_entry("ABC123", "2026-01-01 12:00:00")
log_exit("ABC123", "2026-01-01 13:30:00")