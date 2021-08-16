import csv
from operator import itemgetter
from hashtable import BrownsHash
from package import Package
from graph import Node, Graph


# Parse xPackages.csv and create a Package object for each row.
# Load Package objects into the Hashtable.
# Time complexity: O(N)
# Space complexity: O(N)
def parse_packages():
    # Create HashTable object
    hash_t = BrownsHash()

    # Parse through csv file
    with open('xPackages.csv', mode='r', encoding='utf-8-sig') as csvfile:
        read_packages_csv = csv.reader(csvfile, delimiter=',')

        # Read through each row to create a package.
        # Load each Package into the Hashtable.
        for row in read_packages_csv:
            # Create a new package object for the row of information
            new_pack = Package(row)

            # Insert the package object into the hash table
            hash_t.insert(new_pack)
    # Return the Hashtable
    return hash_t


# Parsing function that will return node name from a string
# of name and address.
# Load Package objects into the Hashtable.
# Time complexity: O(N)
# Space complexity: O(1)
def parse_node_name(name_address_string):
    # Store the name of location.
    parsed_name = ''
    # Find the index of the first digit, this is the start of the address
    for ch in range(0, len(name_address_string)):
        if name_address_string[ch].isdigit():
            # Get index of the start of the address.
            start_of_address = ch

            # Get the node name
            parsed_name = name_address_string[:(start_of_address - 1)]
            break

    # The location name and address proper are returned.
    return parsed_name


# Parsing function that will separate a string into
# a node address and node zip code.
# Load Package objects into the Hashtable.
# Time complexity: O(N)
# Space complexity: O(1)
def parse_address_zip(address_zip_string):
    # Find the starting and ending index values for the zip code.
    # This will exclude the parentheses around the zip code.
    start_of_zip = 0
    end_of_zip = 0
    for c_index in range(0, len(address_zip_string)):
        if address_zip_string[c_index] == '(':
            start_of_zip = c_index
        elif address_zip_string[c_index] == ')':
            end_of_zip = c_index
    # Get the node address
    parsed_address = address_zip_string[:(start_of_zip - 1)]

    # Get the node zip code
    parsed_zip_code = address_zip_string[(start_of_zip + 1):end_of_zip]

    # Return the node address and zip code
    return parsed_address, parsed_zip_code


# Function that will merge, tuple, then sort each adjacency dictionary
# entry with the list of nodes. Then create an undirected edge for each
# node with the adjacent node.
# Load Package objects into the Hashtable.
# Time complexity: O(N)
# Space complexity: O(N)
def merge_nodes_distances(area_map, list_of_nodes):
    for node_key, distance_list in area_map.adj_nodes_dict.items():
        # Create a new list for every dictionary entry.
        new_list = sorted(tuple(zip(distance_list, list_of_nodes)), key=itemgetter(0))
        # Replace the original list in the dictionary with the new one.
        area_map.adj_nodes_dict[node_key] = new_list


# Use Dijkstra's Shortest Route algorithm to adjust for any triangle inequalities.
# This will make the greedy algorithm more efficient.
# Load Package objects into the Hashtable.
# Time complexity: O(N^2)
# Space complexity: O(N)
def dijkstra_shortest_route(area_map, start_node):
    # Create queue to hold every node in the map.
    unvisited_nodes = []

    # Add all nodes in the area map adjacency dictionary to the queue.
    for current_node in area_map.adj_nodes_dict:
        unvisited_nodes.append(current_node)

    # Initialize start nodes distance to 0.0
    start_node.distance = 0.0

    # For every node in the unvisited queue, remove
    # it and determine the shortest path to get there.
    while len(unvisited_nodes) > 0:
        # Set closest node index.
        closest_node = 0

        # Compare the closest_loc's distance to every other
        # location in the queue to find the closest node.
        for node_index in range(1, len(unvisited_nodes)):
            if unvisited_nodes[node_index].distance < unvisited_nodes[closest_node].distance:
                closest_node = node_index

        # Move the current location to the next closest location.
        current_node = unvisited_nodes.pop(closest_node)

        # Find the next location to move to.
        for adjacent_node_tuple in area_map.adj_nodes_dict[current_node]:
            edge_distance = adjacent_node_tuple[0]
            alt_route_distance = current_node.distance + edge_distance

            if alt_route_distance < adjacent_node_tuple[1].distance:
                adjacent_node_tuple[1].distance = alt_route_distance
                adjacent_node_tuple[1].previous_node = current_node


# Parse xLocations.csv and create a node object for each row.
# Load Node objects into the Graph.
# Load Package objects into the Hashtable.
# Time complexity: O(N)
# Space complexity: O(N)
def parse_map():
    # Create Graph object
    area_map = Graph()

    # Store HUB node
    start_node = None

    # Create list to hold every node in same order as the rows ni the csv file
    nodes_list = []

    # Parse through csv file
    with open('xLocations.csv', mode='r', encoding='utf-8-sig') as csvfile:
        read_packages_csv = csv.reader(csvfile, delimiter=',')

        # Read through each row to create a node.
        for row in read_packages_csv:
            # Create list to contain distance values
            distances = []

            # Check if row contains HUB information.
            # Information for the HUB is stored differently in csv.
            if row[1] == 'HUB':
                node_name = parse_node_name(row[0])
                node_address = row[1]
                node_zip = '84107'
                for dist_value in row[2:]:
                    distances.append(float(dist_value))
            else:
                node_name = parse_node_name(row[0])
                node_address, node_zip = parse_address_zip(row[1])
                for dist_value in row[2:]:
                    distances.append(float(dist_value))

            # Create a Node object
            new_node = Node(node_name, node_address, node_zip)

            # Add Node to nodes_list
            nodes_list.append(new_node)

            # Add Node to Graph
            area_map.add_node(new_node, distances)

            # Set start_node equal to node whose address is HUB
            if new_node.loc_address == 'HUB':
                start_node = new_node

    # Merge adjacent distances with corresponding adjacent node for
    # each adjacent nodes dictionary.
    merge_nodes_distances(area_map, nodes_list)
    # Call Dijkstra's algorithm to find shortest paths from each node to HUB.
    dijkstra_shortest_route(area_map, start_node)

    # Return the map and the start node
    return area_map, start_node
