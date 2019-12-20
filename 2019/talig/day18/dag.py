import collections
import copy

Edge = collections.namedtuple('Edge', ['node', 'distance'])
Node = collections.namedtuple('Node', ['name', 'edges', 'visited'])

class DAG:
  def __init__(self, root_name):
    self.nodes = {}
    self.add_node(root_name)
    self.root = self.nodes[root_name]
    self.topo_sort = []

  def add_node(self, name):
    self.nodes[name] = Node(name, [], [])

  def add_edge(self, node_name, depends_on, distance):
    self.nodes[depends_on].edges.append(Edge(self.nodes[node_name], distance))

  def render(self, node, dist):
    buff = '(%s, %d)' % (node.name, dist)
    for edge in node.edges:
      buff += self.render(edge.node, edge.distance)
    return buff

  def __repr__(self):
    return self.render(self.root, 0)

  def _visit(self, node_name, sorted_nodes):
    node = self.nodes[node_name]
    if len(node.visited) == 2:
      return
    node.visited.append(0)
    for e in sorted(node.edges):
      self._visit(e.node.name, sorted_nodes)
    node.visited.append(0)
    sorted_nodes.insert(0, node_name)

  def topological_sort(self):
    if not self.topo_sort:
      self._visit(self.root.name, self.topo_sort)
    return self.topo_sort
