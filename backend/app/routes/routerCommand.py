# Import packages
from fastapi import APIRouter
from ..model.modelCommand import modelCommand
# Local import
from ..lib.proccess.tokens import extract_commands
from ..lib.proccess.commands import execute_commands
from ..config import Settings
# router
router = APIRouter(
  prefix="/command",
  tags=["Command - Console"],
  responses={404: {"description": "Not found"}},
)

def set_settings():
  return Settings()

# endpoint to recieved a command as a string from a body
@router.post("/console-command")
async def consoleCommand(command: modelCommand):
  if not command:
    return {"status": "error", "message": "No command"}
  else:
    # return {"status": "success", "message": "Command recieved"}
    # send function to process command
    commands = extract_commands(command.command)
    response = execute_commands(commands)
    return response
