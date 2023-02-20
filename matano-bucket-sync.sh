#!/bin/bash

if [ "$1" = "lake" ]
then
  filter="matanodpcommonstack-matanolakestoragebucket"
else 
  filter="matano"
fi


for b in `aws s3 ls | grep $filter | cut -d" " -f3`
do
  echo "==== $b ===="
  [[ -d $b ]] || mkdir $b
  aws s3 sync s3://$b $b
  echo
  sleep 2
done
