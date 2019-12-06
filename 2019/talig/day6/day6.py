import math
import sys
import operator
import copy
from functools import partial

class DAG:
  def __init__(self, root):
    self.nodes = {root: []}
    self.root = root
    self.orbits = {root: 0}
    self.reverse_edges = {root:[]}

  def AddNode(self, name):
    self.nodes[name] = []
    self.reverse_edges[name] = []
    self.orbits[name] = 0

  def AddEdge(self, node1, node2):
    if not self.nodes.has_key(node1):
      self.AddNode(node1)
    if not self.nodes.has_key(node2):
      self.AddNode(node2)
    self.nodes[node2].append(node1)
    self.reverse_edges[node1].append(node2)

  def OrbitalTransfers(self, node, target):
    queue = [(node, -1)]
    visited = {}
    while queue:
      current, t = queue.pop(0)
      visited[current] = 1
      if current == target:
          return t - 1
      for n in self.nodes[current]:
        if not queue.count(n) and not visited.has_key(n):
          queue.append((n, t + 1))
      for n in self.reverse_edges[current]:
        if not queue.count(n) and not visited.has_key(n):
          queue.append((n, t + 1))

  def CountOrbits(self):
    # Run BFS and count the orbits
    queue = [self.root]
    while queue:
      for node in self.reverse_edges[queue[0]]:
        self.orbits[node] = self.orbits[queue[0]] + 1
        queue.append(node)
      queue.pop(0)

  def SumOrbits(self):
    self.CountOrbits()
    return sum(self.orbits.values())
    

def BuildOrbitsGraph(orbits):
  dag = DAG('COM')
  for line in orbits:
    nodes = line.split(')')
    dag.AddEdge(nodes[0], nodes[1])
  return dag
    

def CountOrbits(orbits):
  graph = BuildOrbitsGraph(orbits)
  return graph.SumOrbits()

def CountOrbitalTransfers(orbits, a, b):
  graph = BuildOrbitsGraph(orbits)
  return graph.OrbitalTransfers(a, b)


def Expect(expected, existing):
  if expected == existing:
    print 'Passed'
  else:
    print 'Nope! Expected ', expected, ' got:' , existing
    

def TestCaseOrbits():
  tests = [
           (['COM)B',
            'B)C',
            'C)D',
            'D)E',
            'E)F',
            'B)G',
            'G)H',
            'D)I',
            'E)J',
            'J)K',
            'K)L'], 42)]
  for test in tests:
    orbits = CountOrbits(test[0])
    Expect(test[1], orbits)

def TestCaseOrbitalTransfers():
  testdata = ['COM)B',
              'B)C',
              'C)D',
              'D)E',
              'E)F',
              'B)G',
              'G)H',
              'D)I',
              'E)J',
              'J)K',
              'K)L',
              'K)YOU',
              'I)SAN']
  expected = 4
  orbital_transfers = CountOrbitalTransfers(testdata, 'YOU', 'SAN')
  Expect(expected, orbital_transfers)

def Test():
  print 'Testing: '
  TestCaseOrbits()
  TestCaseOrbitalTransfers()
  print '\n\n\n\n', '*'*30, '\n'

def main():
  Test()
  if (len(sys.argv) < 2):
    print 'Missing data file!'
    print 'Usage: python [script] [data]'
    sys.exit(1)

  f = open(sys.argv[1])
  content = [line.strip() for line in f.readlines()]
  f.close()
  
  # (a)
  print 'Orbits! ', CountOrbits(content)

  # (b)
  print 'Orbital Transfers! ', CountOrbitalTransfers(content, 'YOU', 'SAN')
  
if __name__== "__main__":
  main()
