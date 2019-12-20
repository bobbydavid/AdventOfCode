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

Point = collections.namedtuple('Point',['x','y'])

class Grid:
  def __init__(self, rows, columns):
    self.rows = rows
    self.columns = columns
    self.grid = []
    for y in range(rows):
      self.grid.append(['.'] * columns)
    print 'Initialized grid with:', len(self.grid), 'rows X', len(self.grid[0]), 'columns'

  def set(self, point, value):
    self.grid[point.y][point.x] = value
  
  def get(self, point):
    if point.y >= self.rows or point.y < 0 or point.x >= self.columns or point.x<0:
      return '.'
    return self.grid[point.y][point.x]

  def find(self, char):
    for y in range(self.rows):
      for x in range(self.columns):
        p = Point(x, y)
        if self.get(p) == char:
          return p

  def count(self, char):
    counter = 0
    for y in self.grid:
      for x in y:
        if x == char:
          counter +=1
    return counter

  def render(self):
    _ = system('clear')
    for y in self.grid:
      print ''.join(y)

# Part A
def test_point(intcode, x, y, grid=None):
  computer = Computer(intcode, Queue(), Queue())
  computer.start()
  in_q = computer.InputQueue()
  out_q = computer.OutputQueue()
  in_q.put(x)
  in_q.put(y)

  pull = out_q.get()
  computer.join()
  if pull:
    if grid:
      grid.set(Point(x,y), '#')
  return pull

def trace_beam(intcode, gridsize):
  grid = Grid(gridsize, gridsize)
  counter = 0
  for y in range(grid.rows):
    for x in range(grid.columns):
      counter += test_point(intcode, x, y, grid)
  grid.render()
  return counter, grid

# Part B
def test_ship(intcode, x, y, size):
  # Top right
  pull1 = test_point(intcode, x + size - 1, y)
  # Bottom left
  pull2 = test_point(intcode, x, y + size - 1)
  return bool(pull1 and pull2)
  
def search_x_y(intcode, start_y, range_y, size, top_mul, bottom_mul):
  # If both top right and bottom left corners are in the beam, the ship is in the beam.
  for y in range(start_y, start_y + range_y):
    # Search inside the beam.
    for x in range(bottom_mul*y, top_mul*y):
      if test_ship(intcode, x, y, size):
        return True, x, y
  return False, x, y

def get_line_equations(grid):
  ys = []
  # Make it somewhere in the middle.
  x = grid.columns / 2
  for y in range(grid.rows):
    p = Point(x, y)
    if grid.get(p) == '#':
      ys.append(y)

  top_mul = int(math.ceil(float(x)/min(ys)))
  bottom_mul = int(math.floor(float(x)/max(ys)))
  return top_mul, bottom_mul

def chksum(x, y):
  return x * 10000 + y

def main():
  #TestB()
  #sys.exit(0)
  if (len(sys.argv) < 2):
    print 'Missing data file!'
    print 'Usage: python [script] [data]'
    sys.exit(1)

  f = open(sys.argv[1])
  intcode = [int(x) for x in f.read().split(',')]
  f.close()
  
  
  # (a) == > 152
  affected, grid = trace_beam(intcode, 50)
  print 'Sum of points affected by beam:', affected
  
  # For a given row, where is x that's mostly in the beam.
  top_mul, bottom_mul = get_line_equations(grid)
  
  print 'To be in the beam, X maintains:', top_mul, '* y > x > y *', bottom_mul
  # (b) ==> 10730411  (since y is 411)
  found, x,y = search_x_y(intcode, start_y=400, range_y=50,
                          size=100, top_mul=top_mul, bottom_mul=bottom_mul)
  if found:
    print 'Result: ', chksum(x,y)
  else:
    print 'Not found :/ '
    

if __name__== "__main__":
  main()
