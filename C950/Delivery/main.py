#Manuel Perez ID: 001257391
import csv
import datetime

import Truck
from HashTable import CreateHashTable
from Package import Package

#Reads distance file
with open("CSV/Distance_file.csv", newline='') as f1:
    CSV_Distance = list(csv.reader(f1))
#Read address
with open("CSV/Address.csv", newline='') as f2:
    CSV_Address = list(csv.reader(f2))

#read package info
with open("CSV/Package_File.csv", newline='') as f3:
    CSV_Package = list(csv.reader(f3))

#create package objects from the CSV file and loads them into the table
def load_package_data(filename, packHashTable):
    with open(filename) as package_info:
        package_data = csv.reader(package_info, delimiter=',')
        for package in package_data:
            if not package or not package[0].isdigit():
                continue
            pack_ID = int(package[0])
            pack_Address = package[1]
            pack_City = package[2]
            pack_State = package[3]
            pack_Zip = package[4]
            pack_Deadline = package[5]
            pack_Weight = package[6]
            pack_Status = "At Hub"
            #creates package object
            new_package = Package(pack_ID, pack_Address, pack_Zip, pack_City, pack_Deadline, pack_Weight, pack_Status)

            #Inserts data into hash table
            packHashTable.insert(pack_ID, new_package)


#create hash table
packHashTable = CreateHashTable()
#inserts packages into hash table
load_package_data("CSV/Package_File.csv",packHashTable)

# Assign delay times to packages delayed on flight until 9:05 AM
delayed_package_ids = [6, 25, 28, 32]
for pkg_id in delayed_package_ids:
    package = packHashTable.lookup(pkg_id)
    if package:
        package.delay_time = datetime.timedelta(hours=9, minutes=5)

#Finds distance between two addresses by reading the CSV and then returns a float
def distance(x, y):
    dist = CSV_Distance[x][y]
    if dist == '':
        dist = CSV_Distance[y][x]
    return float(dist)

#Converts street address into matrix index int
def readAddress(address):
    for row in CSV_Address:
        if address in row[2]:
            return int(row[0])
#Manually loading trucks
truck1 = Truck.Truck(0.0, 18, [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 40, 33, 35, 37, 39], 16, datetime.timedelta(hours=8, minutes=0), "4001 South 700 East")
truck2 = Truck.Truck(0.0, 18, [3, 6, 18, 25, 28, 32, 34, 36, 38, 2, 4, 5, 7, 8, 10, 11], 16, datetime.timedelta(hours=9, minutes=5), "4001 South 700 East")
truck3 = Truck.Truck(0.0, 18, [9, 21, 22, 23, 24, 26, 27, 12, 17], 16, datetime.timedelta(hours=10, minutes=20), "4001 South 700 East")

#greedy algorithim for  routes
def load_Trucks(truck, truck_number):
    #loads packages that aren't delivered into an array
    not_loaded =[]
    for packageID in truck.load:
        package = packHashTable.lookup(packageID)
        not_loaded.append(package)
    #clears package list of a truck so the list can be repopulated and sorted by the algorithm
    truck.load.clear()

    while len(not_loaded)> 0:
        next_address = float('inf')
        next_package_id = None
        for package in not_loaded:
            #loop where the nearest neighbor algorithm sorts and set the truck routes
            truck_idx = readAddress(truck.destination)
            pkg_idx = readAddress(package.address)
            dist = distance(truck_idx, pkg_idx)

            if dist <next_address:
                next_address = dist
                next_package_id = package
                #adds closets package to truck list
        truck.load.append(next_package_id)
                #removes package from un loaded package list
        not_loaded.remove(next_package_id)
                #adds the distance traveled to the mileage attribute
        truck.mileage += next_address
                #updates truck's current address
        truck.destination = next_package_id.address
                #updates the amount of time the truck took to delivery a package
        truck.time += datetime.timedelta(hours=next_address/18)
        next_package_id.delivery_time = truck.time
        next_package_id.departure_time = truck.depart_time
        next_package_id.truck_number = truck_number


#loading trucks
load_Trucks(truck1, 1)
load_Trucks(truck2, 2)
#truck 3 leaves  after both truck1 and truck2 have left
truck3.depart_time = max(truck1.time, datetime.timedelta(hours=10, minutes=20))
truck3.time = truck3.depart_time

