from collections import defaultdict
import time
import sys
import copy
import aoc


def load_initial_state():
  filename = 'day24.data'
  if 'test' in sys.argv:
    filename = 'day24_test1.data'
  state = set()
  with open(filename, 'r') as contents:
    for y, row in enumerate(contents.readlines()):
      for x, c in enumerate(row.strip()):
        if c == '#':
          state.add((x,y))
  return state


def print_state(state):
  data = []
  for y in range(5):
    for x in range(5):
      c = '#' if (x, y) in state else '.'
      data.append(c)
      
    data.append('\n')
  print(''.join(data))


def calc_biodiversity(state):
  d = 0
  for (x, y) in state:
    exp = y * 5 + x
    d += 2 ** exp
  return d



def advance(old):
  counts = defaultdict(int)
  for x, y in old:
    for neighbor in aoc.neighbor_coords((x, y)):
      counts[neighbor] += 1

  new = set()
  for y in range(5):
    for x in range(5):
      coords = (x, y)
      if counts[coords] == 1:
        new.add(coords)
      elif counts[coords] == 2 and coords not in old:
        new.add(coords)
  return new
  

def solve_part_a(state):
  seen = set()
  while True:
    biod = calc_biodiversity(state)
    if biod in seen:
      print('repeat state seen, biodiversity = %d' % biod)
      print_state(state)
      break
    seen.add(biod)
    state = advance(state)


solve_part_a(load_initial_state())
