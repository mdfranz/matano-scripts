#!/usr/bin/bash 

if [[ -z "$*" ]]
then
  echo "Usage:"
  echo "   pqflat.sh <src_path> <pattern> <dst_path>"
fi

exit 

[[ -d $2 ]] || mkdir $2

for i in `find $1 -name "*.parquet" | grep $3`
do
  cp -av $i $2/
done
