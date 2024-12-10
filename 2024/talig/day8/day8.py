import sys
import math
import time
import os
from copy import deepcopy


class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def add(self, p):
    return Point(self.x + p.x, self.y + p.y)

  def mul(self, times):
    return Point(self.x * times, self.y * times)

  def __str__(self):
    return "(" + str(self.x) + ", " + str(self.y) + ")"

  def __hash__(self):
    return (self.x, self.y).__hash__()

  def __repr__(self):
    return self.__str__()

  def sub(self, p):
    return Point(self.x - p.x, self.y - p.y)

  def __eq__(self, p):
    return self.x == p.x and self.y == p.y


class Map():
  def __init__(self, lines):
    self.map = []
    for line in lines:
      line = line.strip()
      self.width = len(line)
      self.map.append(list(line))
    self.antinodeslist = set()

  def get(self, p):
    return self.map[p.y][p.x]

  def processFrequencies(self):
    frequencies = {}
    for r in range(len(self.map)):
      for c in range(len(self.map[0])):
        p = Point(c, r)
        v = self.get(p)
        if v != '.':
          if v not in frequencies:
            frequencies[v] = []
          frequencies[v].append(p)
    self.frequencies = frequencies

  def makePairs(self, freq):
    pairs = set()
    for i in freq:
      for j in freq:
        if i != j:
          # this will add reflexive pairs, but that's actually nice, because then
          # we automatically get the computation for both directions.
          pairs.add((i,j))
    return pairs

  def inRange(self, p):
    return p.y >= 0 and p.x >= 0 and p.y < len(self.map) and p.x < len(self.map[0])

  def antinodes(self, part2):
    antinodes = set()
    for f in self.frequencies: 
      # we need to do this for every pair :facepalm:
      pairs = self.makePairs(self.frequencies[f])
      for p1, p2 in pairs: 
        sub = p1.sub(p2)
        res = p1.add(sub)
        while self.inRange(res):
          antinodes.add(res)
          res = res.add(sub)
          if not part2:
            break
        if part2:
          antinodes.add(p1)
          antinodes.add(p2)
    self.antinodeslist = antinodes
    return antinodes

  def printMap(self):
    a = self.antinodeslist
    print("antinodes:", a)
    for r in range(len(self.map)):
      for c in range(len(self.map[0])):
        p = Point(c, r)
        v = self.get(p)
        if v != '.':
          print(v, end="")
        elif p in a:
          print('#', end="")
        else:
          print(v, end="")
      print()



def main():
  f = open(sys.argv[1])
  m = Map(f.readlines())
  f.close()
  
  #part 1
  print("Map:", len(m.map), "X", len(m.map[0]))
  m.processFrequencies()
  antinodes = m.antinodes(False)
  m.printMap()
  print("Result part1:", len(antinodes))
  
  antinodes = m.antinodes(True)
  print("Antinodes:", antinodes)
  print("Result part2:", len(antinodes))

if __name__=="__main__":
  main()
