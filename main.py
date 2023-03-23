#FirstName: Andrew, LastName: Cichewicz, StudentID: 010514987

import Hash
from datetime import time
import package
import truck
import graph


#
def get_package_status(time, package_list):
    print(f"package statuses at time: {time}")
    for package in package_list:
        status = package.status
        for i, entry in enumerate(status):
            if i >= len(status)-1:
                print(f"{package.id}: {entry[1]}")
                break
            if time < entry[0] and i == 0:
                print(f"{package.id}: {entry[1]}")
                break
            if time >= entry[0] and time < status[i+1][0]:
                print(f"{package.id}: {entry[1]}")
                break
def update_packages(index, package, truck):
    if truck.time >= package.update_time:
        to_update = truck.storage.get(package.destination)[1][0]
        truck.storage.remove("bad")
        to_update.destination = "300 State St"
        truck.storage.set(to_update.destination, [to_update])
        bad_packages.pop(index)





address_graph = graph.read_distance_file()
packages = package.load_packages()
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
    if truck2.delivered_packages == 8:
        pass
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
    print(f"{package.id}: {package.status[-1][1]},{package.status[-1][0]}, Deadline: {package.deadline}")


response = None
while response != -1:
    response = input("Plesae make a selection:\n1. get status of individual package\n2. get status of all packages\n3. look up package info")



