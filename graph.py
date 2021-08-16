# Node class creates an object for every location in the map/graph
class Node:

    # Node Constructor
    def __init__(self, location_name, location_address, location_zip):
        self.loc_name = location_name
        self.loc_address = location_address
        self.loc_zip = location_zip
        self.distance = float('inf')
        self.previous_node = None

    # String structure for printing Node object.
    def __str__(self):
        return 'Location Name: {}, \nLocation Address: {}, Location Zip Code: {}\n'\
                .format(self.loc_name, self.loc_address, self.loc_zip)


# Graph class
class Graph:

    # Graph Constructor
    def __init__(self):
        self.adj_nodes_dict = {}

    # Function that adds an adjacent node to a given nodes adjacency list.
    # Load Package objects into the Hashtable.
    # Time complexity: O(1)
    # Space complexity: O(N)
    def add_node(self, parsed_node, d_list):
        self.adj_nodes_dict[parsed_node] = d_list

    # Convert a list of address strings to a list of corresponding nodes.
    # Load Package objects into the Hashtable.
    # Time complexity: O(N^2)
    # Space complexity: O(N)
    def addresses_to_nodes(self, addresses):
        # Create list to contain the nodes
        nodes = []

        # For every address, find the matching node and add to nodes list.
        while len(addresses) > 0:
            # Get next node to find.
            next_address = addresses.pop(0)
            # Find node with matching address
            for node in self.adj_nodes_dict.keys():
                if node.loc_address == next_address:
                    nodes.append(node)
                    break

        # Return the list of nodes
        return nodes
