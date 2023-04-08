#!/usr/bin/env python3

import polars as pl 
import sys,psutil

if "lazy" not in sys.argv:
  df = pl.read_parquet("*.parquet")
else:
  print("Lazy read")
  lazy = pl.scan_parquet("*.parquet")

print( "Process Memory", psutil.Process().memory_info().rss )
print( "Virtual Memory", psutil.virtual_memory() )
