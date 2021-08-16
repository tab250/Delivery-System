from datetime import datetime, timedelta


# Truck Class
class Truck:

    # Truck Constructor
    def __init__(self, num, start_time, capacity=16, speed_mph=18):
        self.truck_num = num
        self.start_time = start_time
        self.curr_time = self.start_time
        self.truck_capacity = capacity
        self.speed_mph = speed_mph
        self.speed_miles_per_minute = 60 / self.speed_mph
        self.distance_traveled = 0.0
        self.packages_on_truck = []

    # Function to load truck with packages.
    # Load Package objects into the Hashtable.
    # Time complexity: O(N)
    # Space complexity: O(N)
    def load_truck(self, key_list, hashtable, area_map):
        # Create list of addresses corresponding to the packages.
        address_stops = []

        # Copy the list of keys to maintain the original copy.
        key_list_copy = key_list.copy()

        # Load the packages into the truck and update each package's
        # delivery status.
        while len(key_list_copy) > 0:
            # Get next package to load.
            next_package = key_list_copy.pop(0)
            package_to_load = hashtable.find(next_package)

            # Load package onto truck and update status
            self.packages_on_truck.append(package_to_load)
            package_to_load.del_status = 'En route'

            # Add package's delivery address to stops if not already in list.
            if package_to_load.del_address not in address_stops:
                address_stops.append(package_to_load.del_address)

        # Convert the addresses to nodes.
        node_stops = area_map.addresses_to_nodes(address_stops)

        # Return the list of nodes.
        return node_stops

    # Function to unload packages from truck for a given node.
    # Load Package objects into the Hashtable.
    # Time complexity: O(N)
    # Space complexity: O(1)
    def deliver_packages(self, node):
        for package in self.packages_on_truck:
            if package.del_address == node.loc_address:
                package.del_status = 'Delivered at ' + datetime.strftime(self.curr_time, '%I:%M') \
                                     + ' by Truck ' + str(self.truck_num)

    # Function to update the truck's current time and distance traveled
    # and delivers package(s) for current node.
    # Load Package objects into the Hashtable.
    # Time complexity: O(1)
    # Space complexity: O(1)
    def update_status(self, distance):
        # Update the truck's distance_traveled.
        self.distance_traveled += distance
        # Calculate the time passed from last node to current node.
        minutes_passed = int(self.distance_traveled / self.speed_miles_per_minute)
        # Update the truck's curr_time.
        self.curr_time += timedelta(minutes=minutes_passed)
