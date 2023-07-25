import os
import shutil
from ..setCredentials import setCredentials
# if the path does not exist, return error
# if the name comes but the name file does not exist, return error
# if the name does not come, delete the folder

class Delete():
  def __init__(self, path, name, type) -> None:
    self.path = path
    self.name = name
    self.type = type
    self.s3 = setCredentials()

  def local(self):
    path = self.path.replace('"', '').lstrip('/').rstrip('/')
    name = self.name
    # evaluate if the name is not false
    print(self.name)
    if not self.name:
      name = ""
    # Get the absolute path of the project directory
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    file_ = os.path.join(root_dir, "Archivos", path, name)

    if os.path.exists(file_):
      if os.path.isfile(file_):
        print("archivo?",file_)
        os.remove(file_)
        return {
          "status": "success",
          "message": f"Archivo {name} eliminado exitosamente en el server"
        }
      elif os.path.isdir(file_):
        print("CARPETA?", file_)
        shutil.rmtree(file_)
        return {
          "status": "success",
          "message": f"Carpeta {name} eliminada exitosamente en el server"
        }
    else:
      return {
        "status": "error",
        "message": f"El archivo o carpeta {name} no existe en el server"
      }

  def bucket(self):
    bucket_name = "mia-proyecto2"
    name = self.name

    if self.name == False:
      object_key = 'Archivos' + self.path + ""
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
    else:
      object_key = 'Archivos' + self.path + name
      # evaluate if the name is the key exist
      objects = self.s3.list_objects(Bucket=bucket_name, Prefix=object_key)
      if not "Contents" in objects:
        return {
          "status": "error",
          "message": f"El archivo {name} no existe en el bucket"
        }

      try:
        self.s3.delete_object(Bucket=bucket_name, Key=object_key)

        return {
          "status": "success",
          "message": f"Archivo {name} eliminado exitosamente en el bucket"
        }
      except Exception as e:
        return {
          "status": "error",
          "message": f"Error al eliminar archivo {name} en el bucket: {e}"
        }