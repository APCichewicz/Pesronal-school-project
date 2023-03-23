from Hash import Hash
class Vertex:
    def __init__(self, id):
        self.id = id
        self.neighbors = Hash()
        self.visited = False

    def add_neighbor(self, neighbor, weight=0):
        self.neighbors.set(neighbor.id, weight)

    def get_neighbors(self):
        return self.neighbors.keys()

    def get_weights(self):
        return self.neighbors.values()

    def get_neighbor(self, neighbor):
        return self.neighbors.get(neighbor)

    def get_id(self):
        return self.id
#if the node is in the graph, return the weight of the edge connecting it to this node, else return infinite weight.
    def get_weight(self, neighbor: str):
        result = self.neighbors.get(neighbor)
        if result:
            return result[1]
        return float('inf')

    def visit(self):
        self.visited = True

    def is_visited(self):
        return self.visited

    def clear_visit(self):
        self.visited = False

    def __str__(self):
        return f"{self.id}"


class Graph:
    def __init__(self, vertices: list = []):
        self.vertex_list = vertices
        self.vertices = Hash()
        self.num_vertices = 0

    def add_vertex(self, node):
        self.num_vertices += 1
        new_vertex = Vertex(node)
        self.vertices.set(node, new_vertex)
        self.vertex_list.append(new_vertex)

    def clear_visits(self):
        for vert in self.vertex_list:
            vert.clear_visit()

    def get_vertex(self, n):
        return self.vertices.get(n)[1]

    def add_edge(self, start, end, cost=0):
        if not self.vertices.get(start):
            self.add_vertex(start)
        if not self.vertices.get(end):
            self.add_vertex(end)
        self.vertices.get(start)[1].add_neighbor(self.vertices.get(end)[1], float(cost))
        self.vertices.get(end)[1].add_neighbor(self.vertices.get(start)[1], float(cost))

    def get_vertices_keys(self):
        return self.vertices.keys()

    def get_vertices_values(self):
        return self.vertices.values()

def read_distance_file():
    graph = Graph()
    with open("./data/addresses.csv") as addr:
        lines = addr.readlines()
        addresses = []
        for line in lines:
            line = line.replace('"', "")
            line = line.replace("'", "")
            addresses.append(line.strip())
    with open("./data/distance_table.csv", 'r') as f:
        lines = f.readlines()
        arr = []
        for line in lines:
            line = line.replace('"', "")
            arr.append(line.strip().split(","))
    for i in range(len(arr)):
        for j in range(len(arr) - i):
            graph.add_edge(addresses[i], addresses[i+j], arr[j + i][i])
    bad_vertex = Vertex("bad")
    for vertex in graph.vertex_list:
        graph.add_edge(bad_vertex.id, vertex.id, float('inf'))
    return graph





