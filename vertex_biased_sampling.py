from input_stream import E_new,CORE_x_CORE,E_old#,test_set
from primes import list_of_primes
from time import sleep, time
import operator
import math
import random, sys
import heapq

global L, lo_h, up_h, S, a, b, BIG_PRIME,capacity
capacity = len(E_new)
L = 80
lo_h = 'lower_hetta'
up_h = 'upper_hetta'
S = 'S'
BIG_PRIME = list_of_primes[random.randint(0, len(list_of_primes)-1)]
a = random.randint(0, 2*BIG_PRIME)
b = random.randint(0, 2*BIG_PRIME)

def G(number):
    return ((a * number + b) % BIG_PRIME % 1000) * 0.001

def pre_pro(edges_list):
    structure = {}
    for pair in edges_list:
        u = pair[0]
        v = pair[1]

        structure[u] = {'lower_hetta': 1,
            'upper_hetta': 1,
            'S': set()
            }
        structure[v] = {'lower_hetta': 1,
            'upper_hetta': 1,
            'S': set()
            }

    return structure


def vertex_biased(edges_list, structure):
    for pair in edges_list:
        u = pair[0]
        v = pair[1]

        if v not in structure[u][S]:
            if len(structure[u][S]) < L:
                structure[u][S].add(v)
            else:
                G_v = G(hash(v))

                if G_v <= structure[u][lo_h]:
                    k = None
                    max = -1
                    for w in structure[u][S]:
                        G_w = G(hash(w))
                        if G_w > max:
                            max = G_w
                            k = w

                    G_k = max
                    structure[u][S].remove(k)
                    structure[u][S].add(v)

                    structure[u][up_h] = G_k

                    k_star = None
                    max = -1
                    for w in structure[u][S]:
                        G_w = G(hash(w))
                        if G_w > max:
                            max = G_w
                            k_star = w

                    G_k_star = max                 # hetta_(u) = G(k*)
                    structure[u][lo_h] = G_k_star

        if u not in structure[v][S]:
            if len(structure[v][S]) < L:
                structure[v][S].add(u)
            else:
                G_u = G(u)
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
                    structure[v][S].add(v)

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
    return structure


def get_predicted_links(edges_list, structure):
    common_neighbors = []
    commonNeighbors = {}
    for pair in edges_list:
        u = int(pair[0])
        v = int(pair[1])

        h_u = (structure[u][lo_h] + structure[u][up_h]) / 2
        h_v = (structure[v][lo_h] + structure[v][up_h]) / 2

        countCN = len(list(set(structure[u][S]) & set(structure[v][S]))) / max(h_u, h_v)
        common_neighbors.append(countCN)

        cn = set(structure[u][S]) & set(structure[v][S])
        pair = str(u) + '-' + str(v)
        commonNeighbors[pair] = cn

    return common_neighbors, commonNeighbors

def vertex_biased_unified(edges_list):
    structure  = {}
    set_of_links = set()
    for pair in edges_list:

        u = pair[0]
        v = pair[1]
        structure[u] = {'lower_hetta': 1,
                'upper_hetta': 1,
                'S': set()
                }
        structure[v] = {'lower_hetta': 1,
                'upper_hetta': 1,
                'S': set()
                }
    for pair in edges_list:
        u = pair[0]
        v = pair[1]

        if v not in structure[u][S]:
                if len(structure[u][S]) < L:
                    structure[u][S].add(v)
                else:
                    G_v = G(hash(v))
                    # print(G_v)
                    # sleep(1)
                    if G_v <= structure[u][lo_h]:
                        k = None
                        Max = -1
                        for w in structure[u][S]:
                            G_w = G(hash(w))
                            if G_w > Max:
                                Max = G_w
                                k = w

                        G_k = Max
                        structure[u][S].remove(k)
                        structure[u][S].add(v)

                        structure[u][up_h] = G_k

                        k_star = None
                        Max = -1
                        for w in structure[u][S]:
                            G_w = G(hash(w))
                            if G_w > Max:
                                Max = G_w
                                k_star = w

                        G_k_star = Max                            # h_(u) = G(k*)
                        structure[u][lo_h] = G_k_star

        if u not in structure[v][S]:
                if len(structure[v][S]) < L:
                    structure[v][S].add(u)
                else:
                    G_u = G(hash(u))
                    if G_u <= structure[v][lo_h]:
                        k = None
                        Max = -1
                        for w in structure[v][S]:
                            G_w = G(hash(w))
                            if G_w > Max:
                                Max = G_w
                                k = w

                        G_k = Max
                        structure[v][S].remove(k)
                        structure[v][S].add(v)

                        structure[v][up_h] = G_k

                        k_star = None
                        Max = -1
                        for w in structure[v][S]:
                            G_w = G(hash(w))
                            if G_w > Max:
                                Max = G_w
                                k_star = w

                        G_k_star = Max  # hetta_(u) = G(k*)
                        structure[v][lo_h] = G_k_star

    #make shorter pairs to check
    for vertex in structure.keys():
        for neighbor in structure[vertex][S]:
            for item in structure[neighbor][S]:
                if item not in structure[vertex][S]:
                    candidate_pair = (vertex, item)
                    set_of_links.add(candidate_pair)

    # print("total links with new way are ", len(CORE_x_CORE))
    # print("total links with new way are ", len(set_of_links))
    # # for link in set_of_links:
    # #     print(link)
    # #     sleep(1)



    minheap = [(-1, None)]
    heapq.heapify(minheap)
    start = time()
    print("prediction started")
    for pair in CORE_x_CORE:
        if pair in E_old:
            continue
        u = pair[0]
        v = pair[1]
        h_u = (structure[u][lo_h] + structure[u][up_h]) / 2
        h_v = (structure[v][lo_h] + structure[v][up_h]) / 2
        cn = len(structure[u][S].intersection(structure[v][S]))/max(h_u, h_v)
        if cn >= minheap[0][0]:
            heapq.heappush(minheap, (cn, pair))
        if len(minheap) > capacity:
            heapq.heappop(minheap)

    end = time()
    print("vertex biased prediction for all links is ", end - start, " seconds")
    print("vertex biased prediction average overall time is ", (end-start)/len(E_new), " seconds")
    print("vertex biased sketch size is ", sys.getsizeof(structure)/1000000, "MB")
    final = []
    while minheap:
       x = heapq.heappop(minheap)
       final.append(x[1])

    return final
