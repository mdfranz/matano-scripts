#!/usr/bin/env python3

# Remove all the buckets that start with matano in the region specified

import boto3,sys
DEBUG=False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Usage: matano-bucket-empty.py <region> [debug]")
        sys.exit(1)

    if len(sys.argv) == 3: 
        if sys.argv[2] == 'debug':
            DEBUG = True
   
    bucket_region = sys.argv[1]
    
    s3 = boto3.resource('s3',region_name=bucket_region)
    
    for b in s3.buckets.all():
        if b.name.startswith('matano'):    
            for key in b.objects.all():
                if DEBUG:
                    print ("Deleting %s" % key.key)
                key.delete()
                
            if DEBUG:
                print ("Bucket %s emptied" % b)
            b.delete()