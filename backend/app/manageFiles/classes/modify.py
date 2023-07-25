import os
import shutil
from ..setCredentials import setCredentials
# if the path does not exist, return error
# if the name comes but the name file does not exist, return error
# if the name does not come, delete the folder

class Modify():
  def __init__(self, path, body, type) -> None:
    self.path = path
    self.body = body
    self.type = type
    self.s3 = setCredentials()
  

  def local(self):
    path = self.path.replace("'","").lstrip('/').rstrip('/')
    # Get the absolute path of the project directory
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    file_ = os.path.join(root_dir, "Archivos", path)
    if os.path.exists(file_):
      if os.path.isfile(file_):
        with open(file_, "w") as f:
          f.write(self.body)
        return {
          "status": "success",
          "message": f"Archivo {self.path} modificado exitosamente en el server"
        }
      else:
        return {
          "status": "error",
          "message": f"El archivo {self.path} no existe en el server"
        }
    else:
      return {
        "status": "error",
        "message": f"El archivo {self.path} no existe en el server"
      }

  def bucket(self):
    name_bucket = "mia-proyecto2"
    origin_path_bucket = "Archivos" + self.path
    try:
      # evualuate if the file exists
      object_list_origin = self.s3.list_objects(Bucket=name_bucket, Prefix=origin_path_bucket)
      if "Contents" in object_list_origin:
        # if the file exists, copy the file to the new path
        object_list_origin = object_list_origin["Contents"][0]
        origin_path_bucket = object_list_origin["Key"]
        self.s3.put_object(Bucket=name_bucket, Key=origin_path_bucket, Body=self.body)
        return {
          "status": "success",
          "message": f"Archivo {self.path} modificado exitosamente en el bucket"
        }
      else:
        return {
          "status": "error",
          "message": f"El archivo {self.path} no existe en el bucket" 
        }
    except:
      return {
        "status": "error",
        "message": f"El archivo {self.path} no existe en el bucket"
      }
