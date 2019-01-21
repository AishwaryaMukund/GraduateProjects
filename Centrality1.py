# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 22:12:03 2018

@author: Aishwarya Mukunda
"""
import networkx as nx
import matplotlib.pyplot as plt

nodes = []
edges = []
labels = []
filename = input("Enter filename:")
f = open(filename, 'r')

while True:
    line = f.readline()
    if not line:
        break
    if "id" in line:
        node_id = line.replace("id","").strip()
        if node_id.isdigit():
            nodes.append(int(node_id))
    if "label" in line:
        label = line.replace("label","").strip()
        labels.append(label)
    if "source" in line:
        src = line.replace("source","").strip()
    if "target" in line:
        target = line.replace("target","").strip()
        edges.append((int(src),int(target)))
        
f.close()

labelled_nodes = dict(zip(nodes,labels))
print(labelled_nodes)        
G = nx.Graph()
G.add_nodes_from(nodes)
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
       
def adjacency_matrix():
    for e in G.edges():
        a[e[0]][e[1]] = 1
        a[e[1]][e[0]] = 1
    return a

a = adjacency_matrix()
#print_matrix(a)

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
print("Adjacency List")
print(adj_list)

def degree():
    node_degree = dict()
    for i in G.nodes():
        node_degree[i] = len(adj_list[i]) 
    return node_degree

node_degree = degree()
print(node_degree)

commonNeighbor = dict()
totalNeighbor = dict()

def neighbors():
    for e in edges:
        common = notCommon = 0
        for i in adj_list[e[0]]:
            if i in adj_list[e[1]]:
                common = common + 1
            elif i != e[1]:
                notCommon = notCommon + 1
        commonNeighbor[e] = common
        totalNeighbor[e] = common + notCommon
        
neighbors()
#print(commonNeighbor)
#print(totalNeighbor)
    
class Queue:
    def __init__(self):
        self.items = []
 
    def is_empty(self):
        return self.items == []
 
    def enqueue(self, data):
        self.items.append(data)
 
    def dequeue(self):
        return self.items.pop(0)

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

closeness = dict()

def closeness_centrality():
    for node in nodes:
        path = find_shortest_paths(node)
        closeness[node] = (n-1)/sum(path.values())
    return closeness
    
closeness = closeness_centrality()
print("Closeness Centrality")
print(closeness)

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

def betweeness_centrality():
    cb = {}    
    P = {}
    sigma = {}
    d = {}
    delta = {}
    for v in nodes:
        cb[v] = 0 
    for s in nodes:
        S = Stack()
        for w in nodes:
            P[w] = [] 
            sigma[w] = 0 #for t in nodes
            d[w] = -1 #for t in nodes
        sigma[s] = 1 
        d[s] = 0
        Q = Queue()
        Q.enqueue(s)
        while not Q.is_empty():
            v = Q.dequeue()
            S.push(v)
            for w in adj_list[v]:
                if d[w] < 0:
                    Q.enqueue(w)
                    d[w] = d[v] + 1
                if d[w] == d[v] + 1:
                    sigma[w] = sigma[w]+sigma[v]
                    P[w].append(v)
        for v in nodes:
            delta[v] = 0 
        while not S.isEmpty():
            w = S.pop()
            for v in P[w]:
                delta[v] = delta[v] + ((sigma[v]/sigma[w]) * (1+delta[w]))
            if w != s:
                cb[w] = cb[w] + delta[w]
    #for undirected graph 
    for w in nodes: 
        cb[w] = cb[w]/2           
    return cb
    
betweeness = betweeness_centrality()
print("Betweeness Centrality")
print(betweeness)

def Nmaxelements(centrality, N): 
    max_list = dict()
    for i in range(0, N):  
        max_value = 0   
        for key, value in centrality.items():      
            if value > max_value and value not in max_list.values(): 
                max_value = value
                max_key = key
        max_list[max_key] = max_value
    print(max_list)

print("Top 3 CLoseness, degree, betweeness centrality")   
Nmaxelements(closeness,3)
Nmaxelements(node_degree,3)
Nmaxelements(betweeness, 3)
#Nmaxelements(closeness,5)
#Nmaxelements(node_degree,5)
#Nmaxelements(betweeness, 5)

fw1 = open(filename+"Nodes.csv",'w')
fw1.write("id, label, degree centrality, closeness centrality, betweeness centrality  \n")
for node in nodes:
    if not labelled_nodes:
        fw1.write(str(node) + ", " + str(node) + ", " + str(node_degree[node]) + ", " + str(closeness[node]) + ", " + str(betweeness[node]) + " \n")
    else :
        fw1.write(str(node) + ", " + labelled_nodes[node] + ", " + str(node_degree[node]) + ", " + str(closeness[node]) + ", " + str(betweeness[node]) + " \n")
fw1.close()  

fw2 = open(filename+"Edges.csv", "w")
fw2.write("Source, Target, Type, Source Degree, Target Degree, Common Neighbor, Total Neighbors \n")
for e in edges:
    fw2.write(str(e[0]) + ", " + str(e[1]) + ", Undirected," +  str(node_degree[e[0]]) + ", " + str(node_degree[e[1]]) + ", " + str(commonNeighbor[e]) + ", " + str(totalNeighbor[e]) + " \n")
fw2.close()