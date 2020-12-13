import sys
import functools
import operator
import re
import collections
import copy
import math

DAY = 13

def FindBus(earliest_departure, bus_ids):
  min_dep = sys.maxsize
  min_bid = None
  for bid, idx in bus_ids:
    mul = earliest_departure // bid
    departure = bid * (mul + 1)
    if departure < min_dep:
      min_dep = departure
      min_bid = bid
  return min_bid, min_dep - earliest_departure    

def ParseInput(line):
  ids = line.split(',')
  bus_ids = []
  for i in range(len(ids)):
    if ids[i] != 'x':
      bus_ids.append((int(ids[i]),i))
  bus_ids = sorted(bus_ids)
  bus_ids.reverse()
  return bus_ids

def VerifyWindow(bus_ids, t):
  for bid, i in bus_ids:
    if (t+i) % bid != 0:
        return False
  return True

def CalcTimeStamp(bus_ids, start_at=None): # Brute force
  # Find timestamp t such that:
  # (t + i) % bus_ids[i] = 0
  # We need a window of size len(bus_ids).
  max_id, i = bus_ids[0]
  if start_at != None:
    start_at = max_id * (start_at // max_id + 1)
  else:
    start_at = max_id
  for t in range(start_at, sys.maxsize, max_id):
    if VerifyWindow(bus_ids, t-i):
      return t-i
  return None

def lcm(a, b):
  return abs(a*b) // math.gcd(a, b)

def ReduceBuses(bus_ids):
  k = sorted(copy.deepcopy(bus_ids))
  while len(k) > 1:
    a = k.pop()
    b = k.pop()
    ablcm = lcm(a[0],b[0])
    #
    t = CalcTimeStamp([a,b])
    k.append((ablcm, -t % ablcm ))
  return k[0]

def Test():
  lines = ['939', '7,13,x,x,59,x,31,19']
  departure = int(lines[0])
  bus_ids = ParseInput(lines[1])
  my_bus, wait_time = FindBus(departure, bus_ids)
  if my_bus * wait_time == 295:
    print('Passed test')
  else:
    print('Failed!', my_bus, wait_time, earliest_departure)

  test_cases = [('7,13,x,x,59,x,31,19', 1068781),
                ('17,x,13,19', 3417),
                ('67,7,59,61', 754018),
                ('67,x,7,59,61', 779210),
                ('67,7,x, 59,61', 1261476),
                ('1789,37,47,1889', 1202161486)]
  for case in test_cases:
    bus_ids = ParseInput(case[0])
    print ('Testing: ', case)
    print ('Verifying on output:', VerifyWindow(bus_ids, case[1]))
    print (CalcTimeStamp(bus_ids) == case[1])
    ans = ReduceBuses(bus_ids)
    print ('Or another way: ', -ans[1] % ans[0] ==  case[1])

def main():
  f = open(sys.argv[1])
  lines = f.readlines()
  f.close()
  lines = [x.strip() for x in lines]

  #Test()
  departure = int(lines[0])
  bus_ids = ParseInput(lines[1])
  my_bus, wait_time = FindBus(departure, bus_ids)
  
  print('Day', DAY, ' part 1')
  print('Bus ID * wait time: ', my_bus * wait_time) # 3215
  
  print('Day', DAY, ' part 2')
  ans = ReduceBuses(bus_ids)
  t = ans[0] - ans[1]
  print('Earliest timestamp t maintaining all properties is: ', t, ' Verifying: ', VerifyWindow(bus_ids, t)) # 1001569619313439
  

if __name__== '__main__':
  main()
