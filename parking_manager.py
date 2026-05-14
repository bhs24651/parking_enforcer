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
    # docstring
    'Creates a session in the parking session table with the vehicle\'s plate number and entry time, and exempts it from the time limit if applicable'

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


def list_active():
    # docstring
    'Lists out all the currently active sessions (i.e. sessions with no exit time)'

    # connects to the database
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # executes the statement to pull all currently active sessions from the session table
    statement = "SELECT id, plate, entry_time, is_exempted FROM sessions WHERE exit_time IS NULL;"
    cursor.execute(statement)
    # ... and stores it in a variable
    results = cursor.fetchall()

    # print the results as tuples for now (TODO: Add pretty printing)
    for line in results:
        print(line)
    
    # closes connection to the database
    db.close()


def log_exit(plate, exit_time):
    # docstring
    'Updates the currently active session associated with the plate number with an exit time, and determines compliance with the parking time limit'

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


def list_breaches():
    # docstring
    'Lists out all the sessions in breach of the parking limit and is marked unpaid'

    # connects to the database
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # executes the statement to pull all currently unpaid breaches
    statement = "SELECT id, plate, entry_time, exit_time, breach_status FROM sessions WHERE breach_status = 'unpaid';"
    cursor.execute(statement)
    # ... and stores it in a variable
    results = cursor.fetchall()

    # prints the results as tuples for now (TODO: Add pretty printing)
    for line in results:
        print(line)
    
    # closes connection to database
    db.close()


def pay_breach(id):
    # docstring
    'Marks a breach as paid by session ID'

    # connects to the database
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # executes the statement to mark a breach as paid by session ID
    statement = f"UPDATE sessions SET breach_status = 'paid' WHERE id = {id};"
    cursor.execute(statement)

    # tells the user when the command executes successfully
    print(f"Marked Breach ID {id} as Paid.")

    # saves the new data and closes connection to the database
    db.commit()
    db.close()


# main

# testing entry logging
log_entry("ABC123", "2026-01-01 12:00:00")
log_entry("ABC124", "2026-01-01 12:00:00")

# testing list active sessions function
list_active()

# testing exit logging with a session not in breach
log_exit("ABC123", "2026-01-01 12:30:00")
# testing exit logging with a session in breach
log_exit("ABC124", "2026-01-01 13:30:00")

# testing list unpaid breaches function
list_breaches()

# testing mark breach as paid function
pay_breach(2)