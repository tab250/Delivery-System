# Delivery-System

The goal of this project was to use a variety of Data Structures and Algorithms to solve a derivative of the Traveling Salesman problem (NP-Hard).
The program reads from two csv files to create Location Nodes, which become a graph of nodes with adjacency lists, and Package objects that contain information about
their delivery, such as location and deadline. The packages are hashed according their ID and stored in a hash table for Runtime: O(1). All the packages
must be delivered by the Truck objects which can only have a set number of packages. The problem also has restrictions with regards to the packages. They include
which truck a certain package can be on, if it's delayed and/or has a deadline, and if it has to be delivered with other packages. There is also a mileage limit
with the trucks, they cannot exceed 140 miles. The program uses a simple greedy algorithm, with the help of Dijkstra's algorithm to deliver the packages and 
return to the HUB efficiently. The program provides a simple text-based interface for a user to use to view all packages at a given time, or the status of one
package at a certain time.

What was learned:
* How to use variety of data structures and algorithms, such as dictionaries, graphs, greedy algorithms, Dijkstra's algorithm, and hashing.
* How to build a text-based interface
* How to read from files and parse the information

What can be improved:
* The mileage could be reduced with a more optimal algorithm.
