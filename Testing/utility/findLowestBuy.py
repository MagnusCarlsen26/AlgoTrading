'''

Input  : Order-book without Time stamp.
Output : Index for Buying , Quantity Available for Buying , Price of Buying

'''
import numpy as np

def findLowestBuy(lst):
    nonzero_indices = np.nonzero(lst)[0] 
    if nonzero_indices.size > 0:  
        lowest_index = nonzero_indices[0] 
        return lowest_index, lst[lowest_index], (lowest_index + 1) / 2
    else:
        return -1, 0, 0 

