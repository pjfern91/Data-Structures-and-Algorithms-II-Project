# Truck class constructor for initializing the truck info.
class Truck:

    def __init__(self, truck_number, packages_list, truck_speed, start_time):
        self.truck_number = truck_number
        self.packages = packages_list
        self.truck_speed = truck_speed
        self.start_time = start_time
