'''TestAgent1.py
Nobachess, implementation of an agent that can't play
Baroque Chess.

'''
import time
from datetime import datetime, timedelta
import math
import heapq
import random

# GLOBAL VARIABLES
BEST_STATE = None
TIME_LIMIT_OFFSET = 0.1

BLACK = 0
WHITE = 1

INIT_TO_CODE = {'p': 2, 'P': 3, 'c': 4, 'C': 5, 'l': 6, 'L': 7, 'i': 8, 'I': 9,
                'w': 10, 'W': 11, 'k': 12, 'K': 13, 'f': 14, 'F': 15, '-': 0}

CODE_TO_INIT = {0: '-', 2: 'p', 3: 'P', 4: 'c', 5: 'C', 6: 'l', 7: 'L', 8: 'i', 9: 'I',
                10: 'w', 11: 'W', 12: 'k', 13: 'K', 14: 'f', 15: 'F'}

PIECE_VALS = [0,0,-1,1,-2,2,-2,2,-3,3,-8,8,-100,100,-2,2]

PAST_MOVE = [-1, -1, -1] # Piece, x, y

# initialize zobrist table
ZOBRIST_N = []
ZOBRIST_M = {}
random.seed(0)
for x in range(64):
    ZOBRIST_N.append([])
    for y in range(16):
        ZOBRIST_N[x].append(random.randint(0, 2**64))


class z_node:
    def __init__(self, state):
        self.state = state
        self.children = []

def makeMove(currentState, currentRemark, timelimit):
    now = datetime.now()
    global BEST_STATE
    newMoveDesc = 'I moved!'
    newRemark = "Your turn!"

    # search for 10 seconds
    c_state = State(currentState.board, currentState.whose_move)
    best = iter_deep_search(c_state, now + timedelta(0,timelimit))

    return [[newMoveDesc, best], newRemark]


def nickname():
    return "Bobby F."


def introduce():
    return "I'm an android named Bobby."

def prepare(player2Nickname):
    pass


piece_vals = [0,0,-1,1,-2,2,-2,2,-3,3,-8,8,-100,100,-2,2]

def static_eval(state):
    return sum([sum([piece_vals[j] for j in i]) for i in state.board])


def save_last_move(parent, child):
    p_board = parent.board
    c_board = child.board
    for x in range(0, len(p_board)):
        for y in range(0, len(p_board)):
            if c_board[x][y] != p_board[x][y] and c_board[x][y] == 0\
                    and who(p_board[x][y]) == parent.whose_move:
                PAST_MOVE[0] = p_board[x][y]
                PAST_MOVE[1] = x
                PAST_MOVE[2] = y


def iter_deep_search(currentState, endTime):
    depth = 0
    best = None
    while datetime.now() < endTime:
        depth += 1
        # print("depth", depth)

        # whether to minimize or maximize
        opt = -1 if currentState.whose_move == BLACK else 1
        best_state = minimax(currentState, depth, opt, endTime)
        # print("***************BEST STATE*************")
        # print(best_state)

        if best_state != None:
            best = best_state
        else:
            break


    # TODO: Remove if too intensive
    #save_last_move(currentState, best)

    return best

def is_over_time(endTime):
    global TIME_LIMIT_OFFSET
    now = datetime.now()
    return (now + timedelta(0, TIME_LIMIT_OFFSET)) >= endTime

