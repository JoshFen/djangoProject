from geopy.distance import geodesic
class Graph:
    def __init__(self):
      self.graph = {}

    # Function to represent the graph as a string.
    def to_string(self):
        for keys in self.graph:  # Iterates for the nodes in the graph.
            print('Node: ')
            print(keys)  # Print Node.
            if len(self.graph[keys].keys()) < 1:  # Error Check.
                print('here')
            else:
                for cons in self.graph[keys]:  # Iterates for connections in node.
                    print('Connections: ')
                    print(cons)  # Print Connection.
                print('---------------------------------------')  # Slice.

    # Function to return a list of vertices.
    def get_vertices(self):
        vertices = []  # Create the vertices list.
        for key in  self.graph.keys():  # Iterates for the vertices in the graph.
            vertices.append(key.node_id)  # Appends the vertex
        return vertices  # Return the list.

    # Function to return the edge connections of the graph.
    def generate_edges(self):
        edges = []  # Creates the edges list.
        for key in self.graph:  # Iterates for the vertices in the graph.
            for con in self.graph[key]:  # Iterates for the connections to the current vertex.
                edges.append((key, con))  # Appends the two nodes as an edge.
        return edges  # Returns the edge list.

    # Function to add a vertex to the graph.
    def add_vertex(self, vertex):
        if vertex not in self.graph.keys():  # Checks if the node is already in the graph.
            self.graph[vertex] = {}  # Creates the vertex.

    # Function to add and edge between two vertices.
    def add_edge(self, origin, end):
        self.graph[origin][end] = self.distance(origin, end)  # Create the edge.

    # Function to calculate distance between two nodes.
    def distance(self, origin, end):
        p1 = (origin.lat, origin.lon)  # Set of lat long for origin node.
        p2 = (end.lat, end.lon)  # Set of lat long for destination node.
        return geodesic(p1, p2)  # Return the distance between them in km.

    # Function for data error handling.
    def delete_extras(self, node):
        if self.graph[node].keys is None:  # Checks if the node has any connections.
            del self.graph[node]  # Deletes the node if no connections.

    def dijkstra(self, start, end):
        parent = {}  # previous node to assist in finding the shortest path
        distance = {}  # shortest path from one node to another
        path = []  # path list to store the path
        s = set()
        queue = []  # creating nodes variable

        i1 = (90.0000, 1235.0000)
        i2 = (0.0000, 45.0000)
        infinity = geodesic(i1, i2)  # Large distance value for distance calculating.

        for vertex in self.graph:  # Iterates for each node/vertex in the graph.
            distance[vertex] = infinity  # Sets the distance to infinity (this case two furthest points on earth).
            parent[vertex] = None  # Sets parent to null since unknown.
            queue.append(vertex)  # Appends the node to the queue.

        i1 = (90.0000, 0.0)
        i2 = (90.0000, 0.0)
        distance[start] = geodesic(i1, i2)  # Sets origins distance to 0.

        while queue:  # Iterates while the queue is not empty.
            cur = queue[0]  # Set current node to first element in the queue.
            for node in queue:  # Iterates for each node in the queue.
                if distance[node] < distance[cur]:  # Finds the node with the smallest distance in the queue.
                    cur = node  # Cur is now this node.

            for neighbor, dist in self.graph[cur].items():  # Iterates for each connection of the current node.
                if distance[cur] + dist < distance[neighbor]:  # Checks the for smallest distance.
                    distance[neighbor] = dist + distance[cur]  # Sets the nodes distance to the smallest distance.
                    parent[neighbor] = cur  # Sets currents new parent node.

            queue.remove(cur)  # Removes visited node from the queue.

        path.append(end)  # Adds end node to list.
        while parent[end]:  # Iterates until reaching origin node.
            path.append(parent[end])  # Appends the current node's parent node.
            end = parent[end]  # Moves to that parent node.

        return path  # Return the final path.



