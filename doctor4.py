import socket
import ssl
from threading import Thread

def receive_messages(secure_socket):
    while True:
        try:
            message = secure_socket.recv(1024).decode('utf-8')
            if message:
                print(f"\n{message}\nReply ('bye' to end): ", end="")
        except Exception as e:
            print(f"Connection closed: {e}")
            break

def doctor_client(name, specialization):
    host = 'localhost'
    port = 12345

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as secure_socket:
            # Register the doctor
            secure_socket.sendall(f"REGISTER_DOCTOR:{name}:{specialization}".encode('utf-8'))
            print(f"Registered as {name}, specialization: {specialization}")

            # Start a thread for receiving messages
            Thread(target=receive_messages, args=(secure_socket,), daemon=True).start()

            # Sending messages
            while True:
                msg = input("Reply ('bye' to end): ")
                secure_socket.sendall(msg.encode('utf-8'))
                if msg.lower() == "bye":
                    print("Session ended.")
                    break

if __name__ == "__main__":
    name = input("Enter your name: ")
    specialization = input("Enter your specialization: ")
    doctor_client(name, specialization)
