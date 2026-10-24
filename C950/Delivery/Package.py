#one special note associated with a package
#he delivery address for package #9, Third District Juvenile Court, is wrong and will be corrected at 10:20 a.m. the company does not know until 10:20am
#Look up function

#initializes the package object
class Package:
    def __init__(self, packageID, address, zipcode, city, deadline, weight, status):
        self.packageID = packageID
        self.address = address
        self.zipcode = zipcode
        self.city = city
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.arrival_time = None

    def __str__(self):
        return f" {self.packageID},{self.address}, {self.zipcode}, {self.city}, {self.deadline}, {self.weight}, {self.status}"

#updates the package's status
    def update(self, convert_time):
        if self.departure_time < convert_time:
            self.status = "Departed"
        elif self.departure_time > convert_time:
            self.status = "Arriving"
        else:
            self.status = "Arrived"
