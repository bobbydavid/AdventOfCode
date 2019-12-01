import sys

if len(sys.argv) < 2:
  sys.exit("forgot data file name: python day1.py <data file>")
filename = sys.argv[1]

print 'Data file: ' + filename
with open(filename, 'r') as content_file:
  total_fuel = 0
  for line in content_file.readlines():
    mass = int(line)
    fuel = mass / 3  - 2
    if fuel < 0:
      fuel = 0
    print 'fuel required: ' + str(fuel)
    total_fuel += fuel

  print 'total fuel: ' + str(total_fuel)

  
