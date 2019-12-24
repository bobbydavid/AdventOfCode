from grid import Grid, Point
import sys
from os import system
import copy

def is_bug(char):
  return char == '#'

def get_grid(filename):
  f = open(filename)
  content = [list(line.strip()) for line in f.readlines()]
  f.close()
  
  return Grid(len(content), len(content[0]), content)

def advance_generation(eris):
  new_eris = copy.deepcopy(eris)
  for y in range(new_eris.rows):
    for x in range(new_eris.columns):
      location = Point(x,y)
      n = eris.count_neighbors(location)
      if is_bug(eris.get(location)):
        new_value = '#' if n == 1 else '.'
        new_eris.set(location, new_value)
      elif not is_bug(eris.get(location)):
        new_value = '#' if (n == 1 or n==2) else '.'
        new_eris.set(location, new_value)
  return new_eris

def compute_biodiversity(eris):
  # 5x5 binary has 25 squares, so we're looking at a 25 bit
  # binary.
  binary = []
  for y in eris.grid:
    for x in y:
      digit = '0' if x == '.' else '1'
      binary.insert(0, digit)
  bin_str = '0b' + ''.join(binary)
  return int(bin_str,2)


def expect(expected, real):
  if expected == real:
    print('Pass.')
  else:
    print('Nope! Expected:', expected, 'but got:', real)

def find_first_repetition(eris):
  diversities = {}
  bio = compute_biodiversity(eris)
  current_eris = eris
  current_eris.render()
  while not bio in diversities:
    diversities[bio] = current_eris
    current_eris = advance_generation(current_eris)
    current_eris.render()
    bio = compute_biodiversity(current_eris)
  return diversities, bio
    
def test():
  tests = {'test1.data': 2129920,
          }
  # (a)
  for t in tests:
    eris = get_grid(t)
    d, bio = find_first_repetition(eris) 
    expect(tests[t], bio)

def main():
  if (len(sys.argv) < 2):
    test()
    print('Missing data file!')
    print('Usage: python [script] [data]')
    sys.exit(1)

  # (a) ==> 18404913
  eris = get_grid(sys.argv[1])
  d, b = find_first_repetition(eris)
  print('Biodiversity of first repeating state: ', b)

  # (b) ==>
  
 
if __name__== "__main__":
  main()
