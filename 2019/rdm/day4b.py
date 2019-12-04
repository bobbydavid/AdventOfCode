import sys
import functools

# data
lo = 273025
hi = 767253


def is_valid(digits):
  chain_length = 1  # the 0th element.
  for i in range(1, len(digits)):
    if digits[i] == digits[i - 1]:
      chain_length += 1
    else:
      if chain_length == 2:
        return True
      chain_length = 1  # start of a new chain
  return chain_length == 2
    

def is_ascending(num):
  digits = [int(d) for d in str(num)]
  for i in range(1, len(digits)):
    if digits[i] < digits[i - 1]:
      return False
  return True


def increment_recursive(digits, i):
  assert i < len(digits)
  if digits[i] == 9:
    assert i > 0
    increment_recursive(digits, i - 1)
    digits[i] = digits[i - 1]
  else:
    digits[i] += 1


def increment(digits):
  return increment_recursive(digits, len(digits) - 1)


def get_next(digits):
  increment(digits)
  has_duplicate = len(digits) != len(set(digits)) 
  if not is_valid(digits):
    return get_next(digits)

# input: valid num
# index of digit to consider (0-5), 0=largest, 5=smallest
def next(num):
  digits = [int(d) for d in str(num)]
  get_next(digits)
  num = functools.reduce(lambda a, b: a * 10 + b, digits)
  return num


# make input ascending.
num = lo
while not is_ascending(num):
  num += 1


# now use faster incrementing to find first valid number.
if not is_valid([int(d) for d in str(num)]):
  num = next(num)
  

count = 0
while num <= hi:
  count += 1
  num = next(num)
  
print count


      

  
