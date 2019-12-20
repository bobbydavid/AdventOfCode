import sys
from os import system
import copy
import collections


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
    return abs(o.y - self.y) + abs(o.x - self.x)

DIRECTIONS = [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)]
INF = 90000

class Node:
  def __init__(self, name, location):
    self.name = name
    self.location = location
    self.edges = []
    self.dist = INF
    self.prev = None

  def __repr__(self):
    return '%s %d' % (self.name, self.dist)

  def render(self):
    return '%s %s => %s' % (self.name, self.location, str(self.edges))

  def id(self):
    return '%s %s' % (self.name, self.location)

class Edge:
  def __init__(self, node, distance=None):
    self.next = node
    self.distance = distance

  def __repr__(self):
    return '%s: %s (%d)' % (self.next.name, self.next.location, self.distance)

class Graph:
  def __init__(self, grid):
    self.nodes_by_location = {}
    self.nodes_by_name = {}
    self.edges = []
    self.grid = copy.deepcopy(grid)
    self._build_graph()

  def add_node(self, node):
    # No surprises.
    if self.nodes_by_name.has_key(node.name):
      a = self.nodes_by_name[node.name]
      a.edges.append(Edge(node, 1))
      node.edges.append(Edge(a, 1))
    else:
      self.nodes_by_name[node.name] = node
    self.nodes_by_location[str(node.location)] = node
  
  def _in_grid_bounds(self, n):
    return (n.x >= 0 and n.x < len(self.grid[0]) and
          n.y >= 0 and n.y < len(self.grid))

  
  def _get_neighbors(self, p):
    neighbors = [p]
    for d in DIRECTIONS:
      n = p+d
      if self._in_grid_bounds(n):
        neighbors.append(n)
    return neighbors

  def _get_donut_rims(self, axis):
    if axis == 'x':
      return [0,1, 2, len(self.grid[0]) - 1, len(self.grid[0]) - 2, len(self.grid[0]) - 3]
    if axis == 'y':
      return [0,1, 2, len(self.grid) - 1, len(self.grid) - 2, len(self.grid) - 3]

  def _choose_location(self, locations, center):
    # Farther from center.
    location = max(locations, key=lambda x: center.dist(x[0]))
    p = locations[0][0]
    if p.x in self._get_donut_rims('x') or p.y in self._get_donut_rims('y'):
      # Closer to center
      location = min(locations, key=lambda x: center.dist(x[0]))
    return location

  def _get_node(self, x, y, center):
    locations = []
    for n in self._get_neighbors(Point(x, y)):
      c = self.grid[n.y][n.x]
      if c.isupper() or c == '.':
        locations.append((n, c))
    if len(locations) == 3:
      location = self._choose_location(locations, center)
      locations.remove(location)
      name = ''.join(sorted([x[1] for x in locations]))
      return Node(name, location[0])
    return None

  def _bfs_grid(self, start):
    # Returns distances from the starting point to all the points reachable by grid walk.
    queue = [start]
    visited = {str(start): 0}
    while queue:
      v = queue.pop(0)
      for d in DIRECTIONS:
        n = v + d
        # make sure it's in bounds
        if not self._in_grid_bounds(n) or visited.has_key(str(n)):
          continue
        # only consider '.' and uppercase letters as steps.
        c = self.grid[n.y][n.x]
        if c == '.' or c.isupper():
          visited[str(n)] = visited[str(v)] + 1
          queue.append(n)
        else:
          continue
    return visited

  def _build_graph(self):
    rows = len(self.grid)
    cols = len(self.grid[0])
    center = Point(rows/2, cols/2)
    start = None
    visited = {}
    # Find all nodes.
    for y in range(rows):
      for x in range(cols):
        if self.grid[y][x].isupper():
          node = self._get_node(x,y, center)
          if node == None or visited.has_key(node.id()):
            continue
          visited[node.id()] = 1
          self.add_node(node)

    for node in self.nodes_by_location.values():
      distances = self._bfs_grid(node.location)
      for loc in self.nodes_by_location:
        d = distances.get(str(loc), -1)
        if d > 0:
          node.edges.append(Edge(self.nodes_by_location[loc], d))

  def shortest_path(self, start_name):
    # For AA and ZZ only this is unambiguous.
    start = self.nodes_by_name[start_name]
    start.dist = 0
    queue = [v for v in self.nodes_by_location.values()]
    while queue:
      v = min(queue, key=lambda x: x.dist)
      queue.remove(v)
      for e in v.edges:
        alt = v.dist + e.distance
        if alt < e.next.dist:
          e.next.dist = alt
          e.next.prev = v

def get_grid(filename):
  tunnels = []  
  f = open(filename)
  for line in f.readlines():
    tunnels.append([c for c in line[:-1]])
  f.close()

  return tunnels

def expect(expected, real):
  if expected == real:  
    print 'Pass!'
  else:
    print 'Nope! Expected', expected, 'got', real

def get_moves(filename):
  grid = get_grid(filename)
  graph = Graph(grid)
  graph.shortest_path('AA')
  return graph.nodes_by_name['ZZ'].dist

def test():
  tests = {'test1.data': 23,
           'test2.data': 58,
          }
  
  for t in tests:
    expect(tests[t], get_moves(t))

def main():
  if (len(sys.argv) < 2):
    test()
    print 'Missing data file!'
    print 'Usage: python [script] [data]'
    sys.exit(1)

  moves = get_moves(sys.argv[1])
  print moves, 'moves are required to get from AA to ZZ'  

if __name__== "__main__":
  main()