def minimax_helper(state, depth, opt, endTime, alpha, beta):
    global ZOBRIST_M

    # Time check
    if is_over_time(endTime):
        return None

    # base case
    if depth == 0:
        state.static_eval()
        return state

    state.static_eval()
    board = state.board
    child_states = []
    s = None
    h = z_hash(board)
    # print(h)
    # print(state)
    time.sleep(0.1)
    try:
        s = ZOBRIST_M[h]
    except:
        s = z_node(state)
    if len(s.children) == 0:
        child_states = get_child_states(state, h)
        for c in child_states:
            h1 = z_hash(c.board)
            # if depth==1: print("pincher", h1)
            s.children.append(h1)
            ZOBRIST_M[h1] = z_node(c)
        ZOBRIST_M[h] = s
    else:
        #print("CHILDREN FOUND")
        for c in s.children:
            #print(ZOBRIST_M[c].state)
            child_states.append(ZOBRIST_M[c].state)

    heapq.heapify(child_states)

    best = None
    best_eval = 0

    while len(child_states) != 0:
        c_state = heapq.heappop(child_states)

        # Time check
        if is_over_time(endTime):
            break

        # check alpha beta for invalid state
        if alpha > beta:
            break

        #print("TESTING")
        new_state = minimax_helper(c_state, depth-1, -opt, endTime,
                alpha, beta)
        if new_state != None:
            new_eval = new_state.eval
        else:
            new_eval = 0

        if best == None:
            best = new_state
            best_eval = new_eval
        elif opt*new_eval >= opt*best_eval:
            best = new_state
            best_eval = new_eval

        if opt == 1:
            # set alpha
            alpha = max(alpha, new_eval)
        else:
            # set beta
            beta = min(beta, new_eval)

    return best

def minimax(state, depth, opt, endTime):


    h = z_hash(state.board)
    child_states = []
    s = None
    try:
        s = ZOBRIST_M[h]
    except:
        s = z_node(state)
    if len(s.children) == 0:
        child_states = get_child_states(state, h)
        for c in child_states:
            h1 = z_hash(c.board)
            s.children.append(h1)
            c.static_eval()
            ZOBRIST_M[h1] = z_node(c)
        ZOBRIST_M[h] = s
    else:
        for c in s.children:
            child_states.append(ZOBRIST_M[c].state)

    heapq.heapify(child_states)

    best = None
    best_eval = 0
    alpha = -math.inf
    beta = math.inf

    while len(child_states) != 0:
        c_state = heapq.heappop(child_states)

        #check time
        if is_over_time(endTime):
            best = None
            break

        if alpha > beta:
            break

        new_state = minimax_helper(c_state, depth - 1, -opt, endTime,
                alpha, beta)

        if new_state != None:
            new_eval = new_state.eval
        else:
            new_eval = 0

        if opt == 1:
            # set alpha
            alpha = max(alpha, new_eval)
        else:
            # set beta
            beta = min(beta, new_eval)

        if best == None or opt*new_eval >= opt*best_eval:
            best = c_state
            best_eval = new_eval

    return best


def get_child_states(state, h):
    board = state.board
    child_states = []
    for x in range(0, len(board)):
        for y in range(0, len(board)):
            # Get current piece number
            piece = board[x][y]
            # if current player is the same color as the piece get all child states
            if piece != 0 and who(piece) == state.whose_move:
                child_states += move(state, h, x, y)

    return child_states

def who(piece): return piece % 2

def parse(bs): # bs is board string
    '''Translate a board string into the list of lists representation.'''
    b = [[0,0,0,0,0,0,0,0] for r in range(8)]
    rs9 = bs.split("\n")
    rs8 = rs9[1:] # eliminate the empty first item.
    for iy in range(8):
        rss = rs8[iy].split(' ');
        for jx in range(8):
            b[iy][jx] = INIT_TO_CODE[rss[jx]]
    return b

INITIAL = parse('''
c l i w k i l f
p p p p p p p p
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
P P P P P P P P
F L I W K I L C
''')

INITIAL_2 = parse('''
k - - - - - - -
- - - - - - - -
- - - - - - p -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - -
- - - - - - - K
''')

INITIAL_3 = parse('''
- - - - - - - -
- - - P - - - -
- - P P P P P -
- P P i - P p P
- - P P P P P -
- - - P - - - -
- - - - - - - -
K - - - - - - k
''')

