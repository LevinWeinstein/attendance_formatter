#! /usr/bin/env python3

"""
Filename     : attendance.py
Author       : Levin Weinstein
Organization : USF CS212 Spring 2021
Purpose      : Convert a directory full of attendance lists to a single, aggregated attendance sheet
Usage        : ./attendance.py --directory="DIRECTORY" --event=[lecture|lab] > ${OUTPUT_FILE}
"""

import os
import sys
import argparse

class Attendee:
    """ A class for an individual Attendee, with a name and an email"""

    def __init__(self, name, email):
        """ constructor for the Attendee class

        :param name:  the name of the attendee
        :param email: the email of the attendee
        """
        self.name = name
        self.email = email
    
    def __eq__(self, other):
        """ Equals operator for the Attendee class
        
        We're just using email to determine equivalency for the sake of simplicity.
        
        :param other: the other Attendee to which to compare
        """
        return self.email == other.email
    
    def __hash__(self):
        """ Hash code """
        return hash(self.email)
    
    def __str__(self):
        """ convert an Attendee to string """
        return self.name + ',' + self.email


class Attendance:
    """ A class to take the attendance.

    Contains methods to:
        - add an attendee
        - add a whole file
        - add a whole directory of files
        - a getter for an unmodifiable set of the attendees
        - merge another Attendance set
    """

    def __init__(self, event_type=""):
        """ An initializer for the Attendance """ 
        self._attendees = set()
        self.event_type = event_type

    def add_attendee(self, line):
        """ Method to add an attendee 
        
        :param line: the line from which to parse and add an attendee
        """
        name, email, _, _ = line.split(',')

        new_attendee = Attendee(name, email)
        self._attendees.add(new_attendee)
    
    def add_file(self, filename):
        """ Method to add all attendees from a file

        :param filename: the name of the file
        """
        local_attendance = Attendance(self.event_type)
        try: 
            with open(filename) as f:
                at_names = False

                # Skip the lines above the whitespace, since they are not names
                next(f) # skip the top part header line

                _, topic, _, _, _, _, _, _ = next(f).split(',')
                print(topic, file=sys.stderr)

                if self.event_type not in topic.lower():
                    print(f"Wrong event type. Skipping {filename}", file=sys.stderr)
                    return           
                next(f) # Skip the blank line
                next(f) # Skip the header line with the title "Name", "Email", etc

                for line in f:
                    local_attendance.add_attendee(line)

            self.merge(local_attendance)
        except:
            print(f"Error parsing file: {filename}")

    
    def add_all_files(self, root_directory):
        """Adds all files from the given directory

        :param root_directory: the directory within which to search for attendance files
        """
        for (root, dirs, files) in os.walk(root_directory):
            for f in files:
                self.add_file(os.path.join(root, f))
    
    def attendees(self):
        """A getter for the _attendees set

        :return: an immutable frozenset with the contents of the _attendees set
        """
        return frozenset(self._attendees)
    
    def merge(self, other):
        """Merge another Attendance sheet into this one

        :param other: the other Attendance sheet with which to merge
        """
        self._attendees |= other.attendees()


        
    def __str__(self):
        """ convert the Attendance to string """
        attendees = sorted(self._attendees, key=lambda person: person.email)
        return "\n".join([str(person) for person in attendees])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert a directory full of attendance lists to a single, aggregated attendance sheet")
    parser.add_argument("-e", "--event", help="The event type. Can be either lecture or lab", required=True)
    parser.add_argument("-d", "--directory", help="The directory within which to parse.", required=True)

    arguments = parser.parse_args()
    attendance = Attendance(arguments.event)
    attendance.add_all_files(arguments.directory)

    print(attendance)
