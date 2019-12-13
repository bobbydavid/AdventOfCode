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

Point = collections.namedtuple('Point', ['x', 'y'])

class Grid:
  def __init__(self, rows, columns):
    self.rows = rows
    self.columns = columns
    self.grid = []
    for y in range(rows):
      self.grid.append([0] * columns)
    print 'Initialized grid with: ', len(self.grid), ' rows X ', len(self.grid[0]), ' columns'

  def set(self, point, value):
    self.grid[point.y][point.x] = value
  
  def get(self, point):
    return self.grid[point.y][point.x]

  def render(self):
    blocks = {0: ' ',
              1: '|',
              2: '#',
              3: '_',
              4: '*'}
    for y in self.grid:
      print ''.join([blocks[x] for x in y])
    print '\n'

class ArcadeGame:
  def __init__(self, intcode, columns, rows):
    self.computer = Computer(intcode, self, self)
    self.board = Grid(rows, columns)
    self.input_buffer = []
    self.mutex = False
    self.tiles_of_type = {} # maps tiles to points where they live
    self.score = 0
    self.bar = None
    self.ball = None
  
  def get(self):
    if self.bar and self.ball:
      self.board.render()
      if self.bar.x > self.ball.x:
        return -1
      if self.bar.x < self.ball.x:
        return 1
    return 0
  
  def put(self, value):
    while self.mutex:
      time.sleep(0.1)

    self.mutex = True
    self.input_buffer.append(value)
    if len(self.input_buffer) == 3:
      value = self.input_buffer.pop()
      y = self.input_buffer.pop()
      x = self.input_buffer.pop()
      if x == -1 and y == 0:
        self.score = value
      else:
        p = Point(x, y)
        self.board.set(p, value)
        if value == 3:
          self.bar = p
        if value == 4:
          self.ball = p
        self.tiles_of_type[value] = self.tiles_of_type.get(value, [])
        self.tiles_of_type[value].append(p)
    self.mutex = False
  
  def run(self):
    self.computer.start()
    self.computer.join()

  def get_num_tiles(self, tile):
    return len(self.tiles_of_type[tile])
  
  def get_score(self):
    return self.score

def main():
  if (len(sys.argv) < 2):
    print 'Missing data file!'
    print 'Usage: python [script] [data]'
    sys.exit(1)

  f = open(sys.argv[1])
  intcode = [int(x) for x in f.read().split(',')]
  f.close()

  rows = int(sys.argv[2])
  cols = int(sys.argv[3])
  # (b) set address 0 to 2 to play for free...
  intcode[0] = 2
  game = ArcadeGame(intcode, rows, cols)
  print 'Initialized game.'
  game.run()
  # (a) ==> 173
  print 'Blocks: ', game.get_num_tiles(2)

  # (b) ===> 8942
  print 'Score: ', game.get_score()
      
    

    
if __name__== "__main__":
  main()
