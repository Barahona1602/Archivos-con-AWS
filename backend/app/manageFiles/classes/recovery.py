import os
import shutil
from ..setCredentials import setCredentials
import json
from ... import config
import requests
# if the path does not exist, return error
# if the name comes but the name file does not exist, return error
# if the name does not come, delete the folder

def set_config():
   return config.Settings()

class Recovery():
  def __init__(self, type_to, type_from, ip, port, name) -> None:
    self.type_to = type_to
    self.type_from = type_from
    self.ip = ip
    self.port = port
    self.name = name
    self.s3 = setCredentials()
    self.settings = set_config()

  def local(self, return_data=False):
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))) + "/" + self.name
    if return_data:
      # evaulate if the path exists
      if os.path.exists(base_path):
        # generate the json from the bucket directoy server
        struc_json = self.generate_directory_structure_server(base_path)
        return {
          "type": self.type_to,
          "structure": struc_json
        }
      else:
        return {
          "structure":None
        }
    else:
      if self.type_to == "server":
        return {
          "status": "error",
          "message": "No se puede hacer un recovery en el mismo server"
        }
      # evaulate if the path exists
      if os.path.exists(base_path):
        # delete the "Archivos/" directory in the bucket
        self.s3.delete_object(Bucket="mia-proyecto2", Key="Archivos/")
        # generate the json from the bucket directoy server
        struc_json = self.generate_directory_structure_server(base_path)
        # generate the files on the bucket
        self.generate_recovery_on_bucket(struc_json, "mia-proyecto2", "Archivos/")
        return {
          "status": "success",
          "message": f"El recovery del backup '{self.name}' se realizo con exito en el bucket."
        }
      else:
        return {
          "status": "error",
          "message": f"El backup '{self.name}' no existe en el servidor."
        }

  

  def bucket(self, return_data=False):
    bucket_name = "mia-proyecto2"
    object_key = self.name +"/"
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))) + "/Archivos" 
    if return_data:
      # evaulate if the path exists in the bucket
      list_objects = self.s3.list_objects(Bucket=bucket_name, Prefix=object_key)
      if 'Contents' in list_objects:
        # generate the json from the bucket directoy server
        struc_json = self.generate_directory_structure_bucket(bucket_name)
        return {
          "type": self.type_to,
          "structure": struc_json
        }
      else:
        return {
          "structure":None
        }
    else:
      if self.type_to == "bucket":
        return {
          "status": "error",
          "message": "No se puede hacer un recovery en el mismo bucket"
        }
      # evaulate if the path exists in the bucket
      list_objects = self.s3.list_objects(Bucket=bucket_name, Prefix=object_key)
      if 'Contents' in list_objects:
        # delete the "Archivos/" directory in the server
        shutil.rmtree(base_path)
        # generate the json from the bucket directoy server
        struc_json = self.generate_directory_structure_bucket(bucket_name)
        # return generate_directory_structure_bucket
        # generate the files on the server
        self.generate_recovery_on_server(struc_json, base_path)
        return {
          "status": "success",
          "message": f"El recovery del backup '{self.name}' se realizo con exito en el bucket."
        }
      else:
        return {
          "status": "error",
          "message": f"El backup '{self.name} ' no existe en el bucket."
        }
    


  def local_api(self):
    if self.type_to == "bucket":
      return {
        "status": "error",
        "message": "No se puede hacer un recovery en el mismo bucket"
      }

    # make request to the api
    payload = {
      'name': self.name,
      'type': self.type_from
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f'http://{self.ip}:{self.port}/recovery', data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
      base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))) + "/Archivos" 
      # delete the "Archivos/" directory in the server
      shutil.rmtree(base_path)
      # get the structure from the response
      struc_json = response.json().get("structure")
      if struc_json == None or struc_json == "null":
        return {
          "status": "error",
          "message": f"El backup '{self.name}' no existe en el servidor con la ip: {self.ip}."
        }
      # generate the files on the server
      self.generate_recovery_on_server(struc_json, base_path)
      return {
        "status": "success",
        "message": f"Recovery {self.name} creado existosamente en el servidor con la ip: {self.ip}."
      }
    else:
      return {
        "status": "error",
        "message": f"Error al crear el recovery {self.name} en el servidor con la ip: {self.ip}."
      }
  
  def bucket_api(self):
    if self.type_to == "server":
      return {
        "status": "error",
        "message": "No se puede hacer un recovery en el mismo server"
      }
    # make request to the api
    payload = {
      'name': self.name,
      'type': self.type_from
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f'http://{self.ip}:{self.port}/recovery', data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
      # delete the "Archivos/" directory in the bucket
      self.s3.delete_object(Bucket="mia-proyecto2", Key="Archivos/")
      # generate the json from the bucket directoy server
      struc_json = response.json().get("structure")
      if struc_json == None or struc_json == "null":
        return {
          "status": "error",
          "message": f"El backup '{self.name}' no existe en el servidor con la ip: {self.ip}."
        }
      # generate the files on the bucket
      self.generate_recovery_on_bucket(struc_json, "mia-proyecto2", "Archivos/")
      return {
        "status": "success",
        "message": f"Recovery {self.name} creado existosamente en el bucket con la ip: {self.ip}."
      }
    else:
      return {
        "status": "error",
        "message": f"Error al crear el recovery {self.name} en el bucket con la ip: {self.ip}."
      }

  def generate_directory_structure_server(self, base_path):
    json_data = {}
    
    for item in os.listdir(base_path):
      item_path = os.path.join(base_path, item)
      
      if os.path.isfile(item_path):
          # File
          file_name, file_extension = os.path.splitext(item)
          file_contents = ""
          
          with open(item_path, "r") as file:
              file_contents = file.read()
          
          if "_files" not in json_data:
              json_data["_files"] = []
          
          json_data["_files"].append({
              "file_name": file_name + file_extension,
              "file_contents": file_contents
          })
      
      elif os.path.isdir(item_path):
          # Directory
          sub_json = self.generate_directory_structure_server(item_path)
          json_data[item] = sub_json
    
    return json_data

  def generate_recovery_on_bucket(self,directory_structure, bucket_name="mia-proyecto2", prefix=''):
    s3 = self.s3
    
    for directory_name, directory_content in directory_structure.items():
        if directory_name == '_files':
            # Handle files in the current directory
            for file_info in directory_content:
                file_name = file_info['file_name']
                file_contents = file_info['file_contents']
                file_key = f"{prefix}{file_name}"
                s3.put_object(Body=file_contents, Bucket=bucket_name, Key=file_key)
        else:
            # Handle subdirectories
            subdirectory_prefix = f"{prefix}{directory_name}/"
            s3.put_object(Body='', Bucket=bucket_name, Key=subdirectory_prefix)  # Create empty directory object
            if '_files' in directory_content:
                # Handle files in the subdirectory
                for file_info in directory_content['_files']:
                    file_name = file_info['file_name']
                    file_contents = file_info['file_contents']
                    file_key = f"{subdirectory_prefix}{file_name}"
                    s3.put_object(Body=file_contents, Bucket=bucket_name, Key=file_key)
            # Recursively build subdirectories
            self.generate_recovery_on_bucket(directory_content, bucket_name, subdirectory_prefix)

  #   return backup_data
  def get_files_recursive(self, bucket, prefix):
    remove_string = self.name + "/"
    backup_data = {}

    s3 = self.s3
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    for obj in response.get('Contents', []):
        # Remove the string 'Archivos/' from the file path
        obj['Key'] = obj['Key'].replace(remove_string, '')
        # create a list for each key
        directory_path_list = obj['Key'].split('/')
        print(directory_path_list)
        # iterate
        for dir in directory_path_list:
            if dir.endswith(".txt") or dir == '':
                directory_path_list.remove(dir)
        
        # current dict
        curr_dict = backup_data
        for subdir in directory_path_list:
            if subdir not in curr_dict:
                curr_dict[subdir] = {}
            curr_dict = curr_dict[subdir]

        # create the dict
        curr_dict["_files"] = curr_dict.get("_files", [])

        # get the files within the directory
        sub_response = s3.list_objects(Bucket=bucket, Prefix= self.name +"/"+  obj['Key'] )
        # return sub_response
        for sub_obj in sub_response.get('Contents', []):
            if sub_obj['Key'].endswith(".txt"):
                file_name = sub_obj['Key'].split('/')[-1]
                file_contents = s3.get_object(Bucket=bucket, Key=sub_obj['Key'])['Body'].read().decode('utf-8')

                existing_file = next((f for f in curr_dict["_files"] if f["file_name"] == file_name), None)
                if existing_file:
                    existing_file["file_contents"] = file_contents
                else:
                    curr_dict["_files"].append({"file_name": file_name, "file_contents": file_contents})

    return backup_data
  
  def generate_directory_structure_bucket(self, bucket):
    directory_structure = {}

    s3 = self.s3
    response = s3.list_objects_v2(Bucket=bucket, Delimiter=f"{self.name}/")

    for obj in response.get('CommonPrefixes', []):
        directory_name = obj['Prefix'].strip('/').split('/')[-1]
        files = self.get_files_recursive(bucket, obj['Prefix'])
        if files:
            directory_structure = files

    return directory_structure

  def generate_recovery_on_server(self,directory_structure, base_directory=''):
    for directory_name, directory_content in directory_structure.items():
      if directory_name == '_files':
        # Handle files in the base directory
        for file_info in directory_content:
          file_name = file_info['file_name']
          file_contents = file_info['file_contents']
          file_path = os.path.join(base_directory, file_name)
          with open(file_path, 'w') as file:
            file.write(file_contents)
      else:
        # Handle subdirectories
        sub_directory_path = os.path.join(base_directory, directory_name)
        os.makedirs(sub_directory_path, exist_ok=True)
        if '_files' in directory_content:
          # Handle files in the subdirectory
          for file_info in directory_content['_files']:
            file_name = file_info['file_name']
            file_contents = file_info['file_contents']
            file_path = os.path.join(sub_directory_path, file_name)
            with open(file_path, 'w') as file:
              file.write(file_contents)
        # Recursively process subdirectories
        self.generate_recovery_on_server(directory_content, sub_directory_path)