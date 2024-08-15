#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 15:08:42 2023

@author: ashwinganesan

The program below reproduces the results in the paper 
https://arxiv.org/pdf/2207.00515 (preprint of a manuscript 
submitted to IEEE Transactions on Mobile Computing in December 2023).

More specifically, in this manuscript, an Algorithm 1 is given, 
which uses bisection search to determine the transition values 
of the path loss exponent gamma. Let Uk denote a set of k 
wireless stations placed uniformly on the unit circle.  
The manuscript mentions that as per computer simulations, 
the smallest value of the path loss exponent gamma for which 
U3 is feasible is 1.262, U4 is feasible is 2.543, and U5 is 
feasible is 4.856.  These results can be reproduced by 
running the program below, for which the output obtained is:

===Output===

The smallest value of the path loss exponent gamma such that
U_3 is feasible is 
gamma =  1.26312255859375

The smallest value of the path loss exponent gamma such that
U_4 is feasible is 
gamma =  2.54412841796875

The smallest value of the path loss exponent gamma such that
U_5 is feasible is 
gamma =  4.85784912109375

===End of Output===
"""

#import hypergraph_wireless01.py
from hypergraph_wireless import *

#confirm hand calculations in my notes 2G.(2)
#edge set is [[1,2],[1,2,3],[1,2,4],..,[1,2,n]]
# alpha = 4
# beta = 1
# s0 = (0, 0)

def is_Ur_feasible(alpha, r, beta = 1):
    #input: alpha is path loss exponent, r is a positive integer
    #Ur = r points uniformly placed on unit circle
    #return True iff Ur is feasible
    S = uniformly_on_circle(r)
    H = GenerateHypergraph(S, alpha, beta)
    m = H.getNumEdges()
    if m >= 1:   #then there exists a forbidden set
        return False
    else:
        return True
    
def smallest_alpha_Ur_is_feasible(r=5, low = 4, high = 5):
    #output:=smallest alpha such that Ur is feasible

    #use bisection search
    mid = (low + high) / 2
    tolerance = 0.001   #for alpha value
    while abs(mid-low) > 0.001:
        #print(mid)
        #do another iteration of bisection search
        if is_Ur_feasible(mid, r) == True:
            #print("Ur is feasible when alpha =", mid)
            high = mid
        else:
            #print("Ur is not feasible when alpha =", mid)
            low = mid
        mid = (low + high) / 2
            
    return mid

for k in range(3, 6):   
    print("\nThe smallest value of the path loss exponent gamma such that")
    print("U_" + str(k) + " is feasible is ")
    print("gamma = ", smallest_alpha_Ur_is_feasible(k, 1, 10))
#print('\nNow allow alpha<1.\n')
#print(smallest_alpha_Ur_is_feasible(2, 0, 10))