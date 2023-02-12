aws cloudformation list-stacks | jq '.StackSummaries[] | select(.StackName | contains("Matano"))| select(.StackStatus | contains("DELETE")|not)'

for s in MatanoDPCommonStack MatanoDPMainStack
do
  aws cloudformation describe-stack-resources --stack-name $s | jq -r '.StackResources[] | select(.StackName | contains("Matano"))| [ .ResourceType, .PhysicalResourceId, .StackName] | @csv' | sort -t"," -k1
done


