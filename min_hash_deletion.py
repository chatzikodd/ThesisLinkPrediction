from input_stream import E_old,E_new,CORE_x_CORE,E_new_deletion #edges_list, author_id, id_author,
from primes import list_of_primes,hash_alphabet
from time import sleep, time
import sys
import math
import random
import operator
import heapq
global K  ##number of hash functions
global hash_function_pool
global jaccard_sim_threshold, H, I, capacity, L, S
S = 'S'
K = 50
hash_function_pool = {}
jaccard_sim_threshold = 0.8
H = 'val'
I = 'arg'
L = 80
BP = list_of_primes[random.randint(0, len(list_of_primes)-1)]
A = random.randint(0, 2*BP)
B = random.randint(0, 2*BP)
def create_hf_pool():
    '''
    creates independent variables for each one of k hash functions
    :return: hash_function_pool (dict ) with all of k independent functions' parameters
    '''
    for k in range(K):
        prime = list_of_primes[random.randint(0, len(list_of_primes)-1)]
        h_f_params = {'BIG_PRIME': prime,
                      'a': random.randint(0, 2*prime),
                      'b': random.randint(0, 2*prime),

                      }
        hash_function_pool[k] = h_f_params
    return hash_function_pool


def Ha(number, a, b, BIG_PRIME):
    return ((a * number + b) % BIG_PRIME % 1000) * 0.001

def G(number):
    return ((A * number + B) % BP % 1000) * 0.001

