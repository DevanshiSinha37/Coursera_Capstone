from collections.abc import Iterable
import numpy as np

K = []
D = []


def fillcapacity(str):
    global K, D
    K = [None]*int((len(str)-1)/2)
    for i in range(int((len(str)-1)/2)):
        if i == 0:
            K[i] = float(str[int((len(str)-1)/2 + 1)][1:])
        elif i == int((len(str)-1)/2-1):
            K[i] = float(str[len(str)-1][:-1])
        else:
            K[i] = float(str[int((len(str)-1)/2 + 1 + i)])


def filldemand(str):
    global K, D
    D = [None]*int((len(str)-1)/2)
    for i in range(int((len(str)-1)/2)):
        if i == 0:
            D[i] = float(str[int((len(str)-1)/2 + 1)][1:])
        elif i == int((len(str)-1)/2-1):
            D[i] = float(str[len(str)-1][:-1])
        else:
            D[i] = float(str[int((len(str)-1)/2 + 1 + i)])


def get_second_smallest(arr):
    local_Arr = arr
    return np.partition(local_Arr, 1)[1]


def get_nonzeros(ar):
    return np.count_nonzero(ar)


def check_d(d):
    if (np.all(d >= 0)):
        return 1
    else:
        return 0


def form_loop(X, oi, oj):
    rows = len(X)
    vertices = []
    cordinates_of_rect = []
    if (rows == 0):
        return cordinates_of_rect
    columns = len(X[0])
    X[oi][oj] = 1
    table = {}

    # scanning from top to bottom
    # line by line
    for i in range(rows):
        for j in range(columns - 1):
            for k in range(j + 1, columns):

                # if found two 1's in a column
                if (X[i][j] > 0 and
                        X[i][k] > 0):

                    # check if there exists 1's in same
                    # row previously then return true
                    if (j in table and k in table[j]):
                        for u, v, w in vertices:
                            if v == j and w == k:
                                x_coord = u
                                if (u == oi and v == oj):
                                    cordinates_of_rect.append([u, v])
                                    cordinates_of_rect.append([u, w])
                                    cordinates_of_rect.append([i, k])
                                    cordinates_of_rect.append([i, j])
                                    return cordinates_of_rect
                                if (u == oi and w == oj):
                                    cordinates_of_rect.append([u, w])
                                    cordinates_of_rect.append([u, v])
                                    cordinates_of_rect.append([i, j])
                                    cordinates_of_rect.append([i, k])
                                    return cordinates_of_rect
                        if (i == oi and j == oj):
                            cordinates_of_rect.append([i, j])
                            cordinates_of_rect.append([i, k])
                            cordinates_of_rect.append([x_coord, k])
                            cordinates_of_rect.append([x_coord, j])
                            return cordinates_of_rect
                        if (i == oi and k == oj):
                            cordinates_of_rect.append([i, k])
                            cordinates_of_rect.append([i, j])
                            cordinates_of_rect.append([x_coord, j])
                            cordinates_of_rect.append([x_coord, k])
                            return cordinates_of_rect

                    if (k in table and j in table[k]):
                        for u, v, w in vertices:
                            if v == k and w == j:
                                x_coord = u
                                if (u == oi and v == oj):
                                    cordinates_of_rect.append([u, v])
                                    cordinates_of_rect.append([u, w])
                                    cordinates_of_rect.append([i, j])
                                    cordinates_of_rect.append([i, k])
                                    return cordinates_of_rect
                                if (u == oi and w == oj):
                                    cordinates_of_rect.append([u, w])
                                    cordinates_of_rect.append([u, v])
                                    cordinates_of_rect.append([i, k])
                                    cordinates_of_rect.append([i, j])
                                    return cordinates_of_rect
                        if (i == oi and k == oj):
                            cordinates_of_rect.append([i, k])
                            cordinates_of_rect.append([i, j])
                            cordinates_of_rect.append([x_coord, j])
                            cordinates_of_rect.append([x_coord, k])
                            return cordinates_of_rect
                        if (i == oi and j == oj):
                            cordinates_of_rect.append([i, j])
                            cordinates_of_rect.append([i, k])
                            cordinates_of_rect.append([x_coord, k])
                            cordinates_of_rect.append([x_coord, j])
                            return cordinates_of_rect

                    # store the indexes in hashset
                    vertices.append([i, j, k])
                    if j not in table:
                        table[j] = set()
                    if k not in table:
                        table[k] = set()
                    table[j].add(k)
                    table[k].add(j)
        #print (table)
    return cordinates_of_rect


