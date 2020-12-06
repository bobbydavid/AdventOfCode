# Find two numbers that sum to 2020 and multiply them. 
import sys
import functools
import operator
import re
import collections
import copy

DAY = 6

def GetGroupAnswerSets(lines, anyone):
  groups = []
  group = None
  for line in lines:
    if not line:
      groups.append(copy.deepcopy(group))
      group = None
    else:
      linegroup = set(line)
      if group is None: # setup is fine for both cases, but essential for intersection.
        group = linegroup
      if anyone: # part1
        group = group.union(linegroup)
      else:  # everyone. This is part 2
        group = group.intersection(linegroup)
  return groups

def GetSumOfGroupYes(groups):
  return sum([len(g) for g in groups])

def TestPart2():
  lines = ['abc','','a','b','c','','ab','ac','','a','a','a','a','','b','']
  groups = GetGroupAnswerSets(lines, False)
  print(GetSumOfGroupYes(groups) == 6)

def main():
  f = open(sys.argv[1])
  lines = f.readlines()
  f.close()
  lines = [x.strip() for x in lines]
  if lines[-1]: # not empty
    lines.append('') # Add a new line to the end if needed.
    
  groups = GetGroupAnswerSets(lines, True)
   
  print('Day', DAY, ' part 1')
  print('The sum of anyone in the group "yes"s is: ', GetSumOfGroupYes(groups))

  groups = GetGroupAnswerSets(lines, False)
  print('Day', DAY, ' part 2')
  print('The sum of everyone in the group "yes"s is: ', GetSumOfGroupYes(groups))


if __name__== '__main__':
  main()
