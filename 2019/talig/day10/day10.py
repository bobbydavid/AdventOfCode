import math
import sys
import operator
import copy
from functools import partial
import collections
import logging
import numpy
import bisect

Point = collections.namedtuple('Point', ['x', 'y'])

class AsteroidMap:
  def __init__(self, raw_data):
    self.columns = len(raw_data[0])
    self.rows = len(raw_data)
    self.raw_data = raw_data
    self.max_visibility = {}
    self.visibility = {}

  def ComputeVector(self, src, dst):
    # Compute vector
    v = numpy.array([dst.x - src.x, dst.y - src.y])
    # Normalize it.
    v = v / numpy.linalg.norm(v)
    return (round(v[0], 6), round(v[1], 6))

  def IsAstreroid(self, point):
    return self.raw_data

  def d(self, p1, p2):
    return math.sqrt((p1.x-p2.x)**2 + (p1.y - p2.y)**2)
  
  def clockwise(self, v1, v2):
    center = Point(0, 0)
    res = (v1[0] - center.x) * (v2[1] - center.y) - (v2[0] - center.x) * (v1[1] - center.y)
    if res < 0:
      return 1
    if res > 0:
      return -1
    return 0
    
  def SetVisible(self, src):
    visible = {}
    for y in range(self.rows):
      for x in range(self.columns):
        p = Point(x, y)
        if p == src or self.raw_data[y][x] == '.':
          continue
        # data[p]=='#'
        vector = self.ComputeVector(src, p)
        if (not visible.has_key(vector)):
          visible[vector] = []
        visible[vector].append(p)
    # Sort vectors by distances
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

  def GenerateVectors(self, src):
    vectors = set()
    for y in range(self.rows):
      for x in range(self.columns):
        p = Point(x, y)
        if p == src:
          continue
        vectors.add(self.ComputeVector(src, p))
    # We want to sort in a clockwise order, but how do we do that?
    vectors = sorted(vectors, cmp=self.clockwise )
    #print 'Sorted: ', vectors
    # We want to start with the vector where x == 0 and y = -1.0 , so shift the array.
    i = vectors.index((0.0, -1.0)) # What if not found?
    shifted = vectors[i:] + vectors[:i]
    return shifted

  def VaporizeScan(self, src, bet):
    visible = copy.deepcopy(self.visibility[src])
    # We will be vaporising these astroids in their order in the lists here.
    vectors = self.GenerateVectors(src)
    i = 0
    count_vaporized = 0
    vaporization_order = []
    # Drop all the vectors that aren't relevant.
    # Now rotate
    while visible:
      v = vectors[i]
      if visible.has_key(v):
        next_vaporized = visible[v].pop(0)
        count_vaporized += 1
        vaporization_order.append(next_vaporized)
        if count_vaporized == bet:
          return next_vaporized
        i += 1
        if not visible[v]:
          # We evaporated all the astroids that match this vector. 
          # Just remove it from the map.
          visible.pop(v)
      else: 
        vectors.remove(v)
      i = i % len(vectors)
        

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
    #TestA(content, filename)
    TestB(content)


  else:
  # (a)
    am = AsteroidMap(content)
    max_v, best_point = am.GetBestPoint()
    print 'Best point: ', best_point, ', Max: ', max_v
  # (b)
    res = am.VaporizeScan(best_point, 200)
    print 'Result: ', res.x*100 + res.y
  
if __name__== "__main__":
  main()
