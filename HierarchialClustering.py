# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 23:37:42 2018

@author: Aishu
"""

import networkx as nx
import matplotlib.pyplot as plt
import math

nodes = []
edges = []
labels = []
weights = []
node_values = []

filename = input("Enter filename:")
#filename = "dolphins/dolphins.gml"
#filename = "karate/karate.gml"
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

labelled_nodes = dict(zip(nodes,labels))
print(labelled_nodes)

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

if G.nodes()[1] == 0:
    a = [[0]*(n+1) for i in G.nodes()]  
else :
    a = [[0]*(n+1) for i in range(0,n+1)]

def print_matrix(a):
    for i in G.nodes():
        for j in G.nodes():
            print(a[i][j],end=" ")
        print("\n")

#Find the adjacency matrix of the graph      
def adjacency_matrix():
    for e in G.edges():
        a[e[0]][e[1]] = 1
        a[e[1]][e[0]] = 1
    return a

a = adjacency_matrix()


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

def degree():
    node_degree = dict()
    for i in G.nodes():
        node_degree[i] = len(adj_list[i]) 
    return node_degree

node_degree = degree()

def edge_betweenness_centrality(G, k=None, normalized=True, weight=None,
                                seed=None):
    betweenness = dict.fromkeys(G, 0.0)  
    betweenness.update(dict.fromkeys(G.edges(), 0.0))
    for s in nodes:
        # single source shortest paths using BFS
        S, P, sigma = _single_source_shortest_path(G, s)
        #calculate edge betweenness centrality
        betweenness = _accumulate_edges(betweenness, S, P, sigma, s)
    
    for n in G:  # remove nodes to only return edges
        del betweenness[n]
    #rescaling betweenness values
    betweenness = _rescale_e(betweenness, len(G), normalized=normalized)
    return betweenness

#Number of shortest paths from source s to all other nodes
def _single_source_shortest_path(G, s):
    S = []
    P = {}
    for v in G:
        P[v] = []
    sigma = dict.fromkeys(G, 0.0)    # Keys are nodes, values are no. of shortest paths from s to key 
    D = {}
    sigma[s] = 1.0
    D[s] = 0
    Q = [s]
    while Q:   # use BFS to find shortest paths
        v = Q.pop(0)
        S.append(v) #BFS traversal
        Dv = D[v]
        sigmav = sigma[v]
        for w in G[v]:
            if w not in D:
                Q.append(w)
                D[w] = Dv + 1
            if D[w] == Dv + 1:   # this is a shortest path, count paths
                sigma[w] += sigmav
                P[w].append(v)  # predecessors
    return S, P, sigma       

#Betweenness = number of shortest paths passing through edge e/number of shortest paths
def _accumulate_edges(betweenness, S, P, sigma, s):
    delta = dict.fromkeys(S, 0)
    while S:
        w = S.pop()
        coeff = (1 + delta[w]) / sigma[w]
        for v in P[w]:  
            c = sigma[v] * coeff
            if (v, w) not in betweenness:  #checking for all edges from w to its predecessors
                betweenness[(w, v)] += c   #update betweenness value for that edge
            else:
                betweenness[(v, w)] += c  #undirected graph
            delta[v] += c                 
        if w != s:
            betweenness[w] += delta[w]
    return betweenness

def _rescale_e(betweenness, n, normalized):
    if normalized:
        if n <= 1:
            scale = None  # no normalization b=0 for all nodes
        else:
            scale = 1 / (n * (n - 1))
    else:  
            scale = 0.5
    if scale is not None:
        for v in betweenness:
            betweenness[v] *= scale
    return betweenness

#Find components in Graph     
def connected_components(nodes):
    
        # List of connected components.
        result = []
        nodes = set(nodes)
        # Iterate while we still have nodes to process.
        while nodes:
            # Get a random node and remove it from the global set.
            n = nodes.pop()
            # This set will contain the next group of nodes connected to each other.
            group = {n}
            # Build a queue with this node in it.
            queue = [n]
            # Iterate the queue.
            # When it's empty, we finished visiting a group of connected nodes.
            while queue:
                # Consume the next item from the queue.
                n = queue.pop(0)    
                # Neighbors of n.
                neighbors = set(G[n])    
                # Remove the neighbors we already visited.
                neighbors.difference_update(group)
                # Remove the remaining nodes from the global set.
                nodes.difference_update(neighbors)
                # Add them to the group of connected nodes.
                group.update(neighbors)
                # Add them to the queue, so we visit them in the next iterations.
                queue.extend(neighbors)
            # Add the group to the list of groups.
            result.append(list(group))
        # Return the list of groups.
        return result 

#Compares two lists a and b   
def cmp(a, b):
    return (a > b) - (a < b)     

#Edge Betweenness algorithm to find components and returns a dendrogram  
def edge_betweenness(nodes):
    ebc = edge_betweenness_centrality(G)
    dendrogram = {}
    #Initially list of all nodes is considered as one component/community
    components = [nodes]
    level = 0
    while len(G.edges()) > 0:
        #Finding edge having maximum edge betweenness centrality
        max_value = max(ebc.values())
        for k, v in ebc.items() :
            if v == max_value :
                e = k 
        #Remove that edge
        G.remove_edge(e[0],e[1])
        #Calculate edge betweenness centraility for remaining edges
        ebc = edge_betweenness_centrality(G)
        #Components found in previous iteration
        prevComponents = components
        #Components found as a result of removing the edge
        components = connected_components(G.nodes())
        #If the previous components and current components are not same, then add the components in the level of dendrogram.
        if cmp(prevComponents, components) != 0:
            level = level + 1
            dendrogram[level] = components

    return dendrogram
    
dendrogram = edge_betweenness(nodes)
print("Division of Clusters")
print(dendrogram)

#Calculate modularity for a given cluster
def modularity(levelCluster):
    mod = 0
    for lc in levelCluster:
        for i in lc:
            for j in lc:
                mod += (a[i][j] - (node_degree[i]*node_degree[j]/(2*m)))
    modular = mod/(2*m)
    return modular
    
#Finding ideal clusters based on the dendrogram
def qualityClusters():
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
                print("Number of clusters: ",len(dendrogram[max_level]))
                print("Ideal level for clustering:",max_level)
    #Label the nodes with its corresponding cluster
    i = 0  
    labelledCluster = {}          
    for cluster in dendrogram[max_level]:
        i += 1
        for c in cluster:
            labelledCluster[c] = i 
            
    return labelledCluster

labelledCluster = qualityClusters()

#Write the nodes and its community labels into a csv file. 
fw1 = open(filename+"ebtw.csv",'w')
fw1.write("Node, Label, Community \n")
for node in nodes:
    if not labelled_nodes:
        fw1.write(str(node) + ", " + str(node) + ", " + str(labelledCluster[node]) + " \n")
    else :
        fw1.write(str(node) + ", " + labelled_nodes[node] + ", " + str(labelledCluster[node]) + " \n")
fw1.close()