def occupy_uv(X):
    global D, K, cost_m, np_cost, U, V
    np_X = np.array(X)

    #print ("\nStarting X")
    #print (np_X)

    max_in_rows = (np.apply_along_axis(get_nonzeros, axis=1, arr=np_X))
    max_in_columns = (np.apply_along_axis(get_nonzeros, axis=0, arr=np_X))

    row_max = 1
    column_max = 0
    max_value_in_row = np.amax(max_in_rows)
    max_value_in_column = np.amax(max_in_columns)
    if max_value_in_column > max_value_in_row:
        column_max = 1
        row_max = 0
    if row_max == 1:
        initial_variable = np.where(max_in_rows == max_value_in_row)[0][0]
    if column_max == 1:
        initial_variable = np.where(
            max_in_columns == max_value_in_column)[0][0]

    number_of_rows = np_X.shape[0]
    number_of_columns = np_X.shape[1]
    number_of_eq = number_of_rows + number_of_columns
    coefficients = np.zeros((number_of_eq, number_of_eq))
    RHS = np.zeros(number_of_eq)
    counter = 0

    for x in range(0, number_of_rows):
        for y in range(0, number_of_columns):
            if np_X[x, y] != 0:
                coefficients[counter, x] = 1
                coefficients[counter, number_of_rows+y] = 1
                RHS[counter] = cost_m[x][y]
                counter = counter + 1

    if row_max == 1:
        coefficients[counter, initial_variable] = 1
    else:
        coefficients[counter, number_of_rows + initial_variable] = 1
    #print (coefficients)
    #print (RHS)
    answer = np.linalg.inv(coefficients).dot(RHS)
    #print (answer)
    d = np.zeros((number_of_rows, number_of_columns))
    for x in range(0, number_of_rows):
        for y in range(0, number_of_columns):
            if np_X[x, y] == 0:
                d[x, y] = cost_m[x][y] - answer[x] - answer[number_of_rows+y]
    #print ("\nIntermediate D")
    #print (d)
    minimum_in_d = np.where(d == np.amin(d))
    #print (minimum_in_d)
    minimum_i = minimum_in_d[0][0]
    minimum_j = minimum_in_d[1][0]
    #print (check_d(d))
    if (not check_d(d)):
        cord_list = form_loop(X, minimum_i, minimum_j)
        #print (cord_list)
        X[minimum_i][minimum_j] = 0
        if cord_list:
            units = []
            for a, b in cord_list:
                units.append(X[a][b])
            res = min([i for j, i in enumerate(units) if j % 2 != 0])
            for idx, val in enumerate(cord_list):
                if idx % 2 == 0:
                    X[val[0]][val[1]] = X[val[0]][val[1]] + res
                else:
                    X[val[0]][val[1]] = X[val[0]][val[1]] - res
        occupy_uv(X)
    else:
        print("\nOptimal Solution")
        print(np_X)
        original_cost = np.array(cost_m)
        print("\nOptimal Cost")
        Optimal_cost = (np.multiply(np_X, original_cost))
        print(Optimal_cost.sum())
    return


