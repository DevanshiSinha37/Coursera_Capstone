class Graph:
    def __init__(self):
        self.vertices = []
        self.arcs = []

    def add_vertex(self, v):
        if v not in self.vertices:
            self.vertices.append(v)
        else:
            print("Vertex", v, "already exists")

    def add_arc_costwala(self, head, tail, cost = 0, capacity = 0):
        if head not in self.vertices:
            self.vertices.append(head)
        if tail not in self.vertices:
            self.vertices.append(tail)
        self.arcs.append([head, tail, int(cost), int(capacity)])

    def add_arc_capacitywala(self, head, tail, capacity = 0, cost = 0):
        if head not in self.vertices:
            self.vertices.append(head)
        if tail not in self.vertices:
            self.vertices.append(tail)
        self.arcs.append([head, tail, int(capacity), int(cost)])


def print_graph(graph):
    print('Vertices:', graph.vertices)
    print('Arcs:', graph.arcs)
    for arc in graph.arcs:
            print(arc[0], "->", arc[1], " arc cost:", arc[2], " arc capacity:", arc[3])


######--------------File Reader-----------------#####
def createmygraph():
    # file_name = input("Enter data file name: ")
    #data_file = open("D://IIMA//Term 4//WwN//Python//Quiz3//data files//" + file_name)
    data_file = open("D:\IIMA\Term_4\WwN\Codes\Graphs\quiz3Q2.txt")

    graph = Graph()
    for line in data_file.readlines():
        line = line.split()
        graph.add_arc_costwala(line[0], line[1], line[2], line[3])
        #graph.add_arc_capacitywala(line[0], line[1], line[2], line[3])
    print_graph(graph)
    return graph

