import sys
from collections import defaultdict

if len(sys.argv) < 2:
  sys.exit("forgot data file name: python day1.py <data file>")
filename = sys.argv[1]

# (center, satellite)
orbits = []
print 'Data file: ' + filename
with open(filename, 'r') as content_file:
  for line in content_file.readlines():
    orbits.append(line.strip().split(')'))

# Map from an object to exit points (places to transfer to).
# These are all objects orbiting it, plus the thing it orbits.
exits = defaultdict(list)
for center, satellite in orbits:
  exits[center].append(satellite)
  exits[satellite].append(center)
  if satellite == 'YOU':
    start_loc = center
  elif satellite == 'SAN':
    end_loc = center


def run():
  # Objects we already visited.
  visited = set()
  # Locations where BFS is active.
  frontiers = [start_loc]
  # Current distance we have travelled in each frontier.
  dist = 0
  while frontiers:
    dist += 1
    new_frontiers = []
    for loc in frontiers:
      for exit in exits[loc]:
        if exit == end_loc:
          return dist  # We found our destination
        elif exit not in visited:
          visited.add(exit)
          new_frontiers.append(exit)
    frontiers = new_frontiers

    
print run()
    
