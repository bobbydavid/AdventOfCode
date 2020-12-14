import sys
import functools
import operator
import re
import collections
import copy
import math

DAY = 14
MASK_INDEX = 7
MEM = r'^mem\[(\d+)\] = (\d+)$'

class Computer():
  def __init__(self):
    self.mem = {}
    self.mask = 'X'*36

  def SetMask(self, mask):
    self.mask = mask

  def GetAddressList(self, binary, addresses):
    for i in range(len(self.mask)):
      if self.mask[i] != 'X':
        val = str(int(self.mask[i]) | int(binary[i]))
        for j in range(len(addresses)):
          addresses[j][i] = val
      else:
        new_addresses = copy.deepcopy(addresses)
        for j in range(len(addresses)):
          addresses[j][i] = '1'
          new_addresses[j][i] = '0'
        addresses.extend(new_addresses)
    return 
      
  def WriteToMemoryVer1(self,location, value):
    # Apply mask on value
    binary = "{0:b}".format(value).zfill(36)
    bin_str = ['0'] * 36
    for i in range(len(self.mask)):
      m = self.mask[i]
      bin_str[i] = binary[i] if m == 'X' else m
    self.mem[location] = int(''.join(bin_str), 2)
  
  def WriteToMemoryVer2(self, location, value):
    binary = "{0:b}".format(location).zfill(36)
    # Initialize with one address, all zeroes.
    addresses = [['0']*36]
    self.GetAddressList(binary, addresses)
    for address in addresses:
      self.mem[int(''.join(address),2)] = value
  
  def SumMemoryValues(self):
    return sum(self.mem.values())

def ParseInput(lines, ver2=False):
  c = Computer()
  for line in lines:
    match = re.findall(MEM, line)
    if match:
      if ver2:
        c.WriteToMemoryVer2(int(match[0][0]), int(match[0][1]))
      else:
        c.WriteToMemoryVer1(int(match[0][0]), int(match[0][1]))
    else:
      c.SetMask(line[MASK_INDEX:])
  return c

def Test():
  lines = ['mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X',
          'mem[8] = 11',
          'mem[7] = 101',
          'mem[8] = 0']
  c = ParseInput(lines)
  print('Passed case 1:', c.SumMemoryValues() == 165)

  lines = ['mask = 000000000000000000000000000000X1001X',
           'mem[42] = 100',
           'mask = 00000000000000000000000000000000X0XX',
           'mem[26] = 1']
  c = ParseInput(lines, True)
  print('Passed case 2:', c.SumMemoryValues() == 208)

def main():
  f = open(sys.argv[1])
  lines = f.readlines()
  f.close()
  lines = [x.strip() for x in lines]

  Test()
  print('Day', DAY, ' part 1')
  c = ParseInput(lines)
  print('Sum of memory values:', c.SumMemoryValues())
  
  print('Day', DAY, ' part 2')
  c2 = ParseInput(lines, True)
  print('Sum of memory values:', c2.SumMemoryValues())
  

if __name__== '__main__':
  main()