def king_search(board):
    wKingPiece = None
    bKingPiece = None
    for i in range(0, len(board)):
        for j in range(0, len(board[i])):
            if board[i][j] == INIT_TO_CODE['K']:
                wKingPiece = (i, j)
            elif board[i][j] == INIT_TO_CODE['k']:
                bKingPiece = (i, j)
    return [wKingPiece, bKingPiece]

def freezer_search(board, whose_move):
    frozen = [[],[]]
    for x in range(0, len(board)):
        for y in range(0, len(board[x])):
            if board[x][y] - who(board[x][y]) == INIT_TO_CODE['f']:
                for i, j in vec:
                    if x+i >= 0 and y+j >= 0 and x+i <= 7 and y+j <= 7:
                        frozen[who(board[x][y])].append((x+i, y+j))
    return frozen

def z_hash(board):
    val = 0
    for x in range(8):
        for y in range(8):
            piece = board[x][y]
            if piece != 0:
                val ^= ZOBRIST_N[8*x+y][piece]
    return val

class State:
    def __init__(self, old_board=INITIAL, whose_move=WHITE, kingPos=[], frozen=[]):
        self.whose_move = whose_move;
        self.board = [r[:] for r in old_board]
        if len(kingPos) == 0: self.kingPos = king_search(old_board)
        else: self.kingPos = [(k[0], k[1]) for k in kingPos]
        if len(frozen) == 0: self.frozen = freezer_search(old_board, whose_move)
        else: self.frozen = [[(f[0], f[1]) for f in i] for i in frozen]

        self.eval = None

    def __repr__(self):
        s = ''
        for r in range(8):
            for c in range(8):
                s += CODE_TO_INIT[self.board[r][c]] + " "
            s += "\n"
        if self.whose_move==WHITE: s += "WHITE's move"
        else: s += "BLACK's move"
        s += "\n"
        return s

    def __copy__(self):
        new_state = State(self.board, self.whose_move,
            self.kingPos, self.frozen)
        return new_state

    def __eq__(self, other):
        if isinstance(other, State):
            for i in range(0, len(self.board)):
                if self.board[i] != other.board[i]: return False
            return True
        return False

    def __lt__(self, other):
        if self.whose_move == WHITE:
           lt = static_eval(self) > static_eval(other)
        else:
            lt = static_eval(self) < static_eval(other)
        return lt

    def static_eval(self):
        if self.eval == None:
            self.eval = static_eval(self)
        return self.eval

vec = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1)]

