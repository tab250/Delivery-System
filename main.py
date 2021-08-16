# Tyler Brown, 001326587

from datetime import datetime, date, time
from parse import parse_packages, parse_map
from truck import Truck


# Self-adjusting greedy algorithm for delivering packages.
# Time complexity: O(N^2)
# Space complexity: O(1)
def greedy_delivery_route(truck, nodes, requested_time, area_map, first_node):
    # Return boolean variable to determine if all packages were delivered.
    delivery_complete = False

    # Set starting node.
    current_node = first_node

    # Run route until all packages are delivered.
    if requested_time == 'EOD':
        # Move through list of nodes until it is empty.
        while len(nodes) > 0:
            # Loop through current nodes adjacency list to find closest node.
            for possible_node_tuple in area_map.adj_nodes_dict[current_node]:
                # Check if possible node is in list of nodes to visit.
                if possible_node_tuple[1] in nodes:
                    # Set index of possible node in list of nodes to visit.
                    node_index = nodes.index(possible_node_tuple[1])
                    # Set current node to possible node.
                    current_node = nodes.pop(node_index)
                    # Update distance traveled and current time for truck.
                    truck.update_status(possible_node_tuple[0])
                    # Deliver packages for current node.
                    truck.deliver_packages(current_node)
                    break

        # Return to the HUB.
        while current_node != first_node:
            current_node = current_node.previous_node
            truck.update_status(current_node.distance)

        # If all nodes have been visited, all packages were delivered.
        if len(nodes) == 0:
            delivery_complete = True
    # Run route until specified time.
    else:
        # Move through list of nodes until it is empty.
        while truck.curr_time < requested_time:
            if len(nodes) > 0:
                # Loop through current nodes adjacency list to find closest node.
                for possible_node_tuple in area_map.adj_nodes_dict[current_node]:
                    # Check if possible node is in list of nodes to visit.
                    if possible_node_tuple[1] in nodes:
                        # Set index of possible node in list of nodes to visit.
                        node_index = nodes.index(possible_node_tuple[1])
                        # Set current node to possible node.
                        current_node = nodes.pop(node_index)
                        # Update distance traveled and current time for truck.
                        truck.update_status(possible_node_tuple[0])
                        # Deliver packages for current node.
                        truck.deliver_packages(current_node)
                        break
            else:
                break

        # Return to the HUB.
        while current_node != first_node:
            if truck.curr_time < requested_time:
                current_node = current_node.previous_node
                truck.update_status(current_node.distance)
            else:
                break

        # If all nodes have been visited, all packages were delivered.
        if len(nodes) == 0:
            delivery_complete = True

    # Return the boolean variable.
    return delivery_complete


# Function to create Truck objects and load them into a list.
# Time complexity: O(N)
# Space complexity: O(1)
def create_trucks():
    # Create list to maintain the trucks
    trucks = [None] * 2

    # Declare Trucks, load them into the fleet, get nodes to delivery
    # to and call greedy delivery route.
    for t_index in range(0, len(trucks)):
        if t_index == 0:
            trucks[t_index] = Truck((t_index + 1), start_time=datetime.combine(date.today(), time(8)))
        else:
            trucks[t_index] = Truck((t_index + 1), start_time=datetime.combine(date.today(), time(9, 5)))
    # Return list of trucks
    return trucks


# Print all information about the deliveries.
# Time complexity: O(N)
# Space complexity: O(1)
def print_information(hashtable, trucks):
    # Print every package based on requested time.
    package_key = 0
    while package_key < 40:
        print(hashtable.find(package_key))
        package_key += 1

    # Print distance traveled for each truck and the total distance
    total_distance = 0
    for t in trucks:
        print('Truck ' + str(t.truck_num) + ' traveled: ' + str(t.distance_traveled) + ' miles')
        total_distance += t.distance_traveled
    print('Total distance traveled ' + str(total_distance) + ' miles')


# Reset all information that has been altered due to deliveries.
# Time complexity: O(N)
# Space complexity: O(1)
def reset_all(hashtable, trucks):
    # Set hash key for accessing hashtable
    hash_key = 0

    # Reset every package's status to 'At HUB'.
    while hash_key < 40:
        hashtable.find(hash_key).del_status = 'At hub'
        hash_key += 1

    # Reset every trucks distance traveled and current time.
    # Empty the packages on truck in case it is not empty.
    for t in trucks:
        t.distance_traveled = 0.0
        t.curr_time = t.start_time
        t.packages_on_truck.clear()


