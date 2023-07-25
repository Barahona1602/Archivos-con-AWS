# IMPORT LIBRARIES
import boto3
# IAM user credentials
aws_access_key_id = "AKIA6FWVCESV2P5OT3TL"
aws_secret_access_key = "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"

def setCredentials():
  s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
  )
  # return s3 client 
  return s3

# test
if __name__ == "__main__":
  s3 = setCredentials()
  response = s3.list_buckets()

  # Print bucket names
  for bucket in response['Buckets']:
      print(bucket['Name'])