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
      self.grid.append(['.'] * columns)
    print 'Initialized grid with: ', len(self.grid), ' rows X ', len(self.grid[0]), ' columns'

  def set(self, point, value):
    self.grid[point.y][point.x] = value
  
  def get(self, point):
    return self.grid[point.y][point.x]

  def render(self):
    for y in self.grid:
      print ''.join(y)

class Robot:
  def __init__(self, intcode, columns, rows):
    self.computer = Computer(intcode, self, self)
    # Starts facing up.
    self.direction = Point(0,-1)
    self.current = Point(columns/2, rows/2)
    self.panels = Grid(rows, columns)
    # Set the starting position to white. (b)
    self.panels.set(self.current, '#')
    self.toggle = False
    self.painted = {} # map points to number of times they were painted.

  def turn(self, direction):
    # Turn left (0, -1) => (-1, 0) => (0, 1) => (1, 0)
    if direction == 0:
      self.direction = Point(self.direction.y, -self.direction.x)
    # Turn right (0, -1) => (1, 0) => (0, 1) => (-1, 0)
    if direction == 1:
      self.direction = Point(-self.direction.y, self.direction.x)
    # Move one step in the new direction
    self.current = Point(self.current.x + self.direction.x,
                         self.current.y + self.direction.y)

  def paint(self, color):
    if not self.painted.has_key(self.current):
      self.painted[self.current] = 0
    self.painted[self.current] += 1
    value = '.' if color == 0 else '#'
    self.panels.set(self.current, value)

  def get(self):
    return 0 if self.panels.get(self.current) == '.' else 1
  
  def put(self, value):
    if self.toggle:
      self.turn(value)
    else:
      self.paint(value)
    self.toggle = not self.toggle
    
  def run(self):
    output = self.computer.OutputQueue()
    self.computer.start()
    self.computer.join()

  def unique_painted(self):
    return len(self.painted.keys())

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
  robot = Robot(intcode, rows, cols)
  print 'Initialized robot.'
  robot.run()
  print 'Printing output panels.'
  robot.panels.render()
  print 'Painted panels: ', robot.unique_painted()
  
if __name__== "__main__":
  main()
