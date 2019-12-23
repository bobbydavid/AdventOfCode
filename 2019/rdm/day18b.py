import intcode
from collections import defaultdict
from collections import deque
import string
import time
import copy
import sys
import threading
import os
import random
import tty
from Queue import Queue
import termios

#
# Longest-first search:
# 4576, k, a, u, z, p, t, b, c, e, x, d, w, o, v, s, l, h, m, j, q, f, n, r, g, y
# 4572, k, a, u, p, t, b, c, e, x, z, d, w, o, v, s, l, h, m, j, q, f, n, r, g, y
#
# Shortest-first search:
# 4532, s, p, z, b, x, e, c, k, u, v, o, w, d, a, t, l, f, q, j, m, h, n, r, g, y
# 4528, s, p, z, b, x, e, c, k, a, u, v, o, w, d, t, l, f, q, j, m, h, n, r, g, y
#
# Best order:
# ['p', 'k', 'a', 'z', 't', 'b', 'c', 'e', 'x', 'd', 'w', 'o', 'v', 'u', 's', 'l', 'h', 'm', 'j', 'q', 'f', 'n', 'r', 'g', 'y', 'i']

BEST_ORDER = ['p', 'k', 'z', 'a', 'b', 't', 'x', 'e', 'c', 's', 'u', 'v', 'o', 'w', 'd', 'l', 'f', 'q', 'j', 'm', 'h', 'n', 'r', 'g', 'y', 'i']



filename = 'day18.data'
if len(sys.argv) > 1:
  filename = sys.argv[1]
input_grid = {}
with open(filename, 'r') as contents:
  for y, row in enumerate(contents.readlines()):
    for x, c in enumerate(row.strip()):
      input_grid[(x,y)] = c



def print_grid(grid):
  max_x = max(x for x, _ in grid.keys())
  max_y = max(y for _, y in grid.keys())
  out = []
  for y in range(max_y + 1):
    for x in range(max_x + 1):
      out.append(grid[(x, y)])
    out.append('\n')
  print ''.join(out)


def is_key(c):
  return c >= 'a' and c <= 'z'


def is_door(c):
  return c >= 'A' and c <= 'Z'


def have_all_keys(doors, keys):
  for door in doors:
    assert is_door(door)
    key_needed = door.lower()
    if key_needed not in keys:
      return False
  return True


def find_start(grid):
  for (x, y), c in grid.items():
    if c == '@':
      return (x, y)


# Returns a map from a key to its coordinates.
def find_keys(grid):
  key_map = {}
  for (x, y), c in grid.items():
    if is_key(c):
      key_map[c] = (x, y)
  return key_map


def merge_strings(strs):
  sorted_strs= list(strs)
  sorted_strs.sort()
  return ''.join(sorted_strs)


def add_coords(a, b):
  return (a[0] + b[0], a[1] + b[1])


# Represents a path between two locations.
class Path():
  def __init__(self, start, end, distance, doors):
    self.start = start
    self.end = end
    self.distance = distance
    self.doors = doors

  def __repr__(self):
    return '%s -> %s (%s) doors: %s' % (self.start, self.end, self.distance, merge_strings(self.doors))


class Frontier():
  def __init__(self, coords, distance, doors=set()):
    self.coords = coords
    self.distance = distance
    self.doors = doors

  def adjacent(self, new_coords):
    return Frontier(new_coords, self.distance + 1, copy.copy(self.doors))


# Finds the distance from the start coords to every key.
# Returns a map from key to distance.
def calc_distances(grid, start_coords):
  dist = 0

  paths = []
  start = grid[start_coords]


  visited = set([start_coords])
  frontiers = deque()
  frontiers.append(Frontier(start_coords, 0))
  while frontiers:
    frontier = frontiers.popleft()

    # Process our current location.
    c = grid[frontier.coords]
    if is_key(c):
      paths.append(Path(start, c, frontier.distance, frontier.doors))

    if is_door(c):
      frontier.doors.add(c)

    # Queue up the unvisited neighbors of this location to be processed.
    for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
      neighbor_coords = add_coords(frontier.coords, direction)
      neighbor = grid[neighbor_coords]
      if neighbor == '#' or neighbor_coords in visited:
        continue
      visited.add(neighbor_coords)
      frontiers.append(frontier.adjacent(neighbor_coords))

  return paths


# Returns a map of paths, keyed by (start,end).
def find_all_paths(grid, start_coords):
  starts = list(find_keys(grid).values())
  starts.append(find_start(grid))

  edges = {}
  for start_coords in starts:
    paths = calc_distances(grid, start_coords)
    start = grid[start_coords]
    edges[start] = paths
  return edges




# Returns the shortest path to collect all keys, starting at `coords`,
# and assuming we already are holding `keys`.
#
#
# The cache is keyed by the start location and the keys we have.
def find_min_steps(grid, edges, cache, loc, keys):
  cache_key = '%s|%s' % (loc, merge_strings(keys))
  if cache_key in cache:
    return cache[cache_key]

  relevant_paths = []
  for path in edges[loc]:
    if have_all_keys(path.doors, keys) and path.end not in keys:
      relevant_paths.append(path)

  if not relevant_paths:
    # This should only happen if we have all of the keys.
    # The answer is 0: we don't have to travel at all because we already have
    # all the keys.
    assert len(find_keys(grid)) == len(keys), '%s\n%s' % (keys, find_keys(grid))
    return 0

  min_dist = float("inf")
  for path in relevant_paths:
    assert path.end not in keys
    keys.add(path.end)
    dist = path.distance + find_min_steps(grid, edges, cache, path.end, keys)
    keys.remove(path.end)
    if dist < min_dist:
      min_dist = dist

  cache[cache_key] = min_dist
  return min_dist






def solve_part_a(grid):
  print_grid(grid)
  start_coords = find_start(grid)
  edges = find_all_paths(grid, start_coords)

  cache = {}
  steps = find_min_steps(grid, edges, cache, '@', set())
  print(steps)

solve_part_a(input_grid)

