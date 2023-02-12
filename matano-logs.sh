for lg in `awslogs groups | grep Matano`
do 
  awslogs get --ingestion-time $lg $*
done
