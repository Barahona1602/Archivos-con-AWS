# local imports
from ..scanner.createC import scan_command_line_create
from ..scanner.deleteC import scan_command_line_delete
from ..scanner.copyC import scan_command_line_copy
from ..scanner.transferC import scan_command_line_transfer
from ..scanner.renameC import scan_command_line_rename
from ..scanner.modifyC import scan_command_line_modify
from ..scanner.backupC import scan_command_line_backup
from ..scanner.recoveryC import scan_command_line_recovery
from ..scanner.delete_allC import scan_command_line_delete_all
from ..scanner.openC import scan_command_line_open
# classes
from ...manageFiles.classes.create import Create
from ...manageFiles.classes.delete import Delete
from ...manageFiles.classes.copy import Copy
from ...manageFiles.classes.transfer import Transfer
from ...manageFiles.classes.rename import Rename
from ...manageFiles.classes.modify import Modify
from ...manageFiles.classes.backup import Backup
from ...manageFiles.classes.recovery import Recovery
from ...manageFiles.classes.delete_all import Delete_all
from ...manageFiles.classes.open import Open
# recieve an array of commands and execute them

# 1. extract values from the command string
# 2. valdiate the values
# 3. execute the command


def execute_commands(commands):
  message_string = ""
  for command in commands:
    print(command)
    if command.get("create"):
      create, name, path, body, type = scan_command_line_create(command.get("create"))
      if create and name and path and body and type:
        print("create")
        # create instance of create class
        create_object = Create(name, body, path, type)
        # evaluate if the type is local or bucket
        if type == "server":
          # return create_object.local()
          response = create_object.local()
          message_string += response["message"] + "\n"
        elif type == "bucket":
        #  return  create_object.bucket()
          response = create_object.bucket()
          message_string += response["message"] + "\n"
      else:
        # return {"status": "error", "message": "Comando invalido en create"}
        message_string += "Comando invalido en create" + "\n"


    elif command.get("delete"):
      delete, path, name, type = scan_command_line_delete(command.get("delete"))
      if delete and path and type:
        print("delete")
        # create instance of delete class
        delete_object = Delete(path, name, type)
        # evaluate if the type is local or bucket
        if type == "server":
          # return delete_object.local()
          response = delete_object.local()
          message_string += response["message"] + "\n"
        elif type == "bucket":
          # return delete_object.bucket()
          response = delete_object.bucket()
          message_string += response["message"] + "\n"
        
      else:
        # return {"status": "error", "message": "Comando invalido en delete"}
        message_string += "Comando invalido en delete" + "\n"


    elif command.get("copy"):
      copy, from_, to_, type_to, type_from = scan_command_line_copy(command.get("copy"))
      if copy and from_ and to_ and type_to and type_from:
        print("copy")
        # create instance of copy class
        copy_object = Copy(from_, to_, type_to, type_from)
        # evaluate if the type is local or bucket
        if type_from == "server":
          # return copy_object.local()
          response = copy_object.local()
          message_string += response["message"] + "\n"
        elif type_from == "bucket":
          # return copy_object.bucket()
          response = copy_object.bucket()
          message_string += response["message"] + "\n"
        
      else:
        # return {"status": "error", "message": "Comando invalido en copy"}
        message_string += "Comando invalido en copy" + "\n"

    elif command.get("transfer"):
      transfer, from_, to_, type_to, type_from = scan_command_line_transfer(command.get("transfer"))
      if transfer and from_ and to_ and type_to and type_from:
        # create instance of transfer class
        transfer_object = Transfer(from_, to_, type_to, type_from)
        print("transfer")
        # evaluate if the type is local or bucket
        if type_from == "server":
          # return transfer_object.local()
          response = transfer_object.local()
          message_string += response["message"] + "\n"
        elif type_from == "bucket":
          # return transfer_object.bucket()
          response = transfer_object.bucket()
          message_string += response["message"] + "\n"
      
      else:
        # return {"status": "error", "message": "Comando invalido en transfer"}
        message_string += "Comando invalido en transfer" + "\n"

      
    elif command.get("rename"):
      rename, path, name, type = scan_command_line_rename(command.get("rename"))
      if rename and path and name and type:
        print("rename")
        # create instance of rename class
        rename_object = Rename(path, name, type)
        # evaluate if the type is local or bucket
        if type == "server":
          print("entra server")
          # return rename_object.local()
          response = rename_object.local()
          message_string += response["message"] + "\n"
        elif type == "bucket":
          print("entra server")
          # return rename_object.bucket()
          response = rename_object.bucket()
          message_string += response["message"] + "\n"
      else:
        # return {"status": "error", "message": "Comando invalido en rename"}
        message_string += "Comando invalido en rename" + "\n"
      

    elif command.get("modify"):
      modify, path, body, type = scan_command_line_modify(command.get("modify"))
      if modify and path and body and type:
        print("modify")
        # create instance of modify class
        modify_object = Modify(path, body, type)
        # evaluate if the type is local or bucket
        if type == "server":
          # return modify_object.local()
          response = modify_object.local()
          message_string += response["message"] + "\n"
        elif type == "bucket":
          # return modify_object.bucket()
          response = modify_object.bucket()
          message_string += response["message"] + "\n"
        
      else:
        # return {"status": "error", "message": "Comando invalido en modify"}
        message_string += "Comando invalido en modify" + "\n"

    elif command.get("backup"):
      backup, type_to, type_from, ip , port, name  = scan_command_line_backup(command.get("backup"))
      if backup and type_to and type_from and name:
        print("backup")
        # create instance of backup class
        backup_object = Backup(type_to, type_from, ip , port, name)
        # evaluate if the backup is only in our environment
        if ip == None and port == None:
          # evaluate if the type is local or bucket
          if type_from == "server":
            # return backup_object.bucket()
            response = backup_object.bucket()
            message_string += response["message"] + "\n"

          elif type_from == "bucket":
            # return backup_object.local()
            response = backup_object.local()
            message_string += response["message"] + "\n"

        # evaluate if the backup is in another environment (port and ip)
        elif ip != None and port != None:
          # evaluate if the type is local or bucket
          if type_from == "server":
            # return backup_object.local_api()
            response = backup_object.local_api()
            message_string += response["message"] + "\n"

          elif type_from == "bucket":
            # return backup_object.bucket_api()
            response = backup_object.bucket_api()
            message_string += response["message"] + "\n"

        else:
          # return {"status": "error", "message": "Comando invalido en backup"}
          message_string += "Comando invalido en backup" + "\n"
      else:
        # return {"status": "error", "message": "Comando invalido en backup"}
        message_string += "Comando invalido en backup" + "\n"

    elif command.get("recovery"):
      recovery, type_to, type_from, ip , port, name  = scan_command_line_recovery(command.get("recovery"))
      if recovery and type_to and type_from and name:
        print("recovery")
        # create instance of backup class
        recovery_object = Recovery(type_to, type_from, ip , port, name)
        # evaluate if the backup is only in our environment
        if ip == None and port == None:
          # evaluate if the type is local or bucket
          if type_from == "server":
            # return recovery_object.local()
            response = recovery_object.local()
            message_string += response["message"] + "\n"

          elif type_from == "bucket":
            # return recovery_object.bucket()
            response = recovery_object.bucket()
            message_string += response["message"] + "\n"

        # evaluate if the backup is in another environment (port and ip)
        elif ip != None and port != None:
          # evaluate if the type is local or bucket
          if type_from == "server":
            # return recovery_object.local_api()
            response = recovery_object.local_api()
            message_string += response["message"] + "\n"

          elif type_from == "bucket":
            # return recovery_object.bucket_api()
            response = recovery_object.bucket_api()
            message_string += response["message"] + "\n"

        else:
          # return {"status": "error", "message": "Comando invalido en backup"}
          message_string += "Comando invalido en backup" + "\n"
      else:
        # return {"status": "error", "message": "Comando invalido en recovery"}
        message_string += "Comando invalido en recovery" + "\n"

    elif command.get("delete_all"):
      delete_all, type = scan_command_line_delete_all(command.get("delete_all"))
      if delete_all and type:
        print("delete_all")
        # create instance of delete_all class
        delete_all_object = Delete_all(type)
        # evaluate if the type is local or bucket
        if type == "server":
          # return delete_all_object.local()
          response = delete_all_object.local()
          message_string += response["message"] + "\n"

        elif type == "bucket":
          # return delete_all_object.bucket()
          response = delete_all_object.bucket()
          message_string += response["message"] + "\n"

      else:
        # return {"status": "error", "message": "Comando invalido en delete_all"}
        message_string += "Comando invalido en delete_all" + "\n"

    elif command.get("open"):
      open, type, ip, port, name = scan_command_line_open(command.get("open"))
      if open and type and name:
        print("open")
        # create instance of open class
        open_object = Open(type, ip, port, name)
        # evaluate if the backup is only in our environment
        if ip == None and port == None:
          # evaluate if the type is local or bucket
          if type == "server":
            return open_object.local()
            # response = open_object.local()
            # message_string += response["message"] + "\n"

          elif type == "bucket":
            return open_object.bucket()
            # response = open_object.bucket()
            # message_string += response["message"] + "\n"

        # evaluate if the backup is in another environment (port and ip)
        elif ip != None and port != None:
          print("entra")
          # evaluate if the type is local or bucket
          return open_object.api_ip()
          # response = open_object.api_ip()
          # message_string += response["message"] + "\n"

        else:
          return {"status": "error", "message": "Comando invalido en backup"}
      else:
        return {"status": "error", "message": "Comando invalido en open"}
        # message_string += "Comando invalido en open" + "\n"

  return {"status": "success", "message": message_string}
