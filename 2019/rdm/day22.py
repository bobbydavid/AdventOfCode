import aoc
import math
import sys
import copy
import re



class ModException(Exception):
  pass

class Task():
  def __init__(self, name, num = None):
    self.name = name
    self.num = num

  def __repr__(self):
    data = ''
    if self.num is not None:
      data = ' (%s)' % self.num
    return '%s%s' % (self.name, data)

def parse_task(task):
  if task == 'deal into new stack':
    return Task('reverse', None)
  m = re.match('cut (-?\\d+)', task)
  if m:
    return Task('cut', int(m.group(1)))
  m = re.match('deal with increment (-?\\d+)', task)
  if m:
    return Task('shuffle', int(m.group(1)))
  raise Exception('Cannot parse task: %s' % task)

def parse_tasks(tasks):
  tasks = tasks.split('\n')
  return [parse_task(t.strip()) for t in tasks if t.strip()]

def read_data(dataset):
  if dataset == 'main':
    with open('day22.data', 'r') as contents:
      data = contents.read()
    cards = 10007
  elif dataset == '1':
    data = """
    deal with increment 7
    deal into new stack
    deal into new stack
    """
    cards = 10
  elif dataset == '2':
    data = """
    cut 6
    deal with increment 7
    deal into new stack
    """
    cards = 10
  elif dataset == '3':
    data = """
    deal with increment 7
    deal with increment 9
    cut -2
    """
    cards = 10
  else:
    raise Exception('Unknown dataset: %s' % dataset)
  return data, cards

def read_main_data():
  dataset = 'main'
  data, cards = read_data(dataset)
  tasks = parse_tasks(data)
  return tasks


