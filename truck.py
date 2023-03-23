"""
the time complexity analysis:

"""
from Hash import Hash
from graph import Graph, read_distance_file, Vertex
from package import Package, load_packages
from datetime import datetime, time, timedelta

class Truck:
    def __init__(self, map: Graph, time):
        self.storage = Hash()
        self.travelled_distance = 0
        self.route = None
        self.status_log = []
        self.time = time
        self.speed = 18
        self.map = map
        self.current_location = self.map.get_vertex("HUB")
        self.package_count = 0

    def load(self, pkg):
        # Add package to the storage hash table with the destination as the key
        # additionally, add an extra layer to the insertion such that if there is an address collision,
        # instead of overwriting the value, append the new package to it so all
        # packages at the same address are stored together
        temp = self.storage.get(pkg.destination)
        if temp:
            temp[1].append(pkg)
        else:
            self.storage.set(pkg.destination, [pkg])
        pkg.update_status((self.time, "loaded on truck and en route"))
        self.package_count += 1

    def go_to_address(self, next_loc):
        # Calculate the distance to the next location and update the truck's total travelled distance
        distance = next_loc.get_weight(self.current_location.id)
        self.travelled_distance += distance

        # Calculate the time required to travel the distance and update the truck's current time
        delta = timedelta(minutes=(distance * 60 / 18))
        self.time = (datetime.combine(datetime.min, self.time) + delta).time()

        # Move the truck to the next location and mark it as visited
        self.current_location = next_loc
        self.current_location.visit()

    def deliver(self, package):
        # Update the package's status to 'Delivered' and adjust the package count and delivered_packages accordingly
        package.update_status((self.time, "Delivered"))
        self.package_count -= 1


    def get_deliverables(self, address):
        # Return the list of packages associated with the given address from the truck's storage hash table
        if isinstance(address, Vertex):
            return self.storage.get(address.id)
        else:
            return self.storage.get(address)

    def get_next(self):
        # Generate a list of unvisited locations that the truck needs to deliver packages to
        next_address_list = [loc for loc in self.storage.keys() if not self.map.get_vertex(loc).is_visited() and loc != "bad"]

        min_distance = float('inf')  # Initialize the minimum distance as infinity
        result = None  # Initialize the result to None

        for addr in next_address_list:
            # Retrieve the deadline of packages at the address
            deadlines = [package.deadline for package in self.get_deliverables(addr)[1]]
            is_priority = False

            # Check if there's a package with a priority deadline
            for deadline in deadlines:
                if deadline <= time(hour=10, minute=30):
                    is_priority = True

            vertex = self.map.get_vertex(addr)  # Get the vertex object for the address
            # Calculate the distance from the current location to the address
            distance = self.current_location.get_weight(vertex.id)

            # Subtract 100 from the distance if the address contains a priority package
            if is_priority:
                distance = distance - 100

            # Compare the calculated distance with the current minimum distance
            # If the calculated distance is less than the minimum distance,
            # update the minimum distance and the result (next location)
            if distance < min_distance:
                min_distance = distance
                result = vertex

        # Return the next location (vertex) with the minimum distance from the current location
        return result   



