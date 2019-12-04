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

# format (h, j1, j2, steps_to_h, is_flipped) where j2 > j1
up1 = []
right1 = []
up2 = []
right2 = []

def process_data(raw_data, up, right):
  x = 0  # right
  y = 0  # up
  steps = 0  # initial wire length
  for segment in raw_data:
    direction = segment[0]
    distance = int(segment[1:])
    if direction == 'U':
      up.append((x, y, y + distance, steps, False))
      y = y + distance
    elif direction == 'D':
      up.append((x, y - distance, y, steps, True))
      y = y - distance
    elif direction == 'L':
      right.append((y, x-distance, x, steps, True))
      x = x - distance
    elif direction == 'R':
      right.append((y, x, x + distance, steps, False))
      x = x + distance
    else:
      assert Fail, 'unknown direction: ' + direction
    steps += distance

process_data(line1_raw, up1, right1)
process_data(line2_raw, up2, right2)


def find_shortest_dist(vert_set, horiz_set):
  overlap_points = []
  min_steps = -1
  for v in vert_set:
    for h in horiz_set:
      x = v[0]
      y = h[0]
      if x >= h[1] and x <= h[2] and y >= v[1] and y <= v[2]:
        origin_x = h[3]
        origin_y = v[3]
        steps = origin_x + origin_y
        if h[4]:  #RTL
          steps += (h[2] - x)
        else:     #LTR
          steps += (x - h[1])
        if v[4]:  #TTB
          steps += (v[2] - y)
        else:     #BTT
          steps += (y - v[1])
        overlap_points.append((x, y, steps))
        if min_steps == -1 or min_steps > steps:
          min_steps = steps
  print 'overlap points:'
  print overlap_points
  return min_steps



# Runs twice. Pick the output that's smaller between the two.
dist1 = find_shortest_dist(up1, right2)
dist2 = find_shortest_dist(up2, right1)
print 'min distance: %d' % min(dist1, dist2)

