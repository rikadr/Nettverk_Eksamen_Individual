import socket
import threading
import random
import bots
import sys

utf8 = "utf-8"
server_username = "*Server*"
ip = "127.0.0.1"
port = 7976

s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creating a TCP/IP socket
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # dont know if i need
s_socket.bind((ip, port))  # binds the ip address and port
s_socket.listen()  # Have the server listen for client connections

clients_list = []    # A list to hold the client objects


# A class to hold the client connection and username
class Client:
    """A class to hold the client connection and username"""
    connection = None
    username = None


# Function to continuously listen for new client connections
def listen_for_clients():
    print("Server started up! Now listening for connecting clients ...")
    while True:
        connection, address = s_socket.accept()  # wait for a new connecting client and accept
        # print(f"Accepted connection from {str(address)}")

        try:
            # Asks for username from client and assigns username
            connection.send("USERNAMEREQUEST".encode(utf8))
            username = connection.recv(1024).decode(utf8)
            print(f"SERVER GOT USERNAME: *{username}*")
            client = Client()   # creates a Client object for the new client and adds attributes
            client.connection = connection
            client.username = username
            clients_list.append(client)  # adds new client to the list of connected clients
            print(f"{client.username} connected!")

            # broadcasts to all connected clients about the new joined client
            send_to_clients(server_username, f"{client.username} joined the server")

            # generating a new thread for all new connected clients
            # to be able to listen for new messages from all clients simultaneously
            client_thread = threading.Thread(target=receive_from_clients, args=(client,))
            client_thread.start()
        except:
            connection.close()
            print(f"Unable to reach attempted connection: {address}")


# function to continuously listen for new messages from given client
# intended to be run by each thread for each connected client
def receive_from_clients(client):
    while True:
        try:
            message = client.connection.recv(1024).decode(utf8)
            print(f"Message received from {client.username}: ^{message}^")
            send_to_clients(client.username, message)
            sys.exit("Done sending message. Now exit")
        except:
            print(f"Error in receiving from {client.username}. Disconnecting client ...")
            client.connection.close()  # closes connection if unable to receive from client
            clients_list.remove(client)  # removes client from list of connected clients

            # announces the disconnect to all remaining connected clients
            send_to_clients(server_username, f"{client.username} disconnected")
            print_clients()  # prints list of remaining connected clients
            break


# Function to broadcast new messages to all connected clients
def send_to_clients(sender, message):
    print("Sending now...")
    output_string = str(sender) + ": " + str(message)
    print("Output string: " + output_string)
    for client in clients_list:
        print(f"Going to send ^{message}^ to {client.username}")
        if client.username != sender:
            client.connection.send(output_string.encode(utf8))


# function to print usernames of all connected clients to console
def print_clients():
    all_client_usernames = "Remaining clients usernames: "
    for client in clients_list:
        all_client_usernames += (client.username + " ")
    print(all_client_usernames)


# function to construct and assemble a random request. Verb can be user input
def construct_action_request(user_input):
    # lists of predetermined sentences and actions
    sentence_list = ["Does anyone want to {}?", "Who's up for some {}ing?", "Let's {}!", "{}ing. Yay or nay?"]
    action_list = bots.action_list
    output_string = random.choice(sentence_list)  # picks a random sentence

    if user_input == "":    # without user input
        output_string = output_string.format(random.choice(action_list))
    else:                   # with user input
        output_string = output_string.format(user_input)
    return output_string


def user_input_send_action_request():
    while True:
        user_input = input("Press 'ENTER' to send random action request OR type your own action ...\n")
        send_to_clients(server_username, construct_action_request(user_input))


user_input_thread = threading.Thread(target=user_input_send_action_request)
user_input_thread.start()

# initiates the server by starting the listening-loop
listen_for_clients()

