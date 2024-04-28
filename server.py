import socket

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with open('ip_address.txt', 'r') as f:
    	ip_address = f.read().strip()

    server_socket.bind((ip_address, 2345))
    server_socket.listen(1)
    print("Сервер запущен и ожидает соединений")
    while True:
        client_socket, client_address = server_socket.accept()
        #print(f"Получено соединение от {client_address}")
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                with open("received_file.txt", "ab") as file:
                    file.write(data)
                #print("Данные успешно приняты и сохранены")
        finally:
            client_socket.close()
            #print("Соединение с клиентом закрыто")
            
    server_socket.close()

if __name__ == "__main__":
    main()
