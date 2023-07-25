import re
# Scan copy command line
def scan_command_line_open(command_line):
  # Define regular expressions for matching different components
  pattern_open = r'open\s'
  pattern_type = r'-type->(?:"([^"]+)"|(\S+))(\s|$)'
  patern_ip = r'-ip->(?:"([^"]+)"|(\S+))(\s|$)'
  patern_port = r'-port->(?:"([^"]+)"|(\S+))(\s|$)'
  pattern_name = r"-name\-\>(.*)"

  # pattern_name = r"-name->(?:(?:'([^']+)'|\"([^\"]+)\")|(\S+))(\s|$)"

  # Match the components using regular expressions
  match_open = re.search(pattern_open, command_line,re.I)
  match_type = re.search(pattern_type, command_line,re.I)
  match_ip = re.search(patern_ip, command_line,re.I)
  match_port = re.search(patern_port, command_line,re.I)
  match_name = re.search(pattern_name, command_line,re.I)

  # Extract the values from the matches
  recovery = match_open.group(0) if match_open else None
  ip = None
  port = None
  name = None
  try:
    if match_ip and match_ip.group() is not None:
      ip = match_ip.group().split("->")[1].replace("'", '').replace(" ","")
    if match_port and match_port.group() is not None:
      port = match_port.group().split("->")[1].replace("'", '')
    if match_name and match_name.group() is not None:
      name = match_name.group().split("->")[1].replace("'", '').replace("-port", "")
  except AttributeError:
    ip = False
    port = False
    name = None

  type = match_type.group(1) or match_type.group(2) if match_type else None
  # Return the extracted values
  if name.endswith(" "):
    return recovery.lower().rstrip(" "), type, ip, port, name.rstrip(" ")
  return recovery.lower().strip(), type, ip.strip(), port.strip(), name