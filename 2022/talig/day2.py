import sys
import numpy

SCORE = {0: 0, 1:3, 2:6}

def process_input_pt1(lines):
  total_score = 0
  for line in lines:
    elf = ord(line[0])
    me = ord(line[1])
    score = me - ord('X') +1 + SCORE[(me - elf - 22)%3]
    total_score += score
  return total_score

def process_input_pt2(lines):
  total_score = 0
  for line in lines:
    elf = ord(line[0]) - ord('A')
    outcome = ord(line[1]) - ord('X')
    me = (elf + outcome + 2)%3 + 1 # 0 lose 1 draw and 2 win.
    score = me + SCORE[outcome]
    total_score += score
  return rounds, total_score

def main():
  f = open(sys.argv[1])
  lines = [line.split() for line in f.readlines()]
  f.close()

  total_score = process_input_pt1(lines)
  print("part 1")
  print("total score:" , total_score)
  print("part 2")
  total_score = process_input_pt2(lines)
  print("total score:" , total_score)


if __name__== "__main__":
  main()