def gcd_extended(j, k):
  if j == 0:
    gcd = k
    co_j = 0
    co_k = 1
  else:
    gcd, co_j2, co_k2 = gcd_extended(k % j, j)
    co_j = co_k2 - (k // j) * co_j2
    co_k = co_j2
  return gcd, co_j, co_k


# Returns x s.t. (a*x) % m = 1
def mod_inverse(a, m):
  gcd, co_j, co_k = gcd_extended(a, m)
  if gcd != 1:
    raise ModException('No inverse for %d mod %d' % (a, m))
  return ((co_j % m) + m) % m
  

if len(sys.argv) > 2:
  print('mod inverse = %s' % mod_inverse(int(sys.argv[1]), int(sys.argv[2])))
  sys.exit(0)



def get_factors_of_2(k):
  assert k > 0
  factors = []
  n = 1
  while k:
    next_n = n * 2
    if k % next_n:
      factors.append(n)
    n = next_n
    k = k - (k % n)
  return factors

# Recursively calculates using the cache, which maps from
# k to the result of m^k
# m^k = m^(1 + 2 + 4 + 16 ... )
#     = m^1 * m^2 * m^4 * m^16
#     
def recursive_calc_exponent(cache, m, k, total):
  if k in cache:
    return cache[k]

  if k == 0:
    return 1
  elif k == 1:
    return m
  else:
    n = recursive_calc_exponent(cache, m, k // 2, total)
    n2 = (n * n) % total
    cache[k] = n2
    return n2

# Returns (m ** k) % total
# pos_inv is the inverse of the position number w.r.t. total.
def calc_exponent(m, k, total):
  result = 1
  cache = {}
  for f in get_factors_of_2(k):
    n = recursive_calc_exponent(cache, m, f, total)
    result *= n
    result = result % total
  return result
        


  cache = {}
  return recursive_calc_exponent(cache, m, k, total)
  """
  # Map from n -> m^n
  cache = {}
  # Gets a value from the cache (or adds if not present).
  # Returns m^n
  def get_exp(n):
    if n in cache:
      return cache[n]

    if n == 0:
      v = 1
    elif n == 1:
      v = m
    else:
      factors = get_factors_of_2(n)
      v = 1
      for f in factors:
        v *= get_exp(int(math.log(f)/math.log(2)))
        v = v % pos_inv
      cache[n] = v
    return v

  # m^k = m^(1*a0 + 2*a1 + 4*a2 + ... + 2^x*ax)
  factors = get_factors_of_2(k)
  result = 1
  for factor in factors:
    result *= get_exp(factor)
    result = result % pos_inv
  return result
  """

  

def solve_mb(tasks, card_to_track, total_card_count):
  pos = card_to_track
  total = total_card_count

  #pos_inv = mod_inverse(pos, total)
  #assert pos * pos_inv % total == 1

  m = 1
  b = 0
  for task in tasks:
    if task.name == 'reverse':
      # total - (m*x + b) - 1
      # -m*x + (total - 1 - b)
      m = -1 * m
      b = total - 1 - b
    elif task.name == 'cut':
      #m_inv = mod_inverse(m, total)
      #b = (b - task.num - b) * m_inv
      b = b - task.num
    elif task.name == 'shuffle':
      # Calculate the inverse, just to be sure this is a valid
      # shuffle operation. This will throw an exception on error.
      # On success, ignore the result.
      #n_inv = mod_inverse(task.num, total)
      #print('n=%d, n_inv=%d' % (task.num, n_inv))
      # pos * N
      # (m*pos + b) * N
      # m*N*pos + b*N
      # (y - b*N) / (m * N)
      #
      # m*N_inv*pos + b*N
      #m *= n_inv
      #b *= n_inv

      # pos * N
      # (m*x + b) * N
      # (m*N)*x + (b*N)
      m *= task.num
      b *= task.num
    else:
      raise Exception('unknown task: %s' % task)
    #print('new m = %d, new b = %d' % (m, b))
    m = m % total
    b = b % total
    #print('after mod by %d and %d: new m = %d, new b = %d' % (pos_inv, total, m, b))
  return m, b


# Finds the equation to know where the `card-to-track` card ends up.
# Then, reverses the equation to find which card ends up in the
# `card-to-track` location.
def solve_at_index(tasks, card_to_track, total_card_count):
  m, b = solve_mb(tasks, card_to_track, total_card_count)
  # y = mx + b
  # y - b = mx
  # mx = y - b
  # x = y*m_inv - b*m_inv
  m_inv = mod_inverse(m, total_card_count)
  result = (card_to_track * m_inv - b * m_inv) % total_card_count
  return result

def find_index(tasks, card_to_track, total_card_count):
  m, b = solve_mb(tasks, card_to_track, total_card_count)
  result = (card_to_track * m + b) % total_card_count
  return result


def solve_whole_array(tasks, total_card_count):
  total = total_card_count
  results = []
  for i in range(total):
    try:
      x = solve_at_index(tasks, i, total)
      results.append(x)
    except ModException:
      print('cannot solve i=%d' % i)
  return results

def old_solve_whole_array(tasks, total_card_count):
  total = total_card_count
  results = [None] * total_card_count
  # Find the location of the ith card
  for i in range(total):
    try:
      #print('\ntrying i=%d' % i)
      x = find_index(tasks, i, total)
      #print('SOLVED %d: solution=%d' % (i, x))
      results[x] = i
    except ModException:
      print('cannot solve i=%d' % i)
  return results
  


def run_test():
  arrays = []
  for i in range(-4, 4):
    print('### i=%d' % i)
    tasks = [
      #Task('shuffle', i),
      #Task('reverse'),
      Task('cut', i),
      #Task('reverse'),
    ]
    soln = solve_whole_array(tasks, 10)
    print(i, soln)
    arrays.append((i,soln))
  for i, soln in arrays:
    print(i, soln)

def run_tests():
  test1 = [
    Task('shuffle', 7),
    Task('reverse'),
    Task('reverse'),
  ]
  expected1 = [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
  test2 = [
    Task('cut', 6),
    Task('shuffle', 7),
    Task('reverse'),
  ]
  expected2 = [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]
  test3 = [
    Task('shuffle', 7),
    Task('shuffle', 9),
    Task('cut', -2),
  ]
  expected3 = [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]
  test4 = [
    Task('reverse'),
    Task('cut', -2),
    Task('shuffle', 7),
    Task('cut', 8),
    Task('cut', -4),
    Task('shuffle', 7),
    Task('cut', 3),
    Task('shuffle', 9),
    Task('shuffle', 3),
    Task('cut', -1),
  ]
  expected4 = [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]
  test_pairs = [
    (test1, expected1),
    (test2, expected2),
    (test3, expected3),
    (test4, expected4),
  ]
  for test_case, expected_array in test_pairs:
    result = solve_whole_array(test_case, 10)
    assert len(result) == len(expected_array)
    assert not all(r is None for r in result)
    for i in range(len(result)):
      if result[i] is not None:
        if result[i] != expected_array[i]:
          print('Failed:')
          print(test_case)
          print('Expected: %s' % expected_array)
          print('Actual: %s' % result)
          print('test failed :(')
          sys.exit(1)
    print('%s: %s' % (test_case, result))
  print('PASSED all test cases')


def solve_part_a():
  dataset = 'main'
  data, cards = read_data(dataset)
  tasks = parse_tasks(data)
  pos = find_index(tasks, 2019, 10007)
  print 'SOLVED part a: %d' % pos
  assert pos == 6638
      


def solve_part_b():
  dataset = 'main'
  data, cards = read_data(dataset)
  tasks = parse_tasks(data)

  total_card_count = 119315717514047
  card_to_track = 2020
  repeats = 101741582076661  # R
  answer = solve_like_part_b(tasks, total_card_count, card_to_track, repeats)
  print('SOLVED part b: %s' % answer)
  assert answer > 50952079323838  # I guessed wrong.
  assert answer < 108967639669667  # I guessed wrong again.


def solve_like_part_b(tasks, total_card_count, card_to_track, repeats):

  print('tasks: %s' % tasks)
  print('total_card_count = %d, card_to_track = %d, repeats = %d' % (
      total_card_count, card_to_track, repeats))

  # Solve m/b and then invert it.
  m, b = solve_mb(tasks, card_to_track, total_card_count)
  # y = mx + b
  # mx = y - b
  # x = (y - b) / m
  # x = y*m_inv - b*m_inv
  m_inv = mod_inverse(m, total_card_count)
  m = m_inv
  b = (-b * m_inv) % total_card_count

  
  # At this point, the solution is:
  # f(x) = m * x + b
  # solution = f(f(f(f....
  # f(f(x)) = m(mx + b) + b = m^2 + mb + b
  # f(f(f(x))) = m(m(mx + b) + b) + b = m^3 + m^2b + mb + b
  # == sum from 1..R of m^(R-1)*b + m^R*x
  # (let K = R-1
  # == (sum 0..K of m^(K)) * b + m^R * x
  #  (m^(K+1) - 1) / (m - 1)
  #
  # un-substitute: R = K+1
  #
  # (m^R - 1) * b / (m - 1) + m^R * x

  R = repeats
  m_R = calc_exponent(m, R, total_card_count)
  #print('m=%d, b=%d, m_R=%d' % (m, b, m_R))
  if m == 1:
    answer = (b * R + m_R * card_to_track) % total_card_count
  else:
    answer = ((m_R - 1) * b / (m - 1) + (m_R * card_to_track)) % total_card_count
  return answer


#run_test()
#run_tests()
#solve_part_a()


def check_calc_exponent():
  for i in range(1, 30):
    for j in range(30, 100):
      for k in range(1, 30):
        assert calc_exponent(i, k, j) == (i ** k) % j
  print('PASSED check exponent check')

def check_part_b_solver():
  # reversing an even number of times produces the same results.
  tasks = [Task('reverse')]
  for repeats in [2, 8, 10000, 10000000408]:
    total = 10
    results = []
    for i in range(total):
      results.append(solve_like_part_b(tasks, total, i, repeats))
    assert results == list(range(total))

  # reversing an odd number of times produces the same results.
  tasks = [Task('reverse'),Task('reverse'), Task('reverse')]
  for repeats in [1, 7, 10001, 10000000409]:
    total = 10
    results = []
    for i in range(total):
      results.append(solve_like_part_b(tasks, total, i, repeats))
    assert results == list(range(total - 1, -1, -1))

  # Cutting N times of 1 each.
  tasks = [Task('cut', 1)]
  for repeats in [1, 7, 10001, 10000000409]:
    total = 10
    results = []
    for i in range(total):
      results.append(solve_like_part_b(tasks, total, i, repeats))
    net_shift = repeats % total
    for i, r in enumerate(results):
      assert r == (i + net_shift) % total
    
  # Shuffle N times
  tasks = [Task('shuffle', 3)]
  for repeats in [8, 16, 24364]:
    total = 10
    results = []
    for i in range(total):
      results.append(solve_like_part_b(tasks, total, i, repeats))
    net_shift = repeats % total
    print(results)
    assert results == list(range(total))
    
  print('PASSED part b test')





check_calc_exponent()
run_tests()

check_part_b_solver()
solve_part_a()
solve_part_b()

