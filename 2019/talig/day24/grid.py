from os import system

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __add__(self, o):
    return Point(self.x + o.x, self.y + o.y)

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
    print('Initialized grid with:', len(self.grid), 'rows X', len(self.grid[0]), 'columns')

  def set(self, point, value):
    self.grid[point.y][point.x] = value
  
  def get(self, point):
    if point.y >= self.rows or point.y < 0 or point.x >= self.columns or point.x<0:
      return '.'
    return self.grid[point.y][point.x]

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

class PlutonianGrid:
  def __init__(self, g):
    self.levels = []
    self.rows = g.rows
    self.cols = g.columns
    self.base = copy.deepcopy(g)
    self.base.set(Point(self.rows//2, self.cols//2), '?')

  def get(self, point):
    if point.y >= self.rows or point.y < 0 or point.x >= self.columns or point.x<0:
      # Need to down in the hierarchy
      return '.'
    return self.grid[point.y][point.x]

  def count_neighbors(self, location):
    neighbors = 0
    for d in DIRECTIONS:
      n = self.get(location+d)
      if n == '#':
        neighbors += 1
      elif n == '?':
        # level up in the hierarchy and count.
    return neighbors

