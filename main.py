# Author: Phil Fernandez
# StudentID: 001394824
import datetime
from hashtable import ChainingHashTable
from package import Package
from truck import Truck
import csv


# Reads all the package data and inputs into a hashmap
def load_package_data(filename):
    with open(filename) as packages:
        package_data = csv.reader(packages, delimiter=',')
        for package in package_data:
            package_id = int(package[0])
            package_address = package[1]
            package_city = package[2]
            package_state = package[3]
            package_zip = package[4]
            package_deadline = package[5]
            package_mass = package[6]
            package_notes = package[7]
            # package_delivery_time = package[8]

            package = Package(package_id, package_address, package_city, package_state, package_zip,
                              package_deadline, package_mass, package_notes)

            package_hash.insert(package_id, package)


package_hash = ChainingHashTable()
load_package_data('Files/WGUPS Package File.csv')


# my_package = package_hash.search(1).mass -> used for debugging and testing
# print(my_package)


# Reads the Distance file and inputs all the distances into a 2d list. In order to load the distances, the program must
# first loop through the rows and columns in the distance files list.
def load_distance_data():
    with open('Files/Distance File.csv') as distances:
        distance_data = []
        data = csv.reader(distances, delimiter=',')
        for distance in data:
            row = []
            for col in distance:
                if col != '':
                    row.append(float(col))
                else:
                    row.append(None)
            distance_data.append(row)
    return distance_data


dData = load_distance_data()
# print(dData) --> used for debugging/testing


# Reads the address file and inputs only the address into a list
def load_address_data():
    with open('Files/Address File.csv') as addresses:
        mydata = []
        address_data = csv.reader(addresses, delimiter=',')
        for address in address_data:
            mydata.append(address[2])
    return mydata


aData = load_address_data()
# print(aData)


# function to get the distance between to given address, uses a simple return statement
# to grab the data from the distance file, between 26 addresses, any distance can be found by
# simply getting the targeted index in the 2d list. O(1) space and time complexity.
def distance_between_addresses(address1, address2):
    if dData[aData.index(address1)][aData.index(address2)] == None:
        return dData[aData.index(address2)][aData.index(address1)]
    else:
        return dData[aData.index(address1)][aData.index(address2)]


# distance_between = distance_between_addresses('4001 South 700 East', '1060 Dalton Ave S')--> used for debug/test
# print(distance_between)

truck1 = Truck(1, [1, 5, 7, 8, 10, 13, 14, 15, 16, 19, 20, 21, 22, 29, 34, 37],
               18, datetime.timedelta(hours=8, minutes=0, seconds=0))
truck2 = Truck(2, [2, 3, 9, 11, 12, 17, 18, 23, 24, 33, 27, 35, 36, 38, 39],
               18, datetime.timedelta(hours=10, minutes=20, seconds=0))
truck3 = Truck(3, [4, 6, 25, 26, 28, 30, 31, 32, 40], 18, datetime.timedelta(hours=9, minutes=15, seconds=0))


# The min_distance_from function loops through a list of packages(truck), takes the package id(pid) and uses that id to
# search the hash table for the address associated with that id, passes the address to the
# distance_between_address function and compares the "from address"(f_address) to the address we retrieved after
# searching the hash table (p_address). It takes the distance between those two address and updates the "min_dist"
# variable. The function checks if the package has a delivery time (i.e. the package has been delivered), and if not,
# continues. The algorithm runs at O(n) time.
def min_distance_from(f_address, t_packages):
    min_dist = 10000.0
    next_pid = 0
    next_address = ''
    for pid in t_packages:
        package = package_hash.search(pid)
        p_address = package.address
        if package.delivery_time != None: continue
        dist = distance_between_addresses(f_address, p_address)
        if dist < min_dist:
            min_dist = dist
            next_pid = pid
            next_address = p_address
    return min_dist, next_pid, next_address


# print(min_distance_from('4001 South 700 East', truck1.packages)) --> used for debugging