def move(state, zobrist_h, xPos, yPos):
    # if piece is frozen by opponent's freezer
    if (xPos, yPos) in state.frozen[1-state.whose_move]:
        # print("frozen")
        # print(state)
        # print("whose_move", state.whose_move)
        # print(xPos, yPos)
        # print(state.frozen)
        return []
    child_states = []
    # get current piece
    piece = state.board[xPos][yPos]
    piece_t = piece - who(piece)


    # loop through directions
    directions = vec[0:4] if piece_t == INIT_TO_CODE['p'] else vec
    for i, j in directions:
        x = xPos
        y = yPos
        # don't move pieces off the board or into another piece
        while x+i >= 0 and y+j >= 0 and x+i <= 7 and y+j <= 7 \
                and (state.board[x+i][y+j] == 0\
                or piece_t == INIT_TO_CODE["k"]):

            if piece_t != INIT_TO_CODE["k"]:
                x += i
                y += j

            # TODO: Remove if too intensive
            # Should not move the same piece back to the same position
            if piece == PAST_MOVE[0] and x == PAST_MOVE[1] \
                    and y == PAST_MOVE[2] and piece_t != INIT_TO_CODE["k"]:
                continue

            # copy old state move
            c_state = state.__copy__()
            c_state.whose_move = 1 - c_state.whose_move
            # pick up piece for move
            c_state.board[xPos][yPos] = 0
            c_state.board[x][y] = piece
            z_h = zobrist_h
            z_h ^= ZOBRIST_N[8*xPos+yPos][c_state.board[xPos][yPos]]
            z_h ^= ZOBRIST_N[8*x+y][c_state.board[x][y]]
            if piece_t == INIT_TO_CODE['p']:
                child_states.append(pincher_capture(c_state, x, y, z_h))
            # if piece is coordinator
            elif piece_t == INIT_TO_CODE['c']:
                child_states.append(coordinator_capture(c_state, x, y, z_h))
            # if piece is freezer
            elif piece_t == INIT_TO_CODE['f']:
                child_states.append(freezer_capture(c_state, x, y, z_h))
            # if piece is leaper
            elif piece_t == INIT_TO_CODE['l']:
                child_states.append(leaper_capture(c_state, x, y, i, j, z_h))
            # if piece is imitator
            elif piece_t == INIT_TO_CODE['i']:
                child_states.extend(imitator_capture(c_state,x,y,xPos,yPos,i,j,
                    z_h))
            # if piece is withdrawer
            elif piece_t == INIT_TO_CODE['w']:
                child_states.append(withdrawer_capture(c_state, xPos-i, yPos-j,
                    z_h))
            # if piece is king
            elif piece_t == INIT_TO_CODE['k']:
                child_states.append(king_capture(c_state, x, y, x+i, y+j, z_h))
            #if not child_states[-1].__eq__(defense):
                #child_states.append(defense)
            # king only moves one space
            if piece_t == INIT_TO_CODE['k']: break

    return child_states

def pincher_capture(state, x, y, z_h):
    global ZOBRIST_M
    piece = state.board[x][y]
    # search surrounding spaces to look for a capture
    for i, j in vec[0:4]:
        if is_on_board(x, y) and is_on_board(x+i, y+j) and is_on_board(x+2*i, y+2*j)\
                and who(state.board[x+i][y+j]) != who(piece) \
                and state.board[x+2*i][y+2*j] == piece:
            z_h ^= ZOBRIST_N[8*(x+i)+y+j][state.board[x+i][y+j]]
            state.board[x+i][y+j] = 0
    state.static_eval()
    ZOBRIST_M[z_h] = z_node(state)
    # print("pincher hash", z_h)
    return state

def coordinator_capture(state, x, y, z_h):
    global ZOBRIST_M
    kx, ky = state.kingPos[state.whose_move]
    # try to coordinate with king to capture
    if is_on_board(x,y) and is_on_board(x, ky)\
            and who(state.board[x][y]) != who(state.board[x][ky]):
        z_h ^= ZOBRIST_N[8*x+ky][state.board[x][ky]]
        state.board[x][ky] = 0
    if is_on_board(x,y) and is_on_board(kx, y)\
            and who(state.board[x][y]) != who(state.board[kx][y]):
        z_h ^= ZOBRIST_N[8*kx+y][state.board[kx][y]]
        state.board[kx][y] = 0
    state.static_eval()
    ZOBRIST_M[z_h] = z_node(state)
    return state

def freezer_capture(state, x, y, z_h):
    global ZOBRIST_M
    state.frozen[state.whose_move] = []
    for i, j in vec:
        if is_on_board(x+i, y+j):
            state.frozen[state.whose_move].append((x+i,y+j))
    state.static_eval()
    ZOBRIST_M[z_h] = z_node(state)
    return state

def leaper_capture(state, x, y, i, j, z_h):
    global ZOBRIST_M
    if is_on_board(x,y) and is_on_board(x+i, y+j) and is_on_board(x+2*i,y+2*j)\
            and who(state.board[x+i][y+j]) != who(state.board[x][y]) \
            and state.board[x+i][y+j] != 0 and state.board[x+2*i][y+2*j] == 0:
        z_h ^= ZOBRIST_N[8*(x+2*i)+(y+2*j)][state.board[x][y]]
        z_h ^= ZOBRIST_N[8*x+y][state.board[x][y]]
        z_h ^= ZOBRIST_N[8*(x+i)+y+j][state.board[x+i][y+j]]
        state.board[x+2*i][y+2*j] = state.board[x][y]
        state.board[x][y] = 0
        state.board[x+i][y+j] = 0
    state.static_eval()
    ZOBRIST_M[z_h] = z_node(state)
    return state

