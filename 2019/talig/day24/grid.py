from os import system
from collections import defaultdict
import copy

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __add__(self, o):
    return Point(self.x + o.x, self.y + o.y)
  
  def __sub__(self, o):
    return Point(self.x - o.x, self.y - o.y)

  def __mul__(self, scalar):
    return Point(self.x * scalar, self.y * scalar)
  
  def __rmul__(self, scalar):
    return Point(self.x * scalar, self.y * scalar)
  
  def __repr__(self):
    return '(%d, %d)' % (self.x, self.y)

  def __eq__(self, o):
    return self.x == o.x and self.y == o.y

  def __ne__(self, o):
    return self.x != o.x or self.y != o.y

  def dist(self, o):
    return math.sqrt((o.y - self.y)**2 + (o.x - self.x)**2)

DIRECTIONS = [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)]

class Grid:
  def __init__(self, rows, columns, content):
    self.rows = rows
    self.columns = columns
    self.grid = content
    if not self.grid:
      for y in range(rows):
        self.grid.append(['.'] * columns)

  def set(self, point, value):
    self.grid[point.y][point.x] = value
  
  def get(self, point):
    if not self.in_bounds(point):
      return '.'
    return self.grid[point.y][point.x]
  
  def in_bounds(self, point):
    return point.y < self.rows and point.y >= 0 and point.x < self.columns and point.x>=0

  def count_neighbors(self, location):
    neighbors = 0
    for d in DIRECTIONS:
      if self.get(location+d) != '.':
        neighbors += 1
    return neighbors

  def __repr__(self):
    buff = []
    for y in self.grid:
      buff.append(''.join(y)+'\n')
    return ''.join(buff)

  def render(self):
    print(self)

def get_new_level():
  rows = 5
  cols = 5
  g = Grid(rows, cols, [])
  g.set(Point(rows//2, cols//2), '?')
  return g

class PlutonianGrid:
  def __init__(self, g):
    self.rows = g.rows
    self.cols = g.columns
    self.center = Point(self.rows//2, self.cols//2)
    self.levels = defaultdict(get_new_level)
    self.base = copy.deepcopy(g)
    self.base.set(self.center, '?')
    self.levels[0] = self.base
    self.neighbors_for_pos = {}
    self.set_neighbors_for_pos()

  def set_neighbors_for_pos(self):
    for y in range(self.rows):
      for x in range(self.cols):
        location = Point(x,y)
        neighbors = [(0, location + d) for d in DIRECTIONS]
        # Remove the center point if present:
        if (0, self.center) in neighbors:
          neighbors.remove((0, self.center))

        new_neighbors = []
        # Don't change the list you're iterating over... sigh.
        for t in neighbors:
          # If it's out of bounds, replace it with its level up counterpart.
          if not self.base.in_bounds(t[1]):
            # get the direction this is in.
            d = t[1] - location
            new_neighbors.append((-1, self.center + d)) 
          else:
            new_neighbors.append(t)
        neighbors = new_neighbors
          
        # Down is center.
        if location + Point(0,1) == self.center:
          neighbors.extend([(1, Point(p, 0)) for p in range(self.cols)])
        # Up is center.
        elif location + Point(0, -1) == self.center:
          neighbors.extend([(1, Point(p, self.rows - 1)) for p in range(self.cols)])
        # Right is center.
        elif location + Point(1,0) == self.center:
          neighbors.extend([(1, Point(0, p)) for p in range(self.rows)])
        # Left is center.
        elif location + Point(-1,0) == self.center:
          neighbors.extend([(1, Point(self.cols - 1, p)) for p in range(self.rows)])
        self.neighbors_for_pos[str(location)] = neighbors 
  
  def print_neighbors_for_pos(self):
    for location in self.neighbors_for_pos:
      n = self.neighbors_for_pos[location]
      print(location, ' (', len(n),  '):', n)

  def get(self, location, level):
    return self.levels[level].get(location)

  def set(self, location, level, value):
    self.levels[level].set(location, value)

  def extend_levels(self):
    high = max(self.levels.keys()) + 1
    low = min(self.levels.keys()) - 1
    _ = self.levels[high]
    _ = self.levels[low]

  def get_levels_range(self):
    return range(min(self.levels.keys()), max(self.levels.keys()) + 1)

  def count_neighbors(self, location, level):
    neighbors = 0
    for dl, location in self.neighbors_for_pos[str(location)]:
      if self.get(location, level + dl) == '#':
        neighbors += 1
    return neighbors

