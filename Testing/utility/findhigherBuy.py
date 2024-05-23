'''

Input  : Order-book without Time stamp , Index for Buying , Weights array
Output : Sum of weighted Buy Quantity higher than buy price 

'''
import numpy as np
def findhigherBuy(lst,lowest_index):
    return lst[lowest_index + 1 : lowest_index+6].sum()