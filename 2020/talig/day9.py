# Find two numbers that sum to 2020 and multiply them. 
import sys
import functools
import operator
import re
import collections
import copy

DAY = 9
LEN_PREAMBLE = 25

def HasProperty(prior25, current):
  for k in prior25:
    val = current - k
    if val != k and val in prior25:
      return True
  return False

def FindFirstInvalid(lines):
  for i in range(LEN_PREAMBLE, len(lines)):
    if not HasProperty(set(lines[i-LEN_PREAMBLE:i]), lines[i]):
      return lines[i]

def FindContigousSum(lines, target):
  sums = {}
  for i in range(len(lines)):
    total = 0
    j = i
    while j < len(lines) and total < target:
      total += lines[j]
      j += 1
    if total == target:
      return (i,j)
    

def main():
  f = open(sys.argv[1])
  lines = f.readlines()
  f.close()
  lines = [int(x.strip()) for x in lines]
  
  print('Day', DAY, ' part 1')
  first_invalid = FindFirstInvalid(lines)
  print('The first number that does not have the desired property is:', first_invalid)

  print('Day', DAY, ' part 2')
  start, end = FindContigousSum(lines, first_invalid)
  smallest = min(lines[start:end+1])
  largest = max(lines[start:end+1])
  print('Sum of smallest and largest number in sequence:', smallest+largest)
  

if __name__== '__main__':
  main()
