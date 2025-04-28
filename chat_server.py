#!env python

"""Chat server for CST311 Programming Assignment 3"""
__author__ = "Team3"
__credits__ = [
    "Marcelo Villalobos Diaz"
    "Rob Stanford"
    "Vance Thrasher"
    "Zuhra Totakhail"
]

import threading
import argparse
import socket as s
import time
import logging

# Configure logging
logging.basicConfig()
log = logging.getLogger(f"SERVER:{__name__}")
log.setLevel(logging.DEBUG)

# Gobals
chat_clients = {"x": None, "y": None}

def chat(connection_socket, address, client):
    global chat_clients

    chatting = True
    while chatting:
        sender = "x" if client == "x" else "y"
        reciever = "y" if client == "x" else "x"
        query = connection_socket.recv(1024)
        query_decoded = query.decode()
        log.info(f"Client{sender.upper()} -> Client{reciever.upper()}: \"{query_decoded}\"")
        if query_decoded == "bye":
            if chat_clients['x'] and chat_clients['y']:
                reciever_conn.send(f"Client {sender.upper()}: {query_decoded}\n".encode())
                reciever_conn.send(f" ! Client {sender.upper()} has left the chat".encode())
            chatting = False
            chat_clients[sender] = None
            log.debug(f"{chat_clients=}")
            continue
        elif not (chat_clients['x'] and chat_clients['y']):
            log.warning("Two clients not connected, dropping")
            log.debug(f"{chat_clients=}")
            continue
        
        reciever_conn = chat_clients[reciever]
        reciever_conn.send(f"Client {sender.upper()}: {query_decoded}".encode())

    connection_socket.close()


def run_chat_server(server_host="10.0.0.1", server_port=12000):
    global chat_clients
    # Create a TCP socket
    # Notice the use of SOCK_STREAM for TCP packets
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    # Assign port number to socket, and bind to chosen port
    server_socket.bind((server_host, server_port))

    # Configure how many requests can be queued on the server at once
    server_socket.listen(1)

    # Alert user we are now online
    log.info(f"The chat server is ready to receive on port: {server_port}")

    # Surround with a try-finally to ensure we clean up the socket after we're done
    try:
        # Enter forever loop to listen for requests
        while True:
            # When a client connects, create a new socket and record their address
            connection_socket, address = server_socket.accept()
            # log.info(f"Connected to client at: {address}")

            if not chat_clients["x"]:
                log.info(f"Client X Connected at: {address}")
                chat_clients["x"] = connection_socket
                connection_socket.send(f"Welcome to the chat Client X!".encode())
                client = "x"
            elif not chat_clients["y"]:
                log.info(f"Client Y Connected at: {address}")
                chat_clients["y"] = connection_socket
                connection_socket.send(f"Welcome to the chat Client Y!".encode())
                client = "y"
            # Pass the new socket and address off to a connection handler function
            thread = threading.Thread(target=chat, args=(connection_socket, address, client))
            thread.start()
    finally:
        server_socket.close()
        thread.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="10.0.0.1", type=str, help="Server's hostname or IP address, default 10.0.0.1")
    parser.add_argument("--port", default=12000, type=int, help="Port number used by the chat server, default 12000")

    args = parser.parse_args()
    run_chat_server(server_host=args.host, server_port=args.port)