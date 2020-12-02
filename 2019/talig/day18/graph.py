import collections
import copy
import dag
import heapq


INF = 9999

class Edge:
  def __init__(self, other, dist=INF, depends_on=[]):
    self.node = other
    self.dist = dist

class Node:
  def __init__(self, location, value):
    self.point = location
    self.value = value
    self.dist = INF
    self.depends_on = []
    self.prev = None
    self.edges = {}
    self.marked = 0 # 1 is temp, 2 is permanent.

  def __repr__(self):
    buff = [self.location(), '[%s]' % self.value, 
            '=>', str(self.depends_on), ':', 
            str(
              [(k, self.edges[k].node.depends_on) for k in self.edges.keys()])]
    return ' '.join(buff)

  def location(self):
    return str(self.point)

  def add_edge(self, other, dist=INF):
    # Directions are: (0,1), (0,-1), (1,0), (-1,0)
    self.edges[other.value] = Edge(other, dist)

  def add_dep_to_edge(self, name, dep):
    self.edges[name].depends_on.append(dep)

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
    self.start = None
    self.path = []
    self.dist = None

  def add_node(self, location, value):
    node = Node(location, value)
    self.nodes[node.value] = node
    if value == '@':
      self.start = node

  def get_node(self, location_str):
    return self.nodes.get(location_str, None)

  def can_open_door(self, door, keys):
    return keys.get(door.lower(), False)

  def compute_path_length(self, key_order):
    path_len = 0
    current = self.start
    for key in key_order:
      keynode = current.edges[key]
      path_len += keynode.dist
      current = keynode.node
    return path_len
  
  def build_dependency_graph(self):
    # Build the dependency graph between doors and keys.
    queue = [self.start]
    self.start.depends_on.append('@')
    discovered = {self.start.location() : 1}
    while queue:
      v = queue.pop(0)
      if v.is_door():
        v.depends_on.append(v.value.lower())
      for e in v.edges.values():
        if not discovered.has_key(e.node.location()):
          discovered[e.node.location()] = 1
          e.node.depends_on.extend(v.depends_on)
          queue.append(e.node)
    for node in self.nodes.values():
      print node

  def requirements_met(self, collected, current, depends_on):
    if set(collected + [current]).issuperset(set(depends_on)):
      return True
    return False

  def get_min_distance_requirements_met(self, queue, collected_keys):
    min_d = INF
    min_node = 0
    for i in range(len(queue)):
      if (self.requirements_met(collected_keys, None, queue[i].depends_on) and 
          min_d > queue[i].dist):
        min_d = queue[i].dist
        min_node = i
    return queue.pop(min_node)

  def get_next_given_keys(self, current, collected_keys):
    # Returns the path that collects the maximum keys for minimu

  def dijkstra(self):
    # This can't work, because it's basic assumption is false in this graph.
    # Mark all unvisited. Shallow copy.
    queue = copy.copy(self.nodes.values())
    self.start.dist = 0
    collected_keys = ['@']
    current = None
    while queue:
      current = self.get_min_distance_requirements_met(queue, collected_keys)
      print 'Looking at', current.value
      for e in current.edges.values(): 
        if self.requirements_met(collected_keys, current.value, e.node.depends_on):
          alt = current.dist + e.dist
          if e.node.dist > alt:
            print 'Setting:' , e.node.value, ' prev to', current.value, 'dist:', alt
            e.node.prev = current
            e.node.dist = alt
      if current.is_key():
        collected_keys.append(current.value)
    order = []
    max_d = 0
    last_node = None
    all_nodes = self.nodes.values()

    for k in all_nodes:
      if max_d < k.dist:
        max_d = k.dist
        last_node = k

    while last_node:
      order.insert(0, last_node.value)
      last_node = last_node.prev

    return order, max_d
