# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 22:44:26 2018

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
tol=1.0e-6
#filename = input("Enter filename:")
filename = "dolphins/dolphins.gml"
f = open(filename, 'r')

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
#print(adj_list)

def eigenvector_centrality(G):    

   x = dict([(n,1.0/len(G)) for n in G])
   # normalize starting vector 
   s = 1.0/sum(x.values())
   for k in x: 
      x[k] *= s 
   nnodes = G.number_of_nodes() 
   # make up to max_iter iterations 
   for i in range(100): 
      xlast = x 
      x = dict.fromkeys(xlast, 0) 
      # do the multiplication y^T = x^T A 
      for n in x: 
         for nbr in G[n]: 
            x[nbr] += xlast[n] * a[n][nbr]
      normalize = math.sqrt(sum(v**2 for v in x.values()))
      if normalize == 0:
           s = 1
      else:
           s = 1.0/normalize
      for n in x: 
            x[n] *= s
      # check convergence 
      err = sum([abs(x[n]-xlast[n]) for n in x]) 
      if err < nnodes*tol: 
         return x
   return x

eigen = eigenvector_centrality(G) 
print("Eigenvector centrality")
print(['%s: %0.4f'%(node,eigen[node]) for node in eigen]) 

eigen_nx = nx.eigenvector_centrality_numpy(G)
print("Eigenvector centrality NetworkX") 
print(['%s: %0.4f'%(node,eigen_nx[node]) for node in eigen_nx])

def katz_centrality(G):
    nnodes = G.number_of_nodes() 
    max_iter = 1000
    alpha = 0.1
    beta = 1.0
    x = dict([(n,0) for n in G]) 
    b = dict.fromkeys(G,float(beta)) 
    # make up to max_iter iterations 
    for i in range(max_iter): 
        xlast = x 
        x = dict.fromkeys(xlast, 0) 
        for n in x: 
            for nbr in G[n]: 
                x[nbr] += xlast[n] * a[n][nbr]
        for n in x: 
            x[n] = alpha*x[n] + b[n] 
        
        # check convergence 
        err = sum([abs(x[n]-xlast[n]) for n in x]) 
        if err < nnodes*tol:
            normalize = math.sqrt(sum(v**2 for v in x.values()))
            if normalize == 0:
                s = 1
            else:
                s = 1.0/normalize
            for n in x: 
                x[n] *= s
            return x
    
    normalize = math.sqrt(sum(v**2 for v in x.values()))
    if normalize == 0:
        s = 1
    else:
        s = 1.0/normalize
    for n in x: 
        x[n] *= s
    
    return x
    

katz = katz_centrality(G)
print("Katz Centrality") 
print(['%s: %0.4f'%(node,katz[node]) for node in katz]) 

katz_nx = nx.katz_centrality_numpy(G)
print("Katz Centrality NetworkX") 
print(['%s: %0.4f'%(node,katz_nx[node]) for node in katz_nx])
       
def degree():
    node_degree = dict()
    for i in G.nodes():
        node_degree[i] = len(adj_list[i]) 
    return node_degree

node_degree = degree()

def pagerank_centrality(G):
    nnodes = G.number_of_nodes() 
    max_iter = 1000
    alpha = 0.1
    beta = 1.0
    x = dict([(n,0) for n in G]) 
    b = dict.fromkeys(G,float(beta)) 
    # make up to max_iter iterations 
    for i in range(max_iter): 
        xlast = x 
        x = dict.fromkeys(xlast, 0) 
        for n in x: 
            for nbr in G[n]: 
                x[nbr] += (xlast[n]/node_degree[n]) * a[n][nbr]
        for n in x: 
            x[n] = alpha*x[n] + b[n] 
         
        # check convergence 
        err = sum([abs(x[n]-xlast[n]) for n in x]) 
        if err < nnodes*tol: 
            normalize = math.sqrt(sum(v**2 for v in x.values()))
            if normalize == 0:
                s = 1
            else:
                s = 1.0/normalize
            for n in x: 
                x[n] *= s
            return x
    '''
    normalize = sqrt(sum(v**2 for v in x.values()))
    if normalize == 0:
        s = 1
    else:
        s = 1.0/normalize
    for n in x: 
        x[n] *= s
    '''
    return x
