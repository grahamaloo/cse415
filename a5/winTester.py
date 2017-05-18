

import new_succ as bcs

def winTester(s):
  possibleWin = "No win"
  black_king_detected = False
  white_king_detected = False
  '''Scan the board looking for any king  
  and return a win for one player if the opponent
  has no king.'''
  b = s.board
  for i in range(8):
    for j in range(8):
      if b[i][j] == bcs.BLACK_KING: black_king_detected = True
      if b[i][j] == bcs.WHITE_KING: white_king_detected = True
  if white_king_detected and not black_king_detected: possibleWin = "Win for WHITE"
  if black_king_detected and not white_king_detected: possibleWin = "Win for BLACK"
  return possibleWin
