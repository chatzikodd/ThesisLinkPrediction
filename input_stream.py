from time import sleep, time,perf_counter
import math
import sys
import itertools
import csv
import networkx as nx
import pandas as pd
import random
global id, r


def get_reqs(graph,r):
    Core = set()
    E_old = set()
    E_new = set()
    ### create Core which contains vertices that appear in train and test interval
    for edge in G_t1.edges:
        if edge in G_t0.edges:
            graph_Core.add_edge(edge[0], edge[1])
            Core.add(edge[0])
            Core.add(edge[1])

    ### create E_old containing all edges of E(t0) which vertices are in Core
    for edge in G_t0.edges:
        if edge[0] in Core and edge[1] in Core:
            E_old.add(edge)
            graph_E_old.add_edge(edge[0], edge[1])

    ### create E_new which contains target edges for prediction
    for edge in G_t1.edges:

        if edge[0] in Core and edge[1] in Core and edge not in G_t0.edges:
            graph_E_new.add_edge(edge[0], edge[1])
            E_new.add(edge)
    return Core, E_old, E_new

start = perf_counter()

G = nx.Graph()
G_t0 = nx.Graph()
G_t1 = nx.Graph()
graph_Core = nx.Graph()
graph_E_old = nx.Graph()
graph_E_new = nx.Graph()

# file_name_csv = "Databases/Dblp.csv"
# file_name_csv = "Databases/Amazon.csv"
# file_name_csv = "Databases/Wiki_tstampOrdered.csv"
# file_name_csv = "Databases/redditHyperlinks.csv"
# file_name_csv = "Databases/miniFriendster.csv"
# file_name_csv = "Databases/MathOverflow.csv"
file_name_csv = "Databases/FacebookAnon.csv"

df = pd.read_csv(file_name_csv, nrows=1200000)# define number of edges our graph will have

print("Total edges are ", len(df))

#ASSIGN  +/- FOR  EDGE INSERTION/DELETION RESPECTIVELY  AT TRAINING STAGE
df['sign'] = '+'
for index in df.index:
    temp = random.random()
    if temp < 0.1:# we assign - (minus) with probability of 10%
        df.at[index, 'sign'] = '-'

r = 0.5
# size = 800000
size = len(df)


Core = set()
E_old = set()
E_old_deletion = set()
E_new = set()
E_new_deletion = set()
Core_edges = set()

df = df.head(size)

print()
df_train = df[0: int(r*size)]
df_test = df[int(r*size):size]

print("number of train edges  = ", len(df_train))
print("number of test edges  = ", len(df_test))
G_t0 = nx.from_pandas_edgelist(df_train, source='id1', target='id2', edge_attr='sign')
G_t1 = nx.from_pandas_edgelist(df_test, source='id1', target='id2', edge_attr='sign')
sign = nx.get_edge_attributes(G_t0, 'sign')
sign_future = nx.get_edge_attributes(G_t1, 'sign')


for vertex in G_t0.nodes:
    if vertex in G_t1.nodes:
        Core.add(vertex)


# create E_old containing all edges of E(t0) which vertices are in Core
for edge in G_t0.edges:
    if edge[0] in Core and edge[1] in Core:
        E_old.add(edge)
    if edge[0] in Core and edge[1] in Core and sign[edge] == '+':
        E_old_deletion.add(edge)

# create E_new which contains target edges for prediction
for edge in G_t1.edges:
    if edge[0] in Core and edge[1] in Core and sign_future[edge] == '+':
        if edge not in G_t0.edges:
            E_new_deletion.add(edge)
    if edge[0] in Core and edge[1] in Core:
        if edge not in G_t0.edges:
            E_new.add(edge)
total_edges_core_x_core = int((len(Core)*(len(Core)-1))/2)
print("Core nodes = ", len(Core))
print("Total edges to check are", total_edges_core_x_core)
print("E_old edges = ", len(E_old))
print("E_old_deletion edges = ", len(E_old_deletion))
print("E_new edges = ", len(E_new))
print("E_new_deletion edges = ", len(E_new_deletion))

Core = list(Core)
random.shuffle(Core)
CORE_x_CORE = itertools.combinations(Core, 2)
# CORE_x_CORE = itertools.islice(CORE_x_CORE, 100000000)

end = perf_counter()
print("initialization lasted for ", end - start, " seconds")
