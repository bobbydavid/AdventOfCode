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
  binary = line.replace('F', '0')
  binary = binary.replace('B', '1')
  binary = binary.replace('L', '0')
  binary = binary.replace('R', '1')
  row = int(binary[:7], 2)
  column = int(binary[7:], 2)
  print(row, column)
  seat_id = row * 8 + column
  return row, column, seat_id
  

def ParseSeatData(lines):
  max_id = 0 
  seats = {}
  for line in lines:
    row, column, seat_id = GetSeatData(line)
    seats[seat_id] = True
    if seat_id > max_id:
      print('Found max!' , row, column, seat_id)
      max_id = seat_id
  return seats, max_id 

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
  
  seats, max_id = ParseSeatData(lines)
  print('Day', DAY, ' part 1')
  print('The maximal seat id is: ', max_id)

  print('Day', DAY, ' part 2')
  print('My seat is: ', FindGap(seats, max_id))


if __name__== '__main__':
  main()
