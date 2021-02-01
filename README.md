# Attendance Formatter

## Purpose
This script takes in the path to a directory full of zoom attendance records.
It outputs the aggregates name and email of all attendants across all records.
Duplicates are removed.

## Usage
To use this script, pass the name of a directory full of attendance records to the program as a command line argument.
<br />
`/attendance.py --directory="DIRECTORY" --event=[lecture|lab] > ${OUTPUT_FILE}`

By default, the output goes to a terminal. To output to a file, simple use a redirect, like so:
<br />
`./attendance_formatter.py -d=Documents/this_weeks_lecture --event=lecture > lecture_attendance.txt`
<br />
`./attendance_formatter.py -d=Documents/this_weeks_lab --even=lab > lab_attendance.txt`
