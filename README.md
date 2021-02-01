# Attendance Formatter

## Purpose
This script takes in the path to a directory full of zoom attendance records.
It outputs the aggregates name and email of all attendants across all records.
Duplicates are removed.

## Usage
To use this script, pass the name of a directory full of attendance records to the program as a command line argument.
`python3 attendane_formatter.py Documents/this_weeks_attendance`

By default, the output goes to a terminal. To output to a file, simple use a redirect, like so:
`python3 attendane_formatter.py Documents/this_weeks_attendance > attendance.txt`
