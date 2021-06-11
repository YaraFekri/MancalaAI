import os
import pickle
import sys
import os.path
from os import path
num_of_nodes = 0
verbose = {'Maxdepth': 0, 'AverageBF': 0, 'NumofLeaf': 0, 'values': [], 'numofCut': 0, 'levels': []}
def final(game):
    if sum(game[0:6]) == 0:
        game[13] += sum(game[7:13])
        for i in range(14):
            if (i != 13 and i != 6):
                game[i] = 0
        return 1

    elif sum(game[7:13]) == 0:
        game[6] += sum(game[0:6])
        for i in range(14):
            if (i != 13 and i != 6):
                game[i] = 0
        return 2
    else:
        return 0

def printgame(game):
    for i in range(12, 6, -1):
        print('  ', game[i], '   ', end='')

    print('\n')
    print(game[13], '                                             ', game[6])
    print('\n')

    for i in range(0, 6, 1):
        print('  ', game[i], '   ', end='')
    print('\n')
    
def heuristic(game):
    if final(game):
        if game[13] > game[6]:
            return 49
        elif game[13] == game[6]:
            return 0
        else:
            return -49
    else:
        return game[13] - game[6]

def storeVerbose(i):
    try:
        global num_of_nodes
        verbose['AverageBF'] = (verbose['NumofLeaf'] + num_of_nodes)/(num_of_nodes+1)
        verbose_file = open('verbose.txt', 'a')
        verbose_file.write('Turn' + str(i) + ':  ' + str(verbose) + '\n')
        verbose_file.close()
        verbose['AverageBF'] = 0
        verbose['NumofLeaf'] = 0
        verbose['values'].clear()
        verbose['numofCut'] = 0
        verbose['levels'].clear()
        num_of_nodes = 0
    except:
        print("Unable to write to file")
        
def delete_verbose():
    # open file
    f = open("verbose.txt", "w+")

    # absolute file positioning
    f.seek(0)

    # to erase all data
    f.truncate()
    f.close
