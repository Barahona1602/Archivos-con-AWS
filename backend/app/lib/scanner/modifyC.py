import re
# Scan modify command line
def scan_command_line_modify(command_line):
  # Define regular expressions for matching different components
  pattern_modify = r'modify\s'
  pattern_path = r'-path->(?:"([^"]*)"|/([^/]+/?)+)\s'
  pattern_body = r"-body->'([^']+)'(\s|$)"  # $ is the end of the string
  pattern_type = r'-type->(?:"([^"]+)"|(\S+))(\s|$)'

  # Match the components using regular expressions
  match_modify = re.search(pattern_modify, command_line,re.I)
  match_path = re.search(pattern_path, command_line,re.I)
  match_new_body = re.search(pattern_body, command_line,re.I)
  match_type = re.search(pattern_type, command_line,re.I)

  # Extract the values from the matches
  modify = match_modify.group(0) if match_modify else None
  path = None
  try:
    if match_path and match_path.group() is not None:
      if match_path.group() == "/ ":
        path = "/ "
      else:
        path = match_path.group().split("->")[1].replace("'", '').replace(' -body','').replace(' -type','').replace(' -Type','')

  except AttributeError:
    path = None

  new_body = match_new_body.group(1) if match_new_body else None
  type = match_type.group(1) or match_type.group(2) if match_type else None

  # Return the extracted values
  return modify.lower().strip(" "), path.rstrip(" "), new_body, type