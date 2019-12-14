from collections import defaultdict
from collections import deque
import copy
import functools
import itertools
import math
import sys
import threading

if len(sys.argv) < 2:
  sys.exit("forgot data file name: python day1.py <data file>")
filename = sys.argv[1]

if len(sys.argv) < 3:
  sys.exit("2nd argument should be 'a' or 'b'")
question_part = sys.argv[2]


class Ingredient():
  @staticmethod
  def Parse(quantity_and_chemical):
    parts = quantity_and_chemical.strip().split(' ')
    assert len(parts) == 2
    return Ingredient(int(parts[0]), parts[1])

  def __init__(self, amount, name):
    self.amount = amount
    self.name = name

  def __repr__(self):
    return '%d %s' % (self.amount, self.name)


class Equation():
  def __init__(self, inputs, output):
    self.inputs = inputs
    self.output = output

  def __repr__(self):
    return '%s <= %s' % (self.output, self.inputs)


print('Data file: ' + filename)
# List of [(type, quantity), ...]. The last one is the output.
equations = []
with open(filename, 'r') as content_file:
  for line in content_file.readlines():
    sides = line.strip().split(' => ')
    assert len(sides) == 2
    inputs = [Ingredient.Parse(x) for x in sides[0].split(', ')]
    output = Ingredient.Parse(sides[1])
    equations.append(Equation(inputs, output))

print('Parsed %d equations.' % len(equations))
print equations

# Map from an ingredient to how its produced.
equation_map = {}
for equation in equations:
  equation_map[equation.output.name] = equation


# List of all chemicals.
chemicals = set() 
for equation in equations:
  chemicals.add(equation.output.name)
  for i in equation.inputs:
    chemicals.add(i.name)
chemicals = list(chemicals)


# Is a an ingredient in b?
def is_ingredient_in(a, b):
  assert a != b
  if b in equation_map:
    equation = equation_map[b]
    for ingredient in equation.inputs:
      if ingredient.name == a or is_ingredient_in(a, ingredient.name):
        return True
  return False


# Comparator to help order chemicals from [output..input]
def dependency_direction(a, b):
  if a is Ingredient:
    a = a.name
  if b is Ingredient:
    b = b.name
  if a == b:
    return 0
  if is_ingredient_in(a, b):
    return 1
  else:
    return -1


# Sorts `list` in order of [output..input]. Ingredients of an item
# are always to the right of it.
def sort_dependencies(lst):
  lst.sort(key=functools.cmp_to_key(dependency_direction))


sort_dependencies(chemicals)
print('chemicals in order from output to input')
print(chemicals)


# IMPORTANT: sort dependencies. This makes sure that we take into
# account our full need for ingredient X before we decide how much
# of X to make. Otherwise, we might make too much of it in small
# batches.
for equation in equations:
  sort_dependencies(equation.inputs)


# `available` is a map from ingredient name to what's available
# from previous production.
#
# Returns the ore needed to produce `amount_needed` of `element`.
def produce(available, element, amount_needed):
  assert amount_needed > 0
  if element == 'ORE':
    return amount_needed
  # Use up whatever we have on hand first.
  if element in available:
    amount_available = available[element]
    if amount_available >= amount_needed:
      available[element] -= amount_needed
      print('%s: used up %d of %d available' % (
          element, amount_needed, amount_available))
      return 0  # No cost in ore, we used available supplies.
    else:
      # Used everything we have, and we still need more.
      amount_needed -= available.pop(element)
      print('%s: using up %d available, still need %d' % (
          element, amount_available, amount_needed))
  # Produce what we don't have.
  assert amount_needed > 0
  equation = equation_map[element]
  # How many batches to produce of this equation.
  batches = int(math.ceil(float(amount_needed) / equation.output.amount))
  ore_needed = 0
  for ingredient in equation.inputs:
    ingredient_amount_needed = ingredient.amount * batches
    ore_needed += produce(available, ingredient.name, ingredient_amount_needed)
  amount_produced = equation.output.amount * batches
  # Add any extras for future use.
  leftovers = amount_produced - amount_needed
  print('%s: produced %d, had %d leftover' % (element, amount_produced, leftovers))
  assert leftovers >= 0
  if leftovers > 0:
    if not element in available:
      available[element] = 0
    available[element] += leftovers
  return ore_needed


# Deciding function
def is_possible(fuel_count, ore_count):
  ore_needed = produce({}, 'FUEL', fuel_count)
  return ore_needed <= ore_count



# Finds the maximum amount of fuel we can make with this available ore.
def max_fuel_possible(available_ore):
  # First, find an upper bound on how much fuel can be made.
  upper_bound = 2
  while is_possible(upper_bound, available_ore):
    upper_bound *= 2
  # Narrow the bounds until with binary search.
  lower_bound = upper_bound // 2
  while True:
    print('[%d..%d)' % (lower_bound, upper_bound))
    target = ((upper_bound - lower_bound) // 2) + lower_bound
    if is_possible(target, available_ore):
      lower_bound = target
    else:
      upper_bound = target
    if lower_bound + 1 == upper_bound:
      return lower_bound


if question_part == 'a':
  ore = produce({}, 'FUEL', 1)
  print('ore needed: %d' % ore)
elif question_part == 'b':
  m = max_fuel_possible(1000000000000)
  print('max fuel possible = %d' % m)
else:
  sys.exit('unknown part %s' % question_part)
