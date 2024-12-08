import sys
import math
import time
import os
from copy import deepcopy

class Equation():
  def __init__(self, line):
    line = line.strip()
    self.result, numbers = line.split(':')
    numbers = numbers.strip()
    self.result = int(self.result)
    self.numbers = [int(x) for x in numbers.split(' ')]

  def computeAllOptions(self, part2):
    options = set([self.numbers[0]])
    for n in self.numbers[1:]:
      step = set()
      for option in options:
        step.add(option * n)
        step.add(option + n)
        if part2:
          step.add(int(str(option)+str(n)))
      options = step
    return set(options)
     
  def isSatisfiable(self, part2=False):
    options = self.computeAllOptions(part2)
    if self.result in options:
      return True
    return False

def parse(lines):
  equations = []
  for line in lines:
    line = line.strip()
    equations.append(Equation(line))
  return equations
  
def main():
  f = open(sys.argv[1])
  equations = parse(f.readlines())
  f.close()
  
  satisfiable = []
  total = 0
  for e in equations:
    # Run with False for part 1, with True for part 2.
    if e.isSatisfiable(True):
      total += e.result
      satisfiable.append(e)
      
  print("Result part1:", total)


if __name__=="__main__":
  main()
