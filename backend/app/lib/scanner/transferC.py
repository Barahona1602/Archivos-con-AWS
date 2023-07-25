import re
# Scan copy command line
def scan_command_line_transfer(command_line):
  # Define regular expressions for matching different components
  pattern_transfer = r'transfer\s'
  pattern_from = r'-from->(?:"([^"]*)"|/([^/]+/?)+)\s'
  pattern_to = r'-to->(?:"([^"]+)"|/([^/]+/)+)(\s|$)'
  pattern_type_to = r'-type_to->(?:"([^"]+)"|(\S+))(\s|$)'
  pattern_type_from = r'-type_from->(?:"([^"]+)"|(\S+))(\s|$)'

  # Match the components using regular expressions
  match_transfer = re.search(pattern_transfer, command_line,re.I)
  match_from = re.search(pattern_from, command_line,re.I)
  match_to = re.search(pattern_to, command_line,re.I)
  match_type_to = re.search(pattern_type_to, command_line,re.I)
  match_type_from = re.search(pattern_type_from, command_line,re.I)

  # Extract the values from the matches
  transfer = match_transfer.group(0) if match_transfer else None
  from_path = None
  try:
    if match_from and match_from.group() is not None:
      from_path = match_from.group().split("->")[1].replace("'", '').replace(' -to','')
  except AttributeError:
    from_path = None
  to_path = None
  try:
    if match_to and match_to.group() is not None:
      to_path = match_to.group().split("->")[1].replace("'", '')
  except AttributeError:
    to_path = None
  type_to = match_type_to.group(1) or match_type_to.group(2) if match_type_to else None
  type_from = match_type_from.group(1) or match_type_from.group(2) if match_type_from else None
  # Return the extracted values
  return transfer.lower().rstrip(" "), from_path.replace("-type_from","").rstrip(" "), to_path.rstrip(" "), type_to, type_from