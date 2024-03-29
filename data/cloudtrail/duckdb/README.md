# A First Look at the Data

Matano creates [ECS](https://www.elastic.co/guide/en/ecs/current/index.html) records based a [VRL Transforms](https://github.com/matanolabs/matano/blob/main/data/managed/log_sources/aws_cloudtrail/log_source.yml) that results in events like this when loaded into DuckDB from Parquet files with:

```
create table aws_cloudtrail as select * from "*.parquet";
```

And looking at the fields

```
select * from aws_cloudtrail limit 2;
        ts = 2023-03-07 19:11:30
       aws = {'cloudtrail': {'event_version': 1.08, 'user_identity': {'type': AssumedRole, 'arn': arn:aws:sts::XXXXX3:assumed-role/MatanoDPMainStack-IcebergMetadataWriterFunctionSer-1LW39UZEYJKXX/MatanoDPMainStack-IcebergMetadataWriterFunctionC5F-CQ94l7hRz9pI, 'access_key_id': ASIAXX, 'session_context': {'mfa_authenticated': false, 'creation_date': 2023-03-07 19:11:14, 'session_issuer': {'type': Role, 'principal_id': AROAXXXW, 'arn': arn:aws:iam::XXXXXX:role/MatanoDPMainStack-IcebergMetadataWriterFunctionSer-1LW39UZEYJKXX, 'account_id': XXXXXX}}, 'invoked_by': NULL}, 'error_code': NULL, 'error_message': NULL, 'request_parameters': NULL, 'response_elements': NULL, 'additional_eventdata': NULL, 'request_id': c9b63139-ded8-43e5-9450-45e99426cf58, 'event_type': AwsApiCall, 'api_version': NULL, 'management_event': true, 'read_only': true, 'resources': NULL, 'recipient_account_id': XXXXXX3, 'service_event_details': NULL, 'shared_event_id': NULL, 'vpc_endpoint_id': NULL, 'event_category': Management, 'console_login': NULL, 'flattened': {'additional_eventdata': {"insufficientLakeFormationPermissions":["matano:aws_cloudtrail"],"lakeFormationPrincipal":"arn:aws:iam::XXXXXXXX:role/MatanoDPMainStack-IcebergMetadataWriterFunctionSer-1LW39UZEYJKXX"}, 'request_parameters': {"databaseName":"matano","name":"aws_cloudtrail"}, 'response_elements': NULL, 'service_event_details': NULL}}}
    labels =
      tags =
     cloud = {'account': {'id': XXXXX}, 'availability_zone': NULL, 'instance': NULL, 'machine': NULL, 'project': NULL, 'provider': NULL, 'region': us-east-1}
 container =
       ecs = {'version': 8.5.0}
     error =
     event = {'action': GetTable, 'category': NULL, 'created': 2023-03-07 19:11:30, 'dataset': NULL, 'id': fec373d3-f2c6-486d-bec2-30efabd6fe05, 'ingested': NULL, 'kind': event, 'module': NULL, 'original': NULL, 'outcome': success, 'provider': glue.amazonaws.com, 'type': [info]}
      file =
     group =
      host =
   related =
    source = {'address': 52.87.243.1, 'as': NULL, 'geo': NULL, 'ip': 52.87.243.1}
      user = {'changes': NULL, 'id': AROAZNNSGYKOSARRMB6RW:MatanoDPMainStack-IcebergMetadataWriterFunctionC5F-CQ94l7hRz9pI, 'name': MatanoDPMainStack-IcebergMetadataWriterFunctionSer-1LW39UZEYJKXX, 'target': NULL}
user_agent = {'device': NULL, 'name': NULL, 'original': aws-sdk-java/2.17.131 Linux/4.14.255-301-238.520.amzn2.x86_64 OpenJDK_64-Bit_Server_VM/11.0.14.1+10-LTS Java/11.0.14.1 kotlin vendor/Amazon.com_Inc. exec-env/AWS_Lambda_java11 io/sync http/UrlConnection cfg/retry-mode/legacy, 'os': NULL, 'version': NULL}
```

NOTE: The best way is to set `.mode line` to be able to see fields vertically to get the display above, then you and switch back to `.mode d` to see the default output. 

See [CloudTrail Field Reference](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-record-contents.html)


# Timestamp


# Cloud

In a pure AWS environment the [ECS Cloud Fields](https://www.elastic.co/guide/en/ecs/current/ecs-cloud.html) and when ingesting only a single account's worth of cloutrail, are not super helpful beyond the region.

```
select cloud from aws_cloudtrail limit 1;
cloud = {'account': {'id': XXXXXXXXXX}, 'availability_zone': NULL, 'instance': NULL, 'machine': NULL, 'project': NULL, 'provider': NULL, 'region': us-east-1}
```

Count the number of records across all regions

```
select count(*) as cnt, cloud.region from aws_cloudtrail group by cloud.region;
┌────────┬───────────┐
│  cnt   │  region   │
│ int64  │  varchar  │
├────────┼───────────┤
│ 486632 │ us-east-1 │
│    168 │ us-west-1 │
│     80 │ us-east-2 │
│     90 │ eu-west-2 │
│     80 │ eu-west-1 │
│    124 │ us-west-2 │
└────────┴───────────┘
```

# Source (Network) 

`source.address` is the most common field you will use and can be internal sources or external sources.

```
select distinct (source.address) from aws_cloudtrail where cloud.region in ('eu-west-1','eu-west-2');
┌───────────────┐
│    address    │
│    varchar    │
├───────────────┤
│ 173.67.45.221 │
└───────────────┘
```

For CloudTrail events, `source.address` can also be the AWS Service making the call, for example:

```
select distinct (source.address) from aws_cloudtrail where source.address like '%amazonaws.com';
┌────────────────────────────────────────────────┐
│                    address                     │
│                    varchar                     │
├────────────────────────────────────────────────┤
│ cloudtrail.amazonaws.com                       │
│ lambda.amazonaws.com                           │
│ states.amazonaws.com                           │
│ events.amazonaws.com                           │
│ inspector.amazonaws.com                        │
│ inspector2.amazonaws.com                       │
│ ec2.amazonaws.com                              │
│ athena.amazonaws.com                           │
│ prod.kms-caller.lambda.us-east-1.amazonaws.com │
│ ec2-frontend-api.amazonaws.com                 │
│ cloudformation.amazonaws.com                   │
│ apigateway.amazonaws.com                       │
├────────────────────────────────────────────────┤
│                    12 rows                     │
└────────────────────────────────────────────────┘
```

And now to count them


```
select source.address, count(*) as cnt from aws_cloudtrail where source.address like '%amazonaws.com' group by source.address order by cnt desc;
┌────────────────────────────────────────────────┬───────┐
│                    address                     │  cnt  │
│                    varchar                     │ int64 │
├────────────────────────────────────────────────┼───────┤
│ states.amazonaws.com                           │ 83592 │
│ lambda.amazonaws.com                           │ 57133 │
│ cloudtrail.amazonaws.com                       │ 34207 │
│ events.amazonaws.com                           │  8060 │
│ cloudformation.amazonaws.com                   │  2966 │
│ athena.amazonaws.com                           │  2145 │
│ prod.kms-caller.lambda.us-east-1.amazonaws.com │   490 │
│ inspector.amazonaws.com                        │   176 │
│ inspector2.amazonaws.com                       │   168 │
│ ec2.amazonaws.com                              │    72 │
│ apigateway.amazonaws.com                       │     6 │
│ ec2-frontend-api.amazonaws.com                 │     1 │
├────────────────────────────────────────────────┴───────┤
│ 12 rows                                      2 columns │
└────────────────────────────────────────────────────────┘
```

# User information

## Identity 

```
select distinct (aws.cloudtrail.user_identity.type) from aws_cloudtrail;
┌─────────────┐
│    type     │
│   varchar   │
├─────────────┤
│ AssumedRole │
│ AWSService  │
│ IAMUser     │
│ Root        │
└─────────────┘
```

Now let's count

```
select aws.cloudtrail.user_identity.type, count(*) as cnt from aws_cloudtrail group by aws.cloudtrail.user_identity.type order by cnt desc;
┌─────────────┬───────┐
│    type     │  cnt  │
│   varchar   │ int64 │
├─────────────┼───────┤
│ AssumedRole │ 28521 │
│ AWSService  │  9452 │
│ IAMUser     │  1548 │
│ Root        │   105 │
└─────────────┴───────┘
```

Let's investigate Root access by combining with `user_agent`

```
select distinct (source.ip,user_agent.original) from aws_cloudtrail where aws.cloudtrail.user_identity.type == 'Root';
main.row(source.ip, user_agent.original) = {'v1': 173.67.45.221, 'v2': AWS Internal}

main.row(source.ip, user_agent.original) = {'v1': 173.67.45.221, 'v2': aws-internal/3 aws-sdk-java/1.12.414 Linux/5.10.165-126.735.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.362-b10 java/1.8.0_362 vendor/Oracle_Corporation cfg/retry-mode/standard}

main.row(source.ip, user_agent.original) = {'v1': NULL, 'v2': AWS Internal}

main.row(source.ip, user_agent.original) = {'v1': 173.67.45.221, 'v2': Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36}
```

# Event Categorization Fields

[ECS Categorization](https://www.elastic.co/guide/en/ecs/current/ecs-category-field-values-reference.html) fields are useful and include:

* event.type 
* event.action 
* event.outcome 
* event.provider

## Action

Often the most infrequent actions are the most useful

```
select event.action, count(*) as cnt from aws_cloudtrail group by event.action order by cnt limit 10;

┌───────────────────────────────┬───────┐
│            action             │  cnt  │
│            varchar            │ int64 │
├───────────────────────────────┼───────┤
│ CreateKeyPair                 │     1 │
│ AuthorizeSecurityGroupIngress │     1 │
│ DescribeCoipPools             │     1 │
│ DescribePublicIpv4Pools       │     1 │
│ AllocateAddress               │     1 │
│ AssociateAddress              │     1 │
│ ListRolePolicies              │     1 │
│ CreateInstanceProfile         │     1 │
│ AddRoleToInstanceProfile      │     1 │
│ CreateSecurityGroup           │     1 │
├───────────────────────────────┴───────┤
│ 10 rows                     2 columns │
└───────────────────────────────────────┘
```

## Outcome

These are either success or failure 

```
select distinct event.provider, event.action from aws_cloudtrail where event.outcome = 'failure' order by event.provider;
┌──────────────────────────────┬──────────────────────────────────┐
│           provider           │              action              │
│           varchar            │             varchar              │
├──────────────────────────────┼──────────────────────────────────┤
│ athena.amazonaws.com         │ StopQueryExecution               │
│ athena.amazonaws.com         │ GetQueryResults                  │
│ athena.amazonaws.com         │ StartQueryExecution              │
│ athena.amazonaws.com         │ GetWorkGroup                     │
│ cloudformation.amazonaws.com │ DescribeStacks                   │
│ dynamodb.amazonaws.com       │ DescribeTable                    │
│ ec2.amazonaws.com            │ DescribeSecurityGroupRules       │
│ glue.amazonaws.com           │ GetTable                         │
│ glue.amazonaws.com           │ UpdateTable                      │
│ glue.amazonaws.com           │ BatchGetTable                    │
│ iam.amazonaws.com            │ GetRolePolicy                    │
│ iam.amazonaws.com            │ GetAccountPasswordPolicy         │
│ inspector.amazonaws.com      │ StartAssessmentRun               │
│ lambda.amazonaws.com         │ GetEventSourceMapping20150331    │
│ logs.amazonaws.com           │ CreateLogStream                  │
│ logs.amazonaws.com           │ StartQuery                       │
│ organizations.amazonaws.com  │ ListDelegatedAdministrators      │
│ s3.amazonaws.com             │ GetBucketPolicy                  │
│ s3.amazonaws.com             │ GetBucketPolicyStatus            │
│ s3.amazonaws.com             │ GetAccountPublicAccessBlock      │
│ s3.amazonaws.com             │ GetBucketOwnershipControls       │
│ s3.amazonaws.com             │ ListBuckets                      │
│ s3.amazonaws.com             │ GetBucketWebsite                 │
│ s3.amazonaws.com             │ GetBucketObjectLockConfiguration │
│ s3.amazonaws.com             │ GetBucketTagging                 │
│ s3.amazonaws.com             │ GetBucketEncryption              │
│ s3.amazonaws.com             │ GetBucketLocation                │
│ s3.amazonaws.com             │ GetBucketPublicAccessBlock       │
│ securityhub.amazonaws.com    │ DescribeHub                      │
│ sns.amazonaws.com            │ GetTopicAttributes               │
├──────────────────────────────┴──────────────────────────────────┤
│ 30 rows                                               2 columns │
└─────────────────────────────────────────────────────────────────┘
```


## Type

```
select event.type, count(*) as cnt from aws_cloudtrail group by event.type;
┌───────────────────┬────────┐
│       type        │  cnt   │
│     varchar[]     │ int64  │
├───────────────────┼────────┤
│ [info]            │ 423557 │
│ [creation]        │     14 │
│ [user, info]      │     93 │
│ [group, info]     │     17 │
│ [user, change]    │     10 │
│ [admin, creation] │      1 │
│ [user, creation]  │      2 │
└───────────────────┴────────┘
```




## Provider
```
select distinct (event.provider, cloud.region) from aws_cloudtrail order by cloud.region;
┌───────────────────────────────────────────────────────────────────┐
│             main.row("event".provider, cloud.region)              │
│                  struct(v1 varchar, v2 varchar)                   │
├───────────────────────────────────────────────────────────────────┤
│ {'v1': glue.amazonaws.com, 'v2': us-east-1}                       │
│ {'v1': s3.amazonaws.com, 'v2': us-east-1}                         │
│ {'v1': sts.amazonaws.com, 'v2': us-east-1}                        │
│ {'v1': kms.amazonaws.com, 'v2': us-east-1}                        │
│ {'v1': logs.amazonaws.com, 'v2': us-east-1}                       │
│ {'v1': states.amazonaws.com, 'v2': us-east-1}                     │
│ {'v1': athena.amazonaws.com, 'v2': us-east-1}                     │
│ {'v1': health.amazonaws.com, 'v2': us-east-1}                     │
│ {'v1': iam.amazonaws.com, 'v2': us-east-1}                        │
│ {'v1': ec2.amazonaws.com, 'v2': us-east-1}                        │
│ {'v1': ram.amazonaws.com, 'v2': us-east-1}                        │
│ {'v1': ce.amazonaws.com, 'v2': us-east-1}                         │
│ {'v1': organizations.amazonaws.com, 'v2': us-east-1}              │
│ {'v1': securityhub.amazonaws.com, 'v2': us-east-1}                │
│ {'v1': signin.amazonaws.com, 'v2': us-east-1}                     │
│ {'v1': servicecatalog-appregistry.amazonaws.com, 'v2': us-east-1} │
│ {'v1': access-analyzer.amazonaws.com, 'v2': us-east-1}            │
│ {'v1': inspector.amazonaws.com, 'v2': us-east-1}                  │
│ {'v1': sts.amazonaws.com, 'v2': us-west-1}                        │
│ {'v1': ec2.amazonaws.com, 'v2': us-west-1}                        │
├───────────────────────────────────────────────────────────────────┤
│                              20 rows                              │
└───────────────────────────────────────────────────────────────────┘
```



## Outcomes 

```
select  count(*) as cnt, event.outcome from  aws_cloudtrail group by event.outcome;
┌───────┬─────────┐
│  cnt  │ outcome │
│ int64 │ varchar │
├───────┼─────────┤
│ 57159 │ success │
│   309 │ failure │
└───────┴─────────┘
```

Let's see the failures

```
select event.provider, count(*) as cnt from aws_cloudtrail where event.outcome = 'failure' group by event.provider order by cnt desc;
┌───────────────────────────┬───────┐
│         provider          │  cnt  │
│          varchar          │ int64 │
├───────────────────────────┼───────┤
│ athena.amazonaws.com      │   251 │
│ glue.amazonaws.com        │    46 │
│ inspector.amazonaws.com   │     6 │
│ s3.amazonaws.com          │     2 │
│ securityhub.amazonaws.com │     2 │
│ logs.amazonaws.com        │     2 │
└───────────────────────────┴───────┘
```

What error codes are there for these failures?

```
select distinct ( aws.cloudtrail.error_code, event.provider)  from aws_cloudtrail where event.outcome = 'failure';;
┌───────────────────────────────────────────────────────────────────┐
│       main.row(aws.cloudtrail.error_code, "event".provider)       │
│                  struct(v1 varchar, v2 varchar)                   │
├───────────────────────────────────────────────────────────────────┤
│ {'v1': AccessDenied, 'v2': athena.amazonaws.com}                  │
│ {'v1': NoSuchBucket, 'v2': s3.amazonaws.com}                      │
│ {'v1': InvalidRequestException, 'v2': athena.amazonaws.com}       │
│ {'v1': EntityNotFoundException, 'v2': glue.amazonaws.com}         │
│ {'v1': InvalidAccessException, 'v2': securityhub.amazonaws.com}   │
│ {'v1': NoSuchEntityException, 'v2': inspector.amazonaws.com}      │
│ {'v1': ConcurrentModificationException, 'v2': glue.amazonaws.com} │
│ {'v1': ResourceAlreadyExistsException, 'v2': logs.amazonaws.com}  │
└───────────────────────────────────────────────────────────────────┘
```

Which user failed to access S3?

```
select aws_cloudtrail.user.name, event.action, ts,source.address from aws_cloudtrail where event.outcome = 'failure' and event.provider = 's3.amazonaws.com';
┌─────────┬───────────────────┬─────────────────────┬──────────────────────┐
│  name   │      action       │         ts          │       address        │
│ varchar │      varchar      │      timestamp      │       varchar        │
├─────────┼───────────────────┼─────────────────────┼──────────────────────┤
│ asus    │ GetBucketLocation │ 2023-03-08 01:26:00 │ athena.amazonaws.com │
│ asus    │ GetBucketLocation │ 2023-03-08 01:26:00 │ athena.amazonaws.com │
└─────────┴───────────────────┴─────────────────────┴──────────────────────┘
```

Find Non-AWS User agents 

```
select distinct (user_agent.original, source.address) from aws_cloudtrail where event.outcome = 'failure' and user_agent.original NOT LIKE '%amazonaws.com';
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                main.row(user_agent.original, source.address)                                                 │
│                                                        struct(v1 varchar, v2 varchar)                                                        │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ {'v1': Boto3/1.26.27 Python/3.9.2 Linux/5.10.159-20950-g3963226d9eb4 Botocore/1.29.27, 'v2': 173.67.45.221}                                  │
│ {'v1': Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36, 'v2': 173.67.45.221} │
│ {'v1': awslambda-worker/1.0 rusoto/0.48.0 rust/1.66.0 linux, 'v2': 3.236.107.97}                                                             │
│ {'v1': Boto3/1.26.69 Python/3.10.6 Linux/5.15.0-60-generic Botocore/1.29.69, 'v2': 173.67.45.221}                                            │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