def imitator_capture(state, x, y, x0, y0, i, j, z_h):
    global ZOBRIST_M

    captures = []
    if is_on_board(x,y):
        # # imitate pincher
        p_cap = state.__copy__()
        for i, j in vec[0:4]:
            if is_on_board(x+i, y+j) and is_on_board(x+2*i, y+2*j)\
                    and state.board[x+i][y+j] - state.whose_move == INIT_TO_CODE['p'] \
                    and state.board[x+2*i][y+2*j] + state.whose_move == INIT_TO_CODE['P']:
                p_cap.board[x+i][y+j] = 0
                captures.append(p_cap)

        # imitate coordinator
        kx, ky = state.kingPos[state.whose_move]
        k_cap = state.__copy__()
        k_bool = False
        if is_on_board(x, ky) \
                and who(state.board[x][y]) != who(state.board[x][ky]) \
                and state.board[x][ky] - state.whose_move == INIT_TO_CODE['c']:
            k_cap.board[x][ky] = 0
            k_bool = True
        if is_on_board(kx, y)\
                and who(state.board[x][y]) != who(state.board[kx][y]) \
                and state.board[kx][y] - state.whose_move == INIT_TO_CODE['c']:
            k_cap.board[kx][y] = 0
            k_bool = True

        if k_bool:
            captures.append(k_cap)

        # imitate freezer
        f_cap = state.__copy__()
        f_bool = False
        for i, j in vec:
            if is_on_board(x+i, y+j):
                if state.board[x+i][y+j] - state.whose_move == INIT_TO_CODE['f']:
                    f_bool = True
                f_cap.frozen[state.whose_move].append((x + i,y + j))
        if f_bool:
            captures.append(f_cap)

        # imitate withdrawer
        w_cap = state.__copy__()
        if is_on_board(x0-i, y0-j)\
                and state.board[x0-i][y0-j] - state.whose_move == INIT_TO_CODE['w']:
            w_cap.board[x0-i][y0-j] = 0
            captures.append(w_cap)


    return captures

def withdrawer_capture(state, x, y, z_h):
    global ZOBRIST_M
    if is_on_board(x, y):
        z_h ^= ZOBRIST_N[8*x+y][state.board[x][y]]
        state.board[x][y] = 0
    state.static_eval()
    ZOBRIST_M[z_h] = z_node(state)
    return state

def king_capture(state, x, y, x1, y1, z_h):
    global ZOBRIST_M
    if is_on_board(x,y) and is_on_board(x1, y1)\
            and who(state.board[x1][y1]) != who(state.board[x][y]) \
            or state.board[x1][y1] == 0:
        if state.board[x1][y1] != 0:
            z_h ^= ZOBRIST_N[8*x1+y1][state.board[x1][y1]]
        z_h ^= ZOBRIST_N[8*x1+y1][state.board[x][y]]
        z_h ^= ZOBRIST_N[8*x+y][state.board[x][y]]
        state.board[x1][y1] = state.board[x][y]
        state.board[x][y] = 0
        state.kingPos[state.whose_move] = (x1, y1)
        state.static_eval()
        ZOBRIST_M[z_h] = z_node(state)
    return state

def is_on_board(x,y):
    return x >= 0 and y >= 0 and x <= 7 and y <= 7

if __name__ == "__main__":
    state = State(old_board=INITIAL_2, whose_move=BLACK)
    print(state)



    now = datetime.now()
    new_state = iter_deep_search(state, now + timedelta(0, 10))

    print(new_state)
