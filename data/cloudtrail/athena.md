



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



View the last 25 Creates (that have an associated IP) filtering out CloudWatch noise

```
select  (ts,source_ip,event_action,event_provider) from matano.aws_cloudtrail_view where event_action LIKE 'Create%' and event_action not like '%LogStream' and source_ip is not null order by ts desc limit 25;
 _col0
-----------------------------------------------------------------------------------------
 {2023-03-08 18:10:56.000, 173.67.45.221, CreateSecurityGroup, ec2.amazonaws.com}
 {2023-03-08 18:10:27.000, 173.67.45.221, CreateInstanceProfile, iam.amazonaws.com}
 {2023-03-08 18:10:25.000, 173.67.45.221, CreateRole, iam.amazonaws.com}
 {2023-03-08 18:07:35.000, 173.67.45.221, CreateKeyPair, ec2.amazonaws.com}
 {2023-03-08 18:01:47.000, 173.67.45.221, CreatePolicy, iam.amazonaws.com}
 {2023-03-08 17:58:43.000, 173.67.45.221, CreateRouteTable, ec2.amazonaws.com}
 {2023-03-08 17:58:42.000, 173.67.45.221, CreateRoute, ec2.amazonaws.com}
 {2023-03-08 17:58:42.000, 173.67.45.221, CreateRouteTable, ec2.amazonaws.com}
 {2023-03-08 17:58:41.000, 173.67.45.221, CreateSubnet, ec2.amazonaws.com}
 {2023-03-08 17:58:41.000, 173.67.45.221, CreateRouteTable, ec2.amazonaws.com}
 {2023-03-08 17:58:41.000, 173.67.45.221, CreateInternetGateway, ec2.amazonaws.com}
 {2023-03-08 17:58:40.000, 173.67.45.221, CreateSubnet, ec2.amazonaws.com}
 {2023-03-08 17:58:40.000, 173.67.45.221, CreateSubnet, ec2.amazonaws.com}
 {2023-03-08 17:58:39.000, 173.67.45.221, CreateVpcEndpoint, ec2.amazonaws.com}
 {2023-03-08 17:58:39.000, 173.67.45.221, CreateSubnet, ec2.amazonaws.com}
 {2023-03-08 17:58:37.000, 173.67.45.221, CreateVpc, ec2.amazonaws.com}
 {2023-03-08 12:43:11.000, 173.67.45.221, CreateAccessKey, iam.amazonaws.com}
 {2023-02-17 16:13:06.000, 173.67.45.221, CreateChangeSet, cloudformation.amazonaws.com}
 {2023-02-16 11:24:13.000, 173.67.45.221, CreateBucket, s3.amazonaws.com}
 {2023-02-15 23:34:48.000, 173.67.45.221, CreatePolicyVersion, iam.amazonaws.com}
 {2023-02-15 23:20:20.000, 173.67.45.221, CreateAccessKey, iam.amazonaws.com}
 {2023-02-15 23:19:49.000, 173.67.45.221, CreateUser, iam.amazonaws.com}
 {2023-02-15 23:17:40.000, 173.67.45.221, CreatePolicy, iam.amazonaws.com}
 {2023-02-13 02:15:07.000, 173.67.45.221, CreateChangeSet, cloudformation.amazonaws.com}
 {2023-02-12 21:48:50.000, 173.67.45.221, CreateRole, iam.amazonaws.com}
(25 rows)
```

