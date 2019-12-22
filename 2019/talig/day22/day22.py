import sys
from functools import partial
from os import system
import collections
import itertools
import re
import math

NUMBER = '(-?\d+)'

# Part (a) - straightforward
def new_stack(stack):
  stack.reverse()
  return stack

def cut(n, stack):
  return stack[n:] + stack[:n]

def deal(n, stack):
  new_stack = [-1]*len(stack)
  for j in range(len(stack)):
    new_stack[j*n % len(stack)] = stack[j]
  return new_stack

# Part (b) - index mapping.
def index_stack(size, index):
  # Reverse order
  #print 'reverse: Index %d moves to %d' % (index, (size - 1 - index) % size)
  return (size - 1 - index) % size

def gcd_extended(a,b):
  if a == 0:
    return b, 0, 1
  
  gcd, x1, y1 = gcd_extended(b % a, a)
  
  x = y1 - (b // a) * x1 
  y = x1
  return gcd, x, y; 

def modInverse(a, m): 
  g,x,y = gcd_extended(a,m)
  assert g == 1
  return x % m

def index_deal(n, inverse, size, index):
  #print 'deal %d => %d: Index %d moves to %d' % (inverse, n, index, (index* n) % size)
  return (index * n) % size

def index_cut(n, size, index):
  n = -n 
  #print 'cut %d: Index %d moves to %d' % (n, index, ((size - n) % size + index) %size)
  # 0 --> size - n, 1 --> n + 1, etc
  return ((size - n) % size + index) % size

def parse(filename, stack_size, index=False):
  f = open(filename)
  commands = []
  for line in f.readlines():
    line.strip()
    words = line.split(' ')
    command = None
    if words[0] == 'deal':
      m = re.match(NUMBER, words[-1])
      if m:
        dealX = int(m.group(0))
        command = partial(index_deal, modInverse(dealX, stack_size), dealX) if index else partial(deal, dealX)
      else:
        command = index_stack if index else new_stack
    if words[0] == 'cut':
      cutX = int(words[-1])
      command = partial(index_cut, cutX) if index else partial(cut, cutX)
    if index:
      # Because we're looking for the card that ENDS UP in 2020, we should do this
      # in reverse.
      commands.insert(0, command)
    else:
      commands.append(command)
  f.close()
  return commands

# (a)
def shuffle(filename, stack_size):
  commands = parse(filename, stack_size)
  stack = range(stack_size) # Initialize factory ordering.
  for c in commands:
    stack = c(stack)
  return stack

# (b)
def unshuffle(filename, stack_size, iterations, final_pos):
  commands = parse(filename, stack_size, index=True)
  pos = final_pos
  poses = {pos: [0]}
  for i in xrange(iterations):
    for c in commands:
      pos = c(stack_size, pos)
      if poses.get(pos, None):
        poses[pos].append(i)
      else:
        poses[pos] = [i]
  return pos # AKA initial position, AKA value.

def get_iterations_no_cycle(first, second, iterations):
  # Subtract the first encounter from number of iterations, we'd need to run those
  # just to get into the loop.
  # Then mod by the size of the loop (second-first), to know how far we need to go
  # into the loop.
  extra = (iterations - first) % (second - first)
  # Return first + extra
  return first + extra

def expect(expected, real):
  if expected == real:
    print('Pass.')
  else:
    print('Nope! Expected:', expected, 'but got:', real)
    
def test():
  tests = {'test1.data': [0, 3, 6, 9, 2, 5, 8, 1, 4, 7],
           'test2.data': [3, 0, 7, 4, 1, 8, 5, 2, 9, 6],
           'test3.data': [6, 3, 0, 7, 4, 1, 8, 5, 2, 9],
           'test4.data': [9, 2, 5, 8, 1, 4, 7, 0, 3, 6],
          }
  # (a)
  for t in tests:
    shuffled_stack = shuffle(t, 10)
    expect(tests[t], shuffled_stack)

  # (b)
  for t in tests:
    res = [-1] * 10
    deck = range(10)
    for i in deck:
      x = unshuffle(t, 10, 1, i)
      res[i] = x
    expect(tests[t], res)

def main():
  if (len(sys.argv) < 2):
    test()
    print('Missing data file!')
    print('Usage: python [script] [data]')
    sys.exit(1)

  # (a) ==> 1510
  shuffled = shuffle(sys.argv[1], 10007)
  print('Card 2019 is in position:', shuffled.index(2019))

  # (b) ==> 
  # 30743101856679 is too high :/ 
  deck_size = 119315717514047
  iterations = 101741582076661
  index = 2020

  # 2020 is not a stationary point here, sadly.
  # And I couldn't find a cycle in this thing :(
  #positions = unshuffle(sys.argv[1], deck_size, iterations, index)
  #print('Loopy? ', positions)
  #card_2020 = shuffle_b(sys.argv[1], deck_size, get_iterations_no_cycle(first, second, iterations), index)
  #print 'Card 2020 is in position:', card_2020
  
 
if __name__== "__main__":
  main()
