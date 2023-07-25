import re
# Scan delete command line
def scan_command_line_rename(command_line):
  # Define regular expressions for matching different components
  pattern_rename = r'rename\s'
  # pattern_name = r"-name->(?:(?:'([^']+)'|\"([^\"]+)\")|(\S+))(\s|$)"
  pattern_name = r"-name->('?[\w\s]+\.\w+')?"
  pattern_path = r"-path->(?:(?:'([^']+)'|\"([^\"]+)\")|(\S+))(\s|$)"
  pattern_type = r'-type->(?:"([^"]+)"|(\S+))(\s|$)'

  # Match the components using regular expressionsy 
  match_rename = re.search(pattern_rename, command_line,re.I)
  match_path = re.search(pattern_path, command_line,re.I)
  match_name = re.search(pattern_name, command_line,re.I)
  match_type = re.search(pattern_type, command_line,re.I)

  # Extract the values from the matches
  rename = match_rename.group(0) if match_rename else None
  path = None
  try:
    if match_path and match_path.group() is not None:
      if match_path.group() == "/ ":
        path = "/ "
      else:
        path = match_path.group().split("->")[1].replace("'", '').replace(' -name','').replace('-type','').replace(' -Type','')

  except AttributeError:
    path = None
  # this None could be ambigous, becuase it could come or not
  name = False
  try:
    print(match_name.group(), " nameeeeeeeeeee")
    if match_name and match_name.group() is not None:
      name = match_name.group().split("->")[1]
  except AttributeError:
    name = None

  type = match_type.group(1) or match_type.group(2) if match_type else None

  # Return the extracted values
    
  return rename.lower().rstrip(" "), path.rstrip(" "), name.rstrip(" ").replace("'", ''), type.strip(" ")