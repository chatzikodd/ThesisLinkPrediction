from input_stream import E_old,E_new,CORE_x_CORE#,test_set
from primes import list_of_primes
from time import sleep,time
import random
import math, sys

import heapq
global L, lo_h, up_h, S, a, b, BIG_PRIME, Inv_index, capacity
capacity = len(E_new)
L = 80
lo_h = 'lower_hetta'
up_h = 'upper_hetta'
S = 'S'
BIG_PRIME = list_of_primes[random.randint(0, len(list_of_primes)-1)]
Inv_index = 'Inv_index'
a = random.randint(0, 2*BIG_PRIME)
b = random.randint(0, 2*BIG_PRIME)

def G(number):
    return ((a * number + b) % BIG_PRIME % 10000) * 0.0001




# def pre_adamic(edges_list,structure):
#     for pair in edges_list:
#         u = int(pair[0])
#         v = int(pair[1])
#         if v not in structure[u][S]:
#             if len(structure[u][S]) < L:
#                 structure[u][S].append(v)
#                 structure[v][Inv_index].add(u)
#             else:
#                 G_v = G(v)
#                 # print(G_v)
#                 # sleep(1)
#                 if G_v <= structure[u][lo_h]:
#                     k = None
#                     max = -1
#                     for w in structure[u][S]:
#                         G_w = G(w)
#                         if G_w > max:
#                             max = G_w
#                             k = w
#                     # print(k, structure[u][S])
#                     # sleep(2)
#                     G_k = max
#                     structure[u][S].remove(k)
#                     if u in structure[k][Inv_index]:
#                         structure[k][Inv_index].remove(u)
#
#                     structure[u][S].append(v)
#                     structure[v][Inv_index].add(u)
#
#                     structure[u][up_h] = G_k
#
#                     k_star = None
#                     max = -1
#                     for w in structure[u][S]:
#                         G_w = G(w)
#                         if G_w > max:
#                             max = G_w
#                             k_star = w
#
#                     G_k_star = max                            # hetta_(u) = G(k*)
#                     structure[u][lo_h] = G_k_star
#
#         if u not in structure[v][S]:
#             if len(structure[v][S]) < L:
#                 structure[v][S].append(u)
#                 structure[u][Inv_index].add(v)
#             else:
#                 G_u = G(u)
#                 if G_u <= structure[v][lo_h]:
#                     k = None
#                     max = -1000
#                     for w in structure[v][S]:
#                         G_w =G(w)
#                         if G_w > max:
#                             max = G_w
#                             k = w
#
#                     G_k = max
#                     structure[v][S].remove(k)
#                     if v in structure[k][Inv_index]:
#                         structure[k][Inv_index].remove(v)
#
#                     structure[v][S].append(u)
#                     structure[u][Inv_index].add(v)    #L(u) = v if and only if u in S(v)
#                     structure[v][up_h] = G_k
#
#                     k_star = None
#                     max = -1
#                     for w in structure[v][S]:
#                         G_w = G(w)
#                         if G_w > max:
#                             max = G_w
#                             k_star = w
#
#                     G_k_star = max  # hetta_(u) = G(k*)
#                     structure[v][lo_h] = G_k_star
#     # print(structure)
#     return structure
#
#
# def adamic_adar(nodes,structure,edges_list):
#         AA = {}
#         for w in nodes:     #for vertex w in G(t)
#             for pair in edges_list:
#                 u = pair[0]
#                 v = pair[1]
#                 if u in structure[w][S] and v in structure[w][S]:
#                     if structure[w][lo_h] == 1 and structure[w][up_h] == 1:
#                         edge = str(u) + ',' + str(v)
#                         if edge not in AA:
#                             AA[edge] = 0
#                         AA[edge] = AA[edge] + 1/math.log(len(structure[w][S]))
#         return AA
#
#
# def get_adar_neighbors(structure, edges_list):
#     countCN = []
#     commonNeighbors = {}
#     for pair in edges_list:
#         u = pair[0]
#         v = pair[1]
#         cn = structure[u][Inv_index].intersection(structure[v][Inv_index])
#         countCN.append(len(cn))
#         pair = str(u)+'-'+str(v)
#         commonNeighbors[pair] = cn
#     return countCN, commonNeighbors


