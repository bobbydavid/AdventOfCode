import sys
import copy
import collections
import itertools
import time
from os import system
import graph
import grid

"""
class grid.Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __add__(self, o):
    return grid.Point(self.x + o.x, self.y + o.y)

  def __mul__(self, scalar):
    return grid.Point(self.x * scalar, self.y * scalar)
  
  def __rmul__(self, scalar):
    return grid.Point(self.x * scalar, self.y * scalar)
  
  def __repr__(self):
    return '(%d, %d)' % (self.x, self.y)

  def __eq__(self, o):
    return self.x == o.x and self.y == o.y

  def __ne__(self, o):
    return self.x != o.x or self.y != o.y

grid.DIRECTIONS = [grid.Point(0, 1), grid.Point(1, 0), grid.Point(0, -1), grid.Point(-1, 0)]

class grid.Grid:
  def __init__(self, rows, columns):
    self.rows = rows
    self.columns = columns
    self.maze_grid = []
    for y in range(rows):
      self.maze_grid.append(['.'] * columns)
    print 'Initialized maze_grid with:', len(self.maze_grid), 'rows X', len(self.maze_grid[0]), 'columns'

  def set(self, point, value):
    c = self.get(point)
    self.maze_grid[point.y][point.x] = value

  def find(self, char):
    for y in range(self.rows):
      for x in range(self.columns):
        p = grid.Point(x, y)
        if self.get(p) == char:
          return p

  def count(self, func):
    counter = 0
    for y in self.maze_grid:
      for x in y:
        if func(x):
          counter +=1
    return counter
  
  def get(self, point):
    if point.x < 0 or point.x >= self.columns or point.y < 0 or point.y >= self.rows:
      return False
    return self.maze_grid[point.y][point.x]

  def render(self):
    _ = system('clear')
    for y in self.maze_grid:
      print ''.join(y)

"""
def make_maze_grid(filename):
  tunnels = []  
  f = open(filename)
  for line in f.readlines():
    tunnels.append([c for c in line.strip()])
  f.close()

  maze_grid = grid.Grid(len(tunnels), len(tunnels[0]))
  # This is already a maze_grid, no need to set anything right now.
  for y in range(maze_grid.rows):
    for x in range(maze_grid.columns):
      maze_grid.set(grid.Point(x,y), tunnels[y][x]) 
  maze_grid.render()
  return maze_grid

def bfs_maze_grid(maze_grid, current):
  queue = [current.point]
  discovered = {current.location():0}
  nodes = {}
  while queue:
    v = queue.pop(0)
    for direction in grid.DIRECTIONS:
      next_loc = v + direction
      if not discovered.get(str(next_loc), False):
        discovered[str(next_loc)] = discovered[str(v)] + 1
        c = maze_grid.get(next_loc) 
        if c != '#': 
          queue.append(next_loc)
        if c not in ['#','.','@', False]:
          nodes[c] = discovered[str(next_loc)]
  return nodes

def build_graph(maze_grid):
  graph1 = graph.Graph()
  # Add all nodes.
  for y in range(maze_grid.rows):
    for x in range(maze_grid.columns):
      location = grid.Point(x, y)
      c = maze_grid.get(location)
      if c != '#' and c != '.':
        graph1.add_node(location, maze_grid.get(location))

  for current in graph1.nodes.values():
    nodes = bfs_maze_grid(maze_grid, current)
    for n in nodes:
      # Avoid self-edges.
      if n != current.value:
        node = graph1.nodes[current.value]
        node.add_edge(graph1.nodes[n], nodes[n])
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
    maze_grid = make_maze_grid(t)
    graph1 = build_graph(maze_grid)
    graph1.build_dependency_graph()
    order, max_d = graph1.dijkstra()
    for n in  graph1.nodes:
      k = graph1.nodes[n]
      print 'Key', k.value, 'dist:', k.dist
    print order
    print max_d
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

  maze_grid = make_maze_grid(sys.argv[1])
  graph1 = build_graph(maze_grid)
  print 'Total Keys', graph1.total_keys
  graph1.build_dependency_graph()
  for node in graph1.nodes.values():
    print node
  # Bob's input
  moves = graph1.compute_path_length(['p', 'k', 'a', 'z', 't', 'b', 'c', 'e', 'x', 'd', 'w', 'o', 'v', 'u', 's', 'l', 'h', 'm', 'j', 'q', 'f', 'n', 'r', 'g', 'y', 'i'])
  print 'Total moves:', moves
  #toposort = graph1.build_dependency_graph()
  #start = maze_grid.find('@')
  #print 'Starting point: ', start
  
 
if __name__== "__main__":
  main()
