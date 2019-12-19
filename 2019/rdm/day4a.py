import sys
import functools

# data
lo = 273025
hi = 767253


def increment(digits, i):
  assert i < len(digits)
  if digits[i] == 9:
    assert i > 0
    increment(digits, i - 1)
    digits[i] = digits[i - 1]
  else:
    digits[i] += 1


def get_next(digits):
  increment(digits, len(digits)-1)
  has_duplicate = len(digits) != len(set(digits))
  if not has_duplicate:
    return get_next(digits)

# input: valid num
# index of digit to consider (0-5), 0=largest, 5=smallest
def next(num):
  digits = [int(d) for d in str(num)]
  get_next(digits)
  num = functools.reduce(lambda a, b: a * 10 + b, digits)
  return num

num = 277777  # lo rounded up
count = 0
while num <= hi:
  count += 1
  # print num
  num = next(num)

print count

"""
print next(11123)
print next(11111)
print next(22345)
print next(22399)
print next(12345)
print next(12344)
"""




