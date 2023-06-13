#!/usr/bin/env python3

import psutil,humanize,platform,cpuinfo
import pandas as pd
from pathlib import Path                           

print ("Pandas version:",pd.__version__)
print ("Platform:",platform.machine(),platform.python_version())
print ("CPU:", cpuinfo.get_cpu_info()['brand_raw'])

data_dir=Path(".")                          
df = pd.concat(                         
  pd.read_parquet(parquet_file)           
  for parquet_file in data_dir.glob('*.parquet')
) 

# SQL: select source.address, count(*) as cnt from aws_cloudtrail where source.address like '%amazonaws.com' group by source.address order by cnt desc;"""
print ("\nAWS Service Count")
aws_svc = df[df['source'].apply(lambda x: x.get("address").find("amazonaws.com") >= 0) ]
print('Records: ',len(aws_svc))
print(aws_svc['source'].apply(lambda x: x.get("address")).value_counts())

print ("\nInfrequent Events") 
# SQL: select event.action, count(*) as cnt from aws_cloudtrail group by event.action order by cnt limit 15;
print(df['event'].apply(lambda x: x.get("action")).value_counts().nsmallest(n=15))


print ("\nFrequent Events") 
print(df['event'].apply(lambda x: x.get("action")).value_counts().nlargest(n=15))

print( "Process Memory", humanize.filesize.naturalsize( psutil.Process().memory_info().rss ))
print( "Virtual Memory", psutil.virtual_memory() )
