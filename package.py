import re
from datetime import datetime, time

# a simple data class to hold package information in a way that is easily retrievable.
class Package:
    def __init__(self, id, destination, city, state, zip, deadline, mass, notes, update_time=None):
        self.id = id
        self.destination = destination
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.notes = notes
        self.status = []
        self.update_time = update_time

    def update_status(self, status):
        self.status.append(status)



def load_packages():
    packages = []
    # read the packages from the package csv file and format the data to be usable with the package data class.h
    with open("./data/packages.csv") as pkg:
        lines = pkg.readlines()
        for line in lines:
            id, dest, city, state, zip, dead, mass, notes, *rest = line.strip().split(",")
            if dead == "EOD":
                dead = datetime.strptime("5:00 pm", "%I:%M %p").time()
            else:
                dead = datetime.strptime(dead, "%I:%M %p").time()
            packages.append(Package(id, dest, city, state, zip, dead, mass, notes))
    number_extractor = r'(\d+:\d+)'
    for package in packages:
        # package 9 is known to posess the wrong address. therefore we set the destination to the "bad" address.
        if package.id == "9":
            package.destination = "bad"
            package.update_time = time(hour=10, minute=20)
        # update the delayed packages to reflect the appropriate time they arrived at the hub.
        if "Delayed" in package.notes:
            extracted = re.search(number_extractor, package.notes)
            extracted_time = datetime.strptime(extracted.group(0), "%I:%M").time()
            package.update_status((time(hour=8, minute=0), "En route to hub"))
            package.update_status((extracted_time, "At HUB"))
        else:
            package.update_status((time(hour=8, minute=0), "At HUB"))
    return packages



