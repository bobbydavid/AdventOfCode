import copy
import sys
import itertools

if len(sys.argv) < 2:
  sys.exit("forgot data file name: python day1.py <data file>")
filename = sys.argv[1]

print('Data file: ' + filename)
with open(filename, 'r') as content_file:
  content = content_file.read().strip()


def make_chunks(data, chunk_size):
  for i in range(0, len(data), chunk_size):
    yield data[i : i + chunk_size]


class Layer():
  def __init__(self, data, row_size):
    if len(data) % row_size != 0:
      raise Exception(
          ('raw data (len=%d) does not divide evenly ' +
           'into row_size=%d') % (len(raw_data), row_size))
    self.data = list(copy.deepcopy(data))
    self.data_size = len(data)
    self.row_size = row_size

  def __str__(self):
    rows = []
    rows.append('+' + '-' * self.row_size + '+')
    for row in make_chunks(self.data, self.row_size):
      rows.append('|' + ''.join(row) + '|')
    rows.append('+' + '-' * self.row_size + '+')
    return ''.join([row + '\n' for row in rows])


# Splits the data into layers of (row_size x col_size).
def split_into_layers(raw_data, row_size, col_size):
  layers = []
  layer_size = row_size * col_size
  for raw_layer in make_chunks(raw_data, layer_size):
    layers.append(Layer(raw_layer, row_size))
  return layers


# Every char is mapped according to `char_map`. If a char
# is missing, it becomes `default_char`.
def map_layer(layer, char_map, default_char):
  new_data = []
  for d in layer.data:
    if d in char_map:
      d = char_map[d]
    else:
      d = default_char
    new_data.append(d)
  return Layer(new_data, layer.row_size)


def merge_layers(layers, transparent_char):
  assert len(layers) > 0, 'no layers'
  data_size = layers[0].data_size
  img_data = [transparent_char] * data_size
  for layer in layers:
    for i in range(data_size):
      if img_data[i] == transparent_char:
        img_data[i] = layer.data[i]
  return Layer(img_data, layers[0].row_size)


raw_data = list(content)
layers = split_into_layers(raw_data, 25, 6)
img = merge_layers(layers, transparent_char='2')
img = map_layer(img, {'1':'X'}, ' ')
print(img)
