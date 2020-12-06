# Find two numbers that sum to 2020 and multiply them. 
import sys
import functools
import operator
import re
import collections
import copy

DAY = 5

def GetSeatData(line):
  # Convert to binary
  binary = line.translate(str.maketrans('FBLR','0101'))
  seat_id = int(binary, 2)
  return seat_id
  

def ParseSeatData(lines):
  translation = str.maketrans('FBLR','0101')
  return sorted([int(x.translate(translation), 2) for x in lines])

def FindGap(seats, max_seat):
  # Find a missing seat id where +1 and -1 exist.
  for i in range(max_seat):
    if i not in seats and i+1 in seats and i - 1 in seats:
      return i

def test():
  cases = [('FBFBFFFLLL', (40, 0, 320)), ('FFBBBBFLRR', (30, 3, 243))]
  for case in cases:
    result = GetSeatData(case[0])
    if result != case[1]:
      print('Test failed: ' , case, ' : ', result)


def main():
  f = open(sys.argv[1])
  lines = f.readlines()
  lines = [x.strip() for x in lines]
  f.close()
  
  seats = ParseSeatData(lines)
  max_id = seats[-1]
  print('Day', DAY, ' part 1')
  print('The maximal seat id is: ', max_id)

  print('Day', DAY, ' part 2')
  print('My seat is: ', FindGap(seats, max_id))


if __name__== '__main__':
  main()
