from typing import Dict
from pydantic import BaseModel


class OpenRequest(BaseModel):
  name: str
  type_: str

  class Config:
      fields = {
          'type_': 'type'
      }
class BackupRequest(BaseModel):
  name: str
  type_: str
  structure: Dict

  class Config:
      fields = {
          'type_': 'type'
      }

class RecoveryRequest(BaseModel):
    name: str
    type_: str

    class Config:
        fields = {
            'type_': 'type'
        }