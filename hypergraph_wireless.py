#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 15:22:33 2023

@author: ashwinganesan

The Python module below generates the hypergraph of a wireless network.  

Given a set S of wireless stations on the Euclidean plane, 
a path loss exponent gamma, and a reception threshold beta, 
one can define the hypergraph H=(V,E) generated by the 
wireless network A = <S,gamma,beta> as follows.  
The vertex set V is the set S of stations. A subset W of S is 
forbidden if it cannot be simultaneously active in the sense 
that the interference (or energy) at some station in W due 
to transmissions by the remaining stations in W exceeds the 
reception threshold beta.  The edge set E is defined to be 
the collection of all minimal forbidden subsets of S.  

This system model is defined in detail at 
https://arxiv.org/pdf/2207.00515 
(preprint of a manuscript submitted to 
 IEEE Transactions on Mobile Computing in December 2023).

The Python code below creates the hypergraph H of a wireless network. 
The data structure used is the following:  The edge set E is stored 
as a dictionary where E[k] is the list of edges of size k.  
The set of edges of size k is a subset of the k-th level set 
in the poset of all subsets of V.  This makes it convenient to 
visualize the data structure for the hypergraph's edge set: because 
each edge must be a *minimal* forbidden set, once an edge set is 
found to be forbidden, all its supersets (in the higher levels 
of the poset) can be removed.  

"""


import random
import itertools
from itertools import chain, combinations
import math

# alpha_range = [4, 20]
# alpha=4

def Euclidean_distance(a,b):
    #input: vectors a and b in R^n
    #output: the Euclidean distance between the vectors
    res = 0
    n = len(a)
    for i in range(n):
        res = res + (a[i]-b[i])**2
    res = res ** 0.5
    return res
        
def compute_interference(a,b, alpha):
    #a, b are points in R^2, alpha is the path loss exponent
    #compute: interference at b due to transmission at a    
    dist = Euclidean_distance(a, b)
    return 1 / (dist ** alpha)
    
def energy(S, r, alpha):
    #S: a list of points in 2d plane, where S is a set of senders
    #r: a point in 2D plane, where r is for receiver
    #alpha: path loss exponent
    #compute total energy at r due to points in S
    res = 0
    for s in S:
        res = res + compute_interference(s, r, alpha)
    return res    

def compute_worst_case_interference(W, alpha):
    #input: a set of points W in R^2 and path loss exponent alpha
    #output: worst-case (maximum) interference value and its receiver location
    Emax = 0    #max energy at a receiver w
    current_max_receiver = (0, 0)
    for w in W:
        W_minus_w = W[:]
        W_minus_w.remove(w)
        energy_at_w = energy(W_minus_w, w, alpha)
        # print("at ", point, " energy = ", Epoint)
        if energy_at_w > Emax:
            Emax = energy_at_w
            current_worst_receiver = w
    return energy_at_w, w        

def degree_to_radian(theta):
    #theta: angle in degrees, i.e. in [0, 360]
    #convert to radians
    return theta * math.pi / 180

def polar_to_rectangular(point):
    #Input: a 2-tuple point=(r,theta)
    #r: positive real number
    #theta: angle in radian
    #Output: a 2-tuple (x,y)
    import math
    r, theta = point
    return (r * math.cos(theta), r * math.sin(theta))


def uniformly_on_circle(k):
    #k: a positive integer
    #returns a list of k points uniformly spaced on unit circle, in cartersian form
    #first point is (1,0)
    angles_in_degrees = [(360/k) * i for i in range(k)]
    angles_in_radians = [degree_to_radian(theta) for theta in angles_in_degrees]
    points_polar = [(1, theta) for theta in angles_in_radians]
    points_rect = [polar_to_rectangular(a) for a in points_polar]
    return points_rect    
    


# def conj_min_interference():
#     delta = [12 for i in range(5)]    
#     theta = [60+x for x in delta]
#     angles = [0, theta[0], theta[0] + theta[1], theta[0] + theta[1] + theta[2], \
#               theta[0] + theta[1] + theta[2] + theta[3] ]
#     print(angles)
#     points = convert_angles_to_points(angles)
#     maxinterf, receiver = compute_worst_case_inteference(points)
#     print("Conj min interference and receiver: ", maxinterf, receiver)
#     return maxinterf
    
# def test(minvalue, alpha):
#     #generate 5 points in unit circle such that angle between any two is at least 60 deg
#     currentmin = 2
#     while currentmin > minvalue:
#         delta = [random.random() for i in range(4)]    
#         sumtemp = sum(delta)
#         delta = [a * 120 / sumtemp for a in delta]
#         theta = [60+x for x in delta]
#         angles = [0, theta[0], theta[0] + theta[1], \
#                   theta[0] + theta[1] + theta[2]]
#         # print(angles)
#         points = convert_angles_to_points(angles)
#         maxinterf, receiver = compute_worst_case_inteference(points, alpha)
#         if maxinterf < currentmin:
#             currentmin = maxinterf
#             currentangle = angles
#             print("\n\n currentmin: ", currentmin, "\n angles: ", angles)
        
    
    
    

# angles = [0, 72, 144, 216, 288]
# points = convert_angles_to_points(angles)
# maxinterf, receiver = compute_worst_case_inteference(points, alpha)
# print(maxinterf, receiver)

# minvalue = conj_min_interference()
# test(minvalue, alpha)

#=========================

def powerset(iterable):
    """
    powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    """
    xs = list(iterable)
    # note we return an iterator rather than a list
    return chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1))


def isForbidden(W, alpha, beta):
    #input: a set of locations W, path loss exponent alpha, and reception threshold beta
    #return True iff W is forbidden, as per defn in my July 2022 tech rep
    def EuclidDist(si, sj):
        #returns Euclidean distance between stations si and sj
        return math.sqrt((si[0] - sj[0]) ** 2 + (si[1] - sj[1]) ** 2)

    def Energy(W2, s):
        #energy (or interference at s) due to stations in W2
        res = 0
        for w in W2:
            res = res + EuclidDist(w,s) ** (-alpha)
        return res

    for w in W:
        W_minus_w = W[:]
        W_minus_w.remove(w)
        if round(Energy(W_minus_w, w),3) >= beta: #
            # print('\nW=', W, 'w=', w, 'Energy(W minus w, w)=', Energy(W_minus_w, w))
            return True
        
    return False    
            
        
class Hypergraph(object):
    def __init__(self, N):
        #creates an empty hypergraph H=(V,E), where V=[N]
        self.numVertices = N
        self.V = list(range(1, N+1))
        self.E = {}
        #E is stored as a dictionary where E[k] is the list of edges of size k
        for k in range(0, N+1):
            self.E[k] = []
        self.location = {}    
            
    def setLocation(self, i, s):
        #input: a vertex i and a coordinate s
        #sets location i to s
        self.location[i] = s

    def getLocation(self, i):
        #input: a vertex i in [N]
        #returns location of vertex i
        return self.location[i]
        
    def addEdge(self, e):
        #e is a tuple or list of vertices
        #add hyperedge e to the appropriate level set of self.E
        #First sort e and convert to tuple
        edge_tuple = tuple(sorted(list(e)))
        k = len(edge_tuple)
        if max(e) > self.numVertices:
            print("Error!  You are trying to add an edge with endpoint > N.")
        if edge_tuple not in self.E[k]:
            self.E[k].append(edge_tuple)

    def removeEdge(self, e):
        #e is a tuple or list of vertices
        #remove edge e from appropriate level set of self.E
       edge_tuple = tuple(sorted(list(e)))
       k = len(edge_tuple)
       if edge_tuple in self.E[k]:
           self.E[k].remove(edge_tuple)

    def addEdges(self, F):
        #F is a list of edges (each edge is a tuple or list of vertices)
        #add hyperedge e of F to the appropriate level set of self.E
        #First sort e and convert to tuple
        for e in F:
            self.addEdge(e)
            
    def removeSupersetsOf(self, e):
        #Input: a list or tuple e of vertices (e need not be an edge)
        #remove all supersets of e from self.E 
        k = len(e)
        for i in range(k+1, self.numVertices+1):
            if len(self.E[i]) >= 1: # if ith level set is nonempty
                #temp is the elements in ith level set that should be included 
                temp = []   #creating temp b/c don't want to modify a list I'm iterating on
                for f in self.E[i]:
                    if set(e).issubset(set(f)) == False:
                        temp.append(f)
                self.E[i] = temp[:]
    
    def setLevelSet(self, k, F):
        #input: a positive integer k and a list of k-tuples
        #sets the kth level set of hypergraph to be F
        self.E[k] = F[:]
        
    def getEdgesLevelSet(self, k):
        #input: a postive integer k
        #output: the list E[k] of edges of the hypergraph of size k
        return self.E[k]
        
    def isIndependentSet(self, J):
        #input: a subset J of the vertex set [N]
        #output: true iff J does not contain a hyperedge
        k = len(J)
        for i in range(1, k+1):
            for edge in self.E[i]:
                if set(edge).issubset(set(J)):
                    return False
        return True        

    def Delta(self):
        #input: a hypergraph H
        #output: the matrix Delta_ij defined in [LiNegi]
        
        def zeros_matrix(n, m):
            #create and return an all-zeros matrix of size n by m
            A = [[] for i in range(n)]            
            for i in range(n):
                for j in range(m):
                    A[i].append(0)
            return A
    
        N = self.numVertices
        Delta = zeros_matrix(N,N)
        for k in range(0, N+1):
            for e in self.E[k]:
                interfering_pair = itertools.combinations(e, 2)
                for i, j in interfering_pair:
                    Delta[i-1][j-1] = max(Delta[i-1][j-1], 1.0/(len(e)-1))
                    Delta[j-1][i-1] = Delta[i-1][j-1]
        return Delta

    def AdjacencyList(self):
        #returns a dictionary Adj where Adj[i] is the set of neighbors of i
        Adj = {}
        N = self.numVertices
        for i in range(1, N + 1):
            Adj[i] = []
            
        for k in range(0, N+1):
            for e in self.E[k]:
                interfering_pair = itertools.combinations(e, 2)
                for i, j in interfering_pair:
                    if i not in Adj[j]:
                        Adj[j].append(i)
                    if j not in Adj[i]:
                        Adj[i].append(j)
        return Adj                
 
                    
    def interferenceDegree(self):
        #output: the interference degree of the hypergraph (per defn in my TIT paper)
        N = self.numVertices
        
        Delta = self.Delta()
        Adj = self.AdjacencyList()
        
        Delta_p = []    #intermediate results 
        Delta_pp = []   #intermediate results 
        
        res = 0
        for i in range(1, N+1):
            #find set Hi of all edges containing i, and compute Delta_i
            Delta_i_p = 0   #p for prime. Initialize b/c max over empty set is zero
            Delta_i_pp = 0  #pp for double prime (see my TIT paper)
            subsetsNi = powerset(Adj[i])
            for K in subsetsNi:  #for each J in Ni \int I(H)
                J = list(K) 
                if len(J) >= 1 and self.isIndependentSet(J):
                    s = 0
                    for j in J:
                        s += Delta[i-1][j-1]
                    Delta_i_p = max(Delta_i_p, s)
                L = [i]
                
                if len(J) >= 1 and self.isIndependentSet(set(J).union(set(L))):
                    s = 1
                    for j in J:
                        s += Delta[i-1][j-1]
                    Delta_i_pp = max(Delta_i_pp, s)
                    
            res = max(res, Delta_i_p, Delta_i_pp)
            Delta_p.append( Delta_i_p)
            Delta_pp.append( Delta_i_pp)
        print("Delta_p: ", Delta_p)    
        print("Delta_pp: ", Delta_pp)
        return res


    def printEdges(self):
        #prints the list of edges of the hypergraph, started with lowest level sets
        edgeList = []
        for k in range(0, self.numVertices+1):
            edgeList = edgeList + self.E[k]
        print(edgeList)    
    
    def getNumEdges(self):
        res = 0
        for i in range(self.numVertices+1):
            res = res + len(self.E[i])
        return res
            
    def printLevelSets(self):
        #prints the list of edges of the hypergraph, in order of size (ie by level sets)
        print("The hyperedges are: ")
        for k in range(self.numVertices, -1, -1):
            print("level", k, ":", self.E[k])
            
def GenerateHypergraph(S, alpha, beta):
    #input: a wireles network <S,alpha,beta>, as per my July'22 tech rep
    #output: the hypergraph H=(V,E) generated by the wireless network
    #Here, V is [N] and E is the family of minimal forbidden sets
    #S = a list of 2-tuples, each 2-tuple being the location of a station
    N = len(S)     
    H = Hypergraph(N)  #create empty hypergraph
    for i in range(N):
        H.setLocation(i+1, S[i])
        
    #add level sets 2 to N (and will later remove elements to get MFS)
    for k in range(2, N+1):
        H.addEdges(itertools.combinations(range(1,N+1), k))
        
    #remove subsets so that only minimal forbidden sets remain in H.E
    for k in range(2, N+1):
        temp = [] #don't want to iterate over an object I'm modifying   
        
        for W in H.getEdgesLevelSet(k):
            stationsW = [H.getLocation(w) for w in W] #converts indices to locations
            if isForbidden(stationsW, alpha, beta):
                #know W is also minimal forbidden (not just forbidden), since we started with smallest k first
                #so add W as hyperedge
                temp.append(W)
                H.removeSupersetsOf(W)
        H.setLevelSet(k, temp)
        
                
        
    return H
            
#===================================================
# debug = 1
# import math

# #confirm hand calculations in my notes 2G.(2)
# #edge set is [[1,2],[1,2,3],[1,2,4],..,[1,2,n]]
# alpha = 3
# beta = 1
# s0 = (0, 0)
# S = [s0]
# for i in range(5):
#     angleDegree = 72*i
#     angleRad = angleDegree * math.pi / 180
#     loc = (math.cos(angleRad), math.sin(angleRad))
#     S.append(loc)
# H = GenerateHypergraph(S, alpha, beta)
# H.printLevelSets()
# print("sigma(H) = ", H.interferenceDegree())
# print("Number of hyperedges = ", H.getNumEdges() )