def adamic_adar_unified_deletion(edges_list,sign):
    structure = {}

    for pair in edges_list:
        u = pair[0]
        v = pair[1]
        structure[u] = {'lower_hetta': 1,
                'upper_hetta': 1,
                'S': set(),
                'Inv_index': set()
                }
        structure[v] = {'lower_hetta': 1,
                'upper_hetta': 1,
                'S': set(),
                'Inv_index': set()
                }
    for pair in edges_list:
        u = pair[0]
        v = pair[1]
        if sign[pair] == '+':
            if v not in structure[u][S]:
                if len(structure[u][S]) < L:
                    structure[u][S].add(v)
                    structure[v][Inv_index].add(u)
                else:
                    G_v = G(hash(v))
                    # print(G_v)
                    # sleep(1)
                    if G_v <= structure[u][lo_h]:
                        k = None
                        max = -1
                        for w in structure[u][S]:
                            G_w = G(hash(w))
                            if G_w > max:
                                max = G_w
                                k = w
                        # print(k, structure[u][S])
                        # sleep(2)
                        G_k = max
                        structure[u][S].remove(k)
                        if u in structure[k][Inv_index]:
                            structure[k][Inv_index].remove(u)

                        structure[u][S].add(v)
                        structure[v][Inv_index].add(u)

                        structure[u][up_h] = G_k

                        k_star = None
                        max = -1
                        for w in structure[u][S]:
                            G_w = G(hash(w))
                            if G_w > max:
                                max = G_w
                                k_star = w

                        G_k_star = max  # hetta_(u) = G(k*)
                        structure[u][lo_h] = G_k_star

            if u not in structure[v][S]:
                if len(structure[v][S]) < L:
                    structure[v][S].add(u)
                    structure[u][Inv_index].add(v)
                else:
                    G_u = G(hash(u))
                    if G_u <= structure[v][lo_h]:
                        k = None
                        max = -1
                        for w in structure[v][S]:
                            G_w = G(hash(w))
                            if G_w > max:
                                max = G_w
                                k = w

                        G_k = max
                        structure[v][S].remove(k)
                        if v in structure[k][Inv_index]:
                            structure[k][Inv_index].remove(v)

                        structure[v][S].add(u)
                        structure[u][Inv_index].add(v)  # L(u) = v if and only if u in S(v)
                        structure[v][up_h] = G_k

                        k_star = None
                        max = -1
                        for w in structure[v][S]:
                            G_w = G(hash(w))
                            if G_w > max:
                                max = G_w
                                k_star = w

                        G_k_star = max  # hetta_(u) = G(k*)
                        structure[v][lo_h] = G_k_star
        else:
            if v in structure[u][S]:
                structure[u][S].remove(v)  # delete node
                structure[u][Inv_index].remove(v)
                k = None
                Max = -1
                for w in structure[u][S]:  # find next max arg
                    G_w = G(hash(w))
                    if G_w > Max:
                        Max = G_w
                        k = w

                G_k = Max
                structure[u][up_h] = G_k  # we do not add edge so up_h and lo_h will not differ
                structure[u][lo_h] = G_k

            if u in structure[v][S]:
                structure[v][S].remove(u)
                structure[v][Inv_index].remove(u)
                k = None
                Max = -1
                for w in structure[v][S]:  # find
                    G_w = G(hash(w))
                    if G_w > Max:
                        Max = G_w
                        k = w
                G_k = Max
                structure[v][up_h] = G_k  # we do not add edge so up_h and lo_h will not differ
                structure[v][lo_h] = G_k


    minheap = [(-1, None)]
    heapq.heapify(minheap)
    start = time()
    print("prediction started")
    for pair in CORE_x_CORE:
        if pair in E_old:
            continue
        u = pair[0]
        v = pair[1]
        AA = 0
        for w in structure[u][Inv_index].intersection(structure[v][Inv_index]):
            if u in structure[w][Inv_index] and v in structure[w][Inv_index]:
                if structure[v][lo_h] == 1 and structure[v][up_h] == 1:
                    if math.log2(len(structure[w][S])) != 0:

                        AA += 1 / math.log2(len(structure[w][S]))

        if AA > minheap[0][0]:
            heapq.heappush(minheap, (AA, pair))
        if len(minheap) > capacity:
            heapq.heappop(minheap)

    end = time()
    print("adamic adar prediction for all links is ", end - start, " seconds")
    print("adamic adar prediction average overall time is ", (end-start)/len(E_new), " seconds")
    # print("adamic adar sketch size is ", sys.getsizeof(structure)/1000000, "MB")

    final = []
    while minheap:
        x = heapq.heappop(minheap)
        final.append(x[1])

    return final
