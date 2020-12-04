# Find two numbers that sum to 2020 and multiply them. 
import sys
import functools
import operator
import re

DAY = 3
TREE = '#'

def CountTrees(lines, right, down):
  i,j = (0,0)
  wrap = len(lines[0])
  trees = 0
  while j < len(lines):
    if lines[j][i] == TREE:
      trees += 1
    i = (i + right) % wrap
    j += down
  return trees
    

def main():
  f = open(sys.argv[1])
  lines = f.readlines()
  lines = [x.strip() for x in lines]
  f.close()
  
  # map of slope to number of trees.
  slopes = {(1,1):0, (3,1):0, (5,1):0, (7,1):0, (1,2):0}
  

  print('Day', DAY, ' part 1')
  print('There are ', CountTrees(lines, 3, 1), ' trees on this path.') # 259 for my input

  print('Day', DAY, ' part 2')
  product = 1
  for slope in slopes:
    trees = CountTrees(lines, slope[0], slope[1])
    slopes[slope] = trees
  print(slopes)
  product = functools.reduce(operator.mul, slopes.values())
  print('Product of all trees per slope ', product) # 2224913600 for my input



if __name__== '__main__':
  main()
