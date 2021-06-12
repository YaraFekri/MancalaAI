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

def alphabeta(currentgame, depth, alpha, beta, MinorMax, steal):
    global num_of_nodes
    if depth == 0 or final(currentgame) != 0:
        hursvalue = heuristic(currentgame)
        verbose['NumofLeaf'] += 1
        verbose['values'].append(hursvalue)
        return hursvalue, -1
    if MinorMax:
        v = -1000
        move = -1
        for m in range(7, 13, 1):
            num_of_nodes +=1
            if currentgame[m] == 0: continue
            a = currentgame[:]
            minormax = movegame(a, m, steal)
            newv, _ = alphabeta(a, depth - 1, alpha, beta, minormax, steal)
            if v < newv:
                move = m
                v = newv
            alpha = max(alpha, v)
            if alpha >= beta:
                verbose['numofCut'] += 1
                verbose['levels'].append(depth)
                break
        return v, move
    else:
        v = 1000
        move = -1
        for n in range(0, 6, 1):
            if currentgame[n] == 0: continue
            a = currentgame[:]
            minormax = movegame(a, n, steal);
            num_of_nodes +=1
            newv, _ = alphabeta(a, depth - 1, alpha, beta, not minormax, steal)
            if v > newv:
                move = n
                v = newv
            beta = min(beta, v)
            if alpha >= beta:
                verbose['numofCut'] += 1
                verbose['levels'].append(depth)
                break
        return v, move
loop1=1
Newgame = [0 for i in range(14)]
for i in range(0, 6, 1): Newgame[i] = 4
for i in range(7, 13, 1): Newgame[i] = 4
delete_verbose()

while True:
    try:
        resume = input("New game or Resume ? 0:Newgame, 1:Resume\n")
        if resume.isdigit():
            resume = int(resume)
        else:
            raise ValueError()
        if resume==0:
            break
        if resume==1:
            try:
                if(path.exists("save.txt")):
                    filesize = os.path.getsize("save.txt")            
                    if filesize == 0:
                        print("the file is empty")
                        resume = input("Enter the value 0 for a new game \n")
                    elif filesize!=0:
                        break
                else:
                    raise ValueError()
            except ValueError:
                print("There is no saved game, you will now play a new game")
                resume=0
                loop1=0
        raise ValueError()
    except ValueError:
        if loop1==1 and resume!=0 and resume!=1:
            print("Input must be 0 or 1.\n")
        elif loop1==0:
            break
if resume==1:
    if(path.exists("save.txt")):
        with open('save.txt','rb') as f:
            n,steal,diff=pickle.load(f)
        Newgame = n
        turn = 0
        print('If the result is 0:With Stealing 1:Without Stealing\n',steal)
        print('If the difficulty is 0:easy 1:medium 2:hard\n',diff)
    else:
        print("file does not exit")


elif resume == 0:
    while True:

        try:
            turn = input("Who do you want to start? 0=YOU, 1=BOT\n")
            if turn.isdigit():
                turn = int(turn)
            else:
                raise ValueError()
            if turn == 0 or turn == 1:
                break
            raise ValueError()
        except ValueError:
            print("Input must be 0 or 1.\n")

    while True:
        try:
            steal = input("Do you want stealing? 0=YES, 1=NO\n")
            if steal.isdigit():
                steal = int(steal)
            else:
                raise ValueError()
            if steal == 0 or steal == 1:
                break
            raise ValueError()
        except ValueError:
            print("Input must be 0 or 1.\n")
    
    while True:
        try:
            diff = input("Which difficulty level do you want? 0=easy, 1=medium, 2=hard\n")
            if diff.isdigit():
                diff = int(diff)
                if diff == 0:
                    depth = 4
                elif diff == 1:
                    depth = 8
                elif diff == 2:
                    depth = 12
                verbose['Maxdepth'] = depth
            else:
                raise ValueError()
            if diff == 0 or diff == 1 or diff == 2:
                break
            raise ValueError()
        except ValueError:
            print("Input must be 0 or 1 or 2.\n")
            
diff = int(diff)
if diff == 0:
    depth = 4
elif diff == 1:
    depth = 8
elif diff == 2:
    depth = 12
verbose['Maxdepth'] = depth

i = 1
count = 2
printgame(Newgame)
while (True):
    if final(Newgame):
        whowon = Newgame[13] - Newgame[6]
        break

    while (turn == 1):
        if final(Newgame):
            whowon = Newgame[13] - Newgame[6]
            break
        print("MY TURN ")
        _, k = alphabeta(Newgame, depth, -1000, 1000, True, steal)
        print('I choose to move pit number ', k)
        t = movegame(Newgame, k, steal)
        printgame(Newgame)
        storeVerbose(i)
        i += 1
        if (not t):
            turn = 0
            break
    
    while (turn == 0):
        if final(Newgame):
            break
        while (turn == 0):
            try:
                save = input("Do you want to save the game? 0:NO 1:YES.\n ")
                if save.isdigit():
                    save = int(save)
                else:
                    raise ValueError()
                if save == 0 or save == 1:
                    break
                raise ValueError()
            except ValueError:
                print("Input must be 0 or 1.\n")
        if save == 1:
            with open("save.txt", "wb") as f:
                pickle.dump([Newgame, steal, diff], f)
            sys.exit()
        else:
            while (turn == 0):
                try:
                    h = input("YOUR TURN\nYou choose pit number:")
                    if h.isdigit():
                        h = int(h)
                    else:
                        raise ValueError()
                    if h == 0 or h == 1 or h == 2 or h == 3 or h == 4 or h == 5:
                        break
                    raise ValueError()
                except ValueError:
                    print("You must choose one of your own pits")
            if h > 5 or Newgame[h] == 0:
                print('you can\'t play')
                break
            t = movegame(Newgame, h, steal)
            printgame(Newgame)
            if (not t):
                turn = 1
                break

printgame(Newgame)
if (whowon > 0):
    print('I WIN. HA HA')
elif (whowon < 0):
    print('You won..')
elif (whowon == 0):
    print('Its a Tie')



