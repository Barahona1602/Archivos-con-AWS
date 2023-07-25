import os
# class to create files in local or bucket s3
from ..setCredentials import setCredentials

class Create():
  # constructor
  def __init__(self, name, body, path, type) -> None:
    self.name = name
    self.body = body
    self.path = path
    self.type = type
    # set credentials
    self.s3 = setCredentials()
  
  
  # create file in local

  def local(self):
    name = self.validate_filename(self.name)
    path = self.path.replace('"', '')
    path = self.path.lstrip('/')

    # Get the absolute path of the project directory
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

    file_ = os.path.join(root_dir, "Archivos", path, name)
    if not os.path.exists(file_):
      os.makedirs(os.path.dirname(file_), exist_ok=True)

      with open(file_, "w") as f:
        f.write(self.body)

      return {
        "status": "success",
        "message": f"Archivo {name} creado exitosamente en el server"
      }
    else:
      return {
        "status": "error",
        "message": f"El archivo {name} ya existe en el server"
      }

  

  # create file in bucket s3
  def bucket(self):
    bucket_name = "mia-proyecto2"
    object_key = 'Archivos' + self.path + self.name
    try:
      # evaluate if the file exists
      list_objects = self.s3.list_objects(Bucket=bucket_name, Prefix=object_key)
      if 'Contents' in list_objects:
        return {
          "status": "error",
          "message": f"El archivo {self.name} ya existe en el bucket"
        }
      self.s3.put_object(Bucket=bucket_name, Key=object_key, Body=self.body)
      return {
        "status": "success",
        "message": f"Archivo {self.name} creado exitosamente en el bucket"
      }
    except Exception as e:
      return {
        "status": "error",
        "message": f"Error al crear archivo {self.name} {object_key} ya existe en el bucket"
      }


  def validate_filename(self,name):
    if name:
      if not name.endswith(".txt"):
        name += ".txt"
    return name