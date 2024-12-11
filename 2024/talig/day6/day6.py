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

  def max(self, n):
    return Point(max(self.x, n.x), max(self.y, n.y))

  def min(self, n):
    return Point(min(self.x, n.x), min(self.y, n.y))

SIGNS = ['^', '>','v','<']
# up, right, down, left
STEPS = [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]
 
OBSTACLES = set(['#','O'])
VISITED = 'X'

class Board():

  def __init__(self, lines):
    self.board = []
    for line in lines:
      line = line.strip()
      self.board.append([x for x in list(line)])

    self.findGuard()
    self.visited = 1
    self.turns = {'rows': {}, 'cols': {}}
    self.turnsOrder = set()
    self.bottomRight = Point(0,0)
    self.topLeft = Point(len(self.board), len(self.board[0]))

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
    # if this point is already in the list and in the same direction, we have a loop
    if (p, self.guard) in self.turnsOrder:
      return True
    self.turnsOrder.add((p, self.guard))
    return False

  def isVisited(self, n):
    return self.get(n) in VISITED

  def isOutOfRange(self, n):
    return n.y < 0 or n.x < 0 or n.y >= len(self.board) or n.x >= len(self.board[0])

  def updateBox(self,n):
    self.topLeft = self.topLeft.min(n.add(Point(-1,-1)))
    self.bottomRight = self.bottomRight.max(n.add(Point(1,1)))

  def advanceOne(self):
    isLoop = False
    n = self.guard_location.add(STEPS[self.guard])
    if self.isOutOfRange(n):
      return False, isLoop
    if self.isObstacle(n):
      isLoop = self.turnRight()
      return True, isLoop
    return self.visit(self.guard_location, n), isLoop

  def isObstacle(self, p):
    return self.get(p) in OBSTACLES

  def visit(self,p, n):
    if not self.isVisited(n):
      self.visited += 1
    self.board[p.y][p.x] = VISITED
    self.board[n.y][n.x] = SIGNS[self.guard]
    self.updateBox(n)
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
  if not board.isObstacle(p) and not p == board.guard_location: 
    board.board[row][col] = 'O'
    inBounds, loop = board.advanceOne()
    while inBounds and not loop:
      inBounds, loop = board.advanceOne()
  return loop

def bruteforce(board, tl, br):
  options = []
  reset = deepcopy(board)
  for row in range(len(board.board)):
    for col in range(len(board.board[0])):
      b = deepcopy(board)
      loop = addObstacle(b, row, col)
      if loop:
        options.append(Point(row, col))
        reset.board[row][col] = 'O'
  return options, reset

def traverse(board):
  noor, _ = board.advanceOne()
  while noor:
    noor, _ = board.advanceOne()
    continue
  
 
def main():
  f = open(sys.argv[1])
  b = Board(f.readlines())
  f.close()
  reset = deepcopy(b)
  traverse(b)
  #print(reset)
  
  print("Result part1:", b.countVisited())
  # Part 2:
  options, obsts = bruteforce(reset, b.topLeft, b.bottomRight)
  print("Result part2:", len(options))
  # Result part2: 1703




if __name__=="__main__":
  main()
