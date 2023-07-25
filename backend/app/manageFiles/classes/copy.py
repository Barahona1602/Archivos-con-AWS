import os
import shutil
from ..setCredentials import setCredentials



class Copy():
    
  def __init__(self, from_, to_, type_to, type_from) -> None:
    self.from_ = from_
    self.to_ = to_
    self.type_to = type_to
    self.type_from = type_from
    self.s3 = setCredentials()
  

  def local(self):
    # declare variables
    from_path = self.from_.replace("'","").lstrip("/").rstrip("/")
    to_path = self.to_.replace("'","").lstrip("/").rstrip("/")
    # root file
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    # origin and destiny path
    origin_path = os.path.join(root_dir, "Archivos", from_path)
    destiny_path = os.path.join(root_dir, "Archivos", to_path)

    # evaluate if the type_to is local
    if self.type_to == "server":
      # evaluate if the origin path exists
      if os.path.exists(origin_path):

        if os.path.isdir(origin_path):

          if os.path.isdir(destiny_path) and os.path.basename(origin_path) == os.path.basename(destiny_path):
            return {
              "status": "error",
              "Message":f"Ya existe una carpeta con el nombre '{os.path.basename(origin_path)}' en la ubicación de destino del servidor."
            }
          else:
            self.copyDirectoryLocal(origin_path, destiny_path)
            return {
              "status": "success",
              "message": f"Carpeta {os.path.basename(origin_path)} copiada exitosamente en el servidor"
            }
        elif os.path.isfile(origin_path):
          file_name = os.path.basename(origin_path)

          if os.path.exists(os.path.join(destiny_path,file_name)):
            return {
              "status": "error",
              "message":f"Ya existe un archivo con el nombre '{file_name}' en la ubicación de destino del servidor."
            }
          else:
            self.copyFileLocal(origin_path, os.path.join(destiny_path,file_name))
            return {
              "status": "success",
              "message": f"Archivo {file_name} copiado exitosamente en el servidor"
            }
      else:
        return {
          "status": "error",
          "message": f"El archivo o carpeta {os.path.basename(origin_path)} no existe en el servidor"
        }

    # evaluate if the type_to is bucket
    else:
      origin_path_bucket = "Archivos" + self.from_
      destiny_path_bucket = "Archivos" + self.to_
      name_bucket = "mia-proyecto2"

      # evaluate if the origin path exists
      if os.path.exists(origin_path):
        # evaluate if the origin path is a directory
        if os.path.isdir(origin_path):
          # evaluate if the destiny path bucket exist
          object_list = self.s3.list_objects(Bucket=name_bucket, Prefix=destiny_path_bucket) 
          if "Contents" in object_list:
            # read the files in the origin local path
            for file in os.listdir(origin_path):
              # evaluate if the name of the file  exist in the bucket
              if file in [obj["Key"].split("/")[-1] for obj in object_list["Contents"]]:
                return {
                  "status": "error",
                  "message":f"Ya existe un archivo con el nombre '{file}' en la ubicación de destino del bucket."
                }
              # if the directory not exist in the bucket, upload it
              if file in [obj["Key"].split("/")[-2] for obj in object_list["Contents"]]:
                return {
                  "status": "error",
                  "message":f"Ya existe una carpeta con el nombre '{file}' en la ubicación de destino del bucket."
                }
              # if file is a directory iterate the files inside
              if os.path.isdir(os.path.join(origin_path,file)):
                for file_ in os.listdir(os.path.join(origin_path,file)):
                  self.copyFileBucket(file_, destiny_path_bucket + file + "/", open(os.path.join(origin_path,file,file_), 'rb'), name_bucket)

              elif os.path.isfile(os.path.join(origin_path,file)):
                self.copyFileBucket(file, destiny_path_bucket, open(os.path.join(origin_path,file), 'rb'), name_bucket)
            return {
              "status": "success",
              "message": f"Carpeta {os.path.basename(origin_path)} copiada exitosamente en el bucket"
            }
          else:
            return {
              "status": "error",
              "message": f"La carpeta {destiny_path_bucket} no existe en el bucket"
            }
        # evaluate if the origin path is a file
        elif os.path.isfile(origin_path):
          # evaluate if the destiny path bucket exist
          object_list = self.s3.list_objects(Bucket=name_bucket, Prefix=destiny_path_bucket)
          if "Contents" in object_list:
            # evaluate if the name of the file  exist in the bucket
            if os.path.basename(origin_path) in [obj["Key"].split("/")[-1] for obj in object_list["Contents"]]:
              return {
                "status": "error",
                "message":f"Ya existe un archivo con el nombre '{os.path.basename(origin_path)}' en la ubicación de destino del bucket."
              }
            else:
              self.copyFileBucket(os.path.basename(origin_path), destiny_path_bucket, open(origin_path, 'rb'), name_bucket)
              return {
                "status": "success",
                "message": f"Archivo {os.path.basename(origin_path)} copiado exitosamente en el bucket"
              }
          else:
            return {
              "status": "error",
              "message": f"La carpeta {destiny_path_bucket} no existe en el bucket"
            }
      else:
        return {
          "status": "error",
          "message": f"El archivo o carpeta {os.path.basename(origin_path)} no existe en el bucket"
        }
      
  def bucket(self):
    # declare variables
    from_path = self.from_.replace("'","").lstrip("/").rstrip("/")
    to_path = self.to_.replace("'","").lstrip("/").rstrip("/")
    # root file
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    # origin and destiny path
    origin_path = os.path.join(root_dir, "Archivos", from_path)
    destiny_path = os.path.join(root_dir, "Archivos", to_path)


    if self.type_to == "bucket":
      print("de bucket a bucket")
      origin_path_bucket = "Archivos" + self.from_
      destiny_path_bucket = "Archivos" + self.to_
      name_bucket = "mia-proyecto2"

      # evaluate if the origin path exists in the bucket 
      object_list_origin = self.s3.list_objects(Bucket=name_bucket, Prefix=origin_path_bucket)
      if "Contents" in object_list_origin:
        # evaluate if the destiny path exists in the bucket
        object_list_destiny = self.s3.list_objects(Bucket=name_bucket, Prefix=destiny_path_bucket)
        if "Contents" in object_list_destiny:
          print([obj["Key"].split("/")[-1] for obj in object_list_origin["Contents"]])
          # verify if the origin path is a directory or a file
          if len([obj["Key"].split("/")[-1] for obj in object_list_origin["Contents"]]) > 1:
            print("es directorio")
            # evaluate if the destiny already exist the files to copy 
            if len([obj["Key"].split("/")[-1] for obj in object_list_destiny["Contents"]]) > 1:
              return {
                "status": "error",
                "message":f"Ya existe un archivo en la ubicación de destino del bucket {destiny_path_bucket}."
              }
            else:
              # copy the files from the origin path to the destiny path
              for file in object_list_origin["Contents"]:
                self.copyDirectoryCloud(file["Key"], destiny_path_bucket)
              return {
                "status": "success",
                "message": f"Carpeta {origin_path_bucket} copiada exitosamente en el bucket"
              }
          else:
            print("es archivo")
            # evaluate if the destiny already exist the files to copy
            if len([obj["Key"].split("/")[-1] for obj in object_list_destiny["Contents"]]) > 1:
              return {
                "status": "error",
                "message":f"Ya existe un archivo en la ubicación de destino {destiny_path_bucket}."
              }
            else:
              # copy the files from the origin path to the destiny path
              for file in object_list_origin["Contents"]:
                self.copyDirectoryCloud(file["Key"], destiny_path_bucket)
              return {
                "status": "success",
                "message": f"Archivo {origin_path_bucket} copiado exitosamente en el bucket"
              }
        else:
          return {
            "status": "error",
            "message": f"La carpeta {destiny_path_bucket} no existe en el bucket"
          }
      else:
        return {
          "status": "error",
          "message": f"La carpeta {origin_path_bucket} no existe en el bucket"
        }
    # evaluate if the type_to is local
    else:
      origin_path_bucket = "Archivos" + self.from_
      destiny_path_bucket = "Archivos" + self.to_
      name_bucket = "mia-proyecto2"
      print("de bucket a local")
      # evaluate if the origin path exists in the bucket 
      object_list_origin = self.s3.list_objects(Bucket=name_bucket, Prefix=origin_path_bucket)
      if "Contents" in object_list_origin:
        # evaluate if the destiny path exists in the local 
        if os.path.exists(destiny_path):
          # verify if the origin path is a directory or a file
          if len([obj["Key"].split("/")[-1] for obj in object_list_origin["Contents"]]) > 1:
            print("es directorio")
            print(os.listdir(destiny_path) , [obj["Key"].split("/")[-1] for obj in object_list_origin["Contents"]])
            # evaluate if the some file in the origin path already exist in the destiny path
            if len([obj["Key"].split("/")[-1] for obj in object_list_origin["Contents"]]) > 1 and len([obj for obj in os.listdir(destiny_path) if obj in [obj["Key"].split("/")[-1] for obj in object_list_origin["Contents"]]]) > 0:
              return {
                "status": "error",
                "message":f"Ya existe un archivo en la ubicación de destino {os.path.basename(destiny_path)}."
              }
            # copy the files from the origin path to the destiny path
            for file in object_list_origin["Contents"]:
              self.copyDirectoryCloudToLocal(file["Key"], destiny_path)
            return {
            "status": "success",
            "message": f"Carpeta {origin_path_bucket} copiada exitosamente en el server"
            }
          # file
          else:
            print("es archivo")
            # evaluate if the destiny already exist the files to copy
            if os.path.exists(os.path.join(destiny_path, os.path.basename(origin_path))):
              return {
                "status": "error",
                "message":f"Ya existe un archivo en la ubicación de destino {os.path.basename(destiny_path)}."
              }
            else:
              # copy the files from the origin path to the destiny path
              for file in object_list_origin["Contents"]:
                self.copyDirectoryCloudToLocal(file["Key"], destiny_path)
              return {
                "status": "success",
                "message": f"Archivo {origin_path_bucket} copiado exitosamente en el server"
              }
        else:
          return {
            "status": "error",
            "message": f"La carpeta {destiny_path_bucket} no existe en el bucket"
          }
      else:
        return {
          "status": "error",
          "message": f"La carpeta {origin_path_bucket} no existe en el bucket"
        }


  def copyDirectoryLocal(self,from_directory, to_directory):
    os.makedirs(to_directory, exist_ok=True)
    for item in os.listdir(from_directory):
      item_path = os.path.join(from_directory, item)
      if os.path.isdir(item_path):
        self.copyDirectoryLocal(item_path, os.path.join(to_directory, item))
      elif os.path.isfile(item_path):
        self.copyFileLocal(item_path, to_directory)

  def copyFileBucket(self, name, destination, body, bucket_name):
    try:
      self.s3.put_object(Bucket=bucket_name, Key=f"{destination}{name}", Body=body)
    except Exception as e:
      return {
        "status": "error",
        "message": f"Error al crear archivo {self.name}"
      }
    
  def copyFileLocal(self, src, dst):
    shutil.copy(src, dst)
  
  def copyDirectoryCloud(self, from_directory, to_directory):
    # print(from_directory, to_directory)
    copy_source = {
        'Bucket': 'mia-proyecto2',
        'Key': from_directory
    }
    
    if f"Archivos/{self.from_}".endswith("/"):
      print("entra?")
      substring = "Archivos/" + self.from_
      destination_key = to_directory + from_directory[len(substring) - 1:]
      print(copy_source, destination_key, "es directorio")
      self.s3.copy_object(Bucket='mia-proyecto2', CopySource=copy_source, Key=destination_key)
    else:
      destination_key = to_directory + from_directory.split('/')[-1]
      print(copy_source, destination_key, "es archivo")
      self.s3.copy_object(Bucket='mia-proyecto2', CopySource=copy_source, Key=destination_key)

  def copyDirectoryCloudToLocal(self, from_directory, to_directory):
    # download the files from the bucket
    print(from_directory, to_directory)
    print("mia-proyecto2", from_directory, to_directory )
    self.s3.download_file("mia-proyecto2", from_directory, to_directory + "/" + from_directory.split("/")[-1] )