import sys
import functools
import operator
import re
import collections
import copy
import grid
DAY = 11

OCCUPIED = '#'
EMPTY = 'L'

def CreateGrid(lines):
  g = grid.Grid(len(lines), len(lines[0]))
  

def RunRound(lines, last_g):
  # initialize new grid
  new_g = grid.Grid(lines)
  for y in range(last_g.rows):
    for x in range(last_g.columns):
      location = grid.Point(x, y)
      value = last_g.get(location)
      if value == OCCUPIED and last_g.count_neighbors(location, OCCUPIED) >= 4:
        new_g.set(location, EMPTY)
      elif value == EMPTY and last_g.count_neighbors(location, OCCUPIED) == 0:
        new_g.set(location, OCCUPIED)
      else:
        new_g.set(location, value)
  #new_g.render()
  return new_g

def RunRound2(lines, last_g):
  # initialize new grid
  new_g = grid.Grid(lines)
  for y in range(last_g.rows):
    for x in range(last_g.columns):
      location = grid.Point(x, y)
      value = last_g.get(location)
      if value == OCCUPIED and last_g.count_visible_seats(location, OCCUPIED) >= 5:
        new_g.set(location, EMPTY)
      elif value == EMPTY and last_g.count_visible_seats(location, OCCUPIED) == 0:
        new_g.set(location, OCCUPIED)
      else:
        new_g.set(location, value)
  #new_g.render()
  return new_g


def Run(lines, part, rounds = None):
  g = grid.Grid(lines)
  new_g = None
  if part == 1:
    new_g = RunRound(lines, g)
  else:
    new_g = RunRound2(lines, g)
  r = 0
  while g != new_g and (not rounds or r < rounds):
    # Make new copy, as we are modifying in place.
    tmp = copy.deepcopy(new_g)
    if part == 1:
      new_g = RunRound(lines, new_g)
    else:
      new_g = RunRound2(lines, new_g)
    g = tmp # No need to copy here. This can be a reference.
    r += 1
  return new_g

def TestPart1():
  lines = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".split('\n')
  g = Run(lines, 1, 6)
  print('Part 1 test:', g.count(OCCUPIED) == 37)
  sys.exit(0)

def TestPart2():
  lines = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".split('\n')
  print(lines)
  g = Run(lines, 2,  10)
  print('Part2 test:', g.count(OCCUPIED) == 26)
  sys.exit(0)

def main():
  f = open(sys.argv[1])
  lines = f.readlines()
  f.close()
  lines = [x.strip() for x in lines]

  #TestPart1()
  #TestPart2()

  g = Run(lines, 1)
  
  print('Day', DAY, ' part 1')
  print('Number of occupied seats in a steady state: ', g.count(OCCUPIED)) # 2329
  
  g = Run(lines, 2)
  print('Day', DAY, ' part 2')
  print('Number of occupied seats in a steady state: ', g.count(OCCUPIED)) # 2138
  

if __name__== '__main__':
  main()
