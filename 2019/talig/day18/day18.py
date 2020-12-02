import sys
from os import system
from grid import Grid, Point, DIRECTIONS
from collections import deque, defaultdict
from copy import deepcopy

INF = 99999

class Node:
  def __init__(self, name, point):
    self.name = name
    self.point = point
    self.edges = []
    self.prev = None
    self.require = name.lower()

  def __repr__(self):
    return self.name
  
  def location(self):
    return str(self.point)

class Edge:
  def __init__(self, node, dist):
    self.node = node
    self.visited = False
    self.dist = dist

def get_grid(filename):
  f = open(filename)
  content = [line.strip() for line in f.readlines()]
  f.close()

  for i in range(len(content)):
    content[i] = [x for x in list(content[i])]
  
  g = Grid(len(content), len(content[0]))
  g.grid = content
  #g.build_grid_graph()

  return g

def bfs(start, maze, maze_graph):
  q = deque()
  q.append(start.point)
  distance = defaultdict(int)
  visited = defaultdict(int)
  print ('Starting BFS with node', start)
  while q:
    current = q.popleft()
    for d in DIRECTIONS:
      n = current + d
      if str(n) in visited:
        continue
      value = maze.get(n)
      if value == '#':
        continue
      q.append(n)
      distance[str(n)] = distance[str(current)] + 1
      visited[str(n)] = 0
      # This will skip everything except a-zA-Z, incl. @
      # Also skip the self edge. 
      if value.isalpha() and value != start.name:
        # Add an edge from the starting point.
        next_node = maze_graph[value]
        next_node.name = value
        start.edges.append(Edge(next_node, distance[str(n)]))

def get_nodes(maze):
  maze_graph = {}
  for y in range(maze.rows):
    for x in range(maze.columns):
      loc = Point(x, y)
      v = maze.get(loc)
      if v.isalpha() or v == '@':
        maze_graph[v] = Node(v, loc)
  return maze_graph

def build_graph(g):
  maze_graph = get_nodes(g)
  # Order doesn't matter, build the graph. 
  k = maze_graph.values()
  for v in k:
    bfs(v, g, maze_graph)
  return maze_graph

def recurse(edge, collected_keys, path, path_length, paths, total_keys=26):
  node = edge.node
  if node.require != node.name and node.require not in collected_keys:
    path_length = INF
    path.append(node)
    # don't append to paths... 
    return
  else:
    print('in here')
    collected_keys.add(node.name)
    path_length += edge.dist
    print path_length
    path.append(node)
    if len(collected_keys) == total_keys:
      print ('All keys!')
      paths.append((path, path_length))
    for k in collected_keys:
      # Remove all edges to doors with keys that we have. We will walk right through them.
      node.edges = filter(lambda x: x.node.name != k.upper(), node.edges)
    for e in node.edges:
      if not e.visited and e.node != node.prev:
        e.node.prev = node
        print ('Recursion: Looking at', e.node)
        recurse(e, deepcopy(collected_keys), deepcopy(path), path_length, paths, total_keys)  
        e.visited = True

def find_optimal_path(maze_graph):
  # Now we have the fully connected graph with distances. 
  start = maze_graph['@']
  total_keys = sum([1 for k in maze_graph if k.islower()])
  print('Total keys: ', total_keys)
  collected_keys = set()
  paths = []
  for e in start.edges:
    print ('Looking at', e.node)
    recurse(e, collected_keys, [], 0, paths, total_keys)
    e.visited = True
  min_path = INF
  best_path = []
  for p in paths:
    if p[1] < min_path: 
      best_path = p[0]
      min_path = p[1]
  return best_path, min_path

def everything_together(filename):
  maze = get_grid(filename)
  maze_graph = build_graph(maze)
  best_path, min_path = find_optimal_path(maze_graph)
  print( 'Shortest path is %d steps long: %s' % (min_path, best_path))
  return min_path

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
    moves = everything_together(t)
    expect(tests[t][1], moves)

def main():
  if len(sys.argv) < 2:
    test()
    print('Missing data file. Usage:')
    print('python3 day18.py <file.data>')
    sys.exit(0)

  # (a) => 4204
  maze_grid, nodes = get_grid(sys.argv[1])
  build_graph(maze_grid, nodes)

  
if __name__== "__main__":
  main()
