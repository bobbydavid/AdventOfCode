import sys

if len(sys.argv) < 2:
  sys.exit("forgot data file name: python day1.py <data file>")
filename = sys.argv[1]

# (center, satellite)
orbits = []
print 'Data file: ' + filename
with open(filename, 'r') as content_file:
  for line in content_file.readlines():
    orbits.append(line.strip().split(')'))

direct_orbits = {}
for pair in orbits:
  direct_orbits[pair[1]] = pair[0]

count = 0
for key in direct_orbits.keys():
  ptr = key
  while ptr in direct_orbits:
    count += 1
    ptr = direct_orbits[ptr]

print count

  
