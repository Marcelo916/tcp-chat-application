#!env python

"""Chat client for CST311 Programming Assignment 3"""
__author__ = "Team3"
__credits__ = [
    "Marcelo Villalobos Diaz"
    "Rob Stanford"
    "Vance Thrasher"
    "Zuhra Totakhail"
]

# Import statements
import threading
import argparse
import socket as s
import sys

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(f"CLIENT:{__name__}")
log.setLevel(logging.DEBUG)

# Set global variables
chatting = True

def send_message(client_socket, i):
    global chatting 

    while chatting:
        # Get input from user
        user_input = input('')

        # Set data across socket to server
        #  Note: encode() converts the string to UTF-8 for transmission
        client_socket.send(user_input.encode())

        if user_input == "bye":
            chatting = False
            break

def recieve_message(client_socket, i):
    global chatting 

    while chatting:
        # Read response from server
        server_response = client_socket.recv(1024)
        # Decode server response from UTF-8 bytestream
        server_response_decoded = server_response.decode()

        # Print output from server
        print(f"{server_response_decoded}")

def start_chat_client(server_host="10.0.0.1", server_port=12000):
    # Create socket
    client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    try:
        # Establish TCP connection
        client_socket.connect((server_host, server_port))

        # while chatting:
        thread_recieve = threading.Thread(target=recieve_message, args=(client_socket, 0))
        thread_recieve.start()
        thread_send = threading.Thread(target=send_message, args=(client_socket, 0))
        thread_send.start()

    except Exception as e:
        log.exception(e)
        log.error("***Advice:***")
        if isinstance(e, s.gaierror):
            log.error(
                "\tCheck that server_name and server_port are set correctly.")
        elif isinstance(e, ConnectionRefusedError):
            log.error("\tCheck that server is running and the address is correct")
        else:
            log.error(
                "\tNo specific advice, please contact teaching staff and include text of error and code.")
            exit(8)

    finally:
        try:
            thread_recieve.join()
            thread_send.join()
        except UnboundLocalError:
            pass
        client_socket.close()
        
# This helps shield code from running when we import the module
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", default='10.0.0.1', type=str,
                        help="Chat server's hostname or IP address, default '10.0.0.1'")
    parser.add_argument("--port", default=12000, type=int,
                        help="Port number used by chat server, default 12000")

    args = parser.parse_args()
    start_chat_client(server_host=args.server, server_port=args.port)