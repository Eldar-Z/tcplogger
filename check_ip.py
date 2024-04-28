import subprocess

def get_up_interface_ip():
  output = subprocess.run(['ip', 'a'], capture_output=True, text=True).stdout
  for line in output.splitlines():
    if "state UP" in line:
      interface_name = line.split()[1]
      ip_address = subprocess.run(['ip', 'addr', 'show', interface_name], capture_output=True, text=True).stdout
      for ip_line in ip_address.splitlines():
        if "inet " in ip_line:
          return ip_line.split()[1].split("/")[0]
  return None

def main():
	ip_address = get_up_interface_ip()
	with open('ip_address.txt', 'w') as f:
		f.write(ip_address)

if __name__ == "__main__":
  main()
