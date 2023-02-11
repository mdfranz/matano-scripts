#!/usr/bin/env python3


# From https://importidea.dev/working-with-avro-file-format-in-python-the-right-way

from fastavro import reader
import sys,os

if __name__ == "__main__":
  for af in os.listdir(sys.argv[1]):
    with open(af,"rb")  as out:
      f = reader(out)
      for i in f:
        print(i)
