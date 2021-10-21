from CreateGraph import createmygraph
from Algo_ResidualGraph import Residual_Graph
from Algo_FoldFulkerson import retrive_flow
import math


######--------------File Reader-----------------#####
def graph_creation():
    graph = createmygraph()
    return graph


######--------------Setting Distance Labels-----------------#####
def set_distance_labels(nodes, arcs, end):
    distance = [math.inf] * len(nodes)
    distance[nodes.index(end)] = 0
    active = [end]

    while len(active) > 0:
        mindistance = math.inf
        j = ""
        for node in active:
            if distance[nodes.index(node)] < mindistance:
                mindistance = distance[nodes.index(node)]
                j = node
        active.remove(j)
        for arc in arcs:
            if arc[1] == j and distance[nodes.index(arc[0])] > distance[nodes.index(j)] + 1:
                distance[nodes.index(arc[0])] = distance[nodes.index(j)] + 1
                active.append(arc[0])

    return distance


######--------------Push-----------------#####
def push_flow(nodes, arcs, active, excess, start, end, active_arc, active_node):
    f = min(excess[nodes.index(active_node)], active_arc[3])
    print('Pushing ', f, ' flow to ', active_arc[1], ' along arc ', active_arc)
    excess[nodes.index(active_node)] -= f

    if active_arc[1] != start and active_arc[1] != end:
        excess[nodes.index(active_arc[1])] += f
        if not active_arc[1] in active:
            active.append(active_arc[1])

    if active_arc[1] == end:
        print('Flow to t:', f)

    for arc in arcs:
        if arc[0] == active_arc[0] and arc[1] == active_arc[1]:
            arc[3] -= f
        if arc[0] == active_arc[1] and arc[1] == active_arc[0]:
            arc[3] += f

    if excess[nodes.index(active_node)] == 0:
        active.remove(active_node)


######--------------Relabel-----------------#####
def relabel(nodes, arcs, active, distance):

    min_dist = math.inf
    for node in active:
        if distance[nodes.index(node)] < min_dist:
            min_dist = distance[nodes.index(node)]
            min_dist_node = node

    neighbour_dist = []
    for arc in arcs:
        if arc[0] == min_dist_node and arc[3] > 0:
            print('Neighbour:', arc[1])
            neighbour_dist.append(distance[nodes.index(arc[1])])

    print('Min neighbur dist:', min(neighbour_dist))
    distance[nodes.index(min_dist_node)] = min(neighbour_dist) + 1


######--------------Admissible Arcs-----------------#####
def find_admissiblearcs(nodes, arcs, distance):
    admissible_arcs = []
    for arc in arcs:
        if distance[nodes.index(arc[0])] == distance[nodes.index(arc[1])] + 1 and arc[3] > 0:
            admissible_arcs.append(arc)
    return admissible_arcs


######--------------Pre_Flow_Push-----------------#####
def algo_preflowpush(nodes, arcs, start, end):
    print('\nRunning PreFlow Push Algorithm')

    residual = Residual_Graph(nodes, arcs)
    distance = set_distance_labels(residual.vertices, residual.arcs, end)
    if distance[nodes.index(start)] > len(nodes):
        print('\n start and end are disconnected')
        return

    distance[nodes.index(start)] = len(nodes)
    #distance[nodes.index(start)] = 0
    print('Distance:', distance)
    excess = [0] * len(nodes)
    active = []

    for arc in residual.arcs:
        if arc[0] == start:
            active.append(arc[1])
            excess[nodes.index(arc[1])] = arc[3]
            for backarc in residual.arcs:
                if backarc[0] == arc[1] and backarc[1] == arc[0]:
                    backarc[3] = arc[3]
            arc[3] = 0

    while len(active) != 0:
        admissible_arcs = find_admissiblearcs(
            residual.vertices, residual.arcs, distance)
        push = False
        print('')
        for arc in admissible_arcs:
            if arc[0] in active:
                push_flow(residual.vertices, residual.arcs,
                          active, excess, start, end, arc, arc[0])
                push = True

        if not push:
            print('')
            relabel(residual.vertices, residual.arcs, active, distance)
            print('Active:', active)
            print('Distance:', distance)

    retr_flow = retrive_flow(arcs, residual, end)

    for i3 in retr_flow.flowpath:
        print(i3[0], '->', i3[1], ' Flow =', i3[3])

    print('Total Flow =', retr_flow.flowval)

    return retr_flow


######--------------Take input from user-----------------#####
def run_file():
    mygraph = graph_creation()
    V = mygraph.vertices
    A = mygraph.arcs

    input1 = input('\nCheck Connectivity from node: ')
    input2 = input('Check Connectivity to node: ')
    algo_preflowpush(V, A, input1, input2)


run_file()
