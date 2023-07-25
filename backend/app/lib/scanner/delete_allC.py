import re
# Scan copy command line
def scan_command_line_delete_all(command_line):
  # Define regular expressions for matching different components
  pattern_delete_all = r'delete_all\s'
  pattern_type = r'-type->(?:"([^"]+)"|(\S+))(\s|$)'

  # Match the components using regular expressions
  match_delete_all = re.search(pattern_delete_all, command_line,re.I)
  match_type = re.search(pattern_type, command_line,re.I)

  # Extract the values from the matches
  delete_all = match_delete_all.group(0) if match_delete_all else None
  type = match_type.group(1) or match_type.group(2) if match_type else None

  # Return the extracted values
  return delete_all.lower().rstrip(" "), type.strip(" ")
