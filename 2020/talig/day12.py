import sys
import functools
import operator
import re
import collections
import copy
import math

DAY = 12
X=0
Y=1

DIRECTION = {'E': (1, 0), 'W': (-1, 0), 'N': (0,1), 'S': (0,-1)} # Follwing mathematical axes
TURNS = ['R', 'L']
def Rotate(facing, rot_dir, angle):
  if rot_dir == 'R':
    angle *= -1 # matrix multiplication is counter clockwise
  angle = math.radians(angle)
  return [round(math.cos(angle) * facing[X] - math.sin(angle) * facing[Y]),
          round(math.sin(angle) * facing[X] + math.cos(angle) * facing[Y])]

def CalcJourneyPart1(lines):
  facing = DIRECTION['E']
  location = [0,0]
  for line in lines:
    d = line[X]
    val = int(line[1:])
    if d in DIRECTION:
      location[X] += val * DIRECTION[d][X]
      location[Y] += val * DIRECTION[d][Y]
    elif d in TURNS:
      facing = Rotate(facing, d, val)
    else:
      location[X] += val * facing[X]
      location[Y] += val * facing[Y]
  return location

def CalcJourneyPart2(lines):
  waypoint = [10, 1]
  location = [0,0]
  for line in lines:
    d = line[X]
    val = int(line[1:])
    if d in DIRECTION:
      waypoint[X] += val * DIRECTION[d][X]
      waypoint[Y] += val * DIRECTION[d][Y]
    elif d in TURNS:
      waypoint = Rotate(waypoint, d, val)
    else:
      location[X] += val * waypoint[X]
      location[Y] += val * waypoint[Y]
  return location


def ManhattanDistance(start, finish):
  return abs(finish[X]-start[X]) + abs(finish[Y]-start[Y])  


def Test():
  lines = """F10
N3
F7
R90
F11""".split('\n')
  print(lines)
  location = CalcJourneyPart1(lines)
  print('Test part 1: ', ManhattanDistance((0,0), location) == 25)
  location = CalcJourneyPart2(lines)
  print('Test part 2: ', ManhattanDistance((0,0), location) == 286)
  sys.exit(0)

def main():
  f = open(sys.argv[Y])
  lines = f.readlines()
  f.close()
  lines = [x.strip() for x in lines]

  #Test()

  
  print('Day', DAY, ' part 1')
  location = CalcJourneyPart1(lines)
  print('Manhattan distance in the end: ', ManhattanDistance((0,0), location)) # 962
  
  print('Day', DAY, ' part 2')
  location = CalcJourneyPart2(lines)
  print('Manhattan distance in the end: ', ManhattanDistance((0,0), location)) # 56135
  

if __name__== '__main__':
  main()
