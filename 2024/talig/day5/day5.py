import sys
from collections import defaultdict
import graphlib
import math

def parse_graph(lines):
  graph = defaultdict(set)
  for line in lines:
    line = line.strip()
    nodes = line.split('|')
    graph[int(nodes[1])].add(int(nodes[0]))
  return graph

def isInOrder(pages, topo):
  return pages == topo

def makeSubgraph(graph, pages):
  g = {}
  pageset = set(pages)
  for p in pages:
    g[p] = graph[p].intersection(pageset)
  return g

def printGraph(graph):
  for k  in graph:
    print("node ", k, ": ", graph[k] ) 

def parse_prints(lines, graph):
  correct_updates = []
  incorrect_updates = []
  for line in lines:
    line = line.strip()
    pages = [int(x) for x in line.split(',')]
    
    m_graph = makeSubgraph(graph, pages)
    topo = list(graphlib.TopologicalSorter(m_graph).static_order())
    if isInOrder(pages, topo):
      correct_updates.append(pages)
    else:
      incorrect_updates.append(topo)
  return correct_updates, incorrect_updates

def sumMiddles(updates):
  total = 0
  for update in updates:
    m = math.floor(len(update)/2)
    total += update[m]
  return total    

def main():
  f = open(sys.argv[1])
  graph = parse_graph(f.readlines())
  f.close()

  
  f = open(sys.argv[2])
  goodUpdates, badUpdates = parse_prints(f.readlines(), graph)
  total = sumMiddles(goodUpdates)
  total2 = sumMiddles(badUpdates)

  print("Result part1:", total)
  print("Result part2:", total2)


if __name__=="__main__":
  main()
