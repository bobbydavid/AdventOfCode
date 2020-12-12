from os import sys
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

DIRECTIONS = [Point(x, y) for x in range(-1, 2) for y in range(-1, 2)]
DIRECTIONS.remove(Point(0,0))

class Grid:
  def __init__(self, lines):
    self.rows = len(lines)
    self.columns = len(lines[0])
    self.grid = []
    for line in lines:
      self.grid.append(list(line))

  def set(self, point, value):
    self.grid[point.y][point.x] = value
  
  def in_bounds(self, point):
    if point.y >= self.rows or point.y < 0 or point.x >= self.columns or point.x<0:
      return False
    return True

  def get(self, point):
    if not self.in_bounds(point):
      return '.'
    return self.grid[point.y][point.x]

  def __eq__(self, o):
    if not o:
      return False
    eq = True
    for y in range(self.rows):
      for x in range(self.columns):
        location = Point(x, y)
        eq = eq and (self.get(location) == o.get(location))
    return eq

  def count_neighbors(self, point, occupied):
    counter = 0
    for direction in DIRECTIONS:
      current = point + direction # make sure you don't count yourself.
      if self.get(point + direction) == occupied:
          counter += 1
    return counter

  def count_visible_seats(self, point, occupied):
    counter = 0
    for direction in DIRECTIONS:
      current = point + direction # make sure you don't count yourself.
      while self.get(current) == '.' and self.in_bounds(current):
        current += direction
      if self.get(current) == occupied:
        counter += 1
    return counter

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