def vogel():
    global D, K, cost_m, X, np_cost
    cost = 0
    suppliers_left = len(K)
    demands_unmet = len(D)
    while (suppliers_left > 1 and demands_unmet > 1):
        max_penalty = -1
        for i in range(len(K)):
            if K[i] > 0:
                #m = cost_m[i].index(min(cost_m[i]))
                #n = cost_m[i].index(sorted(cost_m)[1])
                m_row = np.amin(np_cost, axis=1)
                m = m_row[i]
                index_value = np.where(np_cost[i] == np.amin(np_cost[i]))
                m_index = index_value[0][0]
                n = get_second_smallest(np_cost[i])
                row_penalty = n - m
                if (row_penalty > max_penalty):
                    max_penalty = row_penalty
                    frm = i
                    to = m_index
        #print ('\nmax penalty after rows is {}'.format(max_penalty))
        cost_transpose = np_cost.T
        for j in range(len(D)):
            if D[j] > 0:
                m_column = np.amin(cost_transpose, axis=1)
                m = m_column[j]
                index_value = np.where(
                    cost_transpose[j] == np.amin(cost_transpose[j]))
                m_index = index_value[0][0]
                n = get_second_smallest(cost_transpose[j])
                column_penalty = n - m
                #print (column_penalty)
                if (column_penalty > max_penalty):
                    max_penalty = column_penalty
                    frm = m_index
                    to = j
        X[frm][to] = min(K[frm], D[to])
        #print ('max penalty after columns is {}'.format(max_penalty))
        cost = cost + np_cost[frm][to]*X[frm][to]
        K[frm] = K[frm] - X[frm][to]
        D[to] = D[to] - X[frm][to]
        if (K[frm] == float(0)):
            for k in range(len(D)):
                np_cost[frm][k] = float("inf")
            suppliers_left = suppliers_left - 1
        if (D[to] == float(0)):
            for k in range(len(K)):
                np_cost[k][to] = float("inf")
            demands_unmet = demands_unmet - 1
        # print(np_cost)
    if (suppliers_left == 1):
        frm_arr = np.nonzero(K)
        frm = frm_arr[0][0]
        for j in range(len(D)):
            if X[frm][j] == 0:
                X[frm][j] = D[j]
            if np_cost[frm][j] != float("inf"):
                cost = cost + np_cost[frm][j]*X[frm][j]
    else:
        to_arr = np.nonzero(D)
        print(to_arr)
        to = to_arr[0][0]
        for i in range(len(K)):
            if X[i][to] == 0:
                X[i][to] = K[i]
            if np_cost[i][to] != float("inf"):
                cost = cost + np_cost[i][to]*X[i][to]
    print("\nVogel cost")
    print(cost)
    print("\nVogel solution")
    for w in X:
        print(w)


filepath = 'modi.txt'
with open(filepath) as fp:
    line = fp.readline()
    count = 1
    while line:
        str = line.split()
        if count == 1:
            fillcapacity(str)
        elif count == 2:
            filldemand(str)
        line = fp.readline()
        count = count+1

total_cap = sum(K)
total_demand = sum(D)

print("total capacity is {}".format(total_cap))
print("total demand is {}".format(total_demand))
added_column = 0
added_row = 0

if (total_cap > total_demand):
    D.append(total_cap-total_demand)
    added_column = 1

if (total_demand > total_cap):
    K.append(total_demand - total_cap)
    added_row = 1

print("\nCapacities are")
print(K)

print("\nDemands are")
print(D)

cost_m = [None] * len(K)

with open(filepath) as fp:
    line = fp.readline()
    count = 1
    while line:
        str = line.split()
        if count >= 3:
            numbers = [float(x) for x in str]
            if added_column == 1:
                numbers.append(0)
            cost_m[count-3] = numbers
        line = fp.readline()
        count = count+1

if added_row == 1:
    cost_m[-1] = [0]*len(D)

print("\nCosts are")
for j in cost_m:
    print(j)

np_cost = np.array(cost_m)
X = [[0 for x in range(len(D))] for y in range(len(K))]

vogel()

U = [0]*len(K)
V = [0]*len(D)

occupy_uv(X)
