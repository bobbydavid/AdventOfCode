import copy
import sys

if len(sys.argv) < 2:
  sys.exit("forgot data file name: python day1.py <data file>")
filename = sys.argv[1]

print 'Data file: ' + filename
with open(filename, 'r') as content_file:
  lines = content_file.readlines()
  assert len(lines) == 2
  line1_raw = [x for x in lines[0].strip().split(',') if x]
  line2_raw = [x for x in lines[1].strip().split(',') if x]

# format (h, j1, j2) where j2 > j1
up1 = []
right1 = []
up2 = []
right2 = []

def process_data(raw_data, up, right):
  x = 0  # right
  y = 0  # up
  for segment in raw_data:
    direction = segment[0]
    distance = int(segment[1:])
    if direction == 'U':
      up.append((x, y, y + distance))
      y = y + distance
    elif direction == 'D':
      up.append((x, y - distance, y))
      y = y - distance
    elif direction == 'L':
      right.append((y, x-distance, x))
      x = x - distance
    elif direction == 'R':
      right.append((y, x, x + distance))
      x = x + distance
    else:
      assert Fail, 'unknown direction: ' + direction

process_data(line1_raw, up1, right1)
process_data(line2_raw, up2, right2)

overlap_points = []
def find_parallel_overlaps(set_a, set_b, is_vertical):
  for a in set_a:
    for b in set_b:
      if a[0] != b[0]:
        continue
      # these lines are on the same axis, any overlapping values count.
      start = max(a[1], b[1])
      end = min(a[2], b[2])
      for value in range(start, end + 1):
        if is_vertical:
          point = (value, a[0])
        else:
          point = (a[0], value)
        overlap_points.append(point)

def find_overlaps(vert_set, horiz_set):
  for v in vert_set:
    for h in horiz_set:
      x = v[0]
      y = h[0]
      if x >= h[1] and x <= h[2] and y >= v[1] and y <= v[2]:
        overlap_points.append((x, y))
      


#find_parallel_overlaps(up1, up2, True)
#find_parallel_overlaps(right1, right2, False)

find_overlaps(up1, right2)
find_overlaps(up2, right1)

print overlap_points

distances = [abs(x[0]) + abs(x[1]) for x in overlap_points]
print min(distances)
  
  





