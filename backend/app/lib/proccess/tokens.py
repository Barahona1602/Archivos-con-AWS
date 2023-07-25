import re

commands = "create, delete, copy, transfer, rename, modify, backup, recovery, delete_all, open"

def extract_commands(command_string):
  tokens = []
  command_list = commands.split(", ")

  pattern = fr"\b({'|'.join(command_list)})\b"
  matches = re.split(pattern, command_string, flags=re.IGNORECASE)
  for i in range(1, len(matches), 2):
      command = matches[i].rstrip()  # Remove leading whitespace
      if i + 1 < len(matches):
          command += matches[i + 1]  # Include the whitespace after the command
      tokens.append({matches[i].lower(): command.replace("\n", " ")})

  return tokens
