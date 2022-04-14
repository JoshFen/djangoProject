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

    def __str__(self):
        return '[id: ' + str(self.node_id) + ', way id: '+ str(self.way_id) + ', name: ' + str(self.name) +  ', type: ' + str(self.node_type) + ', lat: ' + str(self.lat) + ', lon: ' + str(self.lon) + ', difficulty: ' + str(self.difficulty) + ', status: ' + str(self.status) + ']'

    def get_node_by_name(self, name):
        if self.name == name:
            return self
        else:
            return None

    def get_node_by_node_id(self, node_id):
        if self.node_id == node_id:
            return self
        else:
            return None

    def get_by_name_cord(self, name, node_id):
        if self.name == name and self.node_id == node_id:
            return self
        else:
            return None

    def get_way_name(self):
        return self.name

