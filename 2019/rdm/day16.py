import intcode
import time
import copy
import sys
import threading
import os
import random
import tty
from Queue import Queue
import termios


PATTERN = [0, 1, 0, -1]

# Parses a string of numbers into a list.
def parse_nums(s):
  return [int(x) for x in list(s)]

def make_str(nums):
  return ''.join(str(x) for x in nums)

if len(sys.argv) == 1:
  filename = 'day16.data'
  print('Data file: ' + filename)
  with open(filename, 'r') as content_file:
    digits_str = content_file.read().strip()
else:
  digits_str = sys.argv[1].strip()
digits = parse_nums(digits_str)


def get_multiplier(row, col):
  d = (col + 1) // (row + 1)
  return PATTERN[d % len(PATTERN)]


def vector_mod(vec):
  return [abs(x) % 10 for x in vec]


def run_fft(digits):
  output_digits = [0] * len(digits)
  for n in range(len(digits)):
    s = 0
    for i, d in enumerate(digits):
      s += d * get_multiplier(n, i)
    output_digits[n] = s
  return vector_mod(output_digits)



# Calculates the solution using the slow way.
def solve_full_solution(digits, phases):
  print('SOLVE: phases=%d, input=%s' % (phases, make_str(digits)))
  results = [digits]
  for p in xrange(phases):
    digits = run_fft(digits)
  return make_str(digits)


# Solves part A.
# Returns the 1st 8 digits and the full result.
def solve_part_a(digits, phases):
  print('solving part A...')
  result = solve_full_solution(digits, phases)
  solution = result[:8]
  print('Done. Solution: %s' % solution)
  return solution, result


# Solves FFT for a subset of another input vector, which must
# be from the 2nd half of the original data.
def part_b_solver(v, phases):
  print('PART B SOLVER: len(v)=%d, phases=%d' % (len(v), phases))
  for phase in xrange(phases):
    running_sum = 0
    # Iterate through the vector backwards.
    for i in xrange(len(v) - 1, -1, -1):
      running_sum += v[i]
      v[i] = running_sum
    v = vector_mod(v)
  return make_str(v)



# Run on every test input to find the full result. Use the
# checksum from the problem statement for the first 8 chars.
#
# This verifies that the Part B solver is actually working.
def validate_part_b(digits_str, full_solution):
  # Scraped from the examples in the problem.
  input_pairs = [
    (4, '12345678', '01029498'),
    (100, '80871224585914546619083218645595', '24176176'),
    (100, '19617804207202209144916044189917', '73745418'),
    (100, '69317163492948606335995924319873', '52432133'),
    (100, digits_str, full_solution[:8]),
  ]
  full_output = []
  for phases, input_str, checksum in input_pairs:
    print('Checking next input...')
    # Save time by reusing the full solution from part A
    if input_str == digits_str:
      output = full_solution
    else:
      output = solve_full_solution(parse_nums(input_str), phases)
    actual = output[:8]
    assert actual == checksum, 'checksum=%s but saw %s. Full result:\n%s' % (
        checksum, actual, output)
    full_output.append(output)
    print('pass')
  print('all pass')
  
  print('testing part b solver...')
  for output, (phases, input_str, _) in zip(full_output, input_pairs):
    # Only run on the 2nd half of the input.
    first_digit_idx = len(input_str)/2
    v = parse_nums(input_str[first_digit_idx:])
    result = part_b_solver(v, phases)
    checksum = output[first_digit_idx:]
    assert result == checksum, 'expected:\n%s\nsaw:\n%s\noutput:\n%s' % (
      checksum, result, output)
    print('pass')
  print('all pass')


# Uses the part B solver on the digits that come after the offset.
def solve_part_b(digits):
  offset = int(make_str(digits[:7]))
  part_b_length = len(digits) * 10000
  digits_after_offset = part_b_length - offset
  fraction_skipped = float(offset) / part_b_length
  # Sanity check that we skipped more than half the input.
  assert fraction_skipped > 0.5, 'cannot use fast solver :('
  part_b_input = [digits[d % len(digits)] for d in xrange(offset, part_b_length)]
  result = part_b_solver(part_b_input, 100)
  print('result: ' + result[:8])


part_a_solution, full_solution = solve_part_a(digits, 100)
validate_part_b(digits_str, full_solution)

solve_part_b(digits)

