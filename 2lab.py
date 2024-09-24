#TCP-server
import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 55555  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    serverSocket.bind((HOST, PORT))
    serverSocket.listen()
    conn, addr = serverSocket.accept()
    with conn:
        print(f"Подключение: {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break  
            print(f"Получено от клиента сообщение: {data.decode('utf-8')}")
            conn.sendall(data)

#TCP-client
import socket

HOST = '127.0.0.1'
PORT = 55555

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    message = "Привет, сервер!"
    client_socket.sendall(message.encode('utf-8'))
    data = client_socket.recv(1024)
    print(f"Получено от сервера: {data.decode('utf-8')}")


#UDP-server
import socket

HOST = "127.0.0.1"
PORT = 55555
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udpSocket:
    udpSocket.bind((HOST, PORT))
    while True:
        data, clientAddress = udpSocket.recvfrom(1024)
        print(f"Получены данные от {clientAddress}: {data.decode()}")
        udpSocket.sendto(data, clientAddress)
        udpSocket.close()
        break

#UDP-client
import socket


HOST = '127.0.0.1'
PORT = 55555

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udpClientSocket:
    message = "Привет, сервер!"
    server_address = (HOST, PORT)
    try:
        sent = udpClientSocket.sendto(message.encode(), server_address)
        data, server = udpClientSocket.recvfrom(1024)
        print(f"Получено сообщение от сервера: {data.decode()}")
    finally:
        udpClientSocket.close()



