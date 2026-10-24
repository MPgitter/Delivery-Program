#max 16 packages
#avg speed of 18mph infinite gas
#3trucks available
#loading times are instant

#creates the truck object
class Truck:
    def __init__(self, mileage, speed, load, capacity, depart_time, destination):
        self.mileage = mileage
        self.speed = speed
        self.load = load
        self.capacity = capacity
        self.depart_time = depart_time
        self.time = depart_time
        self.destination = destination


    def __str__(self):
        return f"{self.capacity}, {self.depart_time}, {self.speed}, {self.load}, {self.id}, {self.destination}"