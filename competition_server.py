import random
import socket
import threading
from academy_hustlers.settings import IP


# Select port number
def generate_port_number():
    # Generate a random number between 1000 and 9999 (both inclusive)
    number = random.randint(1000, 9999)
    return number


# IP = socket.gethostbyname(socket.gethostname())
# PORT = generate_port_number()
PORT = generate_port_number()
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

# Counter for connected clients
# client_count = 0


def handle_client(conn, addr):
    # global client_count
    print(f"[New Player Joined this Window] {addr} connected.")

    # # Increment client count and check if it exceeds the limit
    # client_count += 1
    # if client_count > 2:
    #     # print(f"[SERVER FULL] {addr} was rejected due to maximum occupancy.")
    #     # conn.send("Server is full. Try again later.".encode(FORMAT))
    #     conn.close()
    #     client_count -= 1  # Decrement client count if rejected
    #     return

    connected = True
    while connected:

        conn.send("welcome to the BattleField. Finding your worthy contender".encode(FORMAT))

        answer = conn.recv(SIZE).decode(FORMAT)
        if answer == DISCONNECT_MSG:
            connected = False

        print(f"[{addr}] Answer: {answer}")

    # Decrement client count when client disconnects
    # client_count -= 1
    conn.close()


def competition_server():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        # # Check if maximum client count reached
        # if client_count >= 2:
        #     print("[SERVER FULL] Maximum client count reached. Closing server...")
        #     break

        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))

        thread.start()

    # Close the server socket
    server.close()


# # Start the competition server in a separate thread
# competition_thread = threading.Thread(target=competition_server)
# competition_thread.start()
