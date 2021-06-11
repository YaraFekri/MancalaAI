import os
import pickle
import sys
import os.path
from os import path
num_of_nodes = 0
verbose = {'Maxdepth': 0, 'AverageBF': 0, 'NumofLeaf': 0, 'values': [], 'numofCut': 0, 'levels': []}



def printgame(game):
    for i in range(12, 6, -1):
        print('  ', game[i], '   ', end='')

    print('\n')
    print(game[13], '                                             ', game[6])
    print('\n')

    for i in range(0, 6, 1):
        print('  ', game[i], '   ', end='')
    print('\n')
