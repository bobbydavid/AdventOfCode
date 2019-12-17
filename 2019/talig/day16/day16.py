import sys
from os import system
import copy
import collections
import itertools
import re
import math
import numpy

class FFT:
  def __init__(self, input_data, offset=0):
    self.pattern_base = [0, 1, 0, -1]
    self.size = len(input_data)
    self.phases = []
    self.phases.append([int(x) for x in input_data])
    self.offset = offset

  def GetPhase(self, phase):
    if self.phases[phase]:
      return ''.join([str(x) for x in self.phases[phase]])
    else:
      print 'Error! Phase %d has not been computed yet.' % phase
      return ''
  
  def GetPatternParam(self, i, x):
    # x is the index of the element we're computing, i is the element we're calculating for now.
    index = int(math.floor((i + 1)/float(x + 1)) % len(self.pattern_base))
    return self.pattern_base[index]

  def ComputeElement(self, data, x):
    res = 0
    for i in xrange(self.size):
      p = self.GetPatternParam(i, x)
      if not p == 0:
        res += data[i] * self.GetPatternParam(i,x)
    return abs(res) % 10

  def Transform(self, phase):
    next_p = []
    for i in xrange(self.size):
      next_p.append(self.ComputeElement(phase, i))
    return next_p

  def ComputePhases(self, final=100):
    for i in range(1, final):
      self.phases.append(self.Transform(self.phases[i-1]))

  def ComputePhasesB(self, final=100):
    playground = copy.deepcopy(self.phases[0])
    for i in range(1, final+1):
      for j in xrange(self.size - 2 , self.offset - 1, -1):
        playground[j] = abs(playground[j] + playground[j+1]) % 10
    return playground

  def ComputeMessageB(self, phase):
    return ''.join([str(x) for x in phase[self.offset:self.offset+8]])

def GetMessage(initial, phase):
  offset = int(initial[:7])
  fft = FFT(initial, offset)
  # This only works for the second half.
  assert offset > (fft.size / 2)
  playground = fft.ComputePhasesB(phase)
  return fft.ComputeMessageB(playground)

def Expect(expected, found):
  if expected == found:
    print 'Pass'
  else:
    print 'Nope! Found ', found, ' vs. Expected ', expected

def Test():
  tests = {'12345678': {1: '48226158', 2: '34040438', 3: '03415518', 4: '01029498'}, 
           '80871224585914546619083218645595': {100: '24176176'},
           '19617804207202209144916044189917': {100: '73745418'},
           '69317163492948606335995924319873': {100: '52432133'},
          }
  for t in tests:
    fft = FFT(t)
    fft.ComputePhases(max(tests[t].keys()) + 1)
    for phase in tests[t]:
      print 'Test %s phase %d' % (t, phase)
      result = fft.GetPhase(phase)[:8]
      Expect(tests[t][phase], result)
  
  message_tests = [('03036732577212944063491565474664','84462026'),
                   ('02935109699940807407585447034323','78725270'),
                   ('03081770884921959731165446850517','53553731')]
  for t in message_tests:
    print 'Test: ', t
    m = GetMessage(t[0]*10000, 100)
    Expect(t[1], m)


def main():
  if len(sys.argv) < 2:
    print 'Running tests...' 
    Test()
    print '\n' 
    print 'Missing data file!'
    print 'Usage: python [script] [data]'
    sys.exit(1)

  filename = sys.argv[1]
  f = open(filename)
  data = f.read().strip()
  f.close()

  # (a) ==> 10189359  (First 8 digits)
  c = FFT(data)
  c.ComputePhases()
  print 'After 100 phases at offset 0: ', c.GetPhase(100)[:8]
  # (b) ==> 80722126
  # Real input data for (b)
  b_data = data * 10000
  message = GetMessage(b_data, 100)
  print 'Message: ', message

    
if __name__== "__main__":
  main()
