#!/usr/bin/env python3

import polars as pl 
import sys,psutil,platform,humanize,cpuinfo

print ("Polars version:",pl.__version__)
print ("Platform:",platform.machine(),platform.python_version())
print ("CPU:", cpuinfo.get_cpu_info()['brand_raw'])

df = pl.read_parquet("*.parquet")

print ("\nAWS Service Count")
aws_svc = df.filter( pl.col("source").struct["address"].str.contains("amazonaws.com") )
print('Records: ',len(aws_svc))

for r in aws_svc.select( pl.col("source").struct["address"].value_counts(sort=True)).iter_rows():
  print(r)

print ("\nInfrequent Events")
for r in aws_svc.select( pl.col("event").struct["action"].value_counts(sort=True) ).tail(15).iter_rows():
  print(r)

print ("\nFrequent Events")
for r in aws_svc.select( pl.col("event").struct["action"].value_counts(sort=True) ).head(15).iter_rows():
  print(r)

print( "Process Memory", humanize.filesize.naturalsize( psutil.Process().memory_info().rss ))
print( "Virtual Memory", psutil.virtual_memory() )
