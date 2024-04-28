import time
import numpy as np
import cv2

try:
    import boto3
except:
    boto3 = None


def s3_reader(bucket, prefix, *, 
    seekable=False, 
    profile_name=None, 
    region_name=None, 
    aws_access_key_id=None, 
    aws_secret_access_key=None, 
    aws_session_token=None,
    endpoint_url=None
):

    print(f"Building picamkit.ops.sources.s3_reader")


    # create the s3 client
    session = boto3.Session(
        profile_name=profile_name,
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token
    )
    client = session.client('s3')

    def gen():
        for idx, key in enumerate(_s3_scanner(client, bucket, prefix)):
            response = client.get_object(
                Bucket=bucket,
                Key=key
            )
            
            reader = response['Body']
            try:
                ibuf = np.asarray(bytearray(reader.read()))
                img = cv2.imdecode(ibuf, cv2.IMREAD_COLOR)
            finally:
                reader.close()
            
            item = {
                'idx': idx,
                'stamp': time.monotonic_ns(),
                'metadata': {
                    'name': f's3://{bucket}/{key}',
                },
                'main': {
                    'format': 'RGB888',
                    'image': img
                }
            }
            yield item

    return gen()


def _s3_scanner(client, bucket, prefix):

    def gen():
        resp = client.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix,
        )
        
        while True:
            contents = resp.get('Contents', [])
            for c in contents:
                key = c['Key']
                if key.endswith('png'):
                    yield key

            if resp['IsTruncated'] == False:
                break

            ctoken = resp['NextContinuationToken']
            resp = client.list_objects_v2(
                Bucket=bucket,
                Prefix=prefix,
                ContinuationToken=ctoken,
            )

    return gen()

