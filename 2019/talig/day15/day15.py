import math
import sys
import operator
import copy
from functools import partial
import collections
import itertools
import threading
import time
from Queue import Queue
from computer import Computer
from os import system
import random
import pickle

Point = collections.namedtuple('Point', ['x', 'y'])

class Grid:
  def __init__(self, rows, columns):
    self.rows = rows
    self.columns = columns
    self.grid = []
    for y in range(rows):
      self.grid.append([' '] * columns)
    print 'Initialized grid with: ', len(self.grid), ' rows X ', len(self.grid[0]), ' columns'
    self.empty = 0

  def set(self, point, value):
    c = self.get(point)
    if c in ['o', '#','X']:
      return
    self.grid[point.y][point.x] = value
  
  def get(self, point):
    return self.grid[point.y][point.x]

  def CountEmpty(self):
    self.empty = 0
    for y in self.grid:
      self.empty += y.count('.')
    self.empty += 1 # For the 'D'
    self.empty += 1 # For the 'o'
  
  def GetEmpty(self):
    return self.empty

  def set_next(self, point, value, grid):
    c = self.get(point) # This is the value in the original
    if c in ['#','X']:
      return 0
    if (c in ['.', 'o', 'D']) and value != '.':
      grid[point.y][point.x] = value
      return 1
    return 0

  def set_adjacent(self, p, grid):
    # 4 adjacent points to every point, without diagonals
    c = 'O'
    # Row above
    removed = 0
    removed += self.set_next(Point(p.x,  max(p.y - 1, 0)), c, grid)
    # My row
    removed += self.set_next(Point(max(p.x - 1, 0), p.y), c, grid)
    removed += self.set_next(Point(min(p.x + 1, self.columns), p.y), c, grid)
    # Row below  
    removed += self.set_next(Point(p.x,  min(p.y + 1, self.rows)), c, grid)
    return removed

  def Expand(self):
    grid_copy  = copy.deepcopy(self.grid)
    removed = 0
    # One iteration.
    for y in range(self.rows):
      for x in range(self.columns):
        p = Point(x, y)
        if self.get(p) in ['X','O']:
          removed += self.set_adjacent(p, grid_copy)
    self.grid = grid_copy
    self.empty -= removed

  def render(self):
    _ = system('clear')
    for y in self.grid:
      print ''.join(y)

class Robot:
  def __init__(self, intcode, rows, columns, out_pickle_file=None, in_pickle_file=None):
    self.computer = Computer(intcode, self, self)
    self.c_input = Queue()
    self.c_ouput = Queue()
    # Starts facing up.
    self.current = Point(columns/2, rows/2)
    self.initial = self.current
    self.out_pickle_file = out_pickle_file
    if in_pickle_file:
      self.room = pickle.load(open(in_pickle_file))
    else:
      self.room = Grid(rows, columns)
    self.room.set(self.initial,'o')
    self.last_move = (0, 0)
    self.new_move = 2
    self.move_count = 0
    self.MOVE = {1: (0, -1),
                 2: (0, 1),
                 3: (-1, 0),
                 4: (1, 0)}

  def move(self, move, set_current='.'):
    self.last_move = move
    # Move one step in the new direction
    self.room.set(self.current, set_current)
    self.current = Point(self.current.x + move.x,
                         self.current.y + move.y)
    self.room.set(self.current, 'D')
    self.move_count += 1

  def get(self):
    m = random.randint(1,4)
    x, y = self.MOVE[m]
    self.move(Point(x,y))
    return m

  def save_board_and_exit(self, exit=False):
    f = open(self.out_pickle_file, 'w')
    pickle.dump(self.room, f)
    f.close()
    if exit:
      sys.exit(0)

  def put(self, value):
    status = value
    self.status_2 = 0
    if status == 0:
      # need to restore position, and set the wall.
      self.move(Point(-self.last_move.x, -self.last_move.y), '#')
    elif status == 2:
      self.status_2 += 1
      print 'Found the oxygen system!'
      self.room.set(self.current, 'X')
      if self.out_pickle_file:
        self.save_board_and_exit(False)
    if self.move_count % 100000 == 0:
      self.room.render()
      i = raw_input('Pickle now? Y/n')
      if i == 'Y':
        self.save_board_and_exit(True)

  def run(self):
    self.room.render()
    self.computer.start()
    self.computer.join()

def ASolution():
  # (a) 226 moves.
  return [1, 1, 1, 1, 3, 3, 2, 2, 3, 3, 2, 2, 4, 4, 2, 2, 3, 3, 3, 3,
          1, 1, 1, 1, 3, 3, 3, 3, 2, 2, 2, 2, 4, 4, 2, 2, 3, 3, 2, 2,
          4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 4, 4, 4, 4, 4, 4, 2, 2,
          3, 3, 3, 3, 2, 2, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 3, 3, 2, 2,
          2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 4, 4, 4, 4, 1, 1,
          1, 1, 3, 3, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3, 2, 2,
          2, 2, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 2, 2, 4, 4, 2, 2,
          3, 3, 3, 3, 1, 1, 3, 3, 1, 1, 4, 4, 1, 1, 4, 4, 4, 4, 1, 1,
          3, 3, 1, 1, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 2, 2,
          3, 3, 1, 1, 3, 3, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 2, 2, 3, 3,
          2, 2, 3, 3, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 2, 2,
          4, 4, 4, 4, 4, 4]

def Oxygenize(grid):
  minutes = 0
  # Only need to be called once.
  grid.CountEmpty()
  print grid.GetEmpty()
  while grid.GetEmpty() > 0:
    grid.Expand()
    grid.render()
    time.sleep(0.1)
    minutes += 1
    if (minutes % 1000) == 0:
      print 'Minutes: ', minutes
    
  grid.render()
  print 'Minutes: ', minutes
  

def main():
  if (len(sys.argv) < 5):
    print 'Missing data file!'
    print 'Usage: python [script] [data] [rows] [cols] [pickle] [out]'
    print 'Out is 0 for False'
    sys.exit(1)

  f = open(sys.argv[1])
  intcode = [int(x) for x in f.read().split(',')]
  f.close()

  rows = int(sys.argv[2])
  cols = int(sys.argv[3])
  pickle_f = sys.argv[4]
  out = int(sys.argv[5])
  
  in_pickle = None
  out_pickle = pickle_f
  if not out:
    in_pickle = pickle_f
    out_pickle = None

  robot = Robot(intcode, rows, cols, out_pickle, in_pickle)
  _ = system('clear')
  print 'Initialized robot.'
  i = raw_input('Which part of the puzzle, a/b? > ')
  if i == 'a':
    # Part (a)
    if out:
      robot.run()
    else:
      # Try solution
      i = raw_input('Walk the maze yourself? Y/n')
      if i == 'n':
        moves = ASolution()
        for m in moves:
          robot.room.render()
          x, y = robot.MOVE[m]
          robot.move(Point(x,y))
          time.sleep(0.1)
        print 'We made %d moves!' % len(moves)
        
          
      if i == 'Y':
        while not i == 'Q':
          robot.room.render()
          i = raw_input('1: up, 2: down, 3: left, 4: right, Q: quit>')
          if i == 'Q':
            print 'We made %d moves!' % len(moves)
            print moves
            sys.exit(0)
          else:
            moves.append(int(i))
            x, y = robot.MOVE[int(i)]
            robot.move(Point(x,y))
  elif i == 'b':
    Oxygenize(copy.deepcopy(robot.room))
  
if __name__== "__main__":
  main()
