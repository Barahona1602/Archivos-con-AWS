# Import packages
from fastapi import APIRouter
from ..model.modelOBR import BackupRequest, OpenRequest, RecoveryRequest
# Local import
from ..manageFiles.classes.open import Open
from ..manageFiles.classes.backup import Backup
from ..manageFiles.classes.recovery import Recovery
from ..config import Settings
# router
router = APIRouter(
  prefix="",
  tags=["Command - from another EC2"],
  responses={404: {"description": "Not found"}},
)

# endpoint to ooen a file
@router.post("/open") 
async def open(openRequest: OpenRequest):
  # create object
  open = Open(openRequest.type_,  None, None, openRequest.name)
  # evaluate the type 
  if openRequest.type_ == "server":
    response = open.local()
    if response["status"] == "success":
      return {
        "content": response["message"],
      }
    else:
      return {
        "content": None
      }
  elif openRequest.type_ == "bucket":
    response = open.bucket()
    if response["status"] == "success":
      return {
        "content": response["message"],
      }
    else:
      return {
        "content": None
      }
  else:
    return {
      "content": None
    }


# endpoint to backup a file
@router.post("/backup")
async def backup(backupRequest: BackupRequest):
  # create object
  backup = Backup(backupRequest.type_,  None, None, None, backupRequest.name)
  if backupRequest.type_ == "server":
    response = backup.local(backupRequest.structure)
    if response["status"] == "success":
      return {
        "status": True
      }
    else:
      return {
        "status": False
      }
  elif backupRequest.type_ == "bucket":
    response = backup.bucket(backupRequest.structure)
    if response["status"] == "success":
      return {
        "status": True
      }
    else:
      return {
        "status": False
      }
  else:
    return {
      "status": False
    }

# endpoint to recovery a file
@router.post("/recovery")
async def recovery(recoveryRequest: RecoveryRequest):
  # create object
  recovery = Recovery(recoveryRequest.type_,  None, None, None, recoveryRequest.name)
  if recoveryRequest.type_ == "server":
    return recovery.local(True)
  elif recoveryRequest.type_ == "bucket":
    return recovery.bucket(True)
  else:
    return {
      "status": False
    }
