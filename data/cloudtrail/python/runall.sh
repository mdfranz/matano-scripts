for p in `ls *.py`
do
  echo
  echo "==== $p ===="
  time python3 $p
  sleep 1
done
