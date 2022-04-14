import geojson
from djangoProject.Node import Node
from djangoProject.Graph import Graph
import pygeohash as pgh


class PullData:

    def __init__(self):
        self.nodes = []  # List of all the nodes created.
        self.graph = Graph()  # Graph object.
        self.g_dict = {}  # Used for storing and checking node id values for repeats.



    def read_data(self, path):
        read = open(r'C:\Users\Josh\Downloads\{}'.format(path))
        data = geojson.load(read)
        return data


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
                            print(node.name)
                            print(con.name)
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


                if name !='School Hill':
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

        CE_top_cord = self.hash_cords(40.809745, -75.510716)  # 40.8097454, -75.5107162
        CE_top_con_cord = self.hash_cords(40.809465, -75.512166)  # 40.8094649, -75.5121660
        print("##################################################################################################")
        for n in self.nodes:
            if n.get_node_by_node_id(CE_top_cord) is not None:
                temp1 = n

        for n in self.nodes:
            if n.get_node_by_node_id(CE_top_con_cord) is not None:
                temp2 = n

        CE_top_cord_node = temp1
        CE_top_con_cord_node = temp2
        self.graph.add_edge(CE_top_cord_node, CE_top_con_cord_node)

        CE_bottom_cord = self.hash_cords(40.820990, -75.513362)  # 40.8209900, -75.5133619
        TRP_bottom_to_CE = self.hash_cords(40.820735, -75.513652)  # 40.8207352, -75.5136519
        VSW_bottom_to_CE = self.hash_cords(40.820997, -75.514022)  # 40.8209971, -75.5140221
        for n in self.nodes:
            if n.get_node_by_node_id(CE_bottom_cord) is not None:
                temp1 = n

        for n in self.nodes:
            if n.get_node_by_node_id(TRP_bottom_to_CE) is not None:
                temp2 = n

        CE_bottom_cord_node = temp1
        TRP_bottom_to_CE_node = temp2
        self.graph.add_edge(TRP_bottom_to_CE_node, CE_bottom_cord_node)

        VST_bottom_cord = self.hash_cords(40.820009, -75.514396) # 40.8200094, -75.5143964

        for n in self.nodes:
            if n.get_node_by_node_id(VST_bottom_cord) is not None:
                temp2 = n

        VST_bottom_cord_node = temp2
        self.graph.add_edge(TRP_bottom_to_CE_node, VST_bottom_cord_node)


        for n in self.nodes:
            if n.get_node_by_node_id(VSW_bottom_to_CE) is not None:
                temp2 = n

        VSW_bottom_to_CE_node = temp2
        self.graph.add_edge(VSW_bottom_to_CE_node, CE_bottom_cord_node)

        Comet_bottom_cord = self.hash_cords(40.821483, -75.512737)  # 40.8214828, -75.5127367
        Comet_bottom_con_cord = self.hash_cords(40.821734, -75.513073)  # 40.8217339, -75.5130726
        Comet_bottom_con_cord_2 = self.hash_cords(40.821831, -75.512484)  # 40.8218310, -75.5124844

        for n in self.nodes:
            if n.get_node_by_node_id(Comet_bottom_cord) is not None:
                temp1 = n

        for n in self.nodes:
            if n.get_node_by_node_id(Comet_bottom_con_cord) is not None:
                temp2 = n

        Comet_bottom_cord_node = temp1
        Comet_bottom_con_cord_node = temp2
        self.graph.add_edge(Comet_bottom_con_cord_node, Comet_bottom_cord_node)

        for n in self.nodes:
            if n.get_node_by_node_id(Comet_bottom_con_cord_2) is not None:
                temp2 = n

        Comet_bottom_con_cord_2_node = temp2
        self.graph.add_edge(Comet_bottom_con_cord_2_node, Comet_bottom_cord_node)

        Vista_bottom_cord = self.hash_cords(40.812526, -75.518131)  # 40.8125263, -75.5181311
        Vist_bottom_con_cord = self.hash_cords(40.812585, -75.518169)  # 40.8125847, -75.5181690
        for n in self.nodes:
            if n.get_node_by_node_id(Vista_bottom_cord) is not None:
                temp1 = n

        for n in self.nodes:
            if n.get_node_by_node_id(Vist_bottom_con_cord) is not None:
                temp2 = n

        Vista_bottom_cord_node = temp1
        Vist_bottom_con_cord_node = temp2
        self.graph.add_edge(Vist_bottom_con_cord_node, Vista_bottom_cord_node)

        node_id = self.hash_cords(40.813777, -75.515948)
        for n in self.nodes:
            if n.get_by_name_cord('MidWay', node_id) is not None:
                temp1 = n

        for n in self.nodes:
            if n.get_by_name_cord('Lower Main Street', node_id):
                temp2 = n

        MidWay_node = temp1
        MidWay_con_cord = temp2
        self.graph.add_edge(MidWay_node, MidWay_con_cord)

        node_id = self.hash_cords(40.817082, -75.515907)
        for n in self.nodes:
            if n.get_by_name_cord('Burma Road', node_id) is not None:
                temp1 = n

        for n in self.nodes:
            if n.get_by_name_cord('Main Street Chair', node_id):
                temp2 = n

        Burma_node = temp1
        Main_node = temp2
        self.graph.add_edge(Burma_node, Main_node)

        node_id = self.hash_cords(40.809457, -75.515465)
        for n in self.nodes:
            if n.get_by_name_cord("Tut's Lane", node_id) is not None:
                temp1 = n

        for n in self.nodes:
            if n.get_by_name_cord('Lazy Mile', node_id):
                temp2 = n

        Tuts_node = temp1
        LM_node = temp2
        self.graph.add_edge(Tuts_node, LM_node)



pd = PullData()  # Create Pull Data.
d = pd.read_data('BlueMountain2.geojson') # Pass data to read from.

g = pd.convert_data(d) # Graph returned from convert_data.
start = pd.nodes[0]
end = pd.nodes[600]


g.to_string()
find_empty = g.dijkstra(pd.nodes[0], pd.nodes[634])

for pairs in find_empty.items():
    if pairs[1] is None:
        print(pairs[0])
