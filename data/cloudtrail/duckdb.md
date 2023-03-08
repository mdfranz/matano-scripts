# A First Look at the Data

The best way is to set `.mode line` to be able to see fields vertically

```
D select * from aws_cloudtrail limit 2;
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

# User Identity 


```
D select distinct (aws.cloudtrail.user_identity.type) from aws_cloudtrail;
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
D select aws.cloudtrail.user_identity.type, count(*) as cnt from aws_cloudtrail group by aws.cloudtrail.user_identity.type order by cnt desc;
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


# User Agents

```
select distinct (user_agent.original, source.address) from aws_cloudtrail;
```
