for b in `aws s3 ls | grep matano | cut -d" " -f3`
do
  echo $b
  mkdir $b
  aws s3 sync s3://$b $b
done
