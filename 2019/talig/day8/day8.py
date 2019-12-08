import math
import sys
import operator
import copy
from functools import partial
import collections
import logging

class ImageData:
  def __init__(self, columns, rows, raw_data):
    self.columns = columns
    self.rows = rows
    self.raw_data = [int(x) for x in raw_data]
    self.layers = []
    self.SplitToLayers()
    self.superimposed = [0] * self.GetLayerSize()
    self.SuperimposeLayers()

  def GetLayerSize(self):
    return self.columns * self.rows

  def SplitToLayers(self):
    i = 0
    while i < len(self.raw_data):
      self.layers.append(copy.deepcopy(self.raw_data[i:i+self.GetLayerSize()]))
      i += self.GetLayerSize()

  def FindLayerWithMinimumIncidents(self, number):
    min_incidents = self.GetLayerSize()
    min_layer = 0
    for i in range(len(self.layers)):
      incidents = self.layers[i].count(number)
      if incidents < min_incidents:
        min_incidents = incidents
        min_layer = i
    return min_layer

  def ComputeLayerChecksum(self, layer_index, digits):
    layer = self.layers[layer_index]
    checksum = 1
    for d in digits:
      checksum *= layer.count(d)
    return checksum

  def SuperimposeLayers(self):
    for c in range(self.columns):
      for r in range(self.rows):
        offset = r * (self.columns) + c 
        for layer in self.layers:
          if layer[offset] < 2:
            self.superimposed[offset] = layer[offset]
            break

  def PrintImage(self):
    print '-' * self.columns
    for r in range(self.rows):
      offset = r * self.columns
      print ''.join(
            [' ' if x==0 else 'X' for x in self.superimposed[offset:offset+self.columns]])
    print '-' * self.columns

def Expect(expected, existing):
  if expected == existing:
    print 'Passed'
  else:
    print 'Nope! Expected: %s got: %s' % (expected, existing)

def TestCaseImage():
  tests = [(ImageData(3, 2, '123456789012'), 0, 1)]
  for test in tests:
    # Call test
    Expect(test[1], test[0].FindLayerWithMinimumIncidents(0))
    Expect(test[2], test[0].ComputeLayerChecksum(0, [1, 2]))

def TestSuperimpose():
  test = (ImageData(2, 2, '0222112222120000'), [0,1,1,0])
  Expect(test[1], test[0].superimposed)
  

def Test():
  print 'Testing: '
  TestCaseImage()
  TestSuperimpose()
  print '\n\n\n\n', '*'*30, '\n'

def main():
  Test()
  if (len(sys.argv) < 2):
    print 'Missing data file!'
    print 'Usage: python [script] [data]'
    sys.exit(1)

  f = open(sys.argv[1])
  content = f.read().strip()
  f.close()
  
  cols = int(sys.argv[2])
  rows = int(sys.argv[3])
  # (a)
  image = ImageData(cols, rows, content)
  l = image.FindLayerWithMinimumIncidents(0)
  chk = image.ComputeLayerChecksum(l, [1,2])
  print 'Checksum: %d (layer index: %d) ' % (chk, l)

  # (b)
  print 'Superimposed: '
  image.PrintImage()
  
if __name__== "__main__":
  main()
