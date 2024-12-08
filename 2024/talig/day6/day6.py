import sys
import math
import time
import os


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


SIGNS = ['^', '>','v','<']
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
    self.turns = []
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
    self.turns.append(self.guard_location)
    self.just_turned = True
    if self.mark == '|': 
      self.mark = '-'
    else:
      self.mark = '|'

  def isVisited(self, n):
    return self.get(n) in VISITED

  def isOutOfRange(self, n):
    return n.y < 0 or n.x < 0 or n.y >= len(self.board) or n.x >= len(self.board[0])

  def advanceOne(self):
    n = self.guard_location.add(STEPS[self.guard])
    if not self.isOutOfRange(n) and self.isObstacle(n):
      self.turnRight()
      n = self.guard_location.add(STEPS[self.guard])

    if self.isOutOfRange(n):
      return False
    return self.visit(self.guard_location, n)   

  def isObstacle(self, p):
    return self.get(p) == '#' # 'O']

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
     
def traverse(board):
  cont = True
  while board.advanceOne():
    continue

  
def main():
  f = open(sys.argv[1])
  b = Board(f.readlines())
  f.close()
  traverse(b)
  print(b)
  
  
  print("Result part1:", b.countVisited())
  #print("Result part2:", total2)


if __name__=="__main__":
  main()
