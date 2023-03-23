from Hash import Hash
# a class to hold the data of a vertex and its associated adjacency list
class Vertex:
    def __init__(self, id):
        self.id = id
        self.neighbors = Hash()
        self.visited = False
    # function to add a neighbor to the adjacency matrix as implemented with the hash class. associates a neighbor
    # node with a distance/weight
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
# if the node is in the graph, return the weight of the edge connecting it to this node, else return infinite weight.
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
    """
    a graph data structure that wraps around the vertex class and hash class.
    the vertices are stored in a hash for fast access times as well as in a list for iteration
    """
    def __init__(self, vertices: list = []):
        self.vertex_list = vertices
        self.vertices = Hash()
        self.num_vertices = 0
    # add a vertex to the graph. the node is added to the vertex list as well as the hash.
    def add_vertex(self, node):
        self.num_vertices += 1
        new_vertex = Vertex(node)
        self.vertices.set(node, new_vertex)
        self.vertex_list.append(new_vertex)
    # iterate over each vertex in the list and clear the visited boolean value. this is so that the same vertex is not
    # visited more than once.
    def clear_visits(self):
        for vert in self.vertex_list:
            vert.clear_visit()
    # retrieves a vertex with a given address as the key from the vertex hash
    def get_vertex(self, n):
        return self.vertices.get(n)[1]

    # takes a start and end node, checks if each one exists within the address hash. if they do not, they are added
    # once they are guaranteed to exist within the hash, each vertex is added to the other's list of neighbors
    def add_edge(self, start, end, cost=0):
        if not self.vertices.get(start):
            self.add_vertex(start)
        if not self.vertices.get(end):
            self.add_vertex(end)
        self.vertices.get(start)[1].add_neighbor(self.vertices.get(end)[1], float(cost))
        self.vertices.get(end)[1].add_neighbor(self.vertices.get(start)[1], float(cost))
    # returns a list of addresses extant within the hash
    def get_vertices_keys(self):
        return self.vertices.keys()
    #returns all values extant within the hashtable
    def get_vertices_values(self):
        return self.vertices.values()

def read_distance_file():
    #instantiate a new graph
    graph = Graph()
    # read the address file and get the information formatted appropriately for use
    with open("./data/addresses.csv") as addr:
        lines = addr.readlines()
        addresses = []
        for line in lines:
            line = line.replace('"', "")
            line = line.replace("'", "")
            addresses.append(line.strip())
    # read the distance table and make an array of arrays out of the values, indexed such that it can be corresponded
    # the previous array of addresses
    with open("./data/distance_table.csv", 'r') as f:
        lines = f.readlines()
        arr = []
        for line in lines:
            line = line.replace('"', "")
            arr.append(line.strip().split(","))
    # iterate over each of the distance values such that the corresponding addresses match up to the appropriate
    # distance values
    for i in range(len(arr)):
        for j in range(len(arr) - i):
            graph.add_edge(addresses[i], addresses[i+j], arr[j + i][i])
    # set up a "bad" vertex to store the information for incorrectly addressed packages and set the weight to inf
    # so that they will always be the lowest priority delivery while the address remains uncorrected.
    bad_vertex = Vertex("bad")
    for vertex in graph.vertex_list:
        graph.add_edge(bad_vertex.id, vertex.id, float('inf'))
    return graph





