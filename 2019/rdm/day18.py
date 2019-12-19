import intcode
from collections import defaultdict
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



filename = 'day18.data'
if len(sys.argv) > 1:
  filename = sys.argv[1]
input_grid = []
with open(filename, 'r') as contents:
  input_grid = [[c for c in row.strip()
      ] for row in contents.read().strip().split('\n')]

def print_grid(grid, overlays = [], overlay_c = '*'):
  if overlays:
    overlays = set(overlays)
  output = ''
  for y, row in enumerate(grid):
    output_row = []
    for x, c in enumerate(row):
      if (x, y) in overlays:
        c = overlay_c
      output_row.append(c)
    output += ''.join(output_row) + '\n'
  print('%s\n' % output)
  time.sleep(0.1)


def find_keys(grid):
  keys = []
  for row in grid:
    for c in row:
      if is_key(c):
        keys.append(c)
  return keys


def count_keys(grid):
  return len(find_keys(grid))


def search_for(grid, needle):
  for y, row in enumerate(grid):
    for x, c in enumerate(row):
      if c == needle:
        return (x, y)
  return None

def is_door(c):
  return ord(c) >= ord('A') and ord(c) <= ord('Z')

def is_key(c):
  return ord(c) >= ord('a') and ord(c) <= ord('z')

def add_coords(a, b):
  return (a[0] + b[0], a[1] + b[1])


def read_grid(grid, coords):
  return grid[coords[1]][coords[0]]


# Maps from a key to all other.
# Value is (key, doors, dist, destination_coords)
_dest_map = {}
def precalculate_all_destinations(grid):
  print('precalculating...')
  keys = find_keys(grid)
  keys_set = set(keys)
  nodes = copy.deepcopy(keys)
  nodes.append('@')
  for source in nodes:
    values = []
    for sink in nodes:
      if sink == '@' or source == sink:
        continue
      coords = search_for(grid, source)
      candidates = old_find_candidate_moves(grid, keys_set, coords, target=sink)
      assert len(candidates) == 1, '%s %s %s' % (candidates, source, sink)
      sink_coords, dist_from_source, sink, doors = candidates[0]
      values.append( (sink, doors, dist_from_source, sink_coords) )
    values.sort(key=lambda x : x[2], reverse=True)
    _dest_map[source] = values
  print('...done.')
  """
  for source, sinks in _dest_map.iteritems():
    print('SOURCE: ' + source)
    for sink in sinks:
      print('  SINK: ' + repr(sink))
  sys.exit(1)
  """

def has_all_needed_keys(doors, keys):
  for door in doors:
    if string.lower(door) not in keys:
      return False
  return True
    
def find_candidate_moves(grid, keys, initial_coords):
  source = read_grid(grid, initial_coords)
  assert source in _dest_map, source
  candidates = []
  for key, doors, dist, sink_coords in _dest_map[source]:
    if not has_all_needed_keys(doors, keys):
      continue
    if key in keys:
      continue
    candidates.append( (sink_coords, dist, key, doors) )
  return candidates



# Returns a list of candidate moves in format
# (dest_coords, distance_from_initial_cords, whats_there, doors_crossed)
def old_find_candidate_moves(grid, keys, initial_coords, target=None):
  frontiers = [(initial_coords, [])]
  visited = {}
  distance = 0
  candidates = []

  visited[initial_coords] = distance
  while frontiers:
    #print_grid(grid, frontiers, str(distance))
    distance += 1
    new_frontiers = []
    for f, doors in frontiers:
      for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        neighbor_coords = add_coords(f, direction)
        if neighbor_coords in visited:
          continue
        c = read_grid(grid, neighbor_coords)
        if c == '#':
          continue
        if is_door(c):
          if string.lower(c) not in keys:
            continue
          doors.append(c)
        if c == target or (is_key(c) and not c in keys):
          # Found a candidate move.
          candidates.append( (neighbor_coords, distance, c, doors) )
          if target is not None:
            return candidates
          continue
        #assert c == '.' or is_key(c), 'c=%s' % c
        new_frontiers.append( (neighbor_coords, list(doors)) )
        visited[neighbor_coords] = distance
    frontiers = list(new_frontiers)
  return candidates


  

def showkeys(keys):
  keys = list(keys)
  keys.sort()
  return '%s (%d)' % (''.join(keys), len(keys))
          

INFINITY = float("inf")

class Params():
  def __repr__(self):
    members = [d for d in dir(self) if not d.startswith('__')]
    return '<%s>' % ', '.join(['%s=%s' % (m, getattr(self, m)) for m in members])

def recursive_search_for_solution(params, path, keys, coords, to_here):
  candidates = find_candidate_moves(params.grid, keys, coords)
  if False:  # Show debug?
    this_key = read_grid(params.grid, coords)
    print('From %s %s dist = %d, keys = %s:' % (
        this_key, coords, to_here, showkeys(keys)))
    for c in candidates:
      print('    %s %s, dist=%d, doors=%s' % (c[2], c[0], c[1], c[3]))
  best_soln = INFINITY
  for candidate in candidates:
    #print('examining: coords=%s, distance=%d, key=%s' % candidate)
    next_coords, distance, key, _ = candidate
    assert key not in keys

    next_dist = to_here + distance
    if  next_dist >= params.best_known:
      #print('Giving up, since %d is worse than best known' % next_dist)
      continue

    if len(keys) + 1 < params.max_keys:
      keys.add(key)
      path.append(key)
      soln = recursive_search_for_solution(
          params, path, keys, next_coords, next_dist)
      assert path[-1] == key
      path.pop()
      keys.remove(key)
    else:
      soln = next_dist
      params.best_known = min(params.best_known, soln)
      print('SOLUTION: %d, %s' % (soln, ', '.join(path)))
    best_soln = min(best_soln, soln)
  return best_soln


  
      
      



def solve_part_a(grid):
  print_grid(grid)
  start_coords = search_for(grid, '@')

  precalculate_all_destinations(grid)

  params = Params()
  params.grid = grid
  params.max_keys = count_keys(grid)
  params.best_known = INFINITY
  min_steps = recursive_search_for_solution(params, ['@'], set(), start_coords, 0)
  print('min_steps = %s' % min_steps)






solve_part_a(input_grid)


