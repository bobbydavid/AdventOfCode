import copy
import math
import sys
import itertools

if len(sys.argv) < 2:
  sys.exit("forgot data file name: python day1.py <data file>")
filename = sys.argv[1]

space = []
print('Data file: ' + filename)
with open(filename, 'r') as content_file:
  for line in content_file.readlines():
    space.append(list(line.strip()))

def is_occluded(seen, coords):
  for s in seen:
    if math.atan2(s[1], s[0]) == math.atan2(coords[1], coords[0]):
      return True
  return False


def count_astroids(space, root_coords):
  seen = []
  #print('# Considering %s' % (root_coords,))
  for y, row in enumerate(space):
    for x, loc in enumerate(row):
      if loc != '#':
        continue
      coords = (x - root_coords[0], y - root_coords[1])
      if coords != (0, 0) and not is_occluded(seen, coords):
        seen.append(coords)

  return len(seen)


best_loc = None
max_count = 0
for y, row in enumerate(space):
  for x, loc in enumerate(row):
    if loc == '#':
      count = count_astroids(space, (x, y))
      #print('# at %s, count = %d' % ((x, y), count))
      if count > max_count:
        max_count = count
        best_loc = (x, y)


for y, row in enumerate(space):
  for x, loc in enumerate(row):
    if x == best_loc[0] and y == best_loc[1]:
      assert loc == '#'
      loc = '*'
    sys.stdout.write(loc)
  sys.stdout.write('\n')

print('max count = %d at (%d, %d)' % ((max_count,) + best_loc))

