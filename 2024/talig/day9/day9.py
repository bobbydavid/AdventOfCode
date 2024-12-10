import sys
import math
import time
import os
import heapq
from copy import deepcopy

def parse(line):
  line = line.strip()
  files = [int(x) for x in list(line)]
  blocks = []
  emptyBlocks = []
  emptySpans = []
  fileSpans = []
  j = 0
  fileID = 0
  for i in range(len(files)):
    v = files[i]
    if i%2 == 0:
      blocks.extend([fileID]*v)
      fileSpans.append((fileID, v, j))
      fileID += 1
    else:
      blocks.extend(['.']*v)
      emptyBlocks.extend(list(range(j, j+v)))
      emptySpans.append((j, v))
    j+= v  
  heapq.heapify(emptyBlocks)
  emptySpans.sort()
  return blocks, emptyBlocks, emptySpans, fileSpans

def defragPart1(inputBlocks, emptyBlocks):
  blocks = deepcopy(inputBlocks)
  for i in range(len(blocks) -1, -1, -1):
    if blocks[i] == '.':
      continue
    # move one block at a time
    j = heapq.heappushpop(emptyBlocks, i)
    if j >= i:
      # we're done.
      break
    blocks[j] = blocks[i]
    blocks[i] = '.'
  return blocks

def defragPart2(blocks, blockSpans, spans):
  for i in range(len(blockSpans)-1, -1, -1):
    fid, s, j = blockSpans[i]
    k = 0
    found = False
    while k < len(spans):
      start = spans[k]
      if start[0] >= j:
        # don't move files "right".
        break
      if start[1] < s:
        # if it's not big enough, keep going.
        k += 1
        continue
   
      # we're going to use this slot, so push the empty one that will be created. 
      if start[1] > s: 
        spans.insert(0, (start[0]+s, start[1]-s))
        spans.sort()
      # Move the blocks. 
      found = True
      for i in range(s):
        blocks[start[0]+i] = fid
        blocks[j+i] = '.'
      break
    if found:
      spans.pop(k)
      spans.append((j,s))
  return blocks

def printBlocks(blocks):
  print('|'.join([str(x) for x in blocks]))

def checksum(blocks):
  cs = 0
  for i in range(len(blocks)):
    if blocks[i] == '.':
      continue
    cs += blocks[i]*i
  return cs

def main():
  f = open(sys.argv[1])
  blocks, emptyBlocks, spans, fileSpans = parse(f.readlines()[0])
  f.close()
  
  #part 1
  defragged = defragPart1(blocks, emptyBlocks)
  cs = checksum(defragged)
  print("Result part1:", cs)
  

  defragged2 = defragPart2(blocks, fileSpans, spans)
  cs = checksum(defragged2)
  printBlocks(defragged2)
  print("Result part2:", cs)
  ## 6547228115826
if __name__=="__main__":
  main()
