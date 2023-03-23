#FirstName: Andrew, LastName: Cichewicz, StudentID: 010514987

import Hash
from datetime import time
from Hash import Hash
import package
import truck
import graph


# a simple function to retrieve the status of packages at a given time, cales with any number of packages.
def get_package_status(time, package_list):
    print(f"package statuses at time: {time}")
    #iterate over the provided list of packages.
    for package in package_list:
        #retrieve the array of statuses in the package data object
        status = package.status
        #for each entry in the status array check several conditions
        for i, entry in enumerate(status):
            # if the provided time is greater than the time at the end of the array, provide the last entry
            if i >= len(status)-1:
                print(f"{package.id}: {entry[1]}")
                break
            # if the provided time is less than the first entry, provide the first entry which is always "at hub"
            if time < entry[0] and i == 0:
                print(f"{package.id}: {entry[1]}")
                break
            # lastly if the provided time is greater than or equal to the status time of the entry
            # and less than the next entry, return current entry status.
            if time >= entry[0] and time < status[i+1][0]:
                print(f"{package.id}: {entry[1]}")
                break
# a function to run and check for packages with incorrect packages, simulating the right address being added
def update_packages(index, package, truck):
    if truck.time >= package.update_time:
        to_update = truck.storage.get(package.destination)[1][0]
        truck.storage.remove("bad")
        to_update.destination = "300 State St"
        truck.storage.set(to_update.destination, [to_update])
        bad_packages.pop(index)


address_graph = graph.read_distance_file()
packages = package.load_packages()
package_id_hash = Hash()

for package in packages:
    package_id_hash.set(package.id, package)
bad_packages = [package for package in packages if package.destination == "bad"]
temp_packages = []
truck1 = truck.Truck(address_graph, time(hour=8, minute=0))
truck2 = truck.Truck(address_graph, time(hour=9, minute=5))
truck3 = truck.Truck(address_graph, truck2.time)
truck1_list = []
truck2_list = []
truck3_list = []

temp_packages = [package for package in packages if not package.notes and package.id != "13"]
for package in packages:
    if package.notes or package.id == "13":
        truck2.load(package)
        truck2_list.append(package.id)
no_deadline_packages = [package for package in temp_packages if package.deadline == time(hour=17)]
deadline_packages = [package for package in temp_packages if package.deadline < time(hour=17)]
i = 0
j = 0
while truck1.package_count < 14:
    if i < len(deadline_packages):
        truck1.load(deadline_packages[i])
        truck1_list.append(deadline_packages[i].id)
        i += 1
        continue
    truck1.load(no_deadline_packages[j])
    truck1_list.append(temp_packages[j].id)
    j += 1
no_deadline_packages = no_deadline_packages[j:]

while truck1.package_count > 0:
    next = truck1.get_next()
    truck1.go_to_address(next)
    deliverables = truck1.get_deliverables(next)[1]
    for deliverable in deliverables:
        truck1.deliver(deliverable)
truck1.go_to_address(address_graph.get_vertex("HUB"))
address_graph.clear_visits()
while truck2.package_count > 0:
    for i, pkg in enumerate(bad_packages):
        update_packages(i, pkg, truck2)
    next = truck2.get_next()
    truck2.go_to_address(next)
    deliverables = truck2.get_deliverables(next)[1]
    for deliverable in deliverables:
        truck2.deliver(deliverable)
truck2.go_to_address(address_graph.get_vertex("HUB"))
truck3.time = truck2.time
address_graph.clear_visits()
for package in no_deadline_packages:
    truck3.load(package)
    truck3_list.append(package.id)
while truck3.package_count > 0:
    next = truck3.get_next()
    truck3.go_to_address(next)
    deliverables = truck3.get_deliverables(next)[1]
    for deliverable in deliverables:
        truck3.deliver(deliverable)
truck3.go_to_address(address_graph.get_vertex("HUB"))


print(f"Distance traveled:\n truck1: {truck1.travelled_distance} miles\n "
      f"truck2: {truck2.travelled_distance}miles\n truck3: {truck3.travelled_distance} miles")
print(f"Total distance travelled: {truck1.travelled_distance + truck2.travelled_distance + truck3.travelled_distance}")
print("packages on truck 1: ", truck1_list, f"total: {len(truck1_list)}")
print("packages on truck 2: ", truck2_list, f"total: {len(truck2_list)}")
print("packages on truck 3: ", truck3_list, f"total: {len(truck3_list)}")

for package in packages:
    if package.deadline < package.status[-1][0]:
        print(f"{package.id} is late, delivered at {package.status[-1][0]}, deadline was {package.deadline}")

for package in packages:
    print(f"{package.id}: {package.status[-1][1]}: {package.status[-1][0]}, Deadline: {package.deadline}")

response = None
while response != -1:
    response = input("Plesae make a selection:\n1. get status of all packages\n2. look up package info\nResponse: ")
    if response == "1":
        hours = input("please enter the desired hour: ")
        minutes = input("please enter the desired minute ")
        get_package_status(time(hour=int(hours), minute=int(minutes)), packages)
    if response == "2":
        option =  0
        while option != -1:
            pkg_id = input("PackageID: ")
            package = package_id_hash.get(pkg_id)[1]
            # Ask user input
            print('What package information do you want to see?')
            print('1. Package ID number')
            print('2. Delivery address')
            print('3. Delivery deadline')
            print('4. Delivery city')
            print('5. Delivery zip code')
            print('6. Package weight')
            print('7. Delivery status')

            option = int(input('Enter option number: '))

            # Print desired information
            if option == 1:
                print('Package ID number:', package.id)
            elif option == 2:
                print('Delivery address:', package.destination)
            elif option == 3:
                print('Delivery deadline:', package.deadline)
            elif option == 4:
                print('Delivery city:', package.city)
            elif option == 5:
                print('Delivery zip code:', package.zip)
            elif option == 6:
                print('Package weight:', package.mass)
            elif option == 7:
                hours = input("please enter the desired hour: ")
                minutes = input("please enter the desired minute ")
                get_package_status(time(hour=int(hours), minute=int(minutes)), [package])
            elif option == -1:
                continue
            else:
                print('Invalid option number. Please try again.')


