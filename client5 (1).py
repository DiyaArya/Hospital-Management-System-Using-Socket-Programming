
import socket
import ssl
import threading
import sys

def receive_messages(ssl_sock):
    while True:
        data = ssl_sock.recv(1024).decode('utf-8')
        if data == "exit":
            print("Disconnected from server")
            ssl_sock.close()
            break
        print("Received:", data)

def client_communicate():
    host = '192.168.1.100'
    port = 12345
    
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations('server.crt')
    
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            print("SSL connection established. Peer: {}".format(ssock.getpeercert()))
            
            receiver_thread = threading.Thread(target=receive_messages, args=(ssock,))
            receiver_thread.start()
            
            while True:
                message = input("Enter message: ")
                if message == "exit":
                    ssock.sendall(message.encode('utf-8'))
                    break
                ssock.sendall(message.encode('utf-8'))
            receiver_thread.join()

if __name__ == "__main__":
    client_communicate()
