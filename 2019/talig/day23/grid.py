from os import sys

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

class Grid:
  def __init__(self, rows, columns):
    self.rows = rows
    self.columns = columns
    self.grid = []
    for y in range(rows):
      self.grid.append(['.'] * columns)
    print('Initialized grid with:', len(self.grid), 'rows X', len(self.grid[0]), 'columns')

  def set(self, point, value):
    self.grid[point.y][point.x] = value
  
  def get(self, point):
    if point.y >= self.rows or point.y < 0 or point.x >= self.columns or point.x<0:
      return '.'
    return self.grid[point.y][point.x]

  def find(self, char):
    for y in range(self.rows):
      for x in range(self.columns):
        p = Point(x, y)
        if self.get(p) == char:
          return p

  def count(self, char):
    counter = 0
    for y in self.grid:
      for x in y:
        if x == char:
          counter +=1
    return counter

  def render(self):
    _ = system('clear')
    for y in self.grid:
      print(''.join(y))
