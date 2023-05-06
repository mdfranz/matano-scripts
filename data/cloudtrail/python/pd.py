#!/usr/bin/env python3

import psutil,humanize,platform
import pandas as pd
from pathlib import Path                           

print ("Pandas version:",pd.__version__)
print ("Platform:",platform.machine(),platform.python_version())


data_dir=Path(".")                          

df = pd.concat(                         
  pd.read_parquet(parquet_file)           
  for parquet_file in data_dir.glob('*.parquet')
) 

print( "Process Memory", humanize.filesize.naturalsize( psutil.Process().memory_info().rss ))
print( "Virtual Memory", psutil.virtual_memory() )
