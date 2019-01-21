# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 13:10:24 2018

@author: Aishu
"""

import networkx as nx
import matplotlib.pyplot as plt
import math
import copy

nodes = []
edges = []
labels = []
weights = []
node_values = []

#filename = input("Enter filename:")
#filename = "dolphins/dolphins.gml"
filename = "karate/karate.gml"
#filename = "lesmis/lesmis.gml"
#filename = "adjnoun/adjnoun.gml"
#filename = "football/football.gml"
f = open(filename, 'r')

#Reading file
while True:
    line = f.readline()
    if not line:
        break
    if "node" in line:
        flag = 1
    if "edge" in line:
        flag = 0
    if "id" in line:
        node_id = line.replace("id","").strip()
        if node_id.isdigit():
            nodes.append(int(node_id))
    if "label" in line:
        label = line.replace("label","")
        labels.append(label.strip())
    if "source" in line:
        src = int(line.replace("source",""))
    if "target" in line:
        target = int(line.replace("target",""))
        edges.append((src,target))    
    if "value" in line:
        if flag == 1:
            value = int(line.replace("value","").strip())
            node_values.append(value) 
        else:
            weight = float(line.replace("value","").strip())
            weights.append(weight)
        
f.close()

labelled_nodes = dict(zip(nodes,labels))
print(labelled_nodes) 
weighted_edges = dict(zip(edges,weights))
print(weighted_edges)



#Creating a networkX graph      
G = nx.Graph()
G.add_nodes_from(nodes)
if weights != []:
    for i in weighted_edges:
        G.add_edge(i[0], i[1],weight=weighted_edges[i])
else:
    G.add_edges_from(edges)
    
n = G.number_of_nodes()
m = G.number_of_edges()

#################################################################################
#Initializing 2D matrix with 0
def initialize_2Dmatrix():
    if G.nodes()[1] == 0:
        a = [[0]*(n+1) for i in G.nodes()]  
    else :
        a = [[0]*(n+1) for i in range(0,n+1)]
    return a

#Print the 2D matrix
def print_matrix(a):
    for i in G.nodes():
        for j in G.nodes():
            print('%.2f'%(a[i][j]),end=" ")
        print("\n")

#Find the adjacency matrix of the graph      
def adjacency_matrix(a):
    for e in G.edges():
        a[e[0]][e[1]] = 1
        a[e[1]][e[0]] = 1
    return a

adj_matrix = adjacency_matrix(initialize_2Dmatrix())
#print("Adjacency matrix")
#print_matrix(adj_matrix)

#Find the adjacency list of graph
def adjacency_list():
    adj_list = dict()
    for i in G.nodes:
        l = []
        for e in G.edges():
            if i==e[0]:
                l.append(e[1])
            if i==e[1]:
                l.append(e[0])
        adj_list[i] = l
        del(l)
    return adj_list

adj_list = adjacency_list()
#print("Adjacency List")


###########################################################
#Helper function to remove items from dictionary
def entries_to_remove(entries, similarity):
    #Entries is a list of items to be removed
    for key in entries:  
        #If element in entries is present in similarity matrix, then delete that key value pair
        if key in similarity:           
            del similarity[key]        
    return similarity

#Helper recursive function to determine the level in a dendrogram for a given group
#Number of tuples present within an tuple(group) is its level in dendrogram 
def dLevel(group, levelCount):
    if type(group[0]) is tuple:
        levelCount = levelCount + 1
        return dLevel(group[0], levelCount)
    else:
        return levelCount
    
#Group formed is converted to a list from tuple
def recGroup(group, list1):
    for g in group:
        if type(g) is tuple:
            recGroup(g,list1)
        else:
            list1.append(g)
    return list1

#Find the maximum value in similarity matrix and return its indices 
def maxSimilarity(similarity):
    max_similarity = 0
    group = ()
    for i in similarity:
        for j in similarity[i]:
            if max_similarity <= similarity[i][j]:
                max_similarity = similarity[i][j]
                #Indices of maximum value are grouped as a tuple.
                group = (i,j)
    return group

#Calculate similarity values for combination of each group with remaining nodes and groups in network
def singleLinkage(prev_similarity, initial_similarity, g):
    new_similarity = copy.deepcopy(prev_similarity)   
    entries = list(g)
    #Remove the similarity values of elements present in group
    new_similarity = entries_to_remove(entries, new_similarity)
    for s in new_similarity:
        new_similarity[s] = entries_to_remove(entries, new_similarity[s])
    new_similarity[g] = {}
    initial_similarity[g] = {}
    for j in prev_similarity:
        if j not in g:
            if g == j :
                new_similarity[g][j] = 0.0
            else:
                #Update new_similarity and initial_similarity for the group with remaining nodes as the minimum similarity value present between each node in group with remaining nodes. 
                initial_similarity[g][j] = initial_similarity[j][g] = min(initial_similarity[g[0]][j], initial_similarity[g[1]][j])
                new_similarity[g][j] = new_similarity[j][g] = min(initial_similarity[g[0]][j], initial_similarity[g[1]][j])
    return new_similarity, initial_similarity

#Find the number of connections each node has.
def degree():
    node_degree = dict()
    for i in G.nodes():
        node_degree[i] = len(adj_list[i]) 
    return node_degree

node_degree = degree()

#Calculate modularity for a given cluster
def modularity(levelCluster):
    mod = 0
    for lc in levelCluster:
        for i in lc:
            for j in lc:
                mod += (adj_matrix[i][j] - (node_degree[i]*node_degree[j]/(2*m)))
    modular = mod/(2*m)
    return modular
    
#Finding ideal clusters based on the dendrogram
def qualityClusters(dendrogram):
    levelModularity = {}
    #Find modularity for each level of dendrogram
    for d in dendrogram:
            levelModularity[d] = modularity(dendrogram[d])
    print(levelModularity)
    #Find the level of dendrogram that has maximum modularity
    max_value = max(levelModularity.values())  
    print("Max Modularity: ",max_value)
    for k, v in levelModularity.items() :
             if v == max_value :
                max_level = k
                #Final set of clusters obtained
                print(dendrogram[max_level])
                print("Number of clusters: ", len(dendrogram[max_level]))
                print("Ideal level for clustering:",max_level)
    #Label each node with the community it belongs to
    i = 0  
    labelledCluster = {}          
    for cluster in dendrogram[max_level]:
        i += 1
        for c in cluster:
            labelledCluster[c] = i 
            
    return labelledCluster            

#Write the nodes, its labels and its community label to a csv file
def writeFile(labelledCluster, similarity):
    fw1 = open(filename+similarity+".csv",'w')
    fw1.write("Node, Label, Community \n")
    for node in G.nodes():
        if not labelled_nodes:
            fw1.write(str(node) + ", " + str(node) + ", " + str(labelledCluster[node]) + " \n")
        else :
            fw1.write(str(node) + ", " + labelled_nodes[node] + ", " + str(labelledCluster[node]) + " \n")
    fw1.close()

################################################################### 
#Find jaccard value for a given pair of nodes               
def jaccard_value(i,j):
    neighbors_of_i = set(adj_list[i])
    neighbors_of_j = set(adj_list[j])
    commonNeighbors = neighbors_of_j.intersection(neighbors_of_i)
    totalNeighbors = neighbors_of_j.union(neighbors_of_i)
    return len(commonNeighbors)/len(totalNeighbors)

#Find jaccard value for given node with all remaining nodes in network        
def jaccard_similarity(jaccard, i, g):
    jaccard[i] = {}
    for j in G.nodes():
            if j not in g :
                if i == j:
                    jaccard[i][j] = 0
                else:
                    jaccard[i][j] = jaccard_value(i,j)
    return jaccard

#Building dendrogram based on jaccard similarity matrix  
def jaccard_clustering(G):
    jaccard = {}
    initialJaccard = {}
    #Calculate jaccard similarity for every pair of nodes
    for i in G.nodes():
        initialJaccard = jaccard_similarity(initialJaccard, i, ())
    dendrogram_jaccard = {}
    #Initialize the bottom level of dendrogram with each node in its own cluster
    dendrogram_jaccard[0] = [[i] for i in G.nodes()]

    #Loop until no group is formed or when only one cluster is remaining
    while(1):
        if not jaccard:
            prevJaccard = copy.deepcopy(initialJaccard)
        else:
            prevJaccard = copy.deepcopy(jaccard)
        #Group nodes or clusters having maximum similarity value
        group = maxSimilarity(prevJaccard) 
        #If no group formed, then return dendrogram
        if not group:
            return dendrogram_jaccard
        #Find the level o dendrogram to which the group belongs using helper function
        level = dLevel(group,1)
        #Convert the group tuple into a list using a helper function
        l = recGroup(group, [])
        #Initialize every new level of dendrogram with its previous level
        if level not in dendrogram_jaccard:
            dendrogram_jaccard[level] = copy.deepcopy(dendrogram_jaccard[level-1])
        #Remove the nodes present in group from dendrogram of that level
        for li in l:
            for d in dendrogram_jaccard[level]:
                if li in d:
                    dendrogram_jaccard[level].remove(d)
        #Converted group list is added to the dendrogram level.
        dendrogram_jaccard[level].append(l)
        #Calculate the new similarity matrix for the new group formed and repeat
        jaccard, initialJaccard = singleLinkage(prevJaccard, initialJaccard, group)
    
print("Jaccard Similarity")
dendrogram_jaccard = jaccard_clustering(G)      
jaccardLabel = qualityClusters(dendrogram_jaccard)
print(jaccardLabel)
writeFile(jaccardLabel, "jaccard")

###################################################################
#Find the number of common neighbors
def commonNeighbors(i,j):
    cn = 0
    for k in G.nodes():
        cn = cn + adj_matrix[i][k] * adj_matrix[k][j]
    return cn

#Find the number of neighbors a node has
def nodeNeighbors(i):
    nn = 0
    for k in G.nodes():
        nn = nn + adj_matrix[i][k]*adj_matrix[i][k]
    return math.sqrt(nn)

#Calculate the cosine similarity for each node to all other nodes
def cosine_similarity(cos, i, g):
        cos[i] = {}
        for j in G.nodes():
            if j not in g:
                if i == j :
                    cos[i][j] = 0.0
                else:
                    cos[i][j] = commonNeighbors(i,j)/(nodeNeighbors(i) * nodeNeighbors(j))
        return cos  

#Building dendrogram based on cosine similarity matrix  
def cosine_clustering():
    initial_cosine = {}
    dendrogram_cosine = {}
    #Initialize the bottom level of dendrogram with each node in its own cluster
    dendrogram_cosine[0] = [[i] for i in G.nodes()]
    new_cosine = {}
    #Calculate cosine similarity for every pair of nodes
    for i in G.nodes():       
        cosine = cosine_similarity(initial_cosine, i, ())
        
    #Loop until no group is formed or when only one cluster is remaining 
    while(1):
        if not new_cosine:
            prev_cosine = copy.deepcopy(initial_cosine)
        else:
            prev_cosine = copy.deepcopy(new_cosine)
        #Group nodes or clusters having maximum similarity value
        g = maxSimilarity(prev_cosine)
        #If no group formed, then return dendrogram
        if not g:
            return dendrogram_cosine
        #Find the level of dendrogram to which the group belongs using helper function
        level = dLevel(g,1)
        #Convert the group tuple into a list using a helper function
        l = recGroup(g, [])
        #Initialize every new level of dendrogram with its previous level
        if level not in dendrogram_cosine:
            dendrogram_cosine[level] = copy.deepcopy(dendrogram_cosine[level-1])
        #Remove the nodes present in group from dendrogram of that level
        for li in l:
            for d in dendrogram_cosine[level]:
                if li in d:
                    dendrogram_cosine[level].remove(d)
        #Converted group list is added to the dendrogram level.
        dendrogram_cosine[level].append(l)
        #Calculate the new similarity matrix for the new group formed and repeat
        new_cosine, initial_cosine = singleLinkage(prev_cosine, initial_cosine, g)
    
    
print("Cosine Similarity") 
dendrogram_cosine = cosine_clustering()
cosineLabel = qualityClusters(dendrogram_cosine)
print(cosineLabel)
writeFile(cosineLabel, "cosine")

#########################################################################
#Calculate pearson coefficient for a given pair of nodes
def pearsonCoeffecient(i,j):
    nr = commonNeighbors(i,j) - ((node_degree[i]*node_degree[j])/n)
    dr1 = math.sqrt(node_degree[i] - ((node_degree[i]*node_degree[i])/n))
    dr2 = math.sqrt(node_degree[j] - ((node_degree[j]*node_degree[j])/n))
    coeff = nr/(dr1*dr2)
    return coeff

#Calculate the cosine similarity for each node to all other nodes
def pearsonCoeffecient_similarity(pearson, i, g):
        pearson[i] = {}
        for j in G.nodes():
            if j not in g:
                if i == j :
                    pearson[i][j] = 0.0
                else:
                    pearson[i][j] = pearsonCoeffecient(i,j)
        return pearson 
    
#Building dendrogram based on pearson coefficient similarity matrix      
def pearsonCoeffecient_clustering():
    initial_pearsonCoeffecient = {}
    pearson_coeffecient = {}
    dendrogram_pearson = {}
    #Initialize the bottom level of dendrogram with each node in its own cluster
    dendrogram_pearson[0] = [[i] for i in G.nodes()]
    #Calculate pearson coefficient for every pair of nodes
    for i in G.nodes(): 
            initial_pearsonCoeffecient = pearsonCoeffecient_similarity(initial_pearsonCoeffecient, i, ())
    new_pearson = {}
    #Loop until no group is formed or when only one cluster is remaining
    while(1):
        if not new_pearson:
            prev_pearson = copy.deepcopy(initial_pearsonCoeffecient)
        else:
            prev_pearson = copy.deepcopy(new_pearson)
        #Group nodes or clusters having maximum similarity value
        g = maxSimilarity(prev_pearson)
        #If no group formed, then return dendrogram
        if not g:
            return dendrogram_pearson
        #Find the level of dendrogram to which the group belongs using helper function
        level = dLevel(g,1)
        #Convert the group tuple into a list using a helper function
        l = recGroup(g, [])
        #Initialize every new level of dendrogram with its previous level
        if level not in dendrogram_pearson:
            dendrogram_pearson[level] = copy.deepcopy(dendrogram_pearson[level-1])
        #Remove the nodes present in group from dendrogram of that level
        for li in l:
            for d in dendrogram_pearson[level]:
                if li in d:
                    dendrogram_pearson[level].remove(d)
        #Converted group list is added to the dendrogram level.
        dendrogram_pearson[level].append(l)
        #Calculate the new similarity matrix for the new group formed and repeat
        new_pearson, initial_pearson = singleLinkage(prev_pearson, initial_pearsonCoeffecient, g)
    
    
print("Pearson Coefficient")  
dendrogram_pearson = pearsonCoeffecient_clustering()
pearsonLabel = qualityClusters(dendrogram_pearson)
print(pearsonLabel)
writeFile(pearsonLabel, "pearson")
    
