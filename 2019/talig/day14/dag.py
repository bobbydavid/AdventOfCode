import collections
import copy

Edge = collections.namedtuple('Edge', ['cost', 'node'])
Node = collections.namedtuple('Node', ['name', 'formula_source', 'edges', 'visited'])

class DAG:
  def __init__(self, root):
    self.nodes = {}
    self.root = root
    self.topo_sort = []

  def AddNode(self, name, quantity):
    self.nodes[name] = Node(name, quantity, [], [])

  def AddEdges(self, node_name, reactors):
    # Reactors are a pair: name, quantity. 
    for r in reactors.items():
      self.nodes[node_name].edges.append(Edge(r[1], r[0]))

  def Visit(self, node_name, sorted_nodes):
    node = self.nodes[node_name]
    if len(node.visited) == 2:
      return
    node.visited.append(0)
    for e in node.edges:
      self.Visit(e.node, sorted_nodes)
    node.visited.append(0)
    sorted_nodes.insert(0, node_name)

  def TopologicalSort(self):
    if not self.topo_sort:
      self.Visit(self.root, self.topo_sort)
    return self.topo_sort
