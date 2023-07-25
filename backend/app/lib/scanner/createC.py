import re
# Scan create command line
def scan_command_line_create(command_line):
  # Define regular expressions for matching different components
  pattern_create = r'create\s'
  pattern_name = r"-name->(?:(?:'([^']+)'|\"([^\"]+)\")|(\S+))(\s|$)"
  pattern_path = r'-path->(?:"([^"]+)"|/([^/]+/)+)|/(\s|$)'
  pattern_body = r"-body->'([^']+)'(\s|$)"  # $ is the end of the string
  pattern_type = r'-type->(?:"([^"]+)"|(\S+))(\s|$)'


  # Match the components using regular expressions
  match_create = re.search(pattern_create, command_line,re.I)
  match_name = re.search(pattern_name, command_line,re.I)
  match_path = re.search(pattern_path, command_line,re.I)
  match_body = re.search(pattern_body, command_line,re.I)
  match_type = re.search(pattern_type, command_line,re.I)

  # Extract the values from the matches
  create = match_create.group(0) if match_create else None
  name = None
  path = None
  
  try:
    if match_path and match_path.group() is not None:
      if match_path.group() == "/ ":
        path = "/ "
      else:
        path = match_path.group().split("->")[1].replace("'", '')
    if match_name and match_name.group() is not None:
      name = match_name.group().split("->")[1].replace("'", '')
  except AttributeError:
    path = None
    name = None

  body = match_body.group(1) if match_body else None
  type = match_type.group(1) or match_type.group(2) if match_type else None
  # Return the extracted values

  return create.lower().rstrip(" "), name.strip(" "), path.rstrip(" "), body, type