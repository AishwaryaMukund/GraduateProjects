# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 10:44:02 2018

@author: Aishu
"""

import networkx as nx
import numpy as np
import copy
import math

#Sample Graph
nodes = [1,2,3,4,5,6,7,8,9]
edges = [(1,2), (1,3), (2,3), (3,4), (4,5), (4,6), (7,8), (7,9), (8,9), (5,8)]
weights = []

########################################################################################

#Initialization of variables
nodes = []
edges = []
labels = []
weights = []
node_values = []

#Reading path of data file

#filename = input("Enter filename:")
#filename = "karate/karate.gml"
filename = "dolphins/dolphins.gml"
#filename = "lesmis/lesmis.gml"
#filename = "adjnoun/adjnoun.gml"
#filename = "football/football.gml"
f = open(filename, 'r')

#Reading .gml file
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

########################################################################################

#Creating a networkX graph of the data in .gml file 
G = nx.Graph()
G.add_nodes_from(nodes)
if weights != []:
    for i in weighted_edges:
        G.add_edge(i[0], i[1],weight=weighted_edges[i])
else:
    G.add_edges_from(edges)
    
n = G.number_of_nodes()
m = G.number_of_edges()

#Creates a 2D matrix of size number of nodes with all elements set to 0.
def initialize_2Dmatrix(nodes):
    if nodes[1] == 0:
        a = [[0]*(n+1) for i in nodes]  
    else :
        a = [[0]*(n+1) for i in range(0,n+1)]
    return a

#Prints each element of 2D matrix
def print_matrix(a):
    for i in G.nodes():
        for j in G.nodes():
            print('%.2f'%(a[i][j]),end=" ")
        print("\n")

#Creates an adjacency matrix
def adjacency_matrix(a):
    for e in G.edges():
        a[e[0]][e[1]] = 1
        a[e[1]][e[0]] = 1
    return a

adj_matrix = adjacency_matrix(initialize_2Dmatrix(G.nodes()))
#print_matrix(adj_matrix)

#Creates an adjacency list
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

#######################################################################################

pagerank = nx.pagerank_numpy(G)
print("Pagerank Centrality NetwokX")
print(['%s: %f'%(node,pagerank[node]) for node in pagerank])

betweeness = nx.betweenness_centrality(G)
print("Betweenness Centrality NetwokX")
print(['%s: %f'%(node,betweeness[node]) for node in betweeness])

#Function that return Top k centrality values
def Nmaxelements(centrality, N): 
    max_list = dict()
    for i in range(0, N):  
        max_value = 0
        max_key = 0
        for key, value in centrality.items():      
            if value > max_value and key not in max_list.keys(): 
                max_value = value
                max_key = key
        max_list[max_key] = max_value
    #print(['%s: %0.4f'%(node,max_list[node]) for node in max_list])
    return max_list
    
print("Top Pagerank Centrality: ")
max_pagerank = Nmaxelements(pagerank, 3)
print(['%s: %0.4f'%(node,max_pagerank[node]) for node in max_pagerank])
#print(['%s: %s'%(labelled_nodes[node],conferences[valued_nodes[node]]) for node in max_pagerank])
print("Top Betweenness Centrality:")
max_betweenness = Nmaxelements(betweeness, 3)
print(['%s: %0.4f'%(node,max_betweenness[node]) for node in max_betweenness])
#print(['%s: %s'%(labelled_nodes[node],conferences[valued_nodes[node]]) for node in max_betweenness])

#Find new centrality 
def newCentrality():
    newc = {}
    for i in G.nodes():
            #Find neighbor of node i that has max betweenness centrality
            maxBet = betweeness[i]
            max_kb = i
            for k in adj_list[i]:
                if maxBet < betweeness[k]:
                    maxBet = betweeness[k]
                    max_kb = k
            #Find neighbor of node i that has max pagerank centrality
            maxPg = pagerank[i]
            max_kp = i
            for k in adj_list[i]:
                if maxPg < pagerank[k]:
                    maxPg = pagerank[k]
                    max_kp = k
            #Combination of betweenness and pagerank centrality
            newc[i] = (betweeness[max_kb] + pagerank[max_kp])/2
    return newc

#Print the new centrality    
newc = newCentrality()
print("New Centrality")
print(newc)
#print(['%s: %d'%(node,newc[node]) for node in newc])


#Print the top 3 new centrality nodes
print("Top New Centrality:")
max_new = Nmaxelements(newc, 5)
print(['%s: %0.4f'%(node,max_new[node]) for node in max_new])
#print(['%s: %s'%(node,conferences[valued_nodes[node]]) for node in max_new])

#Function to find nodes of low centrality values
def Nminelements(centrality, N): 
    min_list = dict()
    for i in range(0, N):  
        min_value = 99
        min_key = 0
        for key, value in centrality.items():      
            if value < min_value and key not in min_list.keys(): 
                min_value = value
                min_key = key
        min_list[min_key] = min_value
    #print(['%s: %0.4f'%(node,max_list[node]) for node in max_list])
    return min_list


#Print the top 3 new centrality nodes
print("Bottom New Centrality:")
min_new = Nminelements(newc, 3)
print(['%s: %0.4f'%(node,min_new[node]) for node in min_new])

#########################################################################################

#Queue implementation 
class Queue:
    #Initialize an empty list as a queue
    def __init__(self):
        self.items = []
    #Check if queue is empty
    def is_empty(self):
        return self.items == []
    #Insert elements into queue
    def enqueue(self, data):
        self.items.append(data)
    #Remove elements from queue
    def dequeue(self):
        return self.items.pop(0)

#Funtion to find the number of shortest distance from a node src to all other nodes in network using BFS
def find_shortest_paths(src):
    distance = {src: 0} 
    visited = set()
    q = Queue()
    q.enqueue(src)
    visited.add(src)
    while not q.is_empty():
        current = q.dequeue()
        for dest in adj_list[current]:
            if dest not in visited:
                visited.add(dest)
                distance[dest] = distance[current] + 1
                q.enqueue(dest)
    return distance

#Calculate distance centrality of all nodes
def distanceCentrality():
    closeness = {}
    for node in G.nodes():
        #Finds the shortest path for all nodes from node. 
        path = find_shortest_paths(node)
        #Distance centrality of a node is sum of all shortest distances from that node to all other nodes
        closeness[node] = sum(path.values())
    return closeness

#Find a set of leaders based on distance centrality 
def findLeaders(dist):
    leaders = set()
    for v in G.nodes():
        for u in adj_list[v]:
            #If distance centrality of a node is less than its neighbors, then its a leader
            if dist[v] < dist[u]:
                leaders.add(v)
    return leaders

#Find the number of common neighbors between i and j        
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

#Calculate similarity between i and j using the formula.
def cosine_similarity(i, j):
    cosine = (commonNeighbors(i,j) + adj_matrix[i][j])/(nodeNeighbors(i) * nodeNeighbors(j))
    return cosine

#Helper function to remove items from dictionary
def entries_to_remove(entries, similarity):
    #Entries is a list of items to be removed
    for key in entries:  
        #If element in entries is present in similarity matrix, then delete that key value pair
        if key in similarity:           
            del similarity[key]        
    return similarity

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

#####################################################################################################

#Main function to find the leaders and its followers and label them as communities
def leaderFollower():
    #Find distance centrality
    distance = distanceCentrality()
    #print(distance)
    #Find the set of leaders using distance centrality
    leaders = findLeaders(distance)
    #print("Leaders: ", leaders)
    #All nodes in the graph is stored as a set in network
    network = set(G.nodes())   
    #Set difference of leaders from network gives followers
    followers = network.difference(leaders)
    #print("Followers: ", followers)
    
     
    lFollower = {}
    #Each leader indicates a single cluster containing the leader itself
    for l in leaders:
        lFollower[l] = [l]
    #Find leaders for every follower
    for f in followers:
        similarity = {}
        #Find cosine similarity value for each leader with the follower
        for l in leaders:
            similarity[l] = cosine_similarity(f, l)
        max_similarity = 0
        for key in similarity:
            #Find the leader that has maximum similarity with follower
            if max_similarity < similarity[key]:
                max_similarity = similarity[key]
                max_key = key
        #Add the follower into the cluster formed by leader node
        lFollower[max_key].append(f)           
    #print(lFollower)
    
    #Merge all leaders that do not have followers with their most similar leader.  
    entries = []
    for lf in lFollower:
        if len(lFollower[lf]) == 1:
            lsimilarity = {}
            #Find cosine similarity between leader having no follower with all leaders having more than one follower
            for l in leaders:                
                if len(lFollower[l]) != 1:
                    lsimilarity[l] = cosine_similarity(lf, l) 
            max_lsimilarity = 0
            for key in lsimilarity:
                #Find the leader that has maximum similarity with the leader with no follower(lf)
                if max_lsimilarity < lsimilarity[key]:
                    max_lsimilarity = lsimilarity[key]
                    max_l = key  
            #If the centrality of found leader is less than lf then, 
            if distance[max_l] < distance[lf]:
                #lf becomes follower of found leader
                lFollower[max_l].append(lf)
                #Remove lf from the set of leaders and dictionary containing followers for each leader
                leaders.remove(lf)
                entries.append(lf)
            #If centrality of lf is lesser than its closely found leader then,                
            else:
                #Add all followers of found leader as followers of lf
                for f in lFollower[max_l]:
                    lFollower[lf].append(f)
                #Remove the found leader from set of leaders and dictionary containing followers for each leader
                leaders.remove(max_l)
                entries.append(max_l)

    print("Final Leaders: ", leaders)
    leaderFollowers = entries_to_remove(entries, lFollower)
    print("Leader and their followers: ")
    print(leaderFollowers)
    #Find the modularity of the communities found.
    modular = modularity(leaderFollowers.values())
    print("Modularity: ",modular)
    
    #Label each cluster in increasing order
    i = 0  
    labelledCluster = {}          
    for cluster in leaderFollowers:
        i += 1
        for c in leaderFollowers[cluster]:
            labelledCluster[c] = i
    
    #Label if each node is a leader or not as 1 and 0 respectively        
    labelledLeaders = {}        
    for v in G.nodes():
        if v in leaders:
            labelledLeaders[v] = 1
        else:
            labelledLeaders[v] = 0
            
    return labelledCluster, labelledLeaders

    
                    
##########################################################################################

#Write the community and leaders data in csv file for visualization in gephi
def writeFile(labelledCluster, labelledLeaders):
    fw1 = open(filename+"LeadFoll.csv",'w')
    fw1.write("Node, Label, Community \n")
    for node in G.nodes():
        if not labelled_nodes:
            fw1.write(str(node) + ", " + str(node) + ", " + str(labelledCluster[node]) + ", " + str(labelledLeaders[node]) + " \n")
        else :
            fw1.write(str(node) + ", " + labelled_nodes[node] + ", " + str(labelledCluster[node]) + ", " + str(labelledLeaders[node]) +" \n")
    fw1.close()

##############################################################################################
            
labelledCluster, labelledLeaders = leaderFollower()
#print(labelledCluster)
writeFile(labelledCluster, labelledLeaders)
