import sys
from functools import partial
from os import system
import collections
import itertools
import re
import math
from random import randint

NUMBER = '(-?\d+)'

def gcd_extended(a,b):
  if a == 0:
    return b, 0, 1
  
  gcd, x1, y1 = gcd_extended(b % a, a)
  
  x = y1 - (b // a) * x1 
  y = x1
  return gcd, x, y; 

# https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
def mod_inverse(a, m): 
  g,x,y = gcd_extended(a,m)
  assert g == 1
  return x % m

def parse(filename, deck_size):
  f = open(filename)
  lines = f.readlines()
  f.close()
  m = 1
  b = 0
  for line in lines:
    line.strip()
    words = line.split(' ')
    command = None
    if words[0] == 'deal':
      match = re.match(NUMBER, words[-1])
      if match:
        dealX = int(match.group(0))
        m *= dealX
        b *= dealX
      else:
        m *= -1
        b = deck_size - 1 - b
    if words[0] == 'cut':
      cutX = int(words[-1])
      m *= 1
      b -= cutX
  return m % deck_size, b % deck_size

# (a)
def shuffle(filename, deck_size):
  return parse(filename, deck_size)

# (b)
def unshuffle(filename, deck_size):
  m, b = shuffle(filename, deck_size)
  inv_m = mod_inverse(m, deck_size)
  return inv_m, (-b * inv_m) % deck_size

# Common stuff.
def apply_iteratively(m, b, deck_size, iterations, pos):
  iter_m = power_of_m(m, iterations, deck_size)
  return (iter_m * pos + b*((iter_m -1) * mod_inverse(m-1, deck_size))) % deck_size

def get_array(m, b, deck_size, iterations=1):
  res = [-1] * deck_size
  for x in range(deck_size):
    res[apply_iteratively(m,b,deck_size, iterations, x)] = x
  return res

def power_of_m(m, iterations, deck_size):
  # bin(x) == '0b{bin representation}'. 
  # Strips and '0b' and makes it a list.
  binary = list(bin(iterations)[2:])
  # Reverse to start from the 0th power and go up.
  binary.reverse()
  power_m = 1
  total_m = 1
  for i in range(len(binary)):
    if i == 0:
      power_m = m
    else:
      power_m = (power_m * power_m) % deck_size
    if binary[i] == '1':
      total_m = (total_m * power_m) % deck_size
  return total_m


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
    m, b = shuffle(t, 10)
    res = get_array(m,b, 10)
    expect(tests[t], res)

  # (b) 
  for t in tests:
    m, b = unshuffle(t, 10)
    deck = range(10)
    for i in deck:
      # Given the resulting position, what's the original position ( == value).
      x = apply_iteratively(m,b, 10, 1, i)
      res[i] = x
    expect(tests[t], res)

def main():
  if (len(sys.argv) < 2):
    test()
    print('Missing data file!')
    print('Usage: python [script] [data]')
    sys.exit(1)

  # (a) ==> 1510
  deck_size = 10007
  m,b = shuffle(sys.argv[1], deck_size)
  res = get_array(m,b, deck_size)
  print('Card 2019 is in position:', res.index(2019))

  deck_size = 119315717514047
  iterations = 101741582076661
  index = 2020

  m, b = unshuffle(sys.argv[1], deck_size) 
  print 'Curiousity: %d * x + %d' % (m, b)
  # (b) ==>  10307144922975
  # Note: This only works if all the numbers are co-prime.
  # So for examples of deck size 10, it's not always going to work.
  # Note that you can't divide in modulo space, so you must use the
  # modulo inverse of (m-1).
  card_2020 = apply_iteratively(m, b, deck_size, iterations, index)
  print 'Card 2020 is in position:', card_2020
  
 
if __name__== "__main__":
  main()
