import sys
import math
import time
import os
from copy import deepcopy


class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def add(self, p):
    return Point(self.x + p.x, self.y + p.y)

  def mul(self, times):
    return Point(self.x * times, self.y * times)

  def __str__(self):
    return "(" + str(self.x) + ", " + str(self.y) + ")"

  def __hash__(self):
    return (self.x, self.y).__hash__()

  def __repr__(self):
    return self.__str__()

  def sub(self, p):
    return Point(self.x - p.x, self.y - p.y)

  def __eq__(self, p):
    return self.x == p.x and self.y == p.y

  def between(self, a, b):
    if a.x == b.x:
      if a.y> b.y:
        return self.y> b.y and self.y < a.y
      elif a.y < b.y:
        return self.y< b.y and self.y > a.y
    elif a.y == b.y:
      if a.x> b.x:
        return self.x> b.x and self.x < a.x
      elif a.x < b.x:
        return self.x< b.x and self.x > a.x
    return False


SIGNS = ['^', '>','v','<']
# up, right, down, left
STEPS = [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]
 
    
VISITED = set(['X', '|','-','+'])

class Board():

  def __init__(self, lines):
    self.board = []
    for line in lines:
      line = line.strip()
      self.board.append([x for x in list(line)])

    self.findGuard()
    self.visited = 1
    self.turns = {'rows': {}, 'cols': {}}
    self.turnsOrder = []
    self.mark = '|'
    self.just_turned = False

  def findGuard(self):
    for r in range(len(self.board)):
      for c in range(len(self.board[0])):
        if self.board[r][c] in SIGNS:
          self.guard_location = Point(c, r)
          self.guard = SIGNS.index(self.board[r][c])
   
  def get(self, p):
    return self.board[p.y][p.x]

  def turnRight(self):
    self.guard = (self.guard + 1) % len(SIGNS) 
    p = self.guard_location
    if (p, self.guard) not in self.turnsOrder:
      self.turnsOrder.append((p, self.guard))
    else:
      return True # loop
    self.just_turned = True
    if self.mark == '|': 
      self.mark = '-'
    else:
      self.mark = '|'
    return False

  def isVisited(self, n):
    return self.get(n) in VISITED

  def isOutOfRange(self, n):
    return n.y < 0 or n.x < 0 or n.y >= len(self.board) or n.x >= len(self.board[0])

  def advanceOne(self):
    isLoop = False
    n = self.guard_location.add(STEPS[self.guard])
    if not self.isOutOfRange(n) and self.isObstacle(n):
      isLoop = self.turnRight()
      n = self.guard_location.add(STEPS[self.guard])

    if self.isOutOfRange(n) or isLoop:
      return False, isLoop
    return self.visit(self.guard_location, n), isLoop

  def isObstacle(self, p):
    return self.get(p) in  ['#', 'O']

  def visit(self,p, n):
    if not self.isVisited(n):
      self.visited += 1
    sign = self.mark
    if self.just_turned:
      sign = '+'
      self.just_turned = False
    self.board[p.y][p.x] = sign
    self.board[n.y][n.x] = SIGNS[self.guard]
    self.guard_location = n
    return True

  def countVisited(self):
    return self.visited

  def __str__(self):
    ret = ""
    for r in range(len(self.board)):
      for c in range(len(self.board[0])):
        ret += self.board[r][c]
      ret += '\n'
    ret += "Guard location: " + str(self.guard_location) + '\n'
    ret += "Visited: " + str(self.visited)
    return ret

def addObstacle(board, row, col):
  p = Point(col, row)
  loop = False
  if not board.isObstacle(p): 
    board.board[row][col] = 'O'
    inBounds, loop = board.advanceOne()
    while inBounds and not loop:
      inBounds, loop = board.advanceOne()
    #if loop:
  return loop

def bruteforce(board):
  options = []
  c = deepcopy(board)
  for row in range(len(board.board)):
    for col in range(len(board.board[0])):
      loop = addObstacle(board, row, col)
      if loop:
        options.append(Point(row, col))
      board = deepcopy(c)
  return options

def traverse(board):
  while board.advanceOne():
    continue
 
def main():
  f = open(sys.argv[1])
  b = Board(f.readlines())
  f.close()
  reset = deepcopy(b)
  #traverse(b)
  print(reset)
  
  
  print("Result part1:", b.countVisited())
  # Part 2:
  options = bruteforce(reset)
  print(options)
  print("Result part2:", len(options))
  # Result part2: 1577 / submit when there's wifi. too low




if __name__=="__main__":
  main()
