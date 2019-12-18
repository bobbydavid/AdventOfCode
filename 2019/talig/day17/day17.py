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
      self.grid.append(['.'] * columns)
    print 'Initialized grid with:', len(self.grid), 'rows X', len(self.grid[0]), 'columns'

  def set(self, point, value):
    self.grid[point.y][point.x] = value
  
  def get(self, point):
    if point.y >= self.rows or point.y < 0 or point.x >= self.columns or point.x<0:
      return '.'
    return self.grid[point.y][point.x]

  def render(self):
    _ = system('clear')
    for y in self.grid:
      for x in y:
        print x,
      print '\n',

def is_intersection(grid, x, y):
  adjacent = []
  if grid.get(Point(x, y)) == '#':
    if x - 1 > 0:
      adjacent.append(grid.get(Point(x - 1, y)))
    if x + 1 < grid.columns - 1:
      adjacent.append(grid.get(Point(x + 1, y)))
    if y - 1 > 0:
      adjacent.append(grid.get(Point(x, y - 1)))
    if y + 1 < grid.rows - 1:
      adjacent.append(grid.get(Point(x, y + 1)))
  return adjacent.count('#') == 4

def mark_intersections(grid):
  intersections = []
  for y in range(grid.rows):
    for x in range(grid.columns):
      if is_intersection(grid, x, y):
        p = Point(x, y) 
        grid.set(p, 'O')
        intersections.append(p)
  return intersections

def sum_alignment(intersections):
  total = 0
  for p in intersections:
    total += p.x * p.y
  return total

def live_feed(computer, grid):
  out_q = computer.OutputQueue()
  cols = 0
  rows = 0
  last_2_chrs = []
  while last_2_chrs != ['\n','\n']:
    c = chr(out_q.get())
    last_2_chrs.append(c)
    if len(last_2_chrs) == 3:
      last_2_chrs.pop(0)
    if c == '\n':
      rows += 1
      cols = 0
    else:
      grid.set(Point(cols, rows), c)
      cols +=1

def get_scaffolding(computer, grid):
  out_q = computer.OutputQueue()
  #_ = system('clear')
  computer.start()
  live_feed(computer, grid)
  grid.render()
  intersections = mark_intersections(grid)
  grid.render()
  alignment = sum_alignment(intersections)
  print 'Sum of alignment params: ', alignment

def walk_scaffolding(computer, grid):
  out_q = computer.OutputQueue()
  in_q = computer.InputQueue()
  main = 'A,C,A,B,A,B,C,B,B,C\n'
  subroutines = {'A' : 'L,4,L,4,L,10,R,4\n',
                 'B' : 'R,4,L,10,R,10\n',
                 'C' : 'R,4,L,4,L,4,R,8,R,10\n'}

  print 'Feeding queues...'
  for x in main:
    in_q.put(ord(x))
  for x in subroutines['A']:
    in_q.put(ord(x))
  for x in subroutines['B']:
    in_q.put(ord(x))
  for x in subroutines['C']:
    in_q.put(ord(x))
  in_q.put(ord('n'))
  in_q.put(ord('\n')) #no feed.
  computer.start()
  while True:
    c = out_q.get()
    if c > 256:
      print 'Output: ', c

def main():
  if (len(sys.argv) < 2):
    print 'Missing data file!'
    print 'Usage: python [script] [data]'
    sys.exit(1)

  f = open(sys.argv[1])
  intcode = [int(x) for x in f.read().split(',')]
  f.close()
  
  computer = Computer(intcode, Queue(), Queue())
  computer.daemon = True
  # Let's see what we have here. 32 rows, 40 cols
  # (A) 3336
  grid = Grid(50, 50)
  get_scaffolding(computer, grid)
  # (B) Walk the scaffolding : 597517
  intcode[0]=2
  computer = Computer(intcode, Queue(), Queue())
  computer.daemon = True
  walk_scaffolding(computer, grid)
 
if __name__== "__main__":
  main()
