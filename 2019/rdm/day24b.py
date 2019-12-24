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


def print_levels(levels):
  keys = list(levels.keys())
  keys.sort()
  for depth in keys:
    state = levels[depth]
    print('Depth %d:' % depth)
    print_state(state)


# Neighbors are (x, y, depth) tuples.
def get_neighbors_b(coords, depth):
  neighbors = set() 
  x, y = coords
  for nx, ny in aoc.neighbor_coords(coords):
    # Handle neighbors outside the bounds
    if nx == -1:  # left side
      neighbors.add((1, 2, depth - 1))
    elif nx == 5:  # right side
      neighbors.add((3, 2, depth - 1))
    if ny == -1:  # top
      neighbors.add((2, 1, depth - 1))
    elif ny == 5:  # bottom
      neighbors.add((2, 3, depth - 1))

    # Which edge of the center are we touching?
    if (nx, ny) == (2, 2):  
      if (x, y) == (2, 1):  # top
        for i in range(5):
          neighbors.add((i, 0, depth + 1))
      elif (x, y) == (3, 2):  # right side
        for i in range(5):
          neighbors.add((4, i, depth + 1))
      elif (x, y) == (1, 2):  # left side
        for i in range(5):
          neighbors.add((0, i, depth + 1))
      elif (x, y) == (2, 3):  # bottom
        for i in range(5):
          neighbors.add((i, 4, depth + 1))
      else:
        raise Exception('should not border the middle? %s' % coords)
    elif nx >= 0 and nx < 5 and ny >= 0 and ny < 5:
      neighbors.add((nx, ny, depth))  # A "normal" neighbor.
  return neighbors


def advance_b(levels):
  # Keyed by (x, y, depth)
  count = defaultdict(int)
  for depth, level in levels.items():
    for coords in level:
      for neighbor in get_neighbors_b(coords, depth):
        count[neighbor] += 1
  old_levels = levels
  new_levels = defaultdict(set)
  for (x, y, depth), c in count.items():
    if c == 1:
      new_levels[depth].add((x, y))
    elif c == 2 and (x, y) not in old_levels[depth]:
      new_levels[depth].add((x, y))
  return new_levels


def solve_part_b(levels, reps):
  print('# ORIGINAL STATE')
  print_levels(levels)
  for x in range(reps):
    levels = advance_b(levels)
    print('# LEVELS AFTER %d MINUTES' % (x+1))
    print_levels(levels)
  s = 0
  for level in levels.values():
    s += len(level)
  print('Bug count after %d minutes: %d' % (reps, s))
  assert s < 3073  # I guessed wrong.
  assert s < 2043  # I guessed wrong again.
  assert s == 1995  # I guessed right (typo is fixed)



# solve_part_a(load_initial_state())
levels = defaultdict(set)
levels[0] = load_initial_state()

reps = 200
for arg in sys.argv:
  try:
    arg = int(arg)
    reps = arg
  except ValueError:
    pass

solve_part_b(levels, reps)



