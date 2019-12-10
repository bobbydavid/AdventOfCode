import math
import sys
import operator
import copy
from functools import partial
import collections
import logging
import numpy

Point = collections.namedtuple('Point', ['x', 'y'])

class AsteroidMap:
  def __init__(self, raw_data):
    self.columns = len(raw_data[0])
    self.rows = len(raw_data)
    self.raw_data = raw_data
    self.max_visibility = {}
    self.visibility = {}

  def ComputeAngle(self, src, p):
    angle = math.atan2(p.y - src.y, p.x - src.x) 
    return round(angle, 6)

  def IsAstreroid(self, point):
    return self.raw_data

  def d(self, p1, p2):
    return math.sqrt((p1.x-p2.x)**2 + (p1.y - p2.y)**2)
  
  def SetVisible(self, src):
    visible = {}
    for y in range(self.rows):
      for x in range(self.columns):
        p = Point(x, y)
        if p == src or self.raw_data[y][x] == '.':
          continue
        # data[p]=='#'
        angle = self.ComputeAngle(src, p)
        if (not visible.has_key(angle)):
          visible[angle] = []
        visible[angle].append(p)
    # Sort astroids at angle by distances
    for v in visible:
      visible[v] = sorted(visible[v], key=lambda x: self.d(src, x))
    # Keep the visibility map for each source.
    self.visibility[src] = visible
    # The source can see as many asteroids as there are distinct *vectors*
    # connecting it with other asteroids.
    self.max_visibility[src] = len(visible.keys()) 

  def ComputeVisibility(self):
    for y in range(self.rows):
      for x in range(self.columns):
        if self.raw_data[y][x] == '#':
          self.SetVisible(Point(x, y))
  
  def PrintVisibility(self):
    for y in range(self.rows):
      row = []
      for x in range(self.columns):
        row.append('|%3d|' % self.max_visibility.get(Point(x,y), 0))
      print ''.join(row)

  def GetBestPoint(self):
    self.ComputeVisibility()
    max_visible = 0
    best_point = Point(0,0)
    for p in self.max_visibility:
      if self.max_visibility[p] >  max_visible:
        max_visible = self.max_visibility[p]
        best_point = p
    return max_visible, best_point

  def GenerateAngles(self, src):
    angles = set()
    for y in range(self.rows):
      for x in range(self.columns):
        p = Point(x, y)
        if p == src:
          continue
        angles.add(self.ComputeAngle(src, p))
    
    # Angles go clockwise by definition.
    angles = sorted(angles)
    # We want to start with the angle that's straight up, and shift the array.
    i = angles.index(self.ComputeAngle(src, Point(0.0 + src.x, -1.0 + src.y))) # What if not found?
    shifted = angles[i:] + angles[:i]
    return shifted

  def VaporizeScan(self, src, bet):
    visible = copy.deepcopy(self.visibility[src])
    # We will be vaporising these astroids in their order in the lists here.
    angles = self.GenerateAngles(src)
    i = 0
    count_vaporized = 0
    vaporization_order = []
    # Drop all the vectors that aren't relevant.
    # Now rotate
    while visible:
      a = angles[i]
      if visible.has_key(a):
        next_vaporized = visible[a].pop(0)
        count_vaporized += 1
        vaporization_order.append(next_vaporized)
        if count_vaporized == bet:
          return next_vaporized
        i += 1
        if not visible[a]:
          # We evaporated all the astroids that match this vector. 
          # Just remove it from the map.
          visible.pop(a)
      else: 
        angles.remove(a)
      i = i % len(angles)
        

def Expect(expected, existing):
  if expected == existing:
    print 'Passed'
  else:
    print 'Nope! Expected: %s got: %s' % (expected, existing)


def TestA(content, filename):
  tests = {
            'test1.data': [8, Point(3,4)],
            'test2.data': [33, Point(5,8)],
            'test3.data': [35, Point(1,2)],
            'test4.data': [41, Point(6,3)],
            'test5.data': [210, Point(11,13)],
          }

  print 'Testing: '
  expected = tests[filename]
  am = AsteroidMap(content)
  max_v, best_point = am.GetBestPoint()
  print am.PrintVisibility()
  Expect(expected[0], max_v)
  Expect(expected[1], best_point)
  print '\n\n\n\n', '*'*30, '\n'

def TestB(content):
  # Only works for test5.data, best station in 11,13
  am = AsteroidMap(content)
  max_v, best_point = am.GetBestPoint()
  res = am.VaporizeScan(best_point, 200)
  Expect(802, res.x*100 + res.y)
  

def main():
  if (len(sys.argv) < 2):
    print 'Missing data file!'
    print 'Usage: python [script] [data]'
    sys.exit(1)

  filename = sys.argv[1]
  f = open(filename)
  content = [x.strip() for x in f.readlines()]
  f.close()
  
  if filename.startswith('test'):
    TestA(content, filename)
    TestB(content)


  else:
  # (a) ==> 214
    am = AsteroidMap(content)
    max_v, best_point = am.GetBestPoint()
    print 'Best point: ', best_point, ', Max: ', max_v
  # (b) ==> 502
    res = am.VaporizeScan(best_point, 200)
    print 'Result: ', res.x*100 + res.y
  
if __name__== "__main__":
  main()
