import sys
import re
import collections


class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def add(self, p):
    return Point(self.x + p.x, self.y + p.y)

  def mul(self, times):
    return Point(self.x * times, self.y * times)

  def __str__(self):
    return "(" + str(self.x) + ", " + str(self.y) + ")"


DIRECTION = [Point( 1, 0), Point(0, 1), Point(1, 1), Point(1, -1)]
X_MARK = [ Point(-1, 1), Point(-1,-1),Point(1, -1), Point(1, 1)]
QUERY = 'XMAS'
QUERYR = 'SAMX'

ROTATIONS = set(["SMMS", "MMSS","MSSM","SSMM"])

# PART 2:
# A is always in the middle. 
# ends are rotations of "SSMM" :"SMMS", "MMSS","MSSM","SSMM"

def parse_part1(lines):
  boggle = []
  for line in lines:
    line = line.strip()
    if line == "":
      continue
    boggle.append(list(line))
  return boggle

def inRange(curr, width, height):
  if curr.x < 0 or curr.x >= width:
    return False
  if curr.y < 0 or curr.y >= height:
    return False
  return True

def getPoint(boggle, point):
  return boggle[point.y][point.x]

def buildWord(boggle, start, d, l):
  word = []
  # don't start if there's no point
  end = start.add(d.mul(l-1))
  if not inRange(end, len(boggle[0]), len(boggle)):
    #print("skipping: ", start, "End ", end ," not in range")
    return ""
  curr = start
  for i in range(l):
    word.append(getPoint(boggle, curr))
    curr = curr.add(d)
  return ''.join(word)


def isWord(word):
  return QUERY == word or QUERYR == word
    

def getWord(boggle, start):
  words = set()
  for d in DIRECTION:
    w = buildWord(boggle, start, d, len(QUERY))
    #print("built: ", w)
    if isWord(w):
      words.add((start, d))
  return words

def isX(boggle, start):
  if getPoint(boggle, start) != 'A':
    return False
  word = ""
  for x in X_MARK:
    word += getPoint(boggle, start.add(x))
  
  return word in ROTATIONS 


def find(boggle, part):
  # Take the word to find as a list. 
  words = set()
  for y in range(len(boggle)):
    for x in range(len(boggle[0])):
      start = Point(x, y)
      found = set()
      if part == 1:
        found.update(getWord(boggle, start))
      if part == 2: 
        if y == 0 or x == 0 or y ==len(boggle)-1 or x == len(boggle[0]) - 1:
          continue  # We're checking from the middle A.
        if isX(boggle, start):
          found.add(start)
      words.update(found)
  return words


def main():
  f = open(sys.argv[1])
  boggle = parse_part1(f.readlines())
  f.close()
  total = find(boggle,1)
 
  total2 = find(boggle,2)

  print("Result part1:", len(total))
  print("Result part2:", len(total2))


if __name__=="__main__":
  main()
