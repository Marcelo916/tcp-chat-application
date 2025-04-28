#!env python

"""Chat server for CST311 Programming Assignment 3"""
__author__ = "Team3"
__credits__ = [
    "Marcelo Villalobos Diaz",
    "Rob Stanford",
    "Vance Thrasher",
    "Zuhra Totakhail"
]

import threading
import argparse
import socket as s
import logging

# Configure logging
logging.basicConfig()
log = logging.getLogger(f"SERVER:{__name__}")
log.setLevel(logging.DEBUG)

# Globals
clients = {}  # Dictionary to store clients: {username: socket}
offline_messages = {}  # Dictionary to store offline messages: {username: [messages]}
usernames = {"Client 1", "Client 2"}  # Set of all known usernames

def handle_client(client_socket, address):
    global clients, offline_messages, usernames
    try:
        # Receive username from client
        username = client_socket.recv(1024).decode()
        if not username:
            client_socket.close()
            return
        if username in clients:
            # Username already taken
            client_socket.send("Username already taken. Please reconnect with a different username.".encode())
            client_socket.close()
            return
        if username not in usernames:
            # Invalid username
            client_socket.send("Invalid username. Use 'Client 1' or 'Client 2'.".encode())
            client_socket.close()
            return

        # Add client to clients dictionary
        clients[username] = client_socket
        log.info(f"{username} connected from {address}")

        # Send any offline messages to the client
        if username in offline_messages:
            for msg in offline_messages[username]:
                client_socket.send(msg.encode())
            del offline_messages[username]

        # Notify other user
        other_user = "Client 1" if username == "Client 2" else "Client 2"

        client_socket.send(f"Welcome to the chat, {username}!".encode())

        if other_user in clients:
            clients[other_user].send(f"{username} has joined the chat.".encode())
        else:
            # The other user is offline
            pass

        while True:
            message = client_socket.recv(1024)
            if not message:
                # Client has disconnected
                log.info(f"{username} has disconnected.")
                break
            message = message.decode()

            if message.lower() == "bye":
                log.info(f"{username} has left the chat.")
                if other_user in clients:
                    clients[other_user].send(f"{username} has left the chat.".encode())
                else:
                    # Store message for offline client
                    offline_messages.setdefault(other_user, []).append(f"{username} has left the chat.")
                break

            # Send the message to the other user
            if other_user in clients:
                # User is connected
                try:
                    clients[other_user].send(f"{username}: {message}".encode())
                except Exception as e:
                    log.error(f"Could not send message to {other_user}: {e}")
                    # Remove client from clients and store message
                    clients.pop(other_user)
                    offline_messages.setdefault(other_user, []).append(f"{username}: {message}")
            else:
                # User is offline
                offline_messages.setdefault(other_user, []).append(f"{username}: {message}\n")

    except Exception as e:
        log.error(f"Error with client {username}: {e}")
    finally:
        # Clean up client connection
        client_socket.close()
        if username in clients:
            del clients[username]
        log.info(f"Connection with {username} closed.")

def run_chat_server(server_host="10.0.0.1", server_port=12000):
    global clients
    # Create a TCP socket
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    # Assign port number to socket, and bind to chosen port
    server_socket.bind((server_host, server_port))

    # Configure how many requests can be queued on the server at once
    server_socket.listen(5)

    # Alert user we are now online
    log.info(f"The chat server is ready to receive on port: {server_port}")

    try:
        while True:
            # Accept new connection
            client_socket, address = server_socket.accept()
            # Start a new thread for the client
            thread = threading.Thread(target=handle_client, args=(client_socket, address))
            thread.start()
    except KeyboardInterrupt:
        log.info("Server shutting down.")
    finally:
        server_socket.close()
        for client_socket in clients.values():
            client_socket.close()
        log.info("Server closed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="10.0.0.1", type=str, help="Server's hostname or IP address, default 10.0.0.1")
    parser.add_argument("--port", default=12000, type=int, help="Port number used by the chat server, default 12000")

    args = parser.parse_args()
    run_chat_server(server_host=args.host, server_port=args.port)
