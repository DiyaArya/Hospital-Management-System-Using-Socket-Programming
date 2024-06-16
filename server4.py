# import socket
# import ssl
# from threading import Thread

# doctors = {}  # doctor_name: (specialization, doctor_conn, available)
# sessions = {}  # client_conn: (doctor_name, doctor_conn)

# def handle_client(connection, _):
#     global doctors, sessions
#     try:
#         while True:
#             data = connection.recv(1024).decode('utf-8')
#             if not data:
#                 break

#             if data.startswith("REGISTER_DOCTOR"):
#                 _, name, specialization = data.split(':', 2)
#                 doctors[name] = (specialization, connection, True)
#                 print(f"{name} registered as a doctor.")

#             elif data == "REQUEST_DOCTORS_LIST":
#                 available_doctors = {name: spec for name, (spec, _, available) in doctors.items() if available}
#                 doctors_list = ", ".join([f"{name} - {spec}" for name, spec in available_doctors.items()])
#                 connection.sendall(doctors_list.encode('utf-8'))

#             elif data.startswith("SELECT_DOCTOR"):
#                 _, selected_name = data.split(':', 1)
#                 selected_name = selected_name.strip()
#                 if selected_name in doctors and doctors[selected_name][2]:  # Check if doctor is available
#                     selected_doctor_conn = doctors[selected_name][1]
#                     doctors[selected_name] = (doctors[selected_name][0], selected_doctor_conn, False)  # Mark as unavailable
#                     sessions[connection] = (selected_name, selected_doctor_conn)
#                     connection.sendall(f"Connected to {selected_name}. Start chatting!".encode('utf-8'))
#                 else:
#                     connection.sendall("Doctor not available or not found.".encode('utf-8'))

#             elif connection in sessions:
#                 # Relay messages between client and doctor
#                 _, doctor_conn = sessions[connection]
#                 doctor_conn.sendall(data.encode('utf-8'))

#     finally:
#         connection.close()
#         # Remove disconnected clients and free up the doctor
#         if connection in sessions:
#             doctor_name, _ = sessions.pop(connection)
#             doctors[doctor_name] = (doctors[doctor_name][0], doctors[doctor_name][1], True)  # Mark doctor as available
#         print(f"Connection from {connection.getpeername()} closed.")

# def start_server(certfile='server.crt', keyfile='server.key'):
#     host = 'localhost'
#     port = 12345
#     context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
#     context.load_cert_chain(certfile=certfile, keyfile=keyfile)

#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#         sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         sock.bind((host, port))
#         sock.listen(5)
#         print("Server listening...")

#         with context.wrap_socket(sock, server_side=True) as secure_socket:
#             while True:
#                 conn, addr = secure_socket.accept()
#                 print(f"Accepted connection from {addr}")
#                 Thread(target=handle_client, args=(conn, addr)).start()

# if __name__ == "__main__":
#     start_server()
"""
import socket
import ssl
from threading import Thread

# Stores doctor's details and whether they are available
doctors = {}  # doctor_name: (specialization, doctor_conn, available)
# Stores the mapping of clients to doctors and vice versa
sessions = {}  # conn: (doctor_name, peer_conn)

def handle_client(connection, _):
    global doctors, sessions
    try:
        while True:
            data = connection.recv(1024).decode('utf-8')
            if not data:
                break

            if data.startswith("REGISTER_DOCTOR"):
                _, name, specialization = data.split(':', 2)
                doctors[name] = (specialization, connection, True)  # Doctor is initially available
                print(f"{name} registered as a doctor.")

            elif data == "REQUEST_DOCTORS_LIST":
                # Send only available doctors
                available_doctors = {name: spec for name, (spec, _, available) in doctors.items() if available}
                doctors_list = ", ".join([f"{name} - {spec}" for name, spec in available_doctors.items()])
                connection.sendall(doctors_list.encode('utf-8'))

            elif data.startswith("SELECT_DOCTOR"):
                _, selected_name = data.split(':', 1)
                selected_name = selected_name.strip()
                if selected_name in doctors and doctors[selected_name][2]:  # Doctor is available
                    selected_doctor_conn = doctors[selected_name][1]
                    # Update availability and sessions
                    doctors[selected_name] = (doctors[selected_name][0], selected_doctor_conn, False)
                    sessions[connection] = (selected_name, selected_doctor_conn)
                    sessions[selected_doctor_conn] = (selected_name, connection)
                    connection.sendall(f"Connected to {selected_name}. Start chatting!".encode('utf-8'))
                else:
                    connection.sendall("Doctor not available or not found.".encode('utf-8'))

            elif connection in sessions:
                # Relay messages between client and doctor
                _, peer_conn = sessions[connection]
                peer_conn.sendall(data.encode('utf-8'))
                if data.strip().lower() == "bye":  # End conversation
                    # Free up the doctor
                    doctor_name, _ = sessions[connection]
                    _, doctor_conn, _ = doctors[doctor_name]
                    doctors[doctor_name] = (doctors[doctor_name][0], doctor_conn, True)
                    # Remove from sessions
                    del sessions[connection]
                    del sessions[peer_conn]

    finally:
        connection.close()
        # Remove from sessions if present
        if connection in sessions:
            doctor_name, peer_conn = sessions.pop(connection)
            doctors[doctor_name] = (doctors[doctor_name][0], doctors[doctor_name][1], True)
            sessions.pop(peer_conn, None)
        print(f"Connection from {connection.getpeername()} closed.")

def start_server(certfile='server.crt', keyfile='server.key'):
    host = ''
    port = 12345
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(5)
        print("Server listening...")

        with context.wrap_socket(sock, server_side=True) as secure_socket:
            while True:
                conn, addr = secure_socket.accept()
                Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
"""
import socket
import ssl
from threading import Thread

