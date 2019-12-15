import intcode
import copy
import sys
import threading
import os
import random
import tty
from Queue import Queue
import termios

if len(sys.argv) < 2:
  filename = 'day15.data'
else:
  filename = sys.argv[1]
print('Data file: ' + filename)
with open(filename, 'r') as content_file:
  input_data = [int(x) for x in content_file.read().strip().split(',')]



NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

DIRECTIONS = [NORTH, EAST, SOUTH, WEST]


def _rotate_dir(direction, clockwise_turns):
  idx = DIRECTIONS.index(direction)
  return DIRECTIONS[(idx + clockwise_turns) % 4]


def reverse_direction(direction):
  return _rotate_dir(direction, 2)

def char_to_direction(c):
  if c == 'w':
    return NORTH
  elif c == 'a':
    return WEST
  elif c == 's':
    return SOUTH
  elif c == 'd':
    return EAST
  else:
    return None


# coords = across, down
def move_coords(coords, direction):
  if direction == NORTH:
    return ( coords[0], coords[1] - 1 )
  elif direction == SOUTH:
    return ( coords[0], coords[1] + 1 )
  elif direction == WEST:
    return ( coords[0] - 1, coords[1] )
  elif direction == EAST:
    return ( coords[0] + 1, coords[1] )
  else:
    raise Exception('Unknown direction: %s' % direction)

def get_ch():
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
  finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  if ch == '\x03':
      raise KeyboardInterrupt
  elif ch == '\x04':
      raise EOFError
  return ch


def print_grid(grid, robot_coords = None):
  min_x = 0
  max_x = 0
  min_y = 0
  max_y = 0
  for x, y in grid.keys():
    min_x = min(x, min_x)
    max_x = max(x, max_x)
    min_y = min(y, min_y)
    max_y = max(y, max_y)

  for y in range(min_y - 1, max_y + 2):
    for x in range(min_x - 1, max_x + 2):
      c = ' '
      coords = (x, y)
      if coords == robot_coords:
        c = 'D'
      elif coords in grid:
        c = grid[coords]
      sys.stdout.write(c)
    sys.stdout.write('\n')
  

class Robot():
  def __init__(self, input_program):
    self.in_q = Queue()
    self.out_q = Queue()
    self.computer = intcode.Computer(input_program, self.in_q, self.out_q)
    self.computer_thread = threading.Thread(target=self.computer.run)
    self.computer_thread.daemon = True
    self.computer_thread.start()

    self.coords = (0,0)
    self.grid = {}
    self._set_grid_value(self.coords, '.')

    self.oxygen_coords = None

  def _set_grid_value(self, coords, value):
    if coords in self.grid:
      existing = self.grid[coords]
      if value != existing:
        raise Exception('setting %s to %s but it was already %s' % (
            coords, value, existing))
    else:
      self.grid[coords] = value


  def explored(self, direction):
    coords = move_coords(self.coords, direction)
    return coords in self.grid


  def look(self, direction):
    coords = move_coords(self.coords, direction)
    if coords not in self.grid:
      orig_coords = self.coords
      if self.move(direction):
        self.move(reverse_direction(direction))
    assert coords in self.grid
    return self.grid[coords]


  def move(self, direction):
    self.in_q.put(direction)
    result = self.out_q.get()
    if result == 0:
      self._set_grid_value(move_coords(self.coords, direction), '#')
      return False
    elif result == 1:
      c = '.'
    elif result == 2:
      c = 'O'
    else:
      raise Exception('Unexpected result: %s' % (repr(c)))
    self.coords = move_coords(self.coords, direction)
    self._set_grid_value(self.coords, c)
    if c == 'O':
      self.oxygen_coords = self.coords
    return True
      
    

class Solver():
  def __init__(self, input_data):
    self.robot = Robot(input_data)

  
  # Lets you move around manually.
  def explore_manually(self):
    while True:
      ch = get_ch()
      d = char_to_direction(ch)
      if d is None:
        continue
      if self.robot.move(d):
        for d in DIRECTIONS:
          self.robot.look(d)
      self.redraw()

  def redraw(self):
    os.system('clear')
    print_grid(self.robot.grid, robot_coords=self.robot.coords)


  def explore_location_dfs(self):
    initial_coords = self.robot.coords
    for d in DIRECTIONS:
      if not self.robot.explored(d):
        if self.robot.move(d):
          self.explore_location_dfs()
          self.robot.move(reverse_direction(d))
        assert self.robot.coords == initial_coords
        assert self.robot.explored(d)

  # Runs BFS and returns (success, distance).
  def run_bfs(self, grid, initial_location, target):
    frontiers = [initial_location]
    visited = set()
    distance = 0
    while True:
      for f in frontiers:
        assert f not in visited
        visited.add(f)
        c = self.robot.grid[f]
        if c == target:
          return (True, distance)

      new_frontiers = set()

      for f in frontiers:
        for d in DIRECTIONS:
          new_f = move_coords(f, d)
          if new_f not in visited and self.robot.grid[new_f] != '#':
            new_frontiers.add(new_f)
      if not new_frontiers:
        return (False, distance)

      frontiers = new_frontiers
      distance += 1
  
  
  # Solves part A
  def solve(self):
    # First, explore the entire map using DFS.
    self.explore_location_dfs()
    self.redraw()

    # BFS in the now-explored grid data.
    success, min_moves = self.run_bfs(self.robot.grid, (0,0), 'O')
    assert success
    print('min moves to oxygen = %d' % min_moves)
    print('oxygen coords = %s' % (self.robot.oxygen_coords,))

    success, dist = self.run_bfs(self.robot.grid, self.robot.oxygen_coords, '?')
    assert not success
    print('time = %d' % dist)




s = Solver(input_data)
s.solve()
