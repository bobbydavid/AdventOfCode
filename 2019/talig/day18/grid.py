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

DIRECTIONS = [Point(0, 1), Point(1, 0), Point(-1, 0), Point(0, -1)]

class GridNode:
  def __init__(self, location, value):
    self.location = location
    self.value = value
    self.neighbors = []

  def id(self):
    return str(self.location)

class Grid:
  def __init__(self, rows, columns):
    self.rows = rows
    self.columns = columns
    self.grid = []
    self.grid_nodes = []
    for y in range(rows):
      self.grid.append(['.'] * columns)
      self.grid_nodes.append([None] * columns)
    print('Initialized grid with:', len(self.grid), 'rows X', len(self.grid[0]), 'columns')
    self.keys_and_doors = {}

  def set(self, point, value):
    self.grid[point.y][point.x] = value
    #self.grid_nodes[point.y][point.x].value = value
  
  def get(self, point):
    return self.grid[point.y][point.x]
  
  def get_node(self, point):
    node = self.grid_nodes[point.y][point.x]
    if node == None:
      self.grid_nodes[point.y][point.x] = GridNode(
          point, self.get(point))
    return self.grid_nodes[point.y][point.x]

  def find(self, char):
    for y in range(self.rows):
      for x in range(self.columns):
        p = Point(x, y)
        if self.get(p) == char:
          return p

  def find_node(self, char):
    p = self.find(char)
    # Note that this shouldn't be called when things are not yet initialized
    # Because this would create a node.
    return self.get_node(p)

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

  def _is_node(self, location):
    v = maze_grid.get(location)
    return not v == '#'

  def build_grid_graph(self):
    # Make this grid into a graph where every non-wall square
    # is a node, and the edges go in every direction.
    for y in range(maze_grid.rows):
      for x in range(maze_grid.columns):
        location = Point(x, y)
        if self._is_node(location):
          n = self.get_node(location)
          # While we're here, set the keys and doors somewhere.
          if n.value.isalpha():
            self.keys_and_doors[value] = n
          # Set all neighbors.
          for d in DIRECTIONS:
            neighbor = location + d
            if self._is_node(neighbor):
              n.edges.append(self.get_node(neighbor))
    # In the end of this we have a grid graph.
