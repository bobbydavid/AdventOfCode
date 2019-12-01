import sys

if len(sys.argv) < 2:
  sys.exit("forgot data file name: python day1.py <data file>")
filename = sys.argv[1]

print 'Data file: ' + filename
modules = []
with open(filename, 'r') as content_file:
  for line in content_file.readlines():
    modules.append(int(line))

print modules

total_fuel = 0
while not len(modules) == 0:
  mass = modules.pop()
  fuel = mass / 3 - 2
  if fuel > 0:
    modules.append(fuel)
    total_fuel += fuel
print 'total fuel: ' + str(total_fuel)
