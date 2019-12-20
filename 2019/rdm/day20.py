import sys
import aoc
import copy

FILENAME = "day20.data"
if len(sys.argv) > 1:
  FILENAME = sys.argv[1]



def read_grid(grid, coords):
  return aoc.read_grid(grid, coords, default=' ')



# Maps from coordinates to the teleporter available there.
# Upper-case for big, lower-case for small.
def parse_teleporters(grid):
  ports = {}

  def add_port(name, left_coords, right_coords):
    sides = 0
    for coords in (left_coords, right_coords):
      assert coords not in ports
      name = port_name
      if read_grid(grid, coords) == '.':
        sides += 1
        ports[coords] = name
    assert sides == 1, sides

  # Look for horizontal teleporters.
  for y, row in enumerate(grid):
    for x in range(len(row) - 1):
      c1 = row[x]
      c2 = row[x + 1]
      if c1.isalpha() and c2.isalpha():
        port_name = c1 + c2
        add_port(port_name, (x-1,y), (x+2,y))
  # Look for vertical teleporters.
  for x in range(len(grid[0])):
    for y in range(len(grid) - 1):
      c1 = read_grid(grid, (x,y))
      c2 = read_grid(grid, (x,y+1))
      if c1.isalpha() and c2.isalpha():
        port_name = c1 + c2
        add_port(port_name, (x,y-1), (x,y+2))
  return ports


# Input is map from coords to teleporter.
# Output is a teleporter link map (coords to coords) and start/end:
# output format: (link_map, start, end)
def analyze_teleporters(ports):
  link_map = {}
  found = {}  # Previously found port, keyed by name
  for coords, name in ports.iteritems():
    if name in found:
      other_coords = found[name]
      assert other_coords is not None
      assert coords not in link_map
      assert other_coords not in link_map
      link_map[coords] = other_coords
      link_map[other_coords] = coords
      found[name] = None
    else:
      found[name] = coords
  found = {k: v for (k,v) in found.items() if v is not None}
  assert len(found) == 2
  assert "AA" in found, found
  assert "ZZ" in found, found
  return (link_map, found["AA"], found["ZZ"])



def solve_bfs(grid, start, end, links):
  frontiers = [start]
  dist = 0
  end_dist = None
  visited = set(frontiers)
  while end_dist is None and frontiers:
    dist += 1
    new_frontiers = []
    for coords in frontiers:
      choices = []
      # Find dots we can walk to.
      for d in ((0, -1), (1, 0), (0, 1), (-1, 0)):
        n_coords = aoc.add_coords(coords, d)
        if read_grid(grid, n_coords) == '.':
          choices.append(n_coords)
      # Peek through teleporters.
      if coords in links:
        out = links[coords]
        choices.append(out)
      # Remove places we already visited.
      choices = [c for c in choices if c not in visited]
      # Each choice becomes a new frontier.
      for c in choices:
        if c == end:
          end_dist = dist
        else:
          new_frontiers.append(c)
          visited.add(c)
    frontiers = new_frontiers
  if end_dist is None:
    raise Exception('could not find path')
  return end_dist



def solve_part_a():
  grid = aoc.load_file_as_grid(FILENAME)
  aoc.print_grid(grid)

  ports = parse_teleporters(grid)
  links, start, end = analyze_teleporters(ports)
  print('start=%s, end=%s' % (start, end))
  dist = solve_bfs(grid, start, end, links)
  print('dist=%d' % dist)



class Teleporter():
  def __init__(self, name, s, g):
    self.name = name
    self.shrink = s
    self.grow = g

  def __repr__(self):
    return '%s<%s->%s>' % (self.name, self.shrink, self.grow)







# teleporters get upper-case names for the outside and lower for inside.
def parse_teleporters_part_b(grid):
  ports = {}

  def add_port(name, midway, left_coords, right_coords):
    sides = 0
    for coords, small in [(left_coords, midway), (right_coords, not midway)]:
      assert coords not in ports
      name = port_name.lower() if small else port_name
      if read_grid(grid, coords) == '.':
        sides += 1
        ports[coords] = name
    assert sides == 1, sides


  # Look for horizontal teleporters.
  for y, row in enumerate(grid):
    midway = False  # Initially False, becomes true after midway
    for x in range(len(row) - 1):
      c1 = row[x]
      c2 = row[x + 1]
      if c1.isalpha() and c2.isalpha():
        port_name = c1 + c2
        add_port(port_name, midway, (x-1,y), (x+2,y))
      if x >= len(row) / 2:
        midway = True
  # Look for vertical teleporters.
  for x in range(len(grid[0])):
    midway = False
    for y in range(len(grid) - 1):
      c1 = read_grid(grid, (x,y))
      c2 = read_grid(grid, (x,y+1))
      if c1.isalpha() and c2.isalpha():
        port_name = c1 + c2
        add_port(port_name, midway, (x,y-1), (x,y+2))
      if y >= len(grid) / 2:
        midway = True
  return ports


