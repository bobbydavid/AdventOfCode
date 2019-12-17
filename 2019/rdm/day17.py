import intcode
import re
import time
import copy
import sys
import threading
import os
import random
import tty
from Queue import Queue
import termios

filename = 'day17.data'
print('Data file: ' + filename)
with open(filename, 'r') as content_file:
  input_data = [int(x) for x in content_file.read().strip().split(',')]



def print_grid(grid):
  for row in grid:
    print(''.join(row))


def read_grid(q):
  grid = []
  row = []
  while True:
    c = chr(q.get())
    if c != '\n':
      row.append(c)
      continue
    if len(row) == 0:
      return grid
    grid.append(row)
    row = []

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


# Run me to solve part A
def solve_part_a():
  in_q = intcode.SimpleQueue()
  out_q = intcode.SimpleQueue()
  computer = intcode.Computer(input_data, in_q, out_q)
  computer.run()
  output = list(out_q.q)
  grid = read_grid(out_q)
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



# (across, down) clockwise
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def find_path_for_part_b():
  in_q = intcode.SimpleQueue()
  out_q = intcode.SimpleQueue()
  computer = intcode.Computer(input_data, in_q, out_q)
  computer.run()
  output = list(out_q.q)
  grid = read_grid(out_q)
  print_grid(grid)

  pos = (0, 10)  # From looking at the grid.
  direction = 1  # index into DIRECTIONS, from looking at grid.
  path = ['R']  # must be the first thing to do.
  segment_length = 0
  while True:
    front_pos = add_coords(pos, DIRECTIONS[direction])
    front_sq = look(grid, front_pos)
    if front_sq != '.':
      segment_length += 1
      pos = front_pos
      continue
    path.append(str(segment_length))
    segment_length = 0

    left_dir = (direction - 1) % 4
    left_pos = add_coords(pos, DIRECTIONS[left_dir])
    left_sq = look(grid, left_pos)
    right_dir = (direction + 1) % 4
    right_pos = add_coords(pos, DIRECTIONS[right_dir])
    right_sq = look(grid, right_pos)
    if left_sq != '.':
      assert right_sq == '.'
      direction = left_dir
      path.append('L')
    elif right_sq != '.':
      direction = right_dir
      path.append('R')
    else:  # Reached the end.
      print(','.join(path))
      return path



PART_B_PATH = [
    'R', '8', 'L', '10', 'R', '8', 'R', '12', 'R', '8', 'L', '8', 'L', '12',
    'R', '8', 'L', '10', 'R', '8', 'L', '12', 'L', '10', 'L', '8', 'R', '8',
    'L', '10', 'R', '8', 'R', '12', 'R', '8', 'L', '8', 'L', '12', 'L', '12',
    'L', '10', 'L', '8', 'L', '12', 'L', '10', 'L', '8', 'R', '8', 'L', '10',
    'R', '8', 'R', '12', 'R', '8', 'L', '8', 'L', '12']
PART_B_PROG = ','.join(PART_B_PATH)


path = find_path_for_part_b()
assert path == PART_B_PATH

def make_atoms():
  atoms = []
  for turn in ['L', 'R']:
    for dist in ['8', '10', '12']:
      atoms.append( (turn,dist) )
  print('ATOMS: %s' % atoms)
  return atoms

ATOMS = make_atoms()

# Produces the programs for this index. A p
def get_program(idx):
  atoms = []
  while idx >= len(ATOMS):
    atoms.append(ATOMS[idx % len(ATOMS)])
    idx = idx // len(ATOMS)
  atoms.append(ATOMS[idx])
  prog = []
  for atom in atoms:
    prog.append(atom[0])
    prog.append(atom[1])
  return prog


def main_solution(a_prog, b_prog, c_prog):
  path = PART_B_PROG
  path = path.replace(a_prog, 'A')
  path = path.replace(b_prog, 'B')
  path = path.replace(c_prog, 'C')
  if re.match('^[ABC,]+$', path):
    return path
  return None


# as measured in elements (not chars)
def find_solution(path):
  a_size = 1
  b_size = 1
  c_size = 1
  while True:
    a_prog = path[:a_size]
    b_prog = path[a_size:b_size]
    c_prog = path[a_size + b_size:c_size]

    a_prog = ','.join(a_prog)
    b_prog = ','.join(b_prog)
    c_prog = ','.join(c_prog)

    if len(a_prog) < 20:
      a_size += 1
    else:
      a_size = 1
      if len(b_prog) < 20:
        b_size += 1
      else:
        b_size = 1
        if len(c_prog) < 20:
          c_size += 1
        else:
          raise Exception('out of space')

    #print('attempt: a_prog=%s, b_prog=%s, c_prog=%s' % (a_prog, b_prog, c_prog))
    soln = main_solution(a_prog, b_prog, c_prog)
    if soln is not None:
      print(','.join(path))
      print('SOLVED: a_prog=%s, b_prog=%s, c_prog=%s, soln=%s' % (a_prog, b_prog, c_prog, soln))
      return (a_prog, b_prog, c_prog, soln)


def write_str(q, s):
  for c in s:
    q.put(ord(c))
  q.put(ord('\n'))


def solve_part_b(want_debug):
  a_prog, b_prog, c_prog, soln = find_solution(PART_B_PATH)

  input_data[0] = 2  # change to part B
  in_q = Queue()
  out_q = Queue()
  computer = intcode.Computer(input_data, in_q, out_q)

  write_str(in_q, soln)
  write_str(in_q, a_prog)
  write_str(in_q, b_prog)
  write_str(in_q, c_prog)

  write_str(in_q, 'y' if want_debug else 'n')

  if want_debug:
    computer.run_async()
    while not computer.stopped:
      grid = read_grid(out_q)
      os.system('clear')
      time.sleep(.001)
      print_grid(grid)
  else:
    computer.run()
    last_num = 0
    buf = []
    while not out_q.empty():
      buf.append(out_q.get())
    print(''.join([chr(x) for x in buf[:-1]]))
    print('dust collected : %d' % buf[-1])


#solve_part_a()
want_debug = False
solve_part_b(want_debug)
print('Ran with want_debug=%s' % repr(want_debug))

