import collections
import copy
import dag
import heapq

Edge = collections.namedtuple('Edge', ['node', 'dist','depends_on'])

class Node:
  def __init__(self, location, value):
    self.point_location = location
    self.value = value
    self.edges = {}
    # Key edges.
    self.prev = None
    self.dist = 9000
    self.key_edges = {}
    self.marked = 0 # 1 is temp, 2 is permanent.
    self.depends_on = None # Where we got here from.

  def __repr__(self):
    return str(self.point_location) + '[%s]' % self.value + ' :' + str(
              [(k, self.key_edges[k][1]) for k in self.key_edges.keys()])

  def location(self):
    return str(self.point_location)

  def add_edge(self, direction, node, dist=1):
    # Directions are: (0,1), (0,-1), (1,0), (-1,0)
    self.edges[str(direction)] = (node, dist)

  def add_real_edge(self, node, dist, depends_on=[]):
    self.key_edges[node.value] = Edge(node, dist, depends_on)
  
  def add_dep_to_edge(self, name, dep):
    self.key_edges[name].depends_on.append(dep)

  def get_edge(self, direction):
    return self.edges.get(str(direction), None)

  # Note: '.' will return False in both cases.
  def is_door(self):
    return self.value.isupper()
  
  def is_key(self):
    return self.value.islower()

class Graph:
  def __init__(self):
    self.nodes = {}
    self.keys = {}
    self.doors = {}
    self.total_keys = 0
    self.start = None
    self.current = None
    self.moves = 0
    self.path = []
    self.dist = None

  def add_node(self, location, value):
    node = Node(location, value)
    self.nodes[node.location()] = node
    if value == '@':
      self.current = node
      self.start = node
    if node.is_key():
      self.keys[node.value] = node
      self.total_keys += 1
    if node.is_door():
      self.doors[node.value] = node

  def get_node(self, location_str):
    return self.nodes.get(location_str, None)

  def can_open_door(self, door, keys):
    return keys.get(door.lower(), False)

  def all_pairs_shortest_path(self):
    inf = 90000
    self.dist = dict([(k, {}) for k in self.nodes.keys()])
    node_keys = sorted(self.nodes.keys())
    for k in node_keys:
      self.dist[k][k] = 0
      v = self.nodes[k]
      for w, d in v.edges.values():
        self.dist[v.location()][w.location()] = d
    print 'Done setting up. Now computing.'
    print 'This is ', len(node_keys), ' ^3 computations'
    for k in node_keys:
      for i in node_keys:
        for j in node_keys:
          # This condition will only be true if we don't get inf at all on the rhs.
          if self.dist[i].get(j, inf) > self.dist[i].get(k, inf) + self.dist[k].get(j, inf):
            self.dist[i][j] = self.dist[i][k] + self.dist[k][j]
    
  def print_all_pairs(self):
    if not self.dist:
      print 'Compute it first.'
      return None
    else:
      node_keys = sorted(self.nodes.keys())
      print '\t\t', '\t'.join(node_keys)
      for key in node_keys:
        print key, ':\t', '\t'.join([str(self.dist[key][x]) for x in node_keys])
    
  def compute_path_length(self, key_order):
    path_len = 0
    current = self.start
    for key in key_order:
      keynode = current.key_edges[key]
      path_len += keynode[1]
      current = keynode[0]
    return path_len
  
  def build_dependency_graph(self):
    # Build the dependency graph between doors and keys.
    queue = [self.start]
    self.start.depends_on = '@'
    discovered = {self.start.location() : 1}
    while queue:
      v = queue.pop(0)
      if v.is_door():
        v.depends_on = v.value.lower()
      for node, _, _ in v.key_edges.values():
        if not discovered.has_key(node.location()):
          discovered[node.location()] = 1
          node.depends_on = v.depends_on
          queue.append(node)

  def requirements_met(self, collected, depends_on):
    print 'Collected', collected, 'Depends on', depends_on
    if depends_on == None or depends_on in collected:
      return True
    return False
  
  def dijkstra(self):
    # Mark all unvisited.
    unvisited = ['@'] + sorted(self.keys.keys())
    current = self.start
    collected_keys = ['@']
    inf = 90000
    distance = dict([(k, inf) for k in unvisited])
    distance['@'] = 0
    while distance and min(distance.values()) < inf:
      for e in current.key_edges.values(): 
        'Looking at ', e.node.value
        if self.requirements_met(collected_keys, e.node.depends_on):
          if e.node.value in unvisited:
            d_c = distance[current.value]
            d_n = e.dist
            if distance[e.node.value] > d_c + d_n:
              distance[e.node.value] = d_c + d_n
              e.node.prev = current
              e.node.dist = d_c + d_n
      unvisited.remove(current.value)
      distance.pop(current.value)
      if current.is_key():
        collected_keys.append(current.value)
      if distance:
        next_key = min(distance, key=lambda x: distance[x])
        current = self.keys[next_key]
