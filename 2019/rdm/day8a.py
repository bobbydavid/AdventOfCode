import copy
import sys
import itertools

if len(sys.argv) < 2:
  sys.exit("forgot data file name: python day1.py <data file>")
filename = sys.argv[1]

print('Data file: ' + filename)
with open(filename, 'r') as content_file:
  content = content_file.read().strip()

layers = []
i = 0
layer_size = 25 * 6
while i < len(content):
  next_i = i + layer_size
  layers.append(content[i:next_i])
  i = next_i
assert i == len(content), 'content did not divide evenly into layers'

min_zeros = 11
answer = -1
for layer in layers:
  zeros = layer.count('0')
  if zeros < min_zeros:
    answer = layer.count('1') * layer.count('2')

print('answer = %d' % answer)

