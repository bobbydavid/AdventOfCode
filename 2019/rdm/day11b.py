from collections import defaultdict
from collections import deque
import copy
import itertools
import sys
import threading
import intcode

if len(sys.argv) < 2:
  sys.exit("forgot data file name: python day1.py <data file>")
filename = sys.argv[1]

print('Data file: ' + filename)
with open(filename, 'r') as content_file:
  content = content_file.read()
  orig_tape = [int(x) for x in content.split(',') if x]


class Spaceship:
  # Direction in clockwise order.
  DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

  # Colors
  BLACK = 0
  WHITE = 1

  # Modes
  PAINT = 0
  TURN = 1
  MODE_COUNT = 2

  def __init__(self):
    # Location is (x, y) == (across, up)
    self.robot_location = (0, 0)
    # Index into the DIRECTIONS array.
    self.robot_direction_index = 0
    # Map from (x,y) to color.
    self.hull_color = {}
    self.mode = self.PAINT


  # Allows the IntOps computer to read the current color.
  def get(self):
    color = self.color_at(self.robot_location)
    return color


  # Reads the color at a particular location.
  def color_at(self, coords):
    if coords in self.hull_color:
      return self.hull_color[coords]
    return self.BLACK


  # Receives the next instruction.
  def put(self, x):
    if (self.mode == self.PAINT):
      assert x == self.WHITE or x == self.BLACK, ('unexpected color %d' % x)
      self.hull_color[self.robot_location] = x
    elif (self.mode == self.TURN):
      if x == 0:
        self.robot_direction_index -= 1
      elif x == 1:
        self.robot_direction_index += 1
      else:
        raise Exception('unexpected turn direction %d' % x)
      self.robot_direction_index %= len(self.DIRECTIONS)
      delta = self.DIRECTIONS[self.robot_direction_index]
      self.robot_location = (
          self.robot_location[0] + delta[0], self.robot_location[1] + delta[1])
    else:
      raise Exception('unexpected mode %d' % self.mode)
    self.mode += 1
    self.mode %= self.MODE_COUNT


# Part B
ship = Spaceship()
ship.hull_color[(0, 0)] = Spaceship.WHITE  # Paint the starting square white.
computer = intcode.Computer(orig_tape, ship, ship)
computer.debug_level = 0
computer.run()

min_x = 0
max_x = 0
min_y = 0
max_y = 0
for (x, y), color in ship.hull_color.iteritems():
  min_x = min(min_x, x)
  max_x = max(max_x, x)
  min_y = min(min_y, y)
  max_y = max(max_y, y)

# x = across
# y = up
for y in range(max_y + 1, min_y - 2, -1):
  for x in range(min_x - 1, max_x + 2, 1):
    color = ship.color_at((x, y))
    c = ' '
    if color == Spaceship.WHITE:
      c = '#'
    sys.stdout.write(c)
  sys.stdout.write('\n')

