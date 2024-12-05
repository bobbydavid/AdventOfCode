import sys
import re

def parse_part1(text):
  pattern = re.compile('mul\((\d{1,3}),(\d{1,3})\)')
  return pattern.findall(text)

def parse_part2(text):
  text = text.replace('\n', '')
  drop = re.compile("don't\(\).*?do\(\)")
  return parse_part1("".join(drop.split(text)))

def compute(muls):
  return sum([int(t[0]) * int(t[1]) for t in muls])

def main():
  f = open(sys.argv[1])
  muls = parse_part1(f.read())
  f.close()
  total = compute(muls)
 
  f = open(sys.argv[1])
  muls = parse_part2("do()"+f.read()+"do()")
  f.close()
  total2 = compute(muls)

  print("Result part1:", total)
  print("Result part2:", total2)


if __name__=="__main__":
  main()
