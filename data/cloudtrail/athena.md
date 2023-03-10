



# Events

## Actions

Count the top 25 `Describe` API calls 

```
athena:matano_cloudtrail_view> select count(*) as cnt, event_action from matano.aws_cloudtrail_view where event_action LIKE 'Describe%' group by event_action order by cnt desc limit 25;
   cnt | event_action
-------+--------------------------------------
  3050 | DescribeEventAggregates
   687 | DescribeStackEvents
   251 | DescribeMetricFilters
   247 | DescribeStacks
   136 | DescribeInstances
    84 | DescribeInstanceTypes
    48 | DescribeAddresses
    45 | DescribeNetworkInterfaces
    42 | DescribeInstanceAttribute
    37 | DescribeInstanceStatus
    37 | DescribeAccountAttributes
    34 | DescribeChangeSet
    25 | DescribeSecurityGroups
    24 | DescribeInstanceInformation
    22 | DescribeTags
    22 | DescribeKey
    21 | DescribeTable
    21 | DescribeClassicLinkInstances
    21 | DescribeInstanceCreditSpecifications
    20 | DescribeImages
    17 | DescribeSubnets
    17 | DescribeVpcs
    16 | DescribeAvailabilityZones
    14 | DescribeSecurityGroupRules
    13 | DescribeHosts
(25 rows)
```

Find which services have `Create` operations

```
athena:matano_cloudtrail_view> select count(*) as cnt, event_provider from matano.aws_cloudtrail_view where event_action LIKE 'Create%' group by event_provider order by cnt desc;
   cnt | event_provider
-------+------------------------------
  5556 | logs.amazonaws.com
    33 | iam.amazonaws.com
    25 | lambda.amazonaws.com
    20 | kms.amazonaws.com
    16 | sqs.amazonaws.com
    13 | ec2.amazonaws.com
     8 | glue.amazonaws.com
     7 | s3.amazonaws.com
     5 | athena.amazonaws.com
     4 | cloudformation.amazonaws.com
     4 | sns.amazonaws.com
     3 | dynamodb.amazonaws.com
     3 | states.amazonaws.com
(13 rows)
```
