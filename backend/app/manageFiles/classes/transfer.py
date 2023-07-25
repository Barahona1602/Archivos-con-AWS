import os
import shutil
from ..setCredentials import setCredentials



class Transfer():
    
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
      # evaluate if the destiny path exists
      if not os.path.exists(destiny_path):
        return {
          "status": "error",
          "message": f"El archivo o carpeta '{os.path.basename(destiny_path)}' no existe"
        }
      # evaluate if the origin path exists
      if os.path.exists(origin_path):

        if os.path.isdir(origin_path):
          self.transferDirectoryLocal(origin_path, destiny_path)
          return {
            "status": "success",
            "message": f"Carpeta {os.path.basename(origin_path)} transferida exitosamente"
          }
        elif os.path.isfile(origin_path):
          self.transferFile(origin_path, destiny_path)
          return {
            "status": "success",
            "message": f"Archivo {os.path.basename(origin_path)} transferido exitosamente"
          }
      else:
        return {
          "status": "error",
          "message": f"El archivo o carpeta {os.path.basename(origin_path)} no existe"
        }

    # evaluate if the type_to is bucket, move from local to bucket
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
              # change to rename te file
                self.transferLocalToBucket(
                  file,
                  destiny_path_bucket,
                  open(os.path.join(origin_path,file), 'rb'),
                  name_bucket,
                  origin_path+"/",
                  True
                )

              # if the directory not exist in the bucket, upload it
              if file in [obj["Key"].split("/")[-2] for obj in object_list["Contents"]]:
              # change to rename te file
                # self.transferLocalToBucket(
                #   file,
                #   destiny_path_bucket,
                #   open(os.path.join(origin_path,file), 'rb'),
                #   name_bucket,
                #   origin_path,
                #   True
                # )
                pass
              
              # if file is a directory iterate the files inside
              if os.path.isdir(os.path.join(origin_path,file)):
                for file_ in os.listdir(os.path.join(origin_path,file)):
                  self.transferLocalToBucket(
                    file_, 
                    destiny_path_bucket + file + "/", 
                    open(os.path.join(origin_path,file,file_), 'rb'), 
                    name_bucket,
                    origin_path+"/",
                    False
                  )

              elif os.path.isfile(os.path.join(origin_path,file)):
                self.transferLocalToBucket(
                  file, 
                  destiny_path_bucket, 
                  open(os.path.join(origin_path,file), 'rb'), 
                  name_bucket,
                  origin_path+"/",
                  False)

            return {
              "status": "success",
              "message": f"Carpeta {os.path.basename(origin_path)} transferida sexitosamente"
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
            #change to rename te file
              self.transferLocalToBucket(os.path.basename(origin_path), destiny_path_bucket, open(origin_path, 'rb'), name_bucket, origin_path,True)

            self.transferLocalToBucket(os.path.basename(origin_path), destiny_path_bucket, open(origin_path, 'rb'), name_bucket, origin_path,False)
            return {
              "status": "success",
              "message": f"Archivo {os.path.basename(origin_path)} transferido exitosamente"
            }
          else:
            return {
              "status": "error",
              "message": f"La carpeta {destiny_path_bucket} no existe en el bucket"
            }
      else:
        return {
          "status": "error",
          "message": f"El archivo o carpeta {os.path.basename(origin_path)} no existe"
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
            # evaluate if the destiny already exist the files to transfer 
            if origin_path_bucket.split("/")[-1] in [obj["Key"].split("/")[-1] for obj in object_list_destiny["Contents"]]:
              # rename the ile if already exist
              self.transferDirectoryCloud(
                origin_path_bucket,
                destiny_path_bucket,
                True
              )
            # transfer the files from the origin path to the destiny path
            for file in object_list_origin["Contents"]:
              self.transferDirectoryCloud(file["Key"], destiny_path_bucket)
            return {
              "status": "success",
              "message": f"Carpeta {origin_path_bucket} transferida exitosamente"
            }
          else:
            print("es archivo")
            # evaluate if the destiny already exist the files to transfer
            if origin_path_bucket.split("/")[-1] in [obj["Key"].split("/")[-1] for obj in object_list_destiny["Contents"]]:
              # rename the ile if already exist
              self.transferDirectoryCloud(
                origin_path_bucket,
                destiny_path_bucket,
                True
              )
            # transfer the files from the origin path to the destiny path
            for file in object_list_origin["Contents"]:
              self.transferDirectoryCloud(file["Key"], destiny_path_bucket, False)
            return {
              "status": "success",
              "message": f"Archivo {origin_path_bucket} transferido exitosamente"
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
    # evaluate if the type_to is local, move from bucket to local
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
              # rename the ile if already exist
              self.transferDirectoryCloudToLocal(
                origin_path_bucket,
                destiny_path,
                True
              )
            # transfer the files from the origin path to the destiny path
            for file in object_list_origin["Contents"]:
              self.transferDirectoryCloudToLocal(file["Key"], destiny_path,False)
            return {
            "status": "success",
            "message": f"Carpeta {origin_path_bucket} transferida exitosamente"
            }
          # file
          else:
            print("es archivo")
            # evaluate if the destiny already exist the files to transfer
            if os.path.exists(os.path.join(destiny_path, os.path.basename(origin_path))):
              # rename the ile if already exist
              self.transferDirectoryCloudToLocal(
                origin_path_bucket,
                destiny_path,
                True
              )
            else:
              # transfer the files from the origin path to the destiny path
              for file in object_list_origin["Contents"]:
                self.transferDirectoryCloudToLocal(file["Key"], destiny_path, False)

            return {
              "status": "success",
              "message": f"Archivo {origin_path_bucket} transferido exitosamente"
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


  def transferDirectoryLocal(self,from_directory, to_directory):
    if not os.path.exists(to_directory):
      os.makedirs(to_directory)
    folder_name = os.path.basename(from_directory)

    for item in os.listdir(from_directory):
      item_path = os.path.join(from_directory, item)
      self.transferFile(item_path, os.path.join(to_directory, item))

  def transferFile(self,from_path, to_path):
    to_folder = os.path.dirname(to_path)
    if not os.path.exists(to_folder):
        os.makedirs(to_folder)

    file_name = os.path.basename(from_path)
    base_name, extension = os.path.splitext(file_name)

    dest_path = to_path
    if os.path.exists(dest_path):
        counter = 1
        while os.path.exists(dest_path):
            new_file_name = f"{base_name}({counter}){extension}"
            dest_path = os.path.join(to_folder, new_file_name)
            counter += 1

    if os.path.isdir(to_path):
        dest_path = os.path.join(to_path, file_name)

    shutil.move(from_path, dest_path)
    # return f"El archivo '{file_name}' se ha movido exitosamente a '{os.path.basename(dest_path)}'."



  def transferLocalToBucket(self, name, destination, body, bucket_name, origin_path, repeated = False):

    try:
      if repeated:
        # add (1) to the name before .txt
        name = name.split(".")[0] + "(1)." + name.split(".")[1]
        self.s3.put_object(Bucket=bucket_name, Key=f"{destination}{name}", Body=body)
      else:
        self.s3.put_object(Bucket=bucket_name, Key=f"{destination}{name}", Body=body)
      
      # os.remove(os.path.join(origin_path))
      if origin_path.endswith("/"):
        shutil.rmtree(origin_path.rstrip("/"))
        # remove directory
        shutil.rmdir(origin_path.rstrip("/"))
      else:
        os.remove(origin_path)
      # remove from local
    except Exception as e:
      print( {
        "status": "error",
        "message": f"Error al crear archivo {name}"
      })
    
  
  def transferDirectoryCloud(self, from_directory, to_directory, repeated=False):
    transfer_source = {
        'Bucket': 'mia-proyecto2',
        'Key': from_directory
    }
    
    if f"Archivos/{self.from_}".endswith("/"):
        print("entra?")
        substring = "Archivos/" + self.from_
        destination_key = ""
        if repeated:
            destination_key = to_directory + from_directory[len(substring) - 1:] 
        else:
            destination_key = to_directory + from_directory[len(substring) - 1:] 
        print(transfer_source, destination_key, "es directorio")
        self.s3.copy_object(Bucket='mia-proyecto2', CopySource=f"{transfer_source['Bucket']}/{transfer_source['Key']}", Key=destination_key)
        # delete from origin
        self.s3.delete_object(Bucket='mia-proyecto2', Key=from_directory)
    else:
        destination_key = ""
        if repeated:
            destination_key = to_directory + from_directory.split('/')[-1]
            destination_key = destination_key.split(".")[0] + "(1)." + destination_key.split(".")[1]
        else:
            destination_key = to_directory + from_directory.split('/')[-1]

        print(transfer_source, destination_key, "es archivo")
        self.s3.copy_object(Bucket='mia-proyecto2', CopySource=f"{transfer_source['Bucket']}/{transfer_source['Key']}", Key=destination_key)
        # delete from origin
        self.s3.delete_object(Bucket='mia-proyecto2', Key=from_directory)


  def transferDirectoryCloudToLocal(self, from_directory, to_directory, repeated=False):
    # download the files from the bucket
    # print(from_directory, to_directory)
    des = ""
    if repeated:
      des = to_directory + "/" + from_directory.split("/")[-1]
      des = des.split(".")[0] + "(1)." + des.split(".")[1]
       
    else:
      des = to_directory + "/" + from_directory.split("/")[-1]
    print(des ," ?") 
    self.s3.download_file("mia-proyecto2", from_directory, des )
    # delete from bucket
    self.s3.delete_object(Bucket='mia-proyecto2', Key=from_directory)
