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
    
def movegame(borad_mancala, num_pit, stealing):
    num_seed = 0
    another_turn = False
    num_pit_sent = num_pit
    
    if num_pit_sent < 6:
        num_seed = borad_mancala[num_pit]
        borad_mancala[num_pit] = 0
        while (num_seed != 0):
            num_pit += 1
            num_pit = num_pit % 14
            if num_pit == 13:
                continue
            borad_mancala[num_pit] += 1
            num_seed -= 1
            
            if (borad_mancala[num_pit] == 1 and borad_mancala[
                -num_pit + 12] != 0 and num_pit != 6 and num_seed == 0 and stealing == 0 and num_pit < 6):
                
                borad_mancala[6] += borad_mancala[num_pit] + borad_mancala[-num_pit + 12]
                borad_mancala[num_pit] = 0
                borad_mancala[-num_pit + 12] = 0
                
            if (num_pit == 6 and num_seed == 0):
                another_turn = True
    
    if num_pit_sent > 6:
        num_seed = borad_mancala[num_pit]
        borad_mancala[num_pit] = 0
        while (num_seed != 0):
            num_pit += 1
            num_pit = num_pit % 14
            if num_pit == 6:
                continue
            borad_mancala[num_pit] += 1
            num_seed -= 1
            
            if (borad_mancala[num_pit] == 1 and borad_mancala[
                5 - (num_pit - 7)] != 0 and num_pit != 13 and num_seed == 0 and stealing == 0 and num_pit > 6):
                borad_mancala[13] += borad_mancala[num_pit] + borad_mancala[5 - (num_pit - 7)]
                borad_mancala[num_pit] = 0
                borad_mancala[5 - (num_pit - 7)] = 0
                
            if (num_pit == 13 and num_seed == 0):
                another_turn = True
    return another_turn
