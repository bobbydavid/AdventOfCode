import math
import sys
import operator
import copy
import collections
import logging
import numpy
import re

Point = collections.namedtuple('Point', ['x', 'y', 'z'])
Moon = collections.namedtuple('Moon', ['pos', 'vel'])

def FactorNumber(n):
  i = 2
  factors = {}
  while i * i <= n:
      if n % i:
          i += 1
      else:
          n //= i
          factors[i] = factors.get(i,0) + 1
  if n > 1:
      factors[n] = factors.get(n,0) + 1
  return factors

class MoonSimulator:
  def __init__(self, raw_data):
    self.moons = []
    self.initial = []
    pattern = r'(x|y|z)=(-?\d+)'
    for row in raw_data:
      m = dict(re.findall(pattern, row))
      x = int(m['x'])
      y = int(m['y'])
      z = int(m['z'])
      self.moons.append(Moon(Point(x, y, z), Point(0, 0, 0)))
      self.initial.append(Moon(Point(x, y, z), Point(0, 0, 0)))
    self.steps = 0
    self.cycle_by_axis = {'x': 0, 'y': 0, 'z': 0}

  def GetVel(self, d):
    # Returns -1, 1 or 0.
    return d if d == 0 else -d/abs(d)
    
  def GetNewGravityOnAxis(self, moon1, moon2):
    return Point(self.GetVel(moon1.x - moon2.x), 
                 self.GetVel(moon1.y - moon2.y),
                 self.GetVel(moon1.z - moon2.z))

  def Gravity(self, moon1, moon2):
    # Takes two moons' posititions, returns the gravity impact they have on eachother.
    new_v1 = self.GetNewGravityOnAxis(moon1, moon2)
    new_v2 = self.GetNewGravityOnAxis(moon2, moon1)
    return new_v1, new_v2

  def SumV(self, p1, p2):
    p = [sum(x) for x in zip(p1, p2)]
    return Point(p[0], p[1], p[2])

  def StepForward(self):
    next_step_vel = [m.vel for m in self.moons]
    # Compute pairwise gravity influences.
    for i in range(len(self.moons)):
      for j in range(i, len(self.moons)):
        moon1 = next_step_vel[i]
        moon2 = next_step_vel[j]
        # This is computed based on position.
        gr1, gr2 = self.Gravity(self.moons[i].pos, self.moons[j].pos)
        # This is the cumulative sum of gravity influences.
        next_step_vel[i] = self.SumV(moon1, gr1)
        next_step_vel[j] = self.SumV(moon2, gr2)
    
    # Apply velocity
    for i in range(len(self.moons)):
      vel = next_step_vel[i]
      pos = self.SumV(self.moons[i].pos, vel)
      # Update
      self.moons[i] = Moon(pos, vel)
    self.steps += 1

  def Energy(self):
    total = 0
    for m in self.moons:
      pot = sum([abs(x) for x in m.pos])
      kin = sum([abs(v) for v in m.vel])
      total += pot * kin

    return total

  def SimulateTo(self, steps):
    while self.steps < steps:
      self.StepForward()

  def ToString(self, moons):
    r = ''
    for m in moons:
      r += str(m) + '\n'
    return r
      
  def PrintState(self):
    print 'After ', self.steps, ' steps:\n', self.ToString(self.moons)
    print 'Energy: ', self.Energy()

  def GetXState(self, moons):
    return str([(moon.pos.x, moon.vel.x) for moon in moons])

  def GetYState(self, moons):
    return str([(moon.pos.y, moon.vel.y) for moon in moons])  

  def GetZState(self, moons):
    return str([(moon.pos.z, moon.vel.z) for moon in moons])  

  def FindCyclePerAxis(self):
    f = {'x': self.GetXState,
         'y': self.GetYState,
         'z': self.GetZState}
    initial = {'x': f['x'](self.initial),
               'y': f['y'](self.initial),
               'z': f['z'](self.initial)}
    # Reset state of moons. 
    self.moons = [copy.deepcopy(m) for m in self.initial]
    self.steps = 0
    self.cycle_by_axis = {'x': 0, 'y': 0, 'z': 0}
    while 0 in self.cycle_by_axis.values():
      self.StepForward()
      for axis in f:
        moon = f[axis](self.moons)
        if moon == initial[axis] and self.cycle_by_axis[axis] ==0:
          self.cycle_by_axis[axis] = self.steps

  def Divides(self, number):
    # Will only be 0 when they are all 0.
    return sum([number % v for v in self.cycle_by_axis.values()]) == 0

  def ComputeCycle(self):
    # Find the individual cycle per axis.
    self.FindCyclePerAxis()
    # Figure out where they all meet.
    # It's the first number that results in the same number of steps having 
    factors = {}
    for x in self.cycle_by_axis.values():
      fs = FactorNumber(x)
      for f in fs:
        factors[f] = max(fs[f], factors.get(f, 1))
    cycle = 1
    for x in factors:
      cycle *= x**factors[x]
    
    return cycle

def Expect(expected, existing):
  if expected == existing:
    print 'Passed'
  else:
    print 'Nope! Expected: %s got: %s' % (expected, existing)

def TestA_B(content, filename):
  # Filename: #steps, Energy at #steps, length of cycle
  tests = {'test1.data': (10, 179, 2772), 'test2.data': (100, 1940, 4686774924)}
  ms = MoonSimulator(content)
  ms.SimulateTo(tests[filename][0])
  Expect(tests[filename][1], ms.Energy())
  Expect(tests[filename][2], ms.ComputeCycle())

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
    TestA_B(content, filename)

  else:
    ms = MoonSimulator(content)
    if (len(sys.argv) == 3):
      # (a) ==> 12070
      steps = int(sys.argv[2])
      ms.SimulateTo(steps)
      ms.PrintState()
      print '\n'
    else:
      # (b) ==> 500903629351944
      print 'Cycle: ', ms.ComputeCycle()
  
if __name__== "__main__":
  main()
