import intcode
import time
import copy
import sys
import threading
import os
import random
import tty
from Queue import Queue
import termios

if len(sys.argv) < 2:
  filename = 'day17.data'
else:
  filename = sys.argv[1]
print('Data file: ' + filename)
with open(filename, 'r') as content_file:
  input_data = [int(x) for x in content_file.read().strip().split(',')]



def print_grid(grid):
  for row in grid:
    print(''.join(row))

def output_to_grid(output):
  grid = []
  row = []
  for c in output:
    c = chr(c)
    if c == '\n':
      grid.append(row)
      row = []
    else:
      row.append(c)
  return grid

def look(grid, coords):
  x = coords[0]
  y = coords[1]
  if y >= 0 and y < len(grid):
    row = grid[y]
    if x >= 0 and x < len(row):
      return row[x]
  return '.'

def add_coords(coords1, coords2):
  return (coords1[0] + coords2[0], coords1[1] + coords2[1])


def solve_part_a():
  in_q = intcode.SimpleQueue()
  out_q = intcode.SimpleQueue()
  computer = intcode.Computer(input_data, in_q, out_q)
  computer.run()
  output = list(out_q.q)
  grid = output_to_grid(output)
  print_grid(grid)

  s = 0
  for y in range(len(grid)):
    for x in range(len(grid[0])):
      matches = True
      for delta in [(0,0), (0,1), (0,-1), (1,0), (-1,0)]:
        coords = add_coords((x,y), delta)
        if look(grid, coords) == '.':
          matches = False
          break
      if matches:
        grid[y][x] = 'O'
        s += x * y
  print('checksum for part a = %s' % s)

  print_grid(grid)

      


solve_part_a()
