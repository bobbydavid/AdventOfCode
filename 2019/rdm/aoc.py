import sys

def load_file_as_grid(filename):
  grid = []
  with open(filename, 'r') as contents:
    for line in contents.readlines():
      line = line[:-1]
      grid.append([c for c in line])
  return grid


def read_grid(grid, coords, default=None):
  x = coords[0]
  y = coords[1]
  if y >= 0 and y < len(grid):
    row = grid[y]
    if x >= 0 and x < len(row):
      return row[x]
  if default is not None:
    return default
  raise Exception('%s is not in grid:\n%s' % (coords, grid))


def print_grid(grid):
  rows = [''.join([c for c in row]) for row in grid]
  print('\n'.join(rows))

def add_coords(a, b):
  return (a[0]+b[0], a[1]+b[1])
