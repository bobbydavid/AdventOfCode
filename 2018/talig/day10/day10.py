import collections
import re
from os import system
import sys
import math
import time

Point = collections.namedtuple('Point', ['x','y'])
Star = collections.namedtuple('Star', ['pos', 'vel'])

class Grid:
  def __init__(self, raw_data):
    self.stars = collections.defaultdict(list)
    pattern = r'(-?\d+)'
    self.lines = []
    for line in raw_data:
      px, py, vx, vy = re.findall(pattern, line)
      self.lines.append((int(px), int(py), int(vx), int(vy)))
      self.stars[Point(int(px), int(py))].append(Point(int(vx), int(vy)))

  def render(self, shift):
    for y in range(50):
      s = []
      for x in range(200):
        p = Point(x+shift.x, y+shift.y)
        if self.stars.has_key(p):
          s.append('#')
        else:
          s.append('.')
      print ''.join(s)
  
  def FindSmallestBoundingBox(self):
    k = []
    for i in xrange(20000):
      minx = min(x + i * vx for (x, y, vx, vy) in self.lines)
      maxx = max(x + i * vx for (x, y, vx, vy) in self.lines)
      miny = min(y + i * vy for (x, y, vx, vy) in self.lines)
      maxy = max(y + i * vy for (x, y, vx, vy) in self.lines)
      k.append((maxx - minx + maxy - miny, i, Point(minx,miny)))
    return min(k)

  def step_forward(self,steps=1):
    next_stars =  collections.defaultdict(list)
    for s in self.stars:
      for v in self.stars[s]:
        p_n = Point(s.x+ (steps * v.x), s.y + (steps * v.y))
        next_stars[p_n].append(v)
    self.stars = next_stars

  def simulate(self, steps):
    for x in range(steps):
      _ = system('clear')
      self.step_forward(1)
      self.render()
      time.sleep(0.1)

def main():
  if (len(sys.argv) < 2):
    print 'Missing data file!'
    print 'Usage: python [script] [data]'
    sys.exit(1)

  f = open(sys.argv[1])
  content = f.readlines()
  f.close()

  grid = Grid(content)
  constant = grid.FindSmallestBoundingBox()
  # Constant[1] is the answer to (b): 10081
  # Message is: CRXKEZPZ
  print constant
  grid.step_forward(constant[1])
  grid.render(constant[2])
    
if __name__== "__main__":
  main()

