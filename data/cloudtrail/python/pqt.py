#!/usr/bin/env python3

import polars as pl 
import sys,psutil,platform,humanize

print ("Polars version:",pl.__version__)
print ("Platform:",platform.machine(),platform.python_version())

if "lazy" not in sys.argv:
  df = pl.read_parquet("*.parquet")
else:
  print("Lazy read")
  lazy = pl.scan_parquet("*.parquet")

print ("\nAWS Service Count")
aws_svc = df.filter( pl.col("source").struct["address"].str.contains("amazonaws.com") )
print('Records: ',len(aws_svc))

print (aws_svc.select( pl.col("source").struct["address"].value_counts(sort=True)))

print ("\nInfrequent Events")
print (aws_svc.select( pl.col("event").struct["action"].value_counts(sort=True) ).tail(15) ) 

print ("\nFrequent Events")
print (aws_svc.select( pl.col("event").struct["action"].value_counts(sort=True) ).head(15) ) 

print( "Process Memory", humanize.filesize.naturalsize( psutil.Process().memory_info().rss ))
print( "Virtual Memory", psutil.virtual_memory() )
