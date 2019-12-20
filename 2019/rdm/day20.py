import sys
import aoc
import copy

FILENAME = "day20.data"
if len(sys.argv) > 1:
  FILENAME = sys.argv[1]



def read_grid(grid, coords):
  return aoc.read_grid(grid, coords, default=' ')



# Maps from coordinates to the teleporter available there.
def parse_teleporters(grid):
  ports = {}

  def add_port(name, left_coords, right_coords):
    sides = 0
    for coords in [left_coords, right_coords]:
      assert coords not in ports
      if read_grid(grid, coords) == '.':
        sides += 1
        ports[coords] = port_name
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

  #start_coords = find_start_coords(grid)
  ports = parse_teleporters(grid)
  links, start, end = analyze_teleporters(ports)
  print('start=%s, end=%s' % (start, end))
  dist = solve_bfs(grid, start, end, links)
  print('dist=%d' % dist)




solve_part_a()