# Load packages onto trucks and call the greedy delivery algorithm.
# Time complexity: O(N)
# Space complexity: O(1)
def check_deliveries(hashtable, truck_1_first, truck_1_second, truck_2_first, truck_2_second, requested_time, trucks):
    # Deliver packages until end of day (EOD) or specified time.
    for t in trucks:
        if t.truck_num == 1:
            # Load truck and run greedy algorithm.
            nodes_to_visit = t.load_truck(truck_1_first, hashed_packages, map_of_slc)
            complete_delivery = greedy_delivery_route(t, nodes_to_visit, requested_time, map_of_slc, start_location)

            # Run greedy algorithm again with second set of packages
            # if the time constraint wasn't reached.
            if complete_delivery:
                nodes_to_visit = t.load_truck(truck_1_second, hashed_packages, map_of_slc)
                greedy_delivery_route(t, nodes_to_visit, requested_time, map_of_slc, start_location)
        if t.truck_num == 2:
            # Load truck and run greedy algorithm.
            nodes_to_visit = t.load_truck(truck_2_first, hashed_packages, map_of_slc)
            greedy_delivery_route(t, nodes_to_visit, requested_time, map_of_slc, start_location)

            # Run greedy algorithm again with second set of packages
            # if the time constraint wasn't reached.
            if complete_delivery:
                t.curr_time = datetime.combine(date.today(), time(10, 20))
                nodes_to_visit = t.load_truck(truck_2_second, hashed_packages, map_of_slc)
                greedy_delivery_route(t, nodes_to_visit, requested_time, map_of_slc, start_location)

    # Print all the packages in the hashtable.
    print_information(hashtable, trucks)


# Function to interact with user.
# Time complexity: O(1)
# Space complexity: O(1)
def user_requests(hashtable, truck_1_first, truck_1_second, truck_2_first, truck_2_second, trucks):
    # Display next possible actions.
    print()
    print('1 : Check all packages at a certain time')
    print('2 : Check a specific package')
    print('3 : Exit program')

    # Get user request.
    user_req = int(input('Please enter 1, 2, or 3: '))

    if user_req == 1:
        # Reset packages and trucks
        reset_all(hashtable, trucks)

        # Run the greedy delivery algorithm until requested time.
        time_to_check = input('Please enter a time (HH:MM; 24-Hour Time) or EOD to deliver all packages: ')

        # Check if user requested a specific time.
        if time_to_check != 'EOD':
            # Restructure variable to time object if not EOD.
            time_to_check = datetime.strptime(time_to_check, '%H:%M').time()
            restructured_dt = datetime.combine(date.today(), time_to_check)

            # Run the greedy delivery algorithm with new time.
            check_deliveries(hashtable, truck_1_first, truck_1_second, truck_2_first, truck_2_second, restructured_dt, trucks)
        else:
            # Run the greedy delivery algorithm with new time.
            check_deliveries(hashtable, truck_1_first, truck_1_second, truck_2_first, truck_2_second, time_to_check, trucks)

        # Call user request function again.
        user_requests(hashtable, truck_1_first, truck_1_second, truck_2_first, truck_2_second, trucks)
    elif user_req == 2:
        # Check on a specific package.
        package_to_check = int(input('Please enter a package ID between 1 and 40: '))

        # Print requested package.
        print()
        print(hashtable.find(package_to_check))

        # Call user request function again.
        user_requests(hashtable, truck_1_first, truck_1_second, truck_2_first, truck_2_second, trucks)
    else:
        # Close program
        print('Good bye')
        quit()


# Create a hash table and load it with packages from csv file.
hashed_packages = parse_packages()

# Create a graph of all the locations and get the starting location.
map_of_slc, start_location = parse_map()

# Create a list of all the trucks in the fleet.
fleet = create_trucks()

# Lists of package keys to manually load the trucks.
t1d1 = [14, 15, 16, 34, 19, 20, 21, 4, 40, 1, 13, 39, 27, 35, 2, 33]
t1d2 = [7, 11, 12, 17, 22, 23, 24, 29, 30]
t2d1 = [3, 5, 6, 10, 18, 25, 26, 28, 31, 32, 36, 37, 38]
t2d2 = [8, 9]

# Call function for user to interact with.
user_requests(hashed_packages, t1d1, t1d2, t2d1, t2d2, fleet)
