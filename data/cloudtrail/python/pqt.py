#!/usr/bin/env python3

import polars as pl 
import sys,psutil,humanize

if "lazy" not in sys.argv:
  df = pl.read_parquet("*.parquet")
else:
  print("Lazy read")
  lazy = pl.scan_parquet("*.parquet")

print( "Process Memory", humanize.filesize.naturalsize( psutil.Process().memory_info().rss ))
print( "Virtual Memory", psutil.virtual_memory() )
