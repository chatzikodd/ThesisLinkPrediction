from input_stream import E_new, E_old, Core, G_t0, sign, G_t1, E_new_deletion, E_old_deletion
import math
from time import sleep, time

from min_hash import min_hash_unified, create_hf_pool
from vertex_biased_sampling import vertex_biased_unified
from adamic_adar import adamic_adar_unified

from min_hash_deletion import *
from vertex_biased_deletion import vertex_biased_unified_deletion
from adamic_adar_deletion import adamic_adar_unified_deletion

def relative_improvement(new_value, old_value):
    # return (old_value - (old_value - new_value))/old_value
    return (new_value - old_value)/old_value


def combinations(n, r):
    #  n!/(r!*(n-r)!)
    if r == 2:
        return (n*(n-1))/2
    der = 1
    for i in range(r):
        der *= n-i
    return_value = n * (n-1) / math.factorial(r)
    return return_value



def accuracy(predicted_links, target_links):
    count = 0
    for link in predicted_links:
        if link in target_links:# or tuple(reversed(link)) in target_links:
            count += 1
    print("correct predictions = ", count)
    percentage = (count/len(target_links))*100
    return percentage
    # return count/len(test_set)

print("===============================  pre stage   ===============================")
random_predictor = 1/(combinations(len(Core), 2) - len(E_old))
random_predictor_percentage = random_predictor*100*len(E_new)
print("prob of random predictor = ", random_predictor_percentage, " %")
print("total target links are ", len(E_new))
print()


rand_predictor_deletion = 1/(combinations(len(Core), 2) - len(E_old_deletion))
rand_predictor_deletion_percentage = rand_predictor_deletion*100*len(E_new_deletion)
print("prob of random predictor for deletion = ", rand_predictor_deletion_percentage, " %")
print("total target deletion links are ", len(E_new_deletion))

########################         MIN HASH        ##############################
###############################################################################
# # ###############################################################################
# #
# print("------------------------------ Min hash started ---------------------------------")
# hf_pool = create_hf_pool()
# min_hash_predicted_links = min_hash_unified(G_t0.edges, hf_pool)
# min_hash_percentage = accuracy(min_hash_predicted_links, E_new)
# App_Ja_improvement = relative_improvement(min_hash_percentage, random_predictor_percentage)
# print("App-JA links predicted = ", len(min_hash_predicted_links))
# print("MinHash acc = ", App_Ja_improvement)

########################         MIN HASH deletion        ##############################
###############################################################################
###############################################################################

print("------------------------------ Min hash with deletion support started ---------------------------------")
hf_pool = create_hf_pool()
min_hash_predicted_links = min_hash_unified_deletion(G_t0.edges, sign, hf_pool)
min_hash_percentage = accuracy(min_hash_predicted_links, E_new_deletion)
App_Ja_improvement = relative_improvement(min_hash_percentage, rand_predictor_deletion_percentage)
#
print("App-JA (deletion support) links predicted = ", len(min_hash_predicted_links))
print("MinHash (deletion support) acc = ", App_Ja_improvement)

########################       VERTEX BIASED     ##############################
###############################################################################
###############################################################################
# print()
# print("------------------------------ Vertex biased sketching started ----------------------------------")
# vertex_biased_predicted_links = vertex_biased_unified(G_t0.edges)
# vertex_biased_percentage = accuracy(vertex_biased_predicted_links, E_new)
# App_CN_improvement = relative_improvement(vertex_biased_percentage, random_predictor_percentage)
# print("App-CN links predicted = ", len(vertex_biased_predicted_links))
# print("Vertex acc = ", App_CN_improvement)

########################       VERTEX BIASED with deletion support    ##############################
###############################################################################
##############################################################################
# # print()
# print("------------------------------ Vertex biased with deletion suppport started ----------------------------------")
# vertex_biased_predicted_links = vertex_biased_unified_deletion(G_t0.edges, sign)
# vertex_biased_percentage = accuracy(vertex_biased_predicted_links, E_new_deletion)
# App_CN_improvement = relative_improvement(vertex_biased_percentage, rand_predictor_deletion_percentage)
# print("App-CN links predicted = ", len(vertex_biased_predicted_links))
# print("Vertex (deletion support) acc = ", App_CN_improvement)

# ########################       ADAMIC ADAR     ##############################
# ###############################################################################
###############################################################################
# print()
# print("------------------------------ Adamic adar started ----------------------------------")
# adamic_adar_predicted_links = adamic_adar_unified(G_t0.edges)
# adamic_adar_percentage = accuracy(adamic_adar_predicted_links, E_new)
# App_Adar_improvement = relative_improvement(adamic_adar_percentage, random_predictor_percentage)
# print("App-Adar links predicted = ", len(adamic_adar_predicted_links))
# print("Adamic-Adar acc = ", App_Adar_improvement)

########################       ADAMIC ADAR deletion support   ##############################
###############################################################################
###############################################################################
# print()
# print("------------------------------ Adamic adar with deletion support started  ----------------------------------")
# adamic_adar_predicted_links = adamic_adar_unified_deletion(G_t0.edges, sign)
# adamic_adar_percentage = accuracy(adamic_adar_predicted_links, E_new_deletion)
# App_Adar_improvement = relative_improvement(adamic_adar_percentage, rand_predictor_deletion_percentage)
# print("App-Adar links predicted = ", len(adamic_adar_predicted_links))
# print("Adamic-Adar (deletion support)acc = ", App_Adar_improvement)