# Input is map from coords to teleporter door.
#
# Output format: (shrink_links, grow_links, start, end)
# Note: links are coords -> Teleporter
def analyze_teleporters_part_b(ports):
  shrink_links = {}
  grow_links = {}
  # Previously found port, keyed by name.
  # Value is (coords, is_grow).
  found = {}
  for coords, orig_name in ports.iteritems():
    name = orig_name.upper()
    is_grow = (name == orig_name)

    if name in found:
      other_coords, other_is_grow = found[name]
      assert other_coords is not None
      assert coords not in shrink_links
      assert coords not in grow_links
      assert other_coords not in shrink_links
      assert other_coords not in grow_links
      assert is_grow != other_is_grow

      grow_coords = coords if is_grow else other_coords
      shrink_coords = other_coords if is_grow else coords

      t = Teleporter(name, shrink_coords, grow_coords)
      grow_links[shrink_coords] = t
      shrink_links[grow_coords] = t

      found[name] = None
    else:
      found[name] = (coords, is_grow)
  found = {k: v for (k,v) in found.items() if v is not None}
  assert len(found) == 2
  assert "AA" in found, found
  assert "ZZ" in found, found
  return (shrink_links, grow_links, found["AA"][0], found["ZZ"][0])



def solve_bfs_part_b(grid, start, end, shrink_links, grow_links):
  frontiers = [(start, 0, 0, [])]
  paused_frontiers = []
  max_size = 0
  end_dist = None
  best_path = None
  visited = {}
  visited[0] = {start: 0}
  while end_dist is None and frontiers:
    #print('%s' % (frontiers,))
    new_frontiers = []
    for coords, size, dist, path in frontiers:
      choices = []
      # Find dots we can walk to.
      for d in ((0, -1), (1, 0), (0, 1), (-1, 0)):
        n_coords = aoc.add_coords(coords, d)
        if read_grid(grid, n_coords) == '.':
          choices.append((n_coords, size, None))
      # Peek through teleporters.
      if coords in shrink_links:
        t = shrink_links[coords]
        choices.append((t.shrink, size - 1, t))
      if coords in grow_links:
        t = grow_links[coords]
        choices.append((t.grow, size + 1, t))
      # Each choice becomes a new frontier, unless it sucks.
      for coords, size, teleporter in choices:
        new_dist = dist + 1
        # Check this map and every one closer.
        if size not in visited:
          visited[size] = {}
        vmap = visited[size]
        if coords in vmap and vmap[coords] < new_dist:
          continue
        vmap[coords] = new_dist

        # New info for this frontier.
        new_path = copy.copy(path)
        if teleporter is None:
          new_path.append(coords)
        else:
          new_path.append((teleporter, size))
        if coords == end and size == 0:
          # Found the exit.
          end_dist = new_dist
          best_path = new_path
        else:
          # Need to keep searching.
          if size > 0:
            # Disallow getting larger than the max.
            continue
          elif abs(size) <= max_size:
            f = new_frontiers
          else:
            #print('pausing frontier: %s' % (coords,))
            f = paused_frontiers
          f.append((coords, size, new_dist, new_path))
    frontiers = new_frontiers
    if not frontiers and end_dist is None:
      max_size += 1
      print('expanding search to %d' % max_size)
      frontiers = paused_frontiers
      paused_frontiers = []
  if end_dist is None:
    raise Exception('could not find path')
  print 'best path: '
  prev_t = Teleporter("AA", None, None)
  skipped = 0
  steps = 0
  for p in best_path:
    if len(p) == 2 and isinstance(p[0], Teleporter):
      t, size = p
      print('walk from %s to %s (%d steps)' % (prev_t.name, t.name, skipped))
      print('Recurse into level %d through %s (1 step)' % (size, t.name))
      steps += skipped + 1
      skipped = 0
      prev_t = t
    else:
      skipped += 1
  steps += skipped
  print('walk from %s to finish (%d steps)' % (prev_t.name, skipped))
  print('total: %d' % steps)
  return end_dist

def solve_part_b():
  grid = aoc.load_file_as_grid(FILENAME)
  aoc.print_grid(grid)

  #start_coords = find_start_coords(grid)
  ports = parse_teleporters_part_b(grid)
  shrink_links, grow_links, start, end = analyze_teleporters_part_b(ports)
  print('start=%s, end=%s' % (start, end))
  print('shrink=%s' % shrink_links)
  print('grow=%s' % grow_links)
  dist = solve_bfs_part_b(grid, start, end, shrink_links, grow_links)
  print('dist=%d' % dist)


solve_part_b()