# Update Package 9's address attributes BEFORE generating Truck 3's route
package9 = packHashTable.lookup(9)
package9.address = "410 S State St"
package9.zipcode = "84111"

load_Trucks(truck3, 3)


#Converts user time input into a timedelta object for comparing
def parse_time(time_str):
    h, m, s = map(int, time_str.split(":"))
    return datetime.timedelta(hours=h, minutes=m, seconds=s)

#checks and prints a single package's status at any given check_time
def print_package_status(package, check_time):
##checks for any delayed packages and adjusts logic if there is a specific time delay on package object



    address = package.address
    zip_code = package.zipcode

#Updates the UI for the package with the wrong address
    if package.packageID == 9:
        if check_time < datetime.timedelta(hours=10, minutes=20):
            address = "300 State St"
            zip_code = "84103"
        else:
            address = "410 S State St"
            zip_code = "84111"
    if hasattr(package, "delay_time") and package.delay_time and check_time<package.delay_time:
        status = "Delayed"
        delivered_at ="N/A"
    #Package is at hub
    elif check_time<package.departure_time:
        status = "At hub"
        delivered_at ="N/A"
    #Truck has departed but it time has not reached delivery time
    elif check_time<package.delivery_time:
        status = "En Route"
        delivered_at ="N/A"
    #Check time is equal 5to delivery time
    else:
        status = "Delivered"
        delivered_at = str(package.delivery_time)



# Formatting
    print(f"| ID: {package.packageID:<3} | Address: {address:<30} {package.city:<16} {zip_code:<5} | "
      f"Deadline: {package.deadline:<8} | Weight: {package.weight:<3} kg | "
      f"Truck: {getattr(package, 'truck_number', 'N/A'):<2} | "
      f"Status: {status:<10} | Delivery Time: {delivered_at:<8} |")




#User interface
def run_cli():
#Calculate mileage across all turcks
    total_mileage = truck1.mileage + truck2.mileage + truck3.mileage

    ##print(f"Total Mileage: {total_mileage:.1f} miles\n")

    #This keeps the menu active until the user chooses an option to exit.
    while True:
        print("\nPlease Select an option:")
        print("1. View status of a SINGLE package at a specific time")
        print("2. View status of ALL packages at a specific time")
        print("3. View TOTAL MILEAGE of all trucks")
        print("4. Exit Program")
        #To remove whitespace
        command = input("Enter  (1-4)").strip()

        #If statements for each command user may input
        if command == '1':
            try:
                time_input = input("Enter time in HH:MM:SS format (e.g., 09:00:00): ").strip()
                check_time = parse_time(time_input)

                pkg_id = int(input("Enter Package ID (1-40): ").strip())
                # Retrieve package from hash table using lookup/search method
                package = packHashTable.lookup(pkg_id)

                if package:
                    print(f"\n--- Status for Package {pkg_id} at {time_input} ---")
                    print_package_status(package, check_time)
                else:
                    print(f"Package ID {pkg_id} not found in hash table.")

            except ValueError:
                print("Error: Invalid input format. Use HH:MM:SS for time and numbers for ID.")

        elif command == '2':
            try:
                time_input = input("Enter time in HH:MM:SS format (e.g., 09:00:00): ").strip()
                check_time = parse_time(time_input)

                print(f"\n==================== ALL PACKAGES STATUS AT {time_input} ====================")
                for pkg_id in range(1, 41):
                    package = packHashTable.lookup(pkg_id)
                    if package:
                        print_package_status(package, check_time)

                print(
                    "------------------------------------------------------------------------------------------------------------------------")
                print(f"TOTAL MILEAGE TRAVELED ACROSS ALL TRUCKS: {total_mileage:.1f} miles")
                print(
                    "================================================================================----------------------------------------\n")
                print("=============================================================================")

            except ValueError:
                print("Error: Invalid time format. Please enter as HH:MM:SS (e.g., 09:30:00).")

        elif command == '3':
            print(f"\nTotal mileage traveled across all 3 trucks: {total_mileage:.1f} miles")

        elif command == '4':
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid option selected. Please enter 1, 2, 3, or 4.")

        # Entry point execution
if __name__ == "__main__":
            run_cli()