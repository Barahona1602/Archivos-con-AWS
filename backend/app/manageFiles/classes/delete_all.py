import os
import shutil
# class to create files in local or bucket s3
from ..setCredentials import setCredentials

class Delete_all():
  # constructor
  def __init__(self, type) -> None:
    self.type = type
    # set credentials
    self.s3 = setCredentials()
  

  # delete all files in local
  def local(self):
    # Get the absolute path of the project directory
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    path = os.path.join(root_dir, "Archivos")
    if os.path.exists(path):
      # delete files and directories
      shutil.rmtree(path)
      return {
        "status": "success",
        "message": f"Archivos eliminados exitosamente en el servidor"
      }
    else:
      return {
        "status": "error",
        "message": f"No existen la carpeta 'Archivos' en el servidor"
      }

  # delete all files and directories in bucket s3
  def bucket(self):
    bucket_name = "mia-proyecto2"
    object_key = "Archivos/"
    objects = self.s3.list_objects(Bucket=bucket_name, Prefix=object_key)
    if "Contents" in objects:
      key = [obj["Key"] for obj in objects["Contents"]]
      self.s3.delete_objects(Bucket=bucket_name, Delete={"Objects": [{"Key": k} for k in key]})
      return {
        "status": "success",
        "message": f"Carpeta {object_key} eliminada exitosamente del bucket"
      }
    else:
      return {
        "status": "error",
        "message": f"La carpeta {object_key} no existe en el bucket"
      }