# Stores doctor's details and whether they are available
doctors = {}  # doctor_name: (specialization, doctor_conn, available)
# Stores the mapping of clients to doctors and vice versa
sessions = {}  # conn: (doctor_name, peer_conn)

def handle_client(connection, _):
    global doctors, sessions
    try:
        while True:
            data = connection.recv(1024).decode('utf-8')
            if not data:
                break

            if data.startswith("REGISTER_DOCTOR"):
                _, name, specialization = data.split(':', 2)
                doctors[name] = (specialization, connection, True)  # Doctor is initially available
                print(f"{name} registered as a doctor.")

            elif data == "REQUEST_DOCTORS_LIST":
                # Send only available doctors
                available_doctors = {name: spec for name, (spec, _, available) in doctors.items() if available}
                doctors_list = ", ".join([f"{name} - {spec}" for name, spec in available_doctors.items()])
                connection.sendall(doctors_list.encode('utf-8'))

            elif data.startswith("SELECT_DOCTOR"):
                _, selected_name = data.split(':', 1)
                selected_name = selected_name.strip()
                if selected_name in doctors and doctors[selected_name][2]:  # Doctor is available
                    selected_doctor_conn = doctors[selected_name][1]
                    # Update availability and sessions
                    doctors[selected_name] = (doctors[selected_name][0], selected_doctor_conn, False)
                    sessions[connection] = (selected_name, selected_doctor_conn)
                    sessions[selected_doctor_conn] = (selected_name, connection)
                    connection.sendall(f"Connected to {selected_name}. Start chatting!".encode('utf-8'))
                else:
                    connection.sendall("Doctor not available or not found.".encode('utf-8'))

            else:
                # Relay messages between client and doctor
                doctor_name, peer_conn = sessions.get(connection, (None, None))
                if peer_conn:
                    peer_conn.sendall(data.encode('utf-8'))
                    if data.strip().lower() == "bye":  # End conversation
                        # Notify the client that the session has ended
                        peer_conn.sendall("Session ended by the doctor.".encode('utf-8'))
                        # Clean up sessions and mark the doctor as available
                        if doctor_name:
                            doctors[doctor_name] = (doctors[doctor_name][0], doctors[doctor_name][1], True)
                        sessions.pop(connection, None)
                        sessions.pop(peer_conn, None)

    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        connection.close()
        # Clean up after disconnection
        if connection in sessions:
            doctor_name, _ = sessions.pop(connection)
            # Mark the doctor as available if they were in a session
            if doctor_name in doctors:
                doctors[doctor_name] = (doctors[doctor_name][0], doctors[doctor_name][1], True)
        # Also, check the reverse mapping and clean up
        for conn, (name, _) in list(sessions.items()):
            if name in doctors and doctors[name][1] == connection:
                sessions.pop(conn, None)
                doctors[name] = (doctors[name][0], doctors[name][1], True)
        print("Connection closed.")

def start_server(certfile='server.crt', keyfile='server.key'):
    host = ''
    port = 12345
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(5)
        print("Server listening...")

        with context.wrap_socket(sock, server_side=True) as secure_socket:
            while True:
                conn, addr = secure_socket.accept()
                # Handle each client in a separate thread
                Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
