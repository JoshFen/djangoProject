from geopy.distance import geodesic
class Graph:
    def __init__(self):
      self.graph = {}

    def to_string(self):
        for keys in self.graph:
            print('Node: ')
            print(keys)
            if len(self.graph[keys].keys()) < 1:
                print('here')
            else:
                for cons in self.graph[keys]:
                    print('Connections: ')
                    print(cons)
                print('---------------------------------------')

    def get_vertices(self):
        vertices = []
        for key in  self.graph.keys():
            vertices.append(key.node_id)

        return vertices

    def generate_edges(self):
        edges = []
        for key in self.graph:
            s_id = key.node_id
            for con in self.graph[key]:
                edges.append((key, con))
        return edges

    def add_vertex(self, vertex):
        if vertex not in self.graph.keys():
            self.graph[vertex] = {}

    def add_edge(self, origin, end):
        self.graph[origin][end] =  self.distance(origin, end)
        print(self.graph[origin].keys())
        print(self.graph[origin][end])
        print("Edge Added")



    def distance(self, origin, end):
        p1 = (origin.lat ,origin.lon)
        p2 = (end.lat, end.lon)

        return geodesic(p1,p2)

    def delete_extras(self, node):
        if self.graph[node].keys is None:
            del self.graph[node]


    def dijkstra(self, start, end):
        parent= {}  # previous node to assist in finding shortest path
        distance = {}  # shortest path from one node to another
        path = []  # path list to store the path
        s = set()
        queue = []  # creating nodes variable

        i1 = (90.0000, 1235.0000)
        i2 = (0.0000, 45.0000)
        infinity = geodesic(i1, i2)

        for vertex in self.graph:
            distance[vertex] = infinity
            parent[vertex] = None
            queue.append(vertex)

        i1 = (90.0000, 0.0)
        i2 = (90.0000, 0.0)
        distance[start] = geodesic(i1, i2)

        while queue:
            lease = None
            cur = queue[0]
            for node in queue:
                if distance[node] < distance[cur]:
                    cur = node

            for neighbor, dist in self.graph[cur].items():
                if distance[cur] + dist < distance[neighbor]:
                    distance[neighbor] = dist + distance[cur]
                    parent[neighbor] = cur

            queue.remove(cur)

        return(parent)




