from input_stream import E_old, E_new, E_new_deletion, CORE_x_CORE, G_t0, G_t1 #edges_list, author_id, id_author,
from primes import list_of_primes
from time import sleep, time
import sys
import math
import random
import operator
import heapq
global K  ##number of hash functions
global hash_function_pool
global jaccard_sim_threshold, H, I, capacity, L, S
global cb, cg, M, R, S_p
cb = 0
cg = 0
M = 80
S_p = len(E_old)
R = len(G_t0.edges) + len(G_t1.edges)
#e variables
S = 'S'
K = 50
hash_function_pool = {}
jaccard_sim_threshold = 0.8
H = 'val'
I = 'arg'
capacity = len(E_new)
L = 80
def create_hf_pool():
    '''
    creates independent variables for each one of k hash functions
    :return: hash_function_pool (dict ) with all of k independent functions' parameters
    '''
    for k in range(K):
        prime = list_of_primes[random.randint(0, len(list_of_primes)-1)]
        print(prime)
        h_f_params = {'BIG_PRIME': prime,
                      'a': random.randint(0, 2*prime),
                      'b': random.randint(0, 2*prime),

                      }
        hash_function_pool[k] = h_f_params
    return hash_function_pool


def Ha(number, a, b, BIG_PRIME):
    return ((a * number + b) % BIG_PRIME % 1000) * 0.001


def min_hash_unified_deletion(edges_list, sign, hash_function_pool):
    cb = 0
    cg = 0
    dict = {}
    neighbor_dict = {}
    for pair in edges_list:
        u = pair[0]
        v = pair[1]

        temp1 = {}
        temp2 = {}
        for j in range(K):
                temp1[j] = {'val': math.inf, 'arg': None}
                temp2[j] = {'val': math.inf, 'arg': None}

        neighbor_dict[u] = set()
        neighbor_dict[v] = set()
        dict[u] = temp1
        dict[v] = temp2

    for pair in edges_list:
        u = pair[0]
        v = pair[1]
        if sign[pair] == '+':
            Random = random.uniform(0, 1)
            if (cb + cg) == 0:
                if len(neighbor_dict[u]) < M:#if S < M
                    neighbor_dict[u].add(v)  #insert
                elif Random < M/(R + 1):   #elif random() ...
                    neighbor_dict[u].remove(random.sample(neighbor_dict[u], 1)[0])  #overwrite random selected element
                    neighbor_dict[u].add(v)
                if len(neighbor_dict[v]) < M:
                    neighbor_dict[v].add(u)
                elif Random < M/(R + 1):
                    neighbor_dict[v].remove(random.sample(neighbor_dict[v], 1)[0])
                    neighbor_dict[v].add(u)
            else:
                if Random < cb/(cb + cg):
                    cb -= 1
                    neighbor_dict[u].add(v)
                    neighbor_dict[v].add(u)
                else:
                    cg -= 1

            # if len(neighbor_dict[v]) < L:
            #     neighbor_dict[v].add(u)
            for k in range(K):
                a = hash_function_pool[k]['a']
                b = hash_function_pool[k]['b']
                BIG_PRIME = hash_function_pool[k]['BIG_PRIME']

                hf_value_u = Ha(hash(u), a, b, BIG_PRIME)
                hf_value_v = Ha(hash(v), a, b, BIG_PRIME)

                if hf_value_v < dict[u][k][H]:  # hf(v) < Hκ(u) then
                    dict[u][k][H] = hf_value_v  # H(u) = hf (v)
                    dict[u][k][I] = v           # I(u) = v
                if hf_value_u < dict[v][k][H]:
                    dict[v][k][H] = hf_value_u
                    dict[v][k][I] = u
        else:
            if v in neighbor_dict[u]:
                cb += 1
                neighbor_dict[u].remove(v)
                #UPDATE SKETCH OF U
                for k in range(K):
                    # update of sketch of u
                    if dict[u][k][I] == v:
                        dict[u][k][H] = math.inf  # RESET TO INITIAL VALUES
                        dict[u][k][I] = None

                        # COMPUTE NEW H,I (VALUE, ARGUMENT) FOR CURRENT HASHFUNCTION
                        maximum = math.inf
                        maximum_arg = None
                        a = hash_function_pool[k]['a']
                        b = hash_function_pool[k]['b']
                        BIG_PRIME = hash_function_pool[k]['BIG_PRIME']

                        for neighbor in neighbor_dict[u]:

                            # FIND MAXIMUM PRIORITY NEIGHBOR
                            hf_value_neighbor = Ha(hash(neighbor), a, b, BIG_PRIME)
                            if hf_value_neighbor < maximum:
                                maximum = hf_value_neighbor
                                maximum_arg = neighbor

                        dict[u][k][H] = maximum
                        dict[u][k][I] = maximum_arg
            else:
                cg += 1

            if u in neighbor_dict[v]:
                cb += 1
                neighbor_dict[v].remove(u)
                #UPDATE SKETCH OF V
                for k in range(K):
                    # update of sketch of v
                    if dict[v][k][I] == u:
                        dict[v][k][H] = math.inf  # RESET TO INITIAL VALUES
                        dict[v][k][I] = None

                        # COMPUTE NEW H,I (VALUE, ARGUMENT) FOR CURRENT HASHFUNCTION
                        maximum = math.inf
                        maximum_arg = None
                        a = hash_function_pool[k]['a']
                        b = hash_function_pool[k]['b']
                        BIG_PRIME = hash_function_pool[k]['BIG_PRIME']

                        for neighbor in neighbor_dict[v]:

                            # FIND MAXIMUM PRIORITY NEIGHBOR
                            hf_value_neighbor = Ha(hash(neighbor), a, b, BIG_PRIME)
                            if hf_value_neighbor < maximum:
                                maximum = hf_value_neighbor
                                maximum_arg = neighbor

                        dict[v][k][H] = maximum
                        dict[v][k][I] = maximum_arg
            else:
                cg += 1
    print("prediction started ")
    capacity = len(E_new_deletion)
    minheap = [(-1, None)]
    heapq.heapify(minheap)
    start = time()
    for pair in CORE_x_CORE:
            if pair in E_old:
                continue
            u = pair[0]
            v = pair[1]
            r = 0
            r = len([1 for i, j in zip(dict[u].values(), dict[v].values()) if i[I] == j[I]])
            if r > minheap[0][0]:
                heapq.heappush(minheap, (r, pair))
            if len(minheap) > capacity:
                heapq.heappop(minheap)

    end = time()

    print("min hash prediction overall time is ", end-start, " seconds")
    print("min hash prediction average overall time is ", (end-start)/len(E_new), " seconds")
    # print("min hash sketch size is ", sys.getsizeof(dict)/1000000, "MB")
    final = []
    while minheap:
        t = heapq.heappop(minheap)
        final.append(t[1])
    return final
