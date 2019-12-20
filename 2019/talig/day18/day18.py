import sys
import copy
import collections
import itertools
import time
from os import system
import graph

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

DIRECTIONS = [Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)]

class Grid:
  def __init__(self, rows, columns):
    self.rows = rows
    self.columns = columns
    self.grid = []
    for y in range(rows):
      self.grid.append(['.'] * columns)
    print 'Initialized grid with:', len(self.grid), 'rows X', len(self.grid[0]), 'columns'

  def set(self, point, value):
    c = self.get(point)
    self.grid[point.y][point.x] = value

  def find(self, char):
    for y in range(self.rows):
      for x in range(self.columns):
        p = Point(x, y)
        if self.get(p) == char:
          return p

  def count(self, func):
    counter = 0
    for y in self.grid:
      for x in y:
        if func(x):
          counter +=1
    return counter
  
  def get(self, point):
    if point.x < 0 or point.x >= self.columns or point.y < 0 or point.y >= self.rows:
      return False
    return self.grid[point.y][point.x]

  def render(self):
    _ = system('clear')
    for y in self.grid:
      print ''.join(y)


def make_grid(filename):
  tunnels = []  
  f = open(filename)
  for line in f.readlines():
    tunnels.append([c for c in line.strip()])
  f.close()

  grid = Grid(len(tunnels), len(tunnels[0]))
  grid.grid = tunnels # This is already a grid, no need to set anything right now.
  
  grid.render()
  return grid

def bfs_grid(grid, current):
  queue = [current.point_location]
  discovered = {current.location():0}
  nodes = {}
  while queue:
    v = queue.pop(0)
    for direction in DIRECTIONS:
      next_loc = v + direction
      if not discovered.get(str(next_loc), False):
        discovered[str(next_loc)] = discovered[str(v)] + 1
        c = grid.get(next_loc) 
        if c != '#': 
          queue.append(next_loc)
        if c not in ['#','.','@', False]:
          nodes[c] = discovered[str(next_loc)]
  return nodes

def build_graph(grid):
  graph1 = graph.Graph()
  # Add all nodes.
  for y in range(grid.rows):
    for x in range(grid.columns):
      location = Point(x, y)
      c = grid.get(location)
      if c != '#' and c != '.':
        graph1.add_node(location, grid.get(location))

  for current in graph1.nodes.values():
    nodes = bfs_grid(grid, current)
    for n in nodes:
      # Avoid self-edges.
      if n != current.value:
        node = graph1.keys[n] if n.islower() else graph1.doors[n]
        current.add_real_edge(node, nodes[n])
  graph1.build_dependency_graph()
  return graph1

def expect(expected, actual):
  if expected == actual:
    print 'Pass.'
  else:
    print 'Nope! Expected: ', expected, ' actual: ', actual

def test():
  tests = {
    'test1.data': ('abcdef', 86),
    'test2.data': ('bacdfeg', 132),
    'test3.data': ('afbjgnhdloepcikm', 136), 
    'test4.data': ('acfidgbeh', 81)
  }
  for t in tests:
    grid = make_grid(t)
    graph1 = build_graph(grid)
    print 'Total Keys', graph1.total_keys
    graph1.build_dependency_graph()
    #graph1.dijkstra()
    for n in  graph1.keys:
      k = graph1.keys[n]
      print 'Key', k.value, 'dist:', k.dist

    #key = max(graph1.keys, key=lambda x: graph1.keys[x].dist)
    #moves = graph1.keys[key].dist
    moves = graph1.compute_path_length([x for x in tests[t][0]])
    expect(tests[t][1], moves)

def main():
  if (len(sys.argv) < 2):
    test()
    print 'Missing data file!'
    print 'Usage: python [script] [data]'
    sys.exit(1)

  grid = make_grid(sys.argv[1])
  graph1 = build_graph(grid)
  print 'Total Keys', graph1.total_keys
  graph1.build_dependency_graph()
  for node in graph1.nodes.values():
    print node
  # Bob's input
  moves = graph1.compute_path_length(['p', 'k', 'a', 'z', 't', 'b', 'c', 'e', 'x', 'd', 'w', 'o', 'v', 'u', 's', 'l', 'h', 'm', 'j', 'q', 'f', 'n', 'r', 'g', 'y', 'i'])
  print 'Total moves:', moves
  #toposort = graph1.build_dependency_graph()
  #start = grid.find('@')
  #print 'Starting point: ', start
  
 
if __name__== "__main__":
  main()