'''        
eigen = eigenvector_centrality(G) 
#print(eigen)
#print(['%s: %0.2f'%(node,eigen[node]) for node in eigen]) 

eigen_nx = nx.eigenvector_centrality(G) 
#print(['%s: %0.2f'%(node,eigen_nx[node]) for node in eigen_nx]) 

katz = katz_centrality(G) 
#print(['%s: %0.2f'%(node,katz[node]) for node in katz]) 

katz_nx = nx.katz_centrality(G,0.1,1.0,10000) 
#print(['%s: %0.2f'%(node,katz_nx[node]) for node in katz_nx]) 
'''
pagerank = pagerank_centrality(G)
print("Pagerank Centrality") 
print(['%s: %f'%(node,pagerank[node]) for node in pagerank]) 

pagerank_nx = nx.pagerank_numpy(G)
print("Pagerank Centrality NetwokX")
print(['%s: %f'%(node,pagerank_nx[node]) for node in pagerank_nx])

betweeness = nx.betweenness_centrality(G)
closeness = nx.closeness_centrality(G)

def Nmaxelements(centrality, N): 
    max_list = dict()
    for i in range(0, N):  
        max_value = 0
        max_key = 0
        for key, value in centrality.items():      
            if value > max_value and value not in max_list.values(): 
                max_value = value
                max_key = key
        max_list[max_key] = max_value
    print(['%s: %0.4f'%(node,max_list[node]) for node in max_list])

print("Top Centralities")
print("Eigenvector Centrality: ")
Nmaxelements(eigen, 5)
print("Katz Centrality: ")
Nmaxelements(katz, 5)
print("Pagerank Centrality: ")
Nmaxelements(pagerank, 5)

print("Top Centralities of NetworkX functions")
print("Degree Centrality:")
Nmaxelements(node_degree, 3)
print("Closeness Centrality:")
Nmaxelements(closeness, 3)
print("Betweenness Centrality:")
Nmaxelements(betweeness, 3)
print("Eigenvector Centrality: ")
Nmaxelements(eigen_nx, 3)
print("Katz Centrality: ")
Nmaxelements(katz_nx, 3)
print("Pagerank Centrality: ")
Nmaxelements(pagerank_nx, 3)

betweeness = nx.betweenness_centrality(G)
closeness = nx.closeness_centrality(G)



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
print(node_degree[17])
fw1 = open(filename+"Nodes1.csv",'w')
fw1.write("id, label, degree centrality, closeness centrality, betweeness centrality, Eigenvector centrality, Katz centrality, Pagerank centrality  \n")
for node in nodes:
    if not labelled_nodes:
        fw1.write(str(node) + ", " + str(node) + ", " + str(node_degree[node]) + ", " + str(closeness[node]) + ", " + str(betweeness[node]) + ", " + str(eigen_nx[node]) + ", " + str(katz_nx[node]) + ", " + str(pagerank_nx[node]) + " \n")
    else :
        fw1.write(str(node) + ", " + labelled_nodes[node] + ", " + str(node_degree[node]) + ", " + str(closeness[node]) + ", " + str(betweeness[node]) + ", " + str(eigen_nx[node]) + ", " + str(katz_nx[node]) + ", " + str(pagerank_nx[node]) + " \n")
fw1.close()  

fw2 = open(filename+"Edges1.csv", "w")
fw2.write("Source, Target, Type, Source Degree, Target Degree, Common Neighbor, Total Neighbors \n")
for e in edges:
    fw2.write(str(e[0]) + ", " + str(e[1]) + ", Undirected," +  str(node_degree[e[0]]) + ", " + str(node_degree[e[1]]) + ", " + str(commonNeighbor[e]) + ", " + str(totalNeighbor[e]) + " \n")
fw2.close()

#", " + str(weighted_edges[e]) +
