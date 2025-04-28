# TCP Chat Application

A multi-threaded TCP chat server and client system where two users can exchange real-time messages over a network.  
Supports offline message delivery, user validation, and clean session handling.

---

## Authors:
- Marcelo Villalobos Diaz
- Rob Stanford
- Vance Thrasher
- Zuhra Totakhail

## 📁 Project Structure

- `chat_server.py` — Basic TCP chat server (handles two clients).
- `chat_client.py` — Basic TCP chat client (connects to server, sends/receives messages).
- `chat_server_ec_v2.py` — Enhanced chat server with offline message storage and validation.
- `chat_client_ec_v2.py` — Enhanced chat client with username validation and better error handling.

---

## 🚀 How It Works

1. The server (`chat_server_ec_v2.py`) waits for two clients to connect.
2. Clients (`chat_client_ec_v2.py`) join with usernames (**Client 1** or **Client 2**).
3. Clients can send messages to each other in real time.
4. If a client is offline, messages are **queued** and delivered when they reconnect.
5. Typing `bye` ends the chat session cleanly.

---

## 🛠 Prerequisites

- Python 3.6+
- No external libraries required (only built-in Python modules: `socket`, `threading`, `argparse`, `logging`)

---

## 🧠 How to Run

1. **Start the server:**
   ```bash
   python3 chat_server_ec_v2.py --host 10.0.0.1 --port 12000
2. **Start the first client:**
   ```bash
   python3 chat_client_ec_v2.py --server 10.0.0.1 --port 12000
3. **Start the second client:**
   ```bash
   python3 chat_client_ec_v2.py --server 10.0.0.1 --port 12000
4. **Login:**
   - When prompted, enter your username as Client 1 or Client 2.
   - Only these two usernames are accepted.
5. **Chat:**
   - Type messages to chat.
   - Type bye to leave the chat gracefully.
