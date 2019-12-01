# Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.

# (1)  What is the sum of the fuel requirements for all of the modules on your spacecraft?
# (2) Include the self weight of the fuel into the mass, until it's 0 or negative.

import math

f = open(r'day1_input.txt');
lines = f.readlines()
f.close()

def FuelFormula(mass):
  return math.floor(mass/3.0) - 2

def FuelPerModule(mass):
  next = FuelFormula(mass)
  cumulative = 0
  while (next > 0):
    cumulative += next
    next = FuelFormula(next)
  return cumulative
    
def TestFuel1():
  print 2 == FuelPerModule(12)
  print 2 == FuelPerModule(14)
  print 654 == FuelPerModule(1969)
  print 33583 == FuelPerModule(100756)

def TestFuel2():
  print 2, ' == ', FuelPerModule(14)
  print 966, ' == ', FuelPerModule(1969)
  print 50346,' == ', FuelPerModule(100756) 

def main():
	print 'Testing: '
	TestFuel2()

	print 'Executing: '
	fuel_per_module = []
	total = 0
	for line in lines:
		mod = FuelPerModule(int(line))
		total += mod
		fuel_per_module.append(mod)

	print("Total: ", total) 
  
if __name__== "__main__":
  main()
