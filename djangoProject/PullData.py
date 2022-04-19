import geojson
from djangoProject.Node import Node
from djangoProject.Graph import Graph
import pygeohash as pgh


class PullData:

    def __init__(self):
        self.nodes = []  # List of all the nodes created.
        self.graph = Graph()  # Graph object.
        self.g_dict = {}  # Used for storing and checking node id values for repeats.

    # Reads GeoJSon file from file path.
    def read_data(self, path):
        # read = open(r'MacintoshHD\Users\Joshuafentress\Downloads\{}'.format(path))  # For PC
        read = open('/Users/joshuafentress/Downloads/BlueMountain2.geojson')  # For Mac
        data = geojson.load(read)  # Loads file into geojson data.
        return data  # Returns data file.

    # Convert data function for parsing map geojson and creating node and graph objects.
    def convert_data(self, data):
        status = True  # Used for trail/lift status.
        copy = None
        for element in range(len(data['features'])):  # Iterate for each node/way in geoJSon file.

            if 'aerialway' in data[element]['properties'].keys():  # Checks for any lifts/gondolas.

                name = data[element]['properties']['name']  # Retrieves name of lift.
                node_type = 'lift'  # This node is from a ski lift.

                if name != 'Tubing Lift':
                    for points in range(len(data[element]['geometry']['coordinates'])):  # Iterates for each node that is in this lift.
                        way_id = data[element]['properties']['@id']  # Retrieves way id.
                        lon = data[element]['geometry']['coordinates'][points][0]  # Retrieves longitude.
                        lat = data[element]['geometry']['coordinates'][points][1]  # Retrieves latitude.
                        node_id = self.hash_cords(lat, lon)  # Generates an id for the node.

                        node = Node(node_id, way_id,name, node_type, lat, lon, None, status)  # Creates node object.

                        if node_id not in self.g_dict.keys(): # Checks if the node id is a new distinct id.
                            self.g_dict[node_id] = node # Adds the node id to the list.
                            self.graph.add_vertex(node) # Creates vertex from node.
                        else: # If there is already a node with the same id.
                            con = self.g_dict[node_id] # Retrieves the previously created node with same id.
                            self.graph.add_vertex(node) # Creates vertex from node.
                            self.graph.add_edge(con, node)  # Creates edge between the two nodes.
                            self.graph.add_edge(node, con)  # Creates edge between the two nodes.

                        self.nodes.append(node)  # Appends the new node to the nodes list.
                        if points > 0:  # Once iteration reaches second node in the list for lift.
                            self.graph.add_edge(self.nodes[-2], node)  # Start connecting the nodes.
            else:  # If the node type is a ski run.

                node_type = 'run'  # This node is from a ski run.

                if 'name' in data[element]['properties'].keys():  # If the name attribute is in the nodes properties.
                    name = data[element]['properties']['name']  # Retrieve the name.
                else:  # For when the name attribute is not presented.
                    name = 'NA'  # Set the name at not available.

                if name != 'School Hill':
                    for points in range(len(data[element]['geometry']['coordinates'])):  # Iterates for each node that is in the ski run.
                        way_id = data[element]['properties']['@id']  # Retrieves way id.
                        lon = data[element]['geometry']['coordinates'][points][0]  # Retrieves longitude.
                        lat = data[element]['geometry']['coordinates'][points][1]  # Retrieves latitude.
                        dif = data[element]['properties']['piste:difficulty']  # Retrieves the ski runs difficulty
                        node_id = self.hash_cords(lat, lon)  # Generates an id for the node.

                        node = Node(node_id, way_id, name, node_type, lat, lon, dif, status)  # Creates node object.

                        if node_id not in self.g_dict.keys():  # Checks if the node id is a new distinct node.
                            self.g_dict[node_id] = node  # Adds the node to node id list.
                            self.graph.add_vertex(node) # Creates vertex from node.
                        else:  # If there is already a node with the same id.
                            con = self.g_dict[node_id]  # Retrieves previously created nodes with same id.
                            self.graph.add_vertex(node) # Creates vertex from node.
                            self.graph.add_edge(con, node)  # Creates edge between the two nodes.
                            self.graph.add_edge(node, con)  # Creates edge between the two nodes.

                        self.nodes.append(node)  # Appends the new node to nodes list.
                        if points > 0:  # Once iteration reaches second node in list for ski run.
                            self.graph.add_edge(self.nodes[-2], node)  # Start connecting the nodes

        self.bad_con()
        return self.graph

    # Hash function for generating id's for nodes dependent on latitude and longitude points.
    def hash_cords(self, lat, lon):
        return pgh.encode(lat, lon)  # Calls pygeohash encode function.

    # Function for generating list of way names for HTML selection.
    def way_names(self):
        way_list = []  # Create a list for storing ski run/lift names.
        for node in self.nodes:  # Iterates through the list of nodes.
            name = node.get_way_name() # Sets name to current nodes run/lift name.
            if name not in way_list:  # Checks if the name is already in the list.
                way_list.append(name)  # Appends the name to the list.

        return way_list  # Returns the list.

    # Function for connecting the lifts and runs that were not connected originally
    def bad_con(self):
        temp1 = None
        temp2 = None

        ce_top_cord = self.hash_cords(40.809745, -75.510716)  # 40.8097454, -75.5107162
        ce_top_con_cord = self.hash_cords(40.809465, -75.512166)  # 40.8094649, -75.5121660
        for n in self.nodes:
            if n.get_node_by_node_id(ce_top_cord) is not None:
                temp1 = n

        for n in self.nodes:
            if n.get_node_by_node_id(ce_top_con_cord) is not None:
                temp2 = n

        ce_top_cord_node = temp1
        ce_top_con_cord_node = temp2
        self.graph.add_edge(ce_top_cord_node, ce_top_con_cord_node)

        ce_bottom_cord = self.hash_cords(40.820990, -75.513362)  # 40.8209900, -75.5133619
        trp_bottom_to_ce = self.hash_cords(40.820735, -75.513652)  # 40.8207352, -75.5136519
        vsw_bottom_to_ce = self.hash_cords(40.820997, -75.514022)  # 40.8209971, -75.5140221
        for n in self.nodes:
            if n.get_node_by_node_id(ce_bottom_cord) is not None:
                temp1 = n

        for n in self.nodes:
            if n.get_node_by_node_id(trp_bottom_to_ce) is not None:
                temp2 = n

        ce_bottom_cord_node = temp1
        trp_bottom_to_ce_node = temp2
        self.graph.add_edge(trp_bottom_to_ce_node, ce_bottom_cord_node)

        vst_bottom_cord = self.hash_cords(40.820009, -75.514396) # 40.8200094, -75.5143964

        for n in self.nodes:
            if n.get_node_by_node_id(vst_bottom_cord) is not None:
                temp2 = n

        vst_bottom_cord_node = temp2
        self.graph.add_edge(trp_bottom_to_ce_node, vst_bottom_cord_node)


        for n in self.nodes:
            if n.get_node_by_node_id(vsw_bottom_to_ce) is not None:
                temp2 = n

        vsw_bottom_to_ce_node = temp2
        self.graph.add_edge(vsw_bottom_to_ce_node, ce_bottom_cord_node)

        comet_bottom_cord = self.hash_cords(40.821483, -75.512737)  # 40.8214828, -75.5127367
        comet_bottom_con_cord = self.hash_cords(40.821734, -75.513073)  # 40.8217339, -75.5130726
        comet_bottom_con_cord_2 = self.hash_cords(40.821831, -75.512484)  # 40.8218310, -75.5124844

        for n in self.nodes:
            if n.get_node_by_node_id(comet_bottom_cord) is not None:
                temp1 = n

        for n in self.nodes:
            if n.get_node_by_node_id(comet_bottom_con_cord) is not None:
                temp2 = n

        comet_bottom_cord_node = temp1
        comet_bottom_con_cord_node = temp2
        self.graph.add_edge(comet_bottom_con_cord_node, comet_bottom_cord_node)

        for n in self.nodes:
            if n.get_node_by_node_id(comet_bottom_con_cord_2) is not None:
                temp2 = n

        comet_bottom_con_cord_2_node = temp2
        self.graph.add_edge(comet_bottom_con_cord_2_node, comet_bottom_cord_node)

        vista_bottom_cord = self.hash_cords(40.812526, -75.518131)  # 40.8125263, -75.5181311
        vist_bottom_con_cord = self.hash_cords(40.812585, -75.518169)  # 40.8125847, -75.5181690
        for n in self.nodes:
            if n.get_node_by_node_id(vista_bottom_cord) is not None:
                temp1 = n

        for n in self.nodes:
            if n.get_node_by_node_id(vist_bottom_con_cord) is not None:
                temp2 = n

        vista_bottom_cord_node = temp1
        vist_bottom_con_cord_node = temp2
        self.graph.add_edge(vist_bottom_con_cord_node, vista_bottom_cord_node)

        node_id = self.hash_cords(40.813777, -75.515948)
        for n in self.nodes:
            if n.get_by_name_cord('MidWay', node_id) is not None:
                temp1 = n

        for n in self.nodes:
            if n.get_by_name_cord('Lower Main Street', node_id):
                temp2 = n

        midway_node = temp1
        midway_con_cord = temp2
        self.graph.add_edge(midway_node, midway_con_cord)

        node_id = self.hash_cords(40.817082, -75.515907)
        for n in self.nodes:
            if n.get_by_name_cord('Burma Road', node_id) is not None:
                temp1 = n

        for n in self.nodes:
            if n.get_by_name_cord('Main Street Chair', node_id):
                temp2 = n

        burma_node = temp1
        main_node = temp2
        self.graph.add_edge(burma_node, main_node)

        node_id = self.hash_cords(40.809457, -75.515465)
        for n in self.nodes:
            if n.get_by_name_cord("Tut's Lane", node_id) is not None:
                temp1 = n

        for n in self.nodes:
            if n.get_by_name_cord('Lazy Mile', node_id):
                temp2 = n

        tuts_node = temp1
        lm_node = temp2
        self.graph.add_edge(tuts_node, lm_node)

    def find_route(self, start_name, end_name):
        start = None
        end = None
        for node in self.nodes:
            if node.name == start_name:
                start = node.get_node_by_name(start_name)
                break

        for node in self.nodes:
            if node.name == end_name:
                end = node.get_node_by_name(end_name)
                break

        return self.graph.dijkstra(start, end)


pd = PullData()  # Create Pull Data.
d = pd.read_data('BlueMountain2.geojson') # Pass data to read from.

g = pd.convert_data(d)  # Graph returned from convert_data.
start = pd.nodes[0]
end = pd.nodes[16]

route = pd.find_route(start.name, end.name)
print(len(route))
for node in route:
    print(node)

'''for pairs in find_empty.items():
    if pairs[1] is None:
        print(pairs[0])'''
