#!/usr/bin/env python3

import duckdb
import sys,psutil

db = duckdb.connect()

if "view" not in sys.argv:
  db.execute('create table aws_cloudtrail as select * from "*.parquet"')
else:
  db.execute('create view aws_cloudtrail as select * from "*.parquet"')

print( db.execute('select count(*) from aws_cloudtrail').fetchall() )
print( "Process Memory", psutil.Process().memory_info().rss )
print( "Virtual Memory", psutil.virtual_memory() )
