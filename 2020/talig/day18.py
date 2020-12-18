import sys
import functools
import operator
import re
import collections
import copy
import math
import grid

DAY = 18

def Parse(line):
  line = line.replace(')', ' )')
  line = line.replace('(', '( ')
  return line.split(' ')

def Eval(line, advanced = False):
  factors = Parse(line)
  if len(factors) == 3:
    return eval(line)
  p = line.rfind('(')
  while p != -1:
    cp = line.find(')', p) # find the next close paren
    value = Eval(line[p+1:cp], advanced)
    line = line[:p] + str(value) + line[cp+1:]
    p = line.rfind('(')
    
  if advanced:
    # Calculate all additions first
    factors = Parse(line)
    while '+' in factors:
      i = factors.index('+')
      value = eval(''.join(factors[i-1:i+2]))
      factors = factors[:i-1] + [str(value)] + factors[i+2:]
    line = ' '.join(factors)
      
  # No more parens
  factors = Parse(line)
  while len(factors) > 3:
    value = eval(''.join(factors[0:3]))
    factors = [str(value)] + factors[3:]
    line = ' '.join(factors)
  return eval(line)

    
def Test():
  lines = [('2 * 3 + (4 * 5)', 26),
           ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 437),
           ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 12240),
           ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 13632)]
  print('Test case one: ')
  for case in lines:
    print(Eval(case[0]) == case[1])  
  lines = [('2 * 3 + (4 * 5)', 46),
           ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 1445),
           ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 669060),
           ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 23340)]
  print('Test case two: ')
  for case in lines:
    print(Eval(case[0], True) == case[1])  

def main():
  f = open(sys.argv[1])
  lines = f.readlines()
  f.close()
  lines = [x.strip() for x in lines]
  
  Test()
  print('Day', DAY, ' part 1')
  results = []
  for line in lines:
    results.append(Eval(line))
  print('Sum of all results: ', sum(results))
  
  print('Day', DAY, ' part 2')
  results = []
  for line in lines:
    results.append(Eval(line, True))
  print('Sum of all results advanced: ', sum(results))
  

if __name__== '__main__':
  main()
