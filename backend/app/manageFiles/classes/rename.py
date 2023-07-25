import os
import shutil
from ..setCredentials import setCredentials
# if the path does not exist, return error
# if the name comes but the name file does not exist, return error
# if the name does not come, delete the folder

class Rename():
  def __init__(self, path, name, type) -> None:
    self.path = path
    self.name = name
    self.type = type
    self.s3 = setCredentials()

  
  def local(self):
    # return {
    #   "status": "error",
    #   "message": f"El archivo '{self.path}' -- '{self.name}' -- '{self.type}' ",
    # }
    path = self.path.replace("'","").lstrip('/').rstrip('/')
    # Get the absolute path of the project directory
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

    file_ = os.path.join(root_dir, "Archivos", path)

    if os.path.exists(file_):
      if os.path.isfile(file_):
        new_path = os.path.join(os.path.dirname(file_), self.name)

        if os.path.exists(new_path):
          return {
            "status": "error",
            "message": f"El archivo {self.name} ya existe en el server"
          }
        else:
          os.rename(file_, new_path)
          return {
            "status": "success",
            "message": f"Archivo {self.name} renombrado exitosamente en el server"
          }
      elif os.path.isdir(file_):
        parent_dir = os.path.dirname(file_)
        new_path = os.path.join(parent_dir, self.name.replace("'",""))

        if not os.path.exists(new_path):
          shutil.move(file_, new_path)
          return {
            "status": "success",
            "message": f"Archivo {self.name} renombrado exitosamente en el server"
          }
        else:
          return {
            "status": "error",
            "message": f"El archivo {self.name} ya existe en el server"
          }
    else:
      return {
        "status": "error",
        "message": f"El archivo {self.name} no existe en el server"
      }

  def bucket(self):
    # return {
    #   "status": "error",
    #   "message": f"El archivo {self.name} no existe  --- 'Archivos{self.path}' --- '{self.type}' --- '{self.name}' ",
    # }
    name_bucket = "mia-proyecto2"
    origin_path_bucket = "Archivos" + self.path
    new_path = self.path.split("/")
    destini_path_bucket = "Archivos" + "/".join(new_path[:-1]) + "/" + self.name.replace("'","")
    # print(origin_path_bucket, destini_path_bucket)
    # evaluate if its a file or a folder

    if origin_path_bucket.endswith("/"):
      # copy the file
      new_directory = "Archivos" + "/".join(new_path[:-2]) + "/" + self.name.replace("'","") + "/"
      print(new_directory , origin_path_bucket)

      # list the objects in the directory
      object_list_origin = self.s3.list_objects(Bucket=name_bucket, Prefix=origin_path_bucket)
      # Iterate over the objects and copy them to the new directory
      if "Contents" in object_list_origin:
        for obj in object_list_origin["Contents"]:
          # print(obj["Key"])
          # print(obj["Key"].split("/")[-1])
          # print(new_directory + obj["Key"].split("/")[-1])
          self.s3.copy_object(
            Bucket=name_bucket,
            CopySource={
              "Bucket": name_bucket,
              "Key": obj["Key"]
            },
            Key=new_directory + obj["Key"].split("/")[-1]
          )
          # delete the file
          self.s3.delete_object(
            Bucket=name_bucket,
            Key=obj["Key"]
          )
        # delete the directory
        self.s3.delete_object(
          Bucket=name_bucket,
          Key=origin_path_bucket
        )
        return {
        "status": "success",
        "message": f"Carpeta {self.name} renombrado exitosamente en el bucket"
        }
      else:
        return {
          "status": "error",
          "message": f"No se puedo renombrar la carpeta {self.name} porque no existe la carpeta {self.path}"
        }

    object_list_origin = self.s3.list_objects(Bucket=name_bucket, Prefix=origin_path_bucket)
    # print(object_list_origin)
    if "Contents" in object_list_origin:
      # evaluate if the path is a directory
      object_list_destini = self.s3.list_objects(Bucket=name_bucket, Prefix=destini_path_bucket)
      if "Contents" in object_list_destini:
        return {
          "status": "error",
          "message": f"El archivo {self.name} ya existe en el bucket"
        }
      else:
        # evaluate if the origin path is a file or a folder
        if origin_path_bucket.endswith(".txt"):
          self.s3.copy_object(
            Bucket=name_bucket,
            CopySource={
              "Bucket": name_bucket,
              "Key": origin_path_bucket
            },
            Key=destini_path_bucket
          )
          # delete the file
          self.s3.delete_object(
            Bucket=name_bucket,
            Key=origin_path_bucket
          )
          return {
          "status": "success",
          "message": f"Archivo {self.name} renombrado exitosamente en el bucket"
          }
    else:
      return {
        "status": "error",
        "message": f"No se puedo renombrar el archivo {self.path}"
      }
      