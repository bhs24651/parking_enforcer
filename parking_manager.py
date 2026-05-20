#!/bin/python3

# docstring
'''
parking_manager.py - A Management Interface for the Parking Enforcer Database Application.

Copyright (c) 2026 Jason Wu. All rights reserved.
'''

# imports
import sqlite3
import datetime

# constants and variables
DATABASE = "parking.db"
TIME_LIMIT = 60
MAX_PLATE_LENGTH = 8

# functions
def log_entry(plate, entry_time):
    # docstring
    'Creates a session in the parking session table with the vehicle\'s plate number and entry time, and exempts it from the time limit if applicable'

    # connects to the database
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # only execute the below statements if the plate does not already exist in an active session
    statement = "SELECT plate FROM sessions WHERE exit_time IS NULL;"
    cursor.execute(statement)
    results = cursor.fetchall()
    active_plates = list(result[0] for result in results)
    if plate in active_plates:
        print(f"Error: Plate '{plate}' already exists in an active session.")
        return

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

    # connects to the database
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # only execute the below statements if the plate already exists in an active session
    statement = "SELECT plate FROM sessions WHERE exit_time IS NULL;"
    cursor.execute(statement)
    results = cursor.fetchall()
    active_plates = list(result[0] for result in results)
    if plate not in active_plates:
        print(f"Error: Plate '{plate}' does not already exist in an active session.")
        return

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

    # only execute the below statements if the ID already exists in a currently unpaid breach
    statement = "SELECT id FROM sessions WHERE breach_status = 'unpaid';"
    cursor.execute(statement)
    results = cursor.fetchall()
    unpaid_breaches = list(int(result[0]) for result in results)
    if id not in unpaid_breaches:
        print(f"Error: No Breach with ID {id} found to mark Paid.")
        return

    # executes the statement to mark a breach as paid by session ID
    statement = f"UPDATE sessions SET breach_status = 'paid' WHERE id = {id};"
    cursor.execute(statement)

    # tells the user when the command executes successfully
    print(f"Marked Breach ID {id} as Paid.")

    # saves the new data and closes connection to the database
    db.commit()
    db.close()


def create_exemption(plate):
    # docstring
    'Creates an exemption by plate number to exempt future sessions by that plate number from the parking time limit'

    # connects to the database
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # execute the statement to create a new exemption with that plate
    statement = f"INSERT INTO exemptions (plate) VALUES ('{plate}');"
    cursor.execute(statement)

    # tell the user when the command executes successfully
    print(f"Created new exemption for '{plate}'.")
    
    # saves the new data and closes connection to the database
    db.commit()
    db.close()


def list_exemptions():
    # docstring
    'Lists out all the exemption entries'

    # connects to the database
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # executes the statement to pull all exemption entries
    statement = "SELECT * FROM exemptions;"
    cursor.execute(statement)
    # ... and stores it in a variable
    results = cursor.fetchall()

    # prints the results as tuples for now (TODO: Add pretty printing)
    for line in results:
        print(line)
    
    # closes connection to database
    db.close()


def delete_exemption(plate):
    # docstring
    'Deletes an exemption by plate number'

    # connects to the database
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # execute the statement to delete the exemption associated with that plate
    statement = f"DELETE FROM exemptions WHERE plate = '{plate}';"
    cursor.execute(statement)

    # tell the user when the command executes successfully
    print(f"Deleted exemption for '{plate}'.")
    
    # saves the new data and closes connection to the database
    db.commit()
    db.close()


def cleanup(days):
    # docstring
    'Cleans up non-breach and breach-paid parking sessions that are more than specified number of days old'

    # connects to the database
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # execute the statement to clean up old parking records
    statement = f"DELETE FROM sessions WHERE (unixepoch('now') - unixepoch(exit_time)) / 86400.0 > {days} AND (breach_status IS NULL OR breach_status = 'paid');"
    cursor.execute(statement)

    # tells the user when the command eecutes successfully
    print(f"Cleaned up old records greater than {days} days old.")

    # saves the new data and closes connection to the database
    db.commit()
    db.close()


# main

print("Welcome to Parking Enforcer v1.0!")
print("Type 'h' for a list of commands.")
# command input logic
while True:
    command = input("parking_enforcer> ").split()
    if command[0] == "h":
        print("\n"\
              "LIST OF AVAILABLE COMMANDS:\n"\
              "    n <plate> <ISO8601_entry_timestring*> : Insert entry into parking sessions with given entry time\n"\
              "    a : List currently active sessions (sessions with no exit time)\n"\
              "    x <plate> <ISO8601_exit_timestring*> : Update vehicle's session entry with exit time\n"\
              "    b : List currently unpaid breaches\n"\
              "    p <session_id> : Mark breach as paid by session ID\n"\
              "    ec <plate> : Create exemption entry\n"\
              "    el : List all exemption entries\n"\
              "    ed <plate> : Delete exemption entry for plate number\n"\
              "    c <days> : Cleans up old non-breach and breach-paid parking sessions that are more than specified number of days old\n"\
              "    tl <time_limit_minutes> : Update the time limit to specified number of minutes\n"\
              "    h : Show this help message\n"\
              "    q : Quit this program\n"\
              "\n"\
              "*Note on ISO8601 timestrings: They are to be in the format \"yyyy-mm-ddThh:mm:ss\", where lowercase letters are to be replaced with the appropriate numbers.\n"
              )
    elif command[0] == "q":
        # command to quit the program
        print("See you next time...")
        break
    elif command[0] == "n":
        try:
            # parse the 'n' command
            plate = command[1].upper()
            entry_time = command[2]
            
            # reject plates with symbols or plates that are excessively long
            if not plate.isalnum() or len(plate) > MAX_PLATE_LENGTH:
                print("Error: Plate either contains symbols or is excessively long. Remove unnecessary characters from plate and try again.")
                continue
            
            # validates the timestring
            entry_time_object = datetime.datetime.fromisoformat(entry_time)
            parsed_timestamp = entry_time_object.timestamp() # should fail if timestring is invalid

            # if all checks passed, run log_entry
            log_entry(plate, entry_time)
        except:
            # if something goes wrong with syntax parsing (invalid arguments or invalid timestring)...
            print("Invalid command syntax. See 'h' for usage details.")
    elif command[0] == "a":
        # run list_active to fetch all active session data 
        list_active()
    elif command[0] == "x":
        try:
            # parse the 'x' command
            plate = command[1].upper()
            exit_time = command[2]
            
            # reject plates with symbols or plates that are excessively long
            if not plate.isalnum() or len(plate) > MAX_PLATE_LENGTH:
                print("Error: Plate either contains symbols or is excessively long. Remove unnecessary characters from plate and try again.")
                continue
            
            # validates the timestring
            exit_time_object = datetime.datetime.fromisoformat(exit_time)
            parsed_timestamp = exit_time_object.timestamp() # should fail if timestring is invalid

            # if all checks passed, run log_exit
            log_exit(plate, exit_time)
        except:
            # if something goes wrong with syntax parsing (invalid arguments or invalid timestring)...
            print("Invalid command syntax. See 'h' for usage details.")
    elif command[0] == "b":
        # run list_active to fetch all unpaid breach data 
        list_breaches()
    elif command[0] == "p":
        try:
            # parse the 'p' command
            id = int(command[1])

            # if parsing passed, run pay_breach
            pay_breach(id)
        except:
            # if something goes wrong with syntax parsing (invalid arguments or invalid timestring)...
            print("Invalid command syntax. See 'h' for usage details.")
        
    # add more commands here...
    else:
        # command not found
        print("Unrecognized command. Type 'h' for a list of commands.")
