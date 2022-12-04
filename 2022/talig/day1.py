import sys
import numpy

def process_input(lines):
  elves = []
  sums = []
  i = 0
  for line in lines:
    if line == '\n':
      sums.append((sum(elves[i]),i))
      i+=1
    else:
      if len(elves) == i:
        elves.append([])

      elves[i].append(int(line))

  return elves, sums


def main():
  f = open(sys.argv[1])
  lines = f.readlines()
  f.close()

  elves,sums = process_input(lines)
  print("part 1")
  print("elf with most calories:", max([x[0] for x in sums]))
  print("part 2")
  sums = sorted(sums, key=lambda x: x[0], reverse=True)
  print("top 3 total: ", sum([x[0] for x in sums[:3]]))


if __name__== "__main__":
  main()

