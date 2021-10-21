from CreateGraph import createmygraph
import copy


######--------------File Reader-----------------#####
def graph_creation():
    graph = createmygraph()
    return graph

#####--------------Define Graph Output-----------------#####


class RG_graph:
    def __init__(self):
        self.vertices = []
        self.arcs = []


######--------------Define Residual Graph-----------------#####
def Residual_Graph(Nodes, Arcs):
    Residual_G = RG_graph()
    Residual_G.vertices = copy.deepcopy(Nodes)
    Residual_G.arcs = copy.deepcopy(Arcs)
    #print('RG Nodes:', Residual_G.vertices)
    #print('RG Arcs:', Residual_G.arcs)

    for arc in Arcs:
        present = False
        #print('Arc', arc)
        for test in Arcs:
            #print('Test', test)
            if arc[0] == test[1] and arc[1] == test[0]:
                present = True
        if present == False:
            Residual_G.arcs.append([arc[1], arc[0], arc[2], 0])
    return Residual_G


def print_graph(graph):
    print('Vertices:', graph.vertices)
    print('Arcs:', graph.arcs)
    for arc in graph.arcs:
        print(arc[0], "->", arc[1], " arc cost:",
              arc[2], " arc capacity:", arc[3])


######--------------Take input from user-----------------#####
def run_file():
    mygraph = graph_creation()
    V = mygraph.vertices
    A = mygraph.arcs
    RG_Graph_ans = Residual_Graph(V, A)
    # print_graph(RG_Graph_ans)
    return RG_Graph_ans

# run_file()
