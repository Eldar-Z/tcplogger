import socket
import time
import sys

def main():
    if len(sys.argv) != 3:
        print("client.py <period> <num_bytes>")
        sys.exit(1)
    
    period = int(sys.argv[1])
    num_bytes = int(sys.argv[2])
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with open('ip_address.txt', 'r') as f:
    	ip_address = f.read().strip()
    client_socket.connect((ip_address, 2345))
    
    while True:
        data_to_send = b"A" * num_bytes
        client_socket.sendall(data_to_send)
        #print("Данные успешно отправлены на сервер.")
        time.sleep(period)

if __name__ == "__main__":
    main()
