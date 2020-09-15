from input_stream import E_old,E_new,CORE_x_CORE #edges_list, author_id, id_author,
from primes import list_of_primes
from time import sleep, time
import sys
import math
import random
import operator
import heapq
global K  ##number of hash functions
global hash_function_pool
global jaccard_sim_threshold, H, I,capacity
K = 50
hash_function_pool = {}
jaccard_sim_threshold = 0.8
H = 'val'
I = 'arg'
capacity = len(E_new)


### structure for k hashfunctions  { KEY0 : [ [HF0, ARG0] , [HF1,ARG1], .... , [HFK,ARGK]}


def create_hf_pool():
    '''
    creates independent variables for each one of k hash functions
    :return: hash_function_pool (dict ) with all of k independent functions' parameters
    '''
    for k in range(K):
        prime = list_of_primes[random.randint(0, len(list_of_primes)-1)]
        # print(prime)
        h_f_params = {'BIG_PRIME': prime,
                      'a': random.randint(0, 2*prime),
                      'b': random.randint(0, 2*prime),

                      }
        hash_function_pool[k] = h_f_params
    return hash_function_pool

#hash function
def Ha(number, a, b, BIG_PRIME):
    return ((a * number + b) % BIG_PRIME % 1000) * 0.001


def Str_H(string, a, b, BIG_PRIME):
    num = hash(string)
    hashed_value = ((a * num + b) % BIG_PRIME % 1000) * 0.001
    # print(string," hashes to ", hashed_value)
    return hashed_value


def min_hash_unified(edges_list, hash_function_pool):
    dict = {}
    ##INITIALIZATION
    for pair in edges_list:
        u = pair[0]
        v = pair[1]

        # dict[u] = [[math.inf, None] for i in range(k)]
        # dict[v] = [[math.inf, None] for i in range(k)]
        temp1 = {}
        temp2 = {}
        for j in range(K):
                temp1[j] = {'val': math.inf, 'arg': None}
                temp2[j] = {'val': math.inf, 'arg': None}

        dict[u] = temp1
        dict[v] = temp2
    ## algorithm
    for pair in edges_list:
        u = pair[0]
        v = pair[1]
        # u = int(pair[0])
        # v = int(pair[1])
        for k in range(K):
            a = hash_function_pool[k]['a']
            b = hash_function_pool[k]['b']
            BIG_PRIME = hash_function_pool[k]['BIG_PRIME']

            hf_value_u = Ha(hash(u), a, b, BIG_PRIME)
            hf_value_v = Ha(hash(v), a, b, BIG_PRIME)

            if hf_value_v < dict[u][k][H]:  # hf(v) < Hk(u) then
                dict[u][k][H] = hf_value_v  # H(u) = hf (v)
                dict[u][k][I] = v           # I(u) = v
            if hf_value_u < dict[v][k][H]:
                dict[v][k][H] = hf_value_u
                dict[v][k][I] = u

    ## prediction accuracy
    print("prediction started")
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

            if r/K > minheap[0][0]:
                heapq.heappush(minheap, (r/K, pair))
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
