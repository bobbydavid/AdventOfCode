import collections
import re
from os import system
import sys
import math
import time

def CalcPower(x, y, serial):
  rack_id = x+10
  power = rack_id * y
  power += serial
  power = power * rack_id
  power = (power%1000)/100
  power -= 5
  return power

class Grid:
  def __init__(self,serial, rows=300, cols=300):
    self.grid = []
    self.serial = serial
    self.rows = rows
    self.cols = cols
    for y in range(rows):
      self.grid.append([0]*cols)
    self.PowerLevels()
    self.totals_by_dim = {}

  def PowerLevels(self):
    for y in range(self.rows):
      for x in range(self.cols):
        self.grid[y][x] = CalcPower(x+1, y+1, self.serial)

  def get(self, x, y):
    return self.grid[y][x]
  
  def sumTotal(self, x, y, dim):
    prev_dim = self.grid
    if dim > 1:
      prev_dim = self.totals_by_dim[dim - 1]
    xe = x + dim
    ye = y + dim
    s = prev_dim[y][x]
    for i in range(x, xe):
      s += self.grid[ye-1][i]
    for i in range(y, ye):
      s += self.grid[i][xe-1]
    # Correct for the double count
    s -= self.grid[ye-1][xe-1]
    return s

  def FindMaxX(self, dim):
    max_sum = -100000
    max_coords = []
    self.totals_by_dim[dim] = []
    for y in range(self.rows - dim):
      self.totals_by_dim[dim].append([0]*(self.cols - dim))
      for x in range(self.cols - dim):
        s = self.sumTotal(x, y, dim)
        self.totals_by_dim[dim][y][x] = s
        if s > max_sum:
          max_sum = s
          max_coords = (x+1 ,y+1)
    return max_sum, max_coords

  def FindMaxDim(self, top=301):
    max_sum = -100000
    max_coords = []
    for dim in range(1,top):
      print 'Caculating for ', dim
      s, coords = self.FindMaxX(dim)
      if s > max_sum:
        max_sum = s
        max_coords = [coords[0], coords[1], dim]
    return max_sum, max_coords
      
        
def Test():
  power = [[(122, 79), 57, -5],
           [(217, 196), 39, 0],
           [(101, 153), 71, 4]]

  for case in power:
    calc = CalcPower(case[0][0], case[0][1],case[1])
    print 'Calc: ', calc, ' Expected: ', case[2]

  corner = [[18, (33,45)],
            [42, (21,61)]]
  for case in corner:
    g = Grid(case[0])
    calc = g.FindMaxX(3)
    print 'Calc: ', calc[1], ' Expected: ', case[1]

  dims = [[18, [90, 269, 16]],[42, [232, 251, 12]]]
  for case in dims:
    g = Grid(case[0])
    calc = g.FindMaxDim()
    print 'Sum: ', calc[0], ' Calc: ', calc[1], ' Expected: ', case[1]
    
       
def main():
  #Test()
  
  # a => 44, 37
  grid = Grid(9798)
  coords = grid.FindMaxDim(4)
  print '(a)', coords
  coords = grid.FindMaxDim()
  print '(b)', coords
    
if __name__== "__main__":
  main()