def min_hash_unified_deletion(edges_list, sign, hash_function_pool):
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
            if len(neighbor_dict[u]) < L:
                neighbor_dict[u].add(v)
                for k in range(K):
                    a = hash_function_pool[k]['a']
                    b = hash_function_pool[k]['b']
                    BIG_PRIME = hash_function_pool[k]['BIG_PRIME']

                    hf_value_u = Ha(hash(u), a, b, BIG_PRIME)
                    hf_value_v = Ha(hash(v), a, b, BIG_PRIME)

                    if hf_value_v < dict[u][k][H]:  # hf(v) < Hk(u) then
                        dict[u][k][H] = hf_value_v  # H(u) = hf (v)
                        dict[u][k][I] = v  # I(u) = v
                    if hf_value_u < dict[v][k][H]:
                        dict[v][k][H] = hf_value_u
                        dict[v][k][I] = u
            else:
                max = -1
                maxarg = None
                for nei in neighbor_dict[u]:
                    G_nei = G(hash(nei))
                    if G_nei > max:
                        max = G_nei
                        maxarg = nei
                neighbor_dict[u].remove(maxarg)
                neighbor_dict[u].add(v)
                for k in range(K):
                    # update of sketch of u
                    if dict[u][k][I] == maxarg:
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


            if len(neighbor_dict[v]) < L:
                neighbor_dict[v].add(u)
                for k in range(K):
                    a = hash_function_pool[k]['a']
                    b = hash_function_pool[k]['b']
                    BIG_PRIME = hash_function_pool[k]['BIG_PRIME']

                    hf_value_u = Ha(hash(u), a, b, BIG_PRIME)
                    hf_value_v = Ha(hash(v), a, b, BIG_PRIME)

                    if hf_value_v < dict[u][k][H]:  # hf(v) < Hk(u) then
                        dict[u][k][H] = hf_value_v  # H(u) = hf (v)
                        dict[u][k][I] = v  # I(u) = v
                    if hf_value_u < dict[v][k][H]:
                        dict[v][k][H] = hf_value_u
                        dict[v][k][I] = u
            else:
                max = -1
                maxarg = None
                for nei in neighbor_dict[v]:
                    G_nei = G(hash(nei))
                    if G_nei > max:
                        max = G_nei
                        maxarg = nei
                neighbor_dict[v].remove(maxarg)
                neighbor_dict[v].add(v)
                for k in range(K):
                    # update of sketch of u
                    if dict[v][k][I] == maxarg:
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
            # for k in range(K):
            #     a = hash_function_pool[k]['a']
            #     b = hash_function_pool[k]['b']
            #     BIG_PRIME = hash_function_pool[k]['BIG_PRIME']
            #
            #     hf_value_u = Ha(hash(u), a, b, BIG_PRIME)
            #     hf_value_v = Ha(hash(v), a, b, BIG_PRIME)
            #
            #     if hf_value_v < dict[u][k][H]:  # hf(v) < Hk(u) then
            #         dict[u][k][H] = hf_value_v  # H(u) = hf (v)
            #         dict[u][k][I] = v           # I(u) = v
            #     if hf_value_u < dict[v][k][H]:
            #         dict[v][k][H] = hf_value_u
            #         dict[v][k][I] = u
        else:
            flagu = False
            flagv = False
            if v in neighbor_dict[u]:
                neighbor_dict[u].remove(v)
                flagu = True
            if u in neighbor_dict[v]:
                neighbor_dict[v].remove(u)
                flagv = True
            if flagu == True and flagv == True:
                for k in range(K):
                    #update of sketch of u
                    if dict[u][k][I] == v:
                        dict[u][k][H] = math.inf  #RESET TO INITIAL VALUES
                        dict[u][k][I] = None

                        #COMPUTE NEW H,I (VALUE, ARGUMENT) FOR CURRENT HASHFUNCTION
                        maximum = math.inf
                        maximum_arg = None
                        a = hash_function_pool[k]['a']
                        b = hash_function_pool[k]['b']
                        BIG_PRIME = hash_function_pool[k]['BIG_PRIME']

                        for neighbor in neighbor_dict[u]:

                            #FIND MAXIMUM PRIORITY NEIGHBOR
                            hf_value_neighbor = Ha(hash(neighbor), a, b, BIG_PRIME)
                            if hf_value_neighbor < maximum:
                                maximum = hf_value_neighbor
                                maximum_arg = neighbor

                        dict[u][k][H] = maximum
                        dict[u][k][I] = maximum_arg

                    #update of sketch of v
                    if dict[v][k][I] == u:
                        dict[v][k][H] = math.inf  #RESET TO INITIAL VALUES
                        dict[v][k][I] = None

                        # COMPUTE NEW H,I (VALUE, ARGUMENT) FOR CURRENT HASHFUNCTION
                        maximum = math.inf
                        maximum_arg = None
                        a = hash_function_pool[k]['a']
                        b = hash_function_pool[k]['b']
                        BIG_PRIME = hash_function_pool[k]['BIG_PRIME']

                        for neighbor in neighbor_dict[v]:

                            #FIND MAXIMUM PRIORITY NEIGHBOR
                            hf_value_neighbor = Ha(hash(neighbor), a, b, BIG_PRIME)
                            if hf_value_neighbor < maximum:
                                maximum = hf_value_neighbor
                                maximum_arg = neighbor

                        dict[v][k][H] = maximum
                        dict[v][k][I] = maximum_arg
    # set_of_links = set()
    # # make shorter pairs to check
    # for vertex in neighbor_dict.keys():
    #         for neighbor in neighbor_dict[vertex]:
    #             for item in neighbor_dict[neighbor]:
    #                 if item not in neighbor_dict[vertex]:
    #                     candidate_pair = (vertex, item)
    #                     set_of_links.add(candidate_pair)


    # print("total links with new way are ", len(set_of_links))

    print("prediction started")
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
            # i = 0
            # while i < K:
            #     if dict[u][i][I] == dict[v][i][I]:
            #         r += 1
            #     i += 1
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
    #TODO : οταν φτανει το L να βρισκει πιο γειτονας βγαζει μαξ πριοριτυ και να τον βαζει()
    # οπως στο vertex biased (max = 10,max arg = None) for each neighbor in neighbordcit...