from grid import Grid, Point, PlutonianGrid
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
      new_value = '.'
      if n == 1 or (not is_bug(eris.get(location)) and n == 2):
        new_value = '#' 
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

def find_first_repetition(eris):
  diversities = {}
  bio = compute_biodiversity(eris)
  current_eris = eris
  current_eris.render()
  while not bio in diversities:
    diversities[bio] = current_eris
    current_eris = advance_generation(current_eris)
    #current_eris.render()
    bio = compute_biodiversity(current_eris)
  return diversities, bio

# (b)
def get_plutonian_grid(filename):
  eris_level_0 = get_grid(filename)
  plutonian = PlutonianGrid(eris_level_0)
  return plutonian

def plutonian_advance(plutonian):
  # First, note that we will probably need one level up and one level down.
  # So add them to the current one.
  plutonian.extend_levels()
  levels = plutonian.get_levels_range()
  new_plutonian = copy.deepcopy(plutonian)
  for y in range(plutonian.rows):
    for x in range(plutonian.cols):
      location = Point(x, y)
      if location == plutonian.center:
        # No point in looking at this.
        continue
      for l in levels:
        n = plutonian.count_neighbors(location, l)
        new_value = '.'
        if n == 1 or (not is_bug(plutonian.get(location, l)) and n == 2):
          new_value = '#'
        new_plutonian.set(location, l, new_value)
  return new_plutonian

def count_bugs(plutonian):
  total = 0
  for y in range(plutonian.rows):
    for x in range(plutonian.cols):
      location = Point(x, y)
      if location == plutonian.center:
        continue
      for l in plutonian.levels:
        total += 1 if is_bug(plutonian.get(location,l)) else 0
  return total

def run_minutes(minutes, plutonian):
  plutonians = [plutonian]
  for i in range(minutes):
    plutonians.append(plutonian_advance(plutonians[i]))
  return count_bugs(plutonians[-1])

def expect(expected, real):
  if expected == real:
    print('Pass.')
  else:
    print('Nope! Expected:', expected, 'but got:', real)
    
def test():
  # (a)
  test_A = {'test1.data': 2129920}
  for t in test_A:
    eris = get_grid(t)
    d, bio = find_first_repetition(eris) 
    expect(test_A[t], bio)
  
  # (b)
  test_B = {'test1.data': (10, 99)}
  for t in test_B:
    res = run_minutes(test_B[t][0], get_plutonian_grid(t))
    expect(test_B[t][1], res)

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
  bugs = run_minutes(200, get_plutonian_grid(sys.argv[1]))
  print('Bugs after 200 minutes in plutonian grid: ', bugs)
 
if __name__== "__main__":
  main()
