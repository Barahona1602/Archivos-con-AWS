# IMPORT LIBRARIES
import logging
from botocore.exceptions import ClientError
# import project files
from ..setCredentials import setCredentials


# def upload image to s3 bucket using an endpoint
def uploadImageToS3Bucket(image, object_name):
  # s3 client
  s3 = setCredentials()
  # Upload the file
  try:
    response = s3.upload_fileobj(image, "202109567", "files/" + object_name)
    return response
  except ClientError as e:
    logging.error(e)
    return {"status": "error", "message": "Error uploading file", "error": e}