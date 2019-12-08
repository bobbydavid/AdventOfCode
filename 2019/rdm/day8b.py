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

# coords: (x, y) = x across, y down
# offset = x + y * 25
def render(image):
  for y in range(6):
    for x in range(25):
      c = image[x + y * 25]
      output_char_map = {
          '1': 'X',
          '2': ' ',
          '0': ' ',
      }
      sys.stdout.write(output_char_map[c])
    sys.stdout.write('\n')

# 2 == transparent
img = ['2' for x in range(25 * 6)]
for layer in layers:
  for x in range(25 * 6):
    if img[x] == '2':
      img[x] = layer[x]

render(img)
    
  
