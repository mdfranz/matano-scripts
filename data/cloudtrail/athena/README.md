# Python Athena CLI

Interactive connection with [athena-cli](https://pypi.org/project/athena-cli/)

```
athena --profile foo --region us-east-1 --workgroup matano_default --db matano_cloudtrail_view
```

To do a vertical dump, removing NULL fields

```
$ athena --region us-east-1 --workgroup matano_default --db matano_cloudtrail_view --output-format VERTICAL --execute "select * from matano.aws_cloudtrail_view where cloud_region='us-west-1' limit 1" | grep -v NULL
--[RECORD 1]--
 ts                                                                       | 2023-03-09 09:11:58.000
 aws_cloudtrail_event_version                                             | 1.08
 aws_cloudtrail_user_identity_type                                        | AWSService
 aws_cloudtrail_user_identity_invoked_by                                  | inspector2.amazonaws.com
 aws_cloudtrail_request_id                                                | 474ea417-26c8-48c8-ad9c-567f3c2ce671
 aws_cloudtrail_event_type                                                | AwsApiCall
 aws_cloudtrail_management_event                                          | true
 aws_cloudtrail_read_only                                                 | true
 aws_cloudtrail_recipient_account_id                                      | XXXXXXX
 aws_cloudtrail_event_category                                            | Management
 aws_cloudtrail_flattened_request_parameters                              | {"durationSeconds":3600,"roleArn":"arn:aws:iam::XXXXXXX:role/aws-service-role/inspector2.amazonaws.com/AWSServiceRoleForAmazonInspector2","roleSessionName":"MandoService7696354707953764922"}
 aws_cloudtrail_flattened_response_elements                               | {"assumedRoleUser":{"arn":"arn:aws:sts::XXXXXXX:assumed-role/AWSServiceRoleForAmazonInspector2/MandoService7696354707953764922","assumedRoleId":"AROAZNNSGYKOSJMONYTBQ:MandoService7696354707953764922"},"credentials":{"accessKeyId":"ASIAZNNSGYKO5UOGNP5N","expiration":"Mar 9, 2023, 10:11:58 AM","sessionToken":"IQoJb3JpZ2luX2VjEKH//////////wEaCXVzLXdlc3QtMSJIMEYCIQDz7MbGLvd188e7J/cPt1paI8OzyPoXoSwkA0FuV0JzwAIhAIL+/9f5F6kPGUexwKvWudJ/r0+KYYLJdYEPEhwCrGw3KuoCCFoQABoMNjQ3MzAzMTg1MDUzIgxkSgChn6IVE8RiFLIqxwJykZrEPTko/CxVvg9ko/60HOrghzls/ugTJWzvweuhV4R/USarJCGIZsxE6MAY7jXIMldL0A9RMY6CMcMDUvwpn7C/OKndwUYZz/ha+i6KeW+2PXE3tR4z1RXBMfpjRn+EdCjPkTPrWRKKmEDP/0ZxRwkWHuoo0yWxWOFub4QAf90SBb0SKUcSMcB30dr28Zgu7dWBD6FqsnqMyfbyKkfA6RXHYmlv8tEGpTAljUWssY/6l1E3j2JkQcFVDCwrgvF/jI+Tv4hIr4q2mJY7tddAzmhRCn3JvNRexroUz0ZMOKaNtQ7cCGIEgLKZb0jJproXt19dZyF/fxOQqSA2eJHr9LmA9JByVnj6D8fP1Yw64gmMDLcg26NcX3iI8jL/iMCaKgj3YxRsWR/jrbV5feZ+135+XRQYXax927eFNcPSRl8qaTx8tusw3sWmoAY6vgGoyPyWutdZ4/RdtVrizo3r5GMxK+lBOh67R4+O87hIX3MlK4/FqIKrgr1ryjMV7fH/4KTlslpVma3zr+BF3zAj8MEQYS3lHmyg7PXjEVfItka3GwgBFpWtpmULH67ZWTPdWToahRlPtsoMOj52mKs7NCkSV+NPdLgDtoVsvM1Y4S5sN9Gmf68iMMfmtf6ucDJNM8GWOeSFtzrhgtX5Me1Uko3htTXrUliuDLTy8u/32nnieeq7eTg6FpEL85mo"}}
 cloud_region                                                             | us-west-1
 ecs_version                                                              | 8.5.0
 event_action                                                             | AssumeRole
 event_category                                                           | [authentication]
 event_created                                                            | 2023-03-09 09:11:58.000
 event_id                                                                 | dba169ea-09f1-444f-aa72-c912b9ec60ef
 event_kind                                                               | event
 event_outcome                                                            | success
 event_provider                                                           | sts.amazonaws.com
 event_type                                                               | [info]
 source_address                                                           | inspector2.amazonaws.com
 user_agent_original                                                      | inspector2.amazonaws.com
```


# Timestamp


# Cloud

# CloudTrail (aws_cloudtrail_*)

A nice way to find Console Activity by filtering out `AwsApiCall` events

```
select distinct (cloud_region,aws_cloudtrail_event_category, event_provider, aws_cloudtrail_event_type, source_address) from matano.aws_cloudtrail_view where aws_cloudtrail_event_type != 'AwsApiCall';
 _col0                                               
----------------------------------------------------------------------------------------
 {us-east-1, Management, ec2.amazonaws.com, AwsServiceEvent, ec2.amazonaws.com}
 {us-east-1, Management, billingconsole.amazonaws.com, AwsConsoleAction, 173.67.45.221}
 {us-east-1, Management, signin.amazonaws.com, AwsConsoleSignIn, 173.67.45.221}
```

Event Types - `aws_cloudtrail_event_type`

```
select count(*) as cnt, aws_cloudtrail_event_type from matano.aws_cloudtrail_view group by aws_cloudtrail_event_type order by cnt desc;
    cnt | aws_cloudtrail_event_type                  
--------+-----------------------------
 252846 | AwsApiCall
    140 | AwsConsoleAction
      9 | AwsConsoleSignIn
      3 | AwsServiceEvent
```

Confirm it was me doing things at the console
```
select distinct(source_address, user_agent_original) from matano.aws_cloudtrail_view where aws_cloudtrail_event_type='AwsConsoleAction';
 _col0                                               
----------------------------------------------------------------------------------------------------------------------------------
 {173.67.45.221, Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36}
 {173.67.45.221, Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36}
 {173.67.45.221, Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36}
(3 rows)
```
















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
# User

## Identity Invoked By

```
select count(*) as cnt, aws_cloudtrail_user_identity_invoked_by from matano.aws_cloudtrail_view group by aws_cloudtrail_user_identity_invoked_by order by cnt desc;    cnt | aws_cloudtrail_user_identity_invoked_by    
--------+------------------------------------------------
 153756 | NULL
  42819 | states.amazonaws.com
  29370 | lambda.amazonaws.com
  17583 | cloudtrail.amazonaws.com
   4142 | events.amazonaws.com
   1653 | AWS Internal
   1483 | cloudformation.amazonaws.com
   1118 | athena.amazonaws.com
    245 | prod.kms-caller.lambda.us-east-1.amazonaws.com
     92 | inspector.amazonaws.com
     84 | inspector2.amazonaws.com
     63 | ec2.amazonaws.com
      3 | apigateway.amazonaws.com
      1 | spot.amazonaws.com
      1 | ec2-frontend-api.amazonaws.com
(15 rows)
```


