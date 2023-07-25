import re
# Scan copy command line
def scan_command_line_recovery(command_line):
  # Define regular expressions for matching different components
  pattern_recovery = r'recovery\s'
  pattern_type_to = r'-type_to->(?:"([^"]+)"|(\S+))(\s|$)'
  pattern_type_from = r'-type_from->(?:"([^"]+)"|(\S+))(\s|$)'
  patern_ip = r'-ip->(?:"([^"]+)"|(\S+))(\s|$)'
  patern_port = r'-port->(?:"([^"]+)"|(\S+))(\s|$)'
  pattern_name = r"-name->(?:(?:'([^']+)'|\"([^\"]+)\")|(\S+))(\s|$)"

  # Match the components using regular expressions
  match_recovery = re.search(pattern_recovery, command_line,re.I)
  match_type_to = re.search(pattern_type_to, command_line,re.I)
  match_type_from = re.search(pattern_type_from, command_line,re.I)
  match_ip = re.search(patern_ip, command_line,re.I)
  match_port = re.search(patern_port, command_line,re.I)
  match_name = re.search(pattern_name, command_line,re.I)

  # Extract the values from the matches
  recovery = match_recovery.group(0) if match_recovery else None
  ip = None
  port = None
  name = None
  try:
    if match_ip and match_ip.group() is not None:
      ip = match_ip.group().split("->")[1].replace("'", '').replace(" ","")
    if match_port and match_port.group() is not None:
      port = match_port.group().split("->")[1].replace("'", '')
    if match_name and match_name.group() is not None:
      name = match_name.group().split("->")[1].replace("'", '')
  except AttributeError:
    ip = False
    port = False
    name = None

  type_to = match_type_to.group(1) or match_type_to.group(2) if match_type_to else None
  type_from = match_type_from.group(1) or match_type_from.group(2) if match_type_from else None
  # Return the extracted values
  if name.endswith(" "):
    return recovery.lower().rstrip(" "), type_to, type_from, ip, port, name.rstrip(" ")
  return recovery.lower().rstrip(" "), type_to, type_from, ip, port, name