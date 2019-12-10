import copy
from collections import defaultdict
import curses
import math
import os
import sys
import itertools

if len(sys.argv) < 2 or len(sys.argv) > 3:
  sys.exit("format it like this: python day1.py <data file> start,coords")
filename = sys.argv[1]
if len(sys.argv) == 3:
  initial_coords = map(int, sys.argv[2].split(','))
elif filename.endswith('day10.data'):
  initial_coords = (29,28)
elif filename.endswith('day10_test3.data'):
  initial_coords = (8, 3)
elif filename.endswith('day10_test4.data'):
  initial_coords = (11,13)
else:
  raise Exception('Not sure what initial coordinates to use?')


space = []
print('Data file: ' + filename)
with open(filename, 'r') as content_file:
  for line in content_file.readlines():
    space.append(list(line.strip()))


def analyze_astroids(space, root_coords, target, draw_grid = None):
  space[root_coords[1]][root_coords[0]] = 'L'
  # map from angle to all astroid coords at that angle.
  astroids_map = defaultdict(list)
  for y, row in enumerate(space):
    for x, ch in enumerate(row):
      if ch != '#':
        continue
      coords = (x - root_coords[0], y - root_coords[1])
      if coords == (0, 0):
        continue  # Don't blow ourselves up.
      angle = math.atan2(-coords[0], coords[1])
      astroids_map[angle].append(coords)
  # Convert to a list of lists, sorted by angle.
  astroids = list(astroids_map.iteritems())
  astroids.sort(key=lambda x : x[0])  # Sort based on angle
  # If the last element is PI (i.e. straight up), move it to the front.
  if astroids[-1][0] == math.pi:
    astroids = astroids[-1:] + astroids[:-1]
  # Get rid of angle information.
  astroids = [x[1] for x in astroids]
  # Sort each list by manhattan distance.
  for a_list in astroids:
    a_list.sort(key=lambda x : x[0] ** 2 + x[1] ** 2)
  # Explode rows in order until we reach the 200th astroid.
  exploded = 0
  while True:
    empty_list_count = 0
    for a_list in astroids:
      if not a_list:
        empty_list_count += 1
        continue
      coords = a_list.pop(0)
      orig_coords = (root_coords[0] + coords[0], root_coords[1] + coords[1])
      exploded += 1
      if draw_grid is not None:
        space[orig_coords[1]][orig_coords[0]] = '*'
        draw_grid(space)
      if exploded == target:
        return orig_coords
    if empty_list_count == len(astroids):
      raise Exception('Ran out of astroids to explode before reaching %d' % target)
    
    
  #initial_coords = (29, 28)  # for day10.data
  #initial_coords = (8,3)  # for day10_test3.data
  #initial_coords = (11,13)  # for day10_test4.data

try :
  stdscr = curses.initscr()
  curses.noecho()
  curses.cbreak()
  stdscr.clear()


  stdscr.addstr(0, 0, 'Press `n` to blow up the next astroid.')
  stdscr.addstr(1, 0, 'Press `s` to skip to the end.')
  stdscr.addstr(2, 0, 'Press `q` to quit.')
  _ = stdscr.getch()
  stdscr.clear()

  redrawing = True
  def repaint(grid):
    global redrawing
    for y, row in enumerate(space):
      for x, c in enumerate(row):
        if c == '.':
          c = ' '
        elif c == '*':
          c = '.'
        stdscr.addch(y, x, c)
    stdscr.refresh()
    while redrawing:
      c = chr(stdscr.getch())
      if c == 'n':
        break
      elif c == 's':
        redrawing = False
        break
      elif c == 'q':
        sys.exit(0)
  coords = analyze_astroids(space, initial_coords, 200, draw_grid=repaint)

finally:
  curses.nocbreak()
  stdscr.keypad(False)
  curses.echo()
  curses.endwin()

print('200th astroid is %s. answer = %d' % (coords, coords[0] * 100 + coords[1]))
