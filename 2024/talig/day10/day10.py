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

DIRECTIONS = [Point(1, 0), Point(-1,0), Point(0, 1), Point(0, -1)] 

class Map():
  def __init__(self, lines):
    self.map = []
    for line in lines:
      line = line.strip()
      self.width = len(line)
      self.map.append([int(x) for x in list(line)])
    self.trailheads = []

  def get(self, p):
    return self.map[p.y][p.x]

  def inRange(self, p):
    return p.y >= 0 and p.x >= 0 and p.y < len(self.map) and p.x < len(self.map[0])

  def __repr__(self):
    s = ""
    for r in range(len(self.map)):
      for c in range(len(self.map[0])):
        p = Point(c, r)
        v = self.get(p)
        s += str(v)
      s += '\n'
    return s

  def processTrailheads(self):
    for r in range(len(self.map)):
      for c in range(len(self.map[0])):
        p = Point(c, r)
        v = self.get(p)
        if v == 0:
          self.trailheads.append(p)

  def findNext(self, curr, trails):
    if curr == 9:
      return trails
    new_trails = []
    for t in trails:
      p = t[-1]
      for d in DIRECTIONS: 
        n = p.add(d)
        if self.inRange(n) and self.get(n) == (curr + 1) and (n not in t):
          updated = deepcopy(t)
          updated.append(n)
          new_trails.append(updated)
   
    curr += 1
    new_trails = self.findNext(curr, new_trails)
    return new_trails

  def hike(self):
    trails = {}
    curr = 0
    alles = []
    for h in self.trailheads:
      fromh = self.findNext(0, [[h]])
      # how many different peaks?
      by9s = {}
      for t in fromh:
        if t[-1] not in by9s:
          by9s[t[-1]] = []
        by9s[t[-1]].append(t)
      trails[h] = by9s
      alles.extend(fromh)
    return trails, alles
      
def countTrails(m, trails):
  total = 0
  for head in trails:
    total += len(trails[head])
  return total

def main():
  f = open(sys.argv[1])
  m = Map(f.readlines())
  f.close()
  
  #part 
  m.processTrailheads()
  trails, alles = m.hike()
  c = countTrails(m, trails)
  print("Result part1:", c)
  
  print("Result part2:", len(alles))

if __name__=="__main__":
  main()