# The deliver_packages function will loop through a truck(list) until there are no more packages to deliver. The
# function starts by getting the min_distance_from starting at the starting address(f_address), which starts at the hub
# for each truck(list). After returning from the min_distance_from function with a distance, a package id(delivered_id),
# and an address associated with the package delivered(delivered_address), the algorithm will update the time traveled
# starting at the trucks starting time, as well as the miles traveled, which starts at 0.0. The algorithm will also
# update the departure time of each package by setting the departure time to the time the last package was delivered and
# also change the delivery time of each package to the time retrieved from the updated time object after each package is
# visited. Finishes by return the miles(float) and the time(str). Runtime complexity of O(n) as we only loop through
# the truck one time, but also have to call the min_distance_from function which also runs at O(n). Making this
# algorithm run in polynomial time O(n^2) ---> O(n) * O(n) ---> O(n*n) or O(n^2)
def deliver_packages(truck_list, start_time):
    f_address = '4001 South 700 East'  # this is the "Hub" address where each truck will start from when delivering
    miles = 0.0
    time = start_time
    while len(truck_list) != 0:
        distance, delivered_id, delivered_address = min_distance_from(f_address, truck_list)
        if delivered_id == 0:
            break
        package = package_hash.search(delivered_id)
        truck_time_seconds = (distance / 18) * 60 * 60
        f_address = delivered_address
        time += datetime.timedelta(seconds=truck_time_seconds)
        truck_list.remove(delivered_id)
        package.departure_time = start_time
        package.delivery_time = time
        miles += distance
        # print(package.status) --> used for debugging
    return miles, str(time)


truck1_miles, truck1_end_time = deliver_packages(truck1.packages, truck1.start_time)
truck2_miles, truck2_end_time = deliver_packages(truck2.packages, truck2.start_time)
truck3_miles, truck3_end_time = deliver_packages(truck3.packages, truck3.start_time)
# print("%.1f" % truck1_miles, truck1_end_time, "%.1f" % truck2_miles, truck2_end_time, "%.1f" % truck3_miles,
#      truck3_end_time)

total_miles_traveled = "%.2f" % (truck1_miles + truck2_miles + truck3_miles)
# print("Total miles traveled: " + "%.2f" % total_miles_traveled)

# Our UI for the program. Has 4 options to choose from. The first option prints the total miles traveled between all
# trucks. The second print the status of a specific package at specific time. The third option prints the status of all
# packages at a specific time. And the fourth option just exits the program.
if __name__ == '__main__':
    print("Welcome to the WGUPS Routing Program!")

    is_exit = True
    while is_exit:
        print("Options:")
        print("1. Total miles traveled by all trucks:")
        print("2. Status of a package at a certain time:")
        print("3. Status of all packages at a certain time:")
        print("4. Exit Program")
        option = input("Select a number from the options above...")
        if option == "1":
            print(f"\033[1;34mTotal miles traveled between all trucks: {total_miles_traveled}\033[0m")

        elif option == "2":
            input_id = input("Enter a Package ID ")
            input_time = input("Enter a time in the form HH:MM:SS ")
            package = package_hash.search(int(input_id))
            hour, minute, second = input_time.split(":")
            check_time = datetime.timedelta(hours=int(hour), minutes=int(minute), seconds=int(second))
            package.check_status(check_time)
            print(package)

        elif option == "3":
            input_time = input("Enter a time in the form HH:MM:SS ")
            hour, minute, second = input_time.split(":")
            check_time = datetime.timedelta(hours=int(hour), minutes=int(minute), seconds=int(second))
            for p in range(1, 41):
                package = package_hash.search(p)
                package.check_status(check_time)
                print(package)
            print(f"\033[1;34mChecking status of all packages at: {input_time}\033[0m")

        elif option == "4":
            is_exit = False

        else:
            print("\033[1;31m Invalid selection. Please select a valid option from the list above.\033[0m")
