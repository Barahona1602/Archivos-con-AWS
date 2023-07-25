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

class Open():
  def __init__(self, type, ip, port, name) -> None:
    self.type = type
    self.ip = ip
    self.port = port
    self.name = name
    self.s3 = setCredentials()
    self.settings = set_config()
  

  def local(self):
    path = self.name.replace("'", '')
    path = path.lstrip("/")

    # Get the absolute path of the project directory
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    file_ = os.path.join(root_dir, "Archivos", path)
    if os.path.exists(file_):
      with open(file_, "r") as f:
        body = f.read()
      return {
        "status": "success",
        "message": body,
      }
    else:
      return {
        "status": "error",
        "message": f"El archivo {self.name} no existe en el server"
      }
    
  def bucket(self):
    bucket_name = "mia-proyecto2"
    object_key = 'Archivos' + self.name
    try:
      # evaluate if the file exists
      list_objects = self.s3.list_objects(Bucket=bucket_name, Prefix=object_key)
      if 'Contents' in list_objects:
        # donwload the file
        response = self.s3.get_object(Bucket=bucket_name, Key=object_key)
        body = response['Body'].read().decode('utf-8')
        return {
          "status": "success",
          "message": body,
        }
      return {
        "status": "error",
        "message": f"El archivo {self.name} no existe en el bucket"
      }
    except:
      return {
        "status": "error",
        "message": f"El archivo {self.name} no existe en el bucket"
      }

  def api_ip(self):
    payload = {
      "name": self.name,
      "type": self.type,
    }
    print(payload)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f'http://{self.ip}:{self.port}/open', data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
      # if content is null, return error
      if response.json()["content"] == None or response.json()["content"] == "null":
        print(response.json(), " resultado")
        return {
          "status": "error",
          "message": f"El archivo {self.name} no existe en el servidor con la ip: {self.ip}" 
        }
      return {
      "status": "success",
      "message": response.json()["content"]
      }
    else:
      return {
        "status": "error",
        "message": f"Error al crear el backup {self.name} en el servidor con la ip: {self.ip}."
      }
  