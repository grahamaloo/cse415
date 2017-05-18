'''TimedGameMaster.py based on GameMaster.py which in turn is
 based on code from RunKInARow.py

S. Tanimoto, May 3
with enhancements by Tyler Williamson eliminating several bugs and
adding better diagnostic printout when an agent makes an error.

'''
VERSION = '1.0-BETA'

# Get names of players and time limit from the command line.

import sys
TIME_PER_MOVE = 25 # default time limit is ten seconds.
if len(sys.argv) > 1:
    import importlib
    player1 = importlib.import_module(sys.argv[1])
    player2 = importlib.import_module(sys.argv[2])
    if len(sys.argv) > 3:
        TIME_PER_MOVE = float(sys.argv[3])
else:
    import Wilham_BC_Player as player1
    import Bobby_BC_Player as player2


# Specify details of a match here:

#import baroque_succ as bcs
import new_succ as bcs

VALIDATE_MOVES = True # If players are trusted not to cheat, this could be turned off to save time.
USE_HTML = False

from winTester import winTester

CURRENT_PLAYER = bcs.WHITE

PLAYER_MAP = (player1.nickname(), player2.nickname())

FINISHED = False
def runGame():
    currentState = bcs.BC_state()
    print('Baroque Chess Gamemaster v'+VERSION)
    print('The Gamemaster says, "Players, introduce yourselves."')
    print('     (Playing WHITE:) '+player1.introduce())
    print('     (Playing BLACK:) '+player2.introduce())

    try:
        p1comment = player1.prepare(player2.nickname())
    except:
        report = 'Player 1 ('+player1.nickname()+' failed to prepare, and loses by default.'
        print(report)
        report = 'Congratulations to Player 2 ('+player2.nickname()+')!'
        print(report)
        return
    try:
        p2comment = player2.prepare(player1.nickname())
    except:
        report = 'Player 2 ('+player2.nickname()+' failed to prepare, and loses by default.'
        print(report)
        report = 'Congratulations to Player 1 ('+player1.nickname()+')!'
        print(report)
        return

    print('The Gamemaster says, "Let\'s Play!"')
    print('The initial state is...')

    currentRemark = "The game is starting."

    WHITEsTurn = True
    name = None
    global FINISHED
    FINISHED = False
    turnCount = 1
    print(currentState)
    while not FINISHED:
        who = currentState.whose_move
        if who==bcs.WHITE:
            side = 'WHITE'
        else:
            side = 'BLACK'
        global CURRENT_PLAYER
        CURRENT_PLAYER = who
        if VALIDATE_MOVES:
            legal_states = bcs.successors(currentState)
            if legal_states==[]:
                print("Stalemate: "+side+" has no moves!"); break
        if WHITEsTurn:
            playerResult = timeout(player1.makeMove,args=(currentState, currentRemark, TIME_PER_MOVE), kwargs={}, timeout_duration=TIME_PER_MOVE, default=(None,"I give up!"));
            name = player1.nickname()
            WHITEsTurn = False
        else:
            playerResult = timeout(player2.makeMove,args=(currentState, currentRemark, TIME_PER_MOVE), kwargs={}, timeout_duration=TIME_PER_MOVE, default=(None,"I give up!"));
            name = player2.nickname()
            WHITEsTurn = True
        moveAndState, currentRemark = playerResult
        if moveAndState==None:
            FINISHED = True; continue
        if VALIDATE_MOVES:
            if not OCCURS_IN(moveAndState[1], legal_states):
                print("Illegal move by "+side+" as "+str(moveAndState[0]))
                print("Returned state is:")
                print(moveAndState[1])
                break
        move, currentState = moveAndState
        moveReport = "Turn "+str(turnCount)+": Move is by "+side+" as "+str(move)
        print(moveReport)
        utteranceReport = name +' says: '+currentRemark
        print(utteranceReport)
        possibleWin = winTester(currentState)
        if possibleWin != "No win":
            FINISHED = True
            print(currentState)
            print(possibleWin)
            return
        print(currentState)
        turnCount += 1
        #if turnCount == 9: FINISHED=True
    print(currentState)
    print("Game over.")


import sys
import time
from traceback import print_exc
def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
    '''This function will spawn a thread and run the given function using the args, kwargs and
    return the given default value if the timeout_duration is exceeded
    '''
    import threading
    class PlayerThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = default
        def run(self):
            try:
                self.result = func(*args, **kwargs)
            except:
                print("Seems there was a problem with the time.")
                print_exc()
                self.result = default

    pt = PlayerThread()
    #print("timeout_duration = "+str(timeout_duration))
    pt.start()
    started_at = time.time()
    #print("makeMove started at: " + str(started_at))
    pt.join(timeout_duration)
    ended_at = time.time()
    #print("makeMove ended at: " + str(ended_at))
    diff = ended_at - started_at
    print("Time used in makeMove: %0.4f seconds out of " % diff, timeout_duration)
    if pt.isAlive():
        print("Took too long.")
        print("We are now terminating the game.")
        print("Player "+PLAYER_MAP[CURRENT_PLAYER]+" loses.")
        if USE_HTML: gameToHTML.reportResult("Player "+PLAYER_MAP[CURRENT_PLAYER]+" took too long (%04f seconds) and thus loses." % diff)
        if USE_HTML: gameToHTML.endHTML()
        exit()
    else:
        print("Within the time limit -- nice!")
        return pt.result


def OCCURS_IN(state, listOfStates):
  for s in listOfStates:
    if DEEP_EQUALS(state, s):
        return True
  return False

def DEEP_EQUALS(s1, s2):
  if s1.whose_move != s2.whose_move:
    return False
  b1 = s1.board
  b2 = s2.board
  for i in range(8):
    for j in range(8):
      if b1[i][j] != b2[i][j]: return False
  return True

runGame()
