import os
import sys

class Attendee:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def __eq__(self, other):
        return self.email == other.email
    
    def __hash__(self):
        return hash(self.email)
    
    def __repr__(self):
        return self.name + ',' + self.email


class Attendance:
    def __init__(self):
        self._attendees = set()
    
    def add_attendee(self, line):
        name, email, _, _ = line.split(',')

        new_attendee = Attendee(name, email)
        self._attendees.add(new_attendee)
    
    def attendees(self):
        return frozenset(self._attendees)
    
    def merge(self, other):
        self._attendees |= other.attendees()

    def add_file(self, filename):
        local_attendance = Attendance()
        try: 
            with open(filename) as f:
                at_names = False

                # Skip the lines above the whitespace, since they are not names
                while next(f).strip() != "":
                    continue
                
                next(f) # Skip the header line with the title "Name", "Email", etc

                for line in f:
                    local_attendance.add_attendee(line)

            self.merge(local_attendance)
        except:
            print(f"Error parsing file: {filename}")

    
    def add_all_files(self, root_directory):
        for (root, dirs, files) in os.walk(root_directory):
            for f in files:
                self.add_file(os.path.join(root, f))
        
    def __str__(self):
        return "\n".join([str(person) for person in self._attendees])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python ./attendance.py ${ATTENDANCE DIRECTORY}")
    else:
        directory = sys.argv[1]

        attendance = Attendance()
        attendance.add_all_files(directory)
        print(attendance)