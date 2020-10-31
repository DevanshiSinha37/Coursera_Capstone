from CreateGraph import *
from Algo_ResidualGraph import Residual_Graph
import math
import copy


######--------------File Reader-----------------#####
def graph_creation():
    graph = createmygraph()
    return graph


#####--------------Define Graph Output-----------------#####
class FlowOutput:
    def __init__(self):
        self.flowpath = []
        self.flowval = 0


######--------------Find a path with positive capacity-----------------#####
def s_t_path(R, start, end):

    active = []
    active.append(start)
    parent = [0] * len(R.vertices)
    parent[R.vertices.index(start)] = start
    unseen = R.vertices.copy()
    unseen.remove(start)

    while len(active) != 0 and len(unseen) != 0:
        j = active[0]
        active.remove(j)

        for arc in R.arcs:
            if arc[0] == j:
                if arc[3] > 0:
                    if arc[1] in unseen:
                        parent[R.vertices.index(arc[1])] = j
                        unseen.remove(arc[1])
                        active.append(arc[1])

    if not end in unseen:
        reverse_path = []
        node = end
        while node != start:
            reverse_path.append(node)
            node = parent[R.vertices.index(node)]
        reverse_path.append(start)
        reverse_path.reverse()
        #print('Path:', reverse_path)
        return reverse_path

    else:
        #print('Node in', unseen, 'cannot be visited from', start)
        return []


######--------------Find a path with positive capacity-----------------#####
def retrive_flow(Arcs, R, end):

    flow = []
    actual_flow = []
    flowval = 0

    for arc in Arcs:
        for r_arc in R.arcs:
            if arc[0] == r_arc[0] and arc[1] == r_arc[1]:
                flow.append([arc[0], arc[1], arc[2], max(arc[3] - r_arc[3], 0)])

                if arc[3] > r_arc[3]:
                    actual_flow.append([arc[0], arc[1], arc[2], arc[3] - r_arc[3]])

                    if arc[1] == end:
                        flowval = flowval + arc[3] - r_arc[3]

    flow_output = FlowOutput()
    flow_output.flowval = flowval
    flow_output.flowpath = actual_flow

    return flow_output



######--------------Define Ford Fulkerson-----------------#####
def FoldFulkerson(Nodes, Arcs, start, end):
    RG_Residual = Residual_Graph(Nodes, Arcs)
    R_Arc_copy = copy.deepcopy(RG_Residual.arcs)
    flow_val = 0

    path_st = s_t_path(RG_Residual,start,end)

    #print('Actual Arcs:', Arcs)
    #print('Residual Arcs:', R_Arc_copy)

    while len(path_st) != 0:

        min_capacity = math.inf
        j = 1
        for i in path_st:
            if j < len(path_st):
                for arc in R_Arc_copy:
                    if arc[0] == i and arc[1] == path_st[j]:
                        if min_capacity > arc[3]:
                            min_capacity = arc[3]
            j = j + 1

        flow_val = flow_val + min_capacity

        j2 = 1
        for i2 in path_st:
            if j2 < len(path_st):
                for arc2 in R_Arc_copy:
                    if arc2[0] == i2 and arc2[1] == path_st[j2]:
                        R_Arc_copy[R_Arc_copy.index(arc2)][3] = R_Arc_copy[R_Arc_copy.index(arc2)][3] - min_capacity
                        #print('Arc:', Arcs[R_Arc_copy.index(arc2)])
                    elif arc2[0] == path_st[j2] and arc2[1] == i2:
                        R_Arc_copy[R_Arc_copy.index(arc2)][3] = R_Arc_copy[R_Arc_copy.index(arc2)][3] + min_capacity
            j2 = j2 + 1

        #print('Path Flow:', path_st)
        #print('Flow Value:', flow_val)
        RG_Residual.arcs = R_Arc_copy.copy()
        path_st = s_t_path(RG_Residual,start,end)


    flow_path = retrive_flow(Arcs, RG_Residual, end)

    print('\nTotal Flow Value:', flow_val)
    for i3 in flow_path.flowpath:
        print(i3[0], '->', i3[1], ' Flow =', i3[3])
    #print('Flow Path:', flow_path.flowpath)
    #print_graph(RG_Residual)

    return flow_val


######--------------Take input from user-----------------#####
def run_file():
    mygraph = graph_creation()
    V = mygraph.vertices
    A = mygraph.arcs

    input1 = input('\nCheck Connectivity from node: ')
    input2 = input('Check Connectivity to node: ')

    FoldFulkerson(V, A, input1, input2)

run_file()




