#!/usr/bin/env python3

import duckdb,humanize
import sys,psutil

db = duckdb.connect()

q = {}
q['aws_svc_cnt'] = """select source.address, count(*) as cnt from aws_cloudtrail 
                      where source.address like '%amazonaws.com' group by source.address order by cnt desc;"""
q['infreq_events'] = """select event.action, count(*) as cnt from aws_cloudtrail 
group by event.action order by cnt limit 15;"""

db.execute('set threads to 4')

if "view" not in sys.argv:
  db.execute('create table aws_cloudtrail as select * from "*.parquet"')
else:
  db.execute('create view aws_cloudtrail as select * from "*.parquet"')

print( humanize.intword(db.execute('select count(*) from aws_cloudtrail').fetchall()[0][0] ))

for k,v in q.items():
  print (f"=== {k} ===")
  print( db.execute(v).fetchall())
  print( "Process Memory", humanize.filesize.naturalsize( psutil.Process().memory_info().rss ))
  print( "Virtual Memory", psutil.virtual_memory() )
