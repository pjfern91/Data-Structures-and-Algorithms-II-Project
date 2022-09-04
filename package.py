# Package class used to initialize all data from the package data file
import datetime


class Package:
    def __init__(self, pid, address, city, state, zip_code, deadline, mass, special_notes):
        self.pid = pid
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip_code
        self.deadline = deadline
        self.mass = mass
        self.special_notes = special_notes
        self.status = None
        self.delivery_time = None

    def __str__(self):
        return "%s %s %s %s %s %s %s %s %s" % (self.pid, self.address, self.city, self.state, self.zip,
                                               self.deadline, self.mass, self.special_notes, self.status)

# check status function to check the status of a package at specific time. After comparing the input time with the
# delivery time and departure time we update the status accordingly with the correct status.
    def check_status(self, time):
        if self.pid == 9:
            if time >= datetime.timedelta(hours=10, minutes=20, seconds=0):
                self.address = "410 S State St"
                self.city = "Salt Lake City"
                self.state = "UT"
                self.zip = "84111"

        if time < self.departure_time:
            self.status = "\033[1;31m at hub \033[0m"

        elif time < self.delivery_time:
            self.status = "\033[1;33m en route \033[0m"

        else:
            self.status = f"\033[1;32m Package {self.pid} delivered at: {self.delivery_time} \033[0m"
