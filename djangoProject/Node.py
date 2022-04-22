class Node:

    def __init__(self, node_id, way_id, name, node_type, lat, lon, difficulty, status):
        self.node_id = node_id
        self.way_id = way_id
        self.name = name
        self.node_type = node_type
        self.lat = lat
        self.lon = lon
        self.difficulty = difficulty
        self.status = status

    # Function to convert node to string representation.
    def __str__(self):
        return '[id: ' + str(self.node_id) + ', way id: '+ str(self.way_id) + ', name: ' + str(self.name) +  ', type: ' + str(self.node_type) + ', lat: ' + str(self.lat) + ', lon: ' + str(self.lon) + ', difficulty: ' + str(self.difficulty) + ', status: ' + str(self.status) + ']'

    # Function to find a node by its name value.
    def get_node_by_name(self, name):
        if self.name == name:  # Compares node's name value to passed name.
            return self  # Returns node if a match.
        else:  # If no match.
            return None

    # Function to find a node by its geohash id value.
    def get_node_by_node_id(self, node_id):
        if self.node_id == node_id:  # Compares current node's id value to passed id.
            return self  # Returns node if a match.
        else:  # If no match.
            return None

    # Function to retrieve node by its name and geohash id value.
    def get_by_name_cord(self, name, node_id):
        if self.name == name and self.node_id == node_id:  # Compares node's name and id value to passed values.
            return self  # Returns node if a match.
        else:  # If no match.
            return None

    # Function to retrieve node's name value.
    def get_way_name(self):
        return self.name

