# Hashtable class
class BrownsHash:

    # Hashtable Constructor
    def __init__(self, table_size=40):
        self.hash_table = []
        for i in range(table_size):
            self.hash_table.append([])

    # Insertion function that takes package object
    # and passes it's ID into hash function and adds
    # the package object to hashed location.
    # Time complexity: O(1)
    # Space complexity: O(1)
    def insert(self, package):
        # Get the bucket that the package object will be inserted into
        bucket = package.packID % len(self.hash_table)

        # Insert the package object into the bucket
        self.hash_table[bucket] = package

    # Find function that finds if a package,
    # with provided id, is in the hash table.
    # Time complexity: O(1)
    # Space complexity: O(1)
    def find(self, pack_id):
        key = pack_id % len(self.hash_table)

        if self.hash_table[key] is not None:
            return self.hash_table[key]
        else:
            return None
