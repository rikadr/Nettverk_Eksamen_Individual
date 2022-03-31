import socket
import threading
import random
import bots

#####################################################################################
# Start: Setup

utf8 = "utf-8"
server_username = "*Server*"
ip = "127.0.0.21"
port = 7996

s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Creating a TCP/IP socket
s_socket.bind((ip, port))                                       # binds the ip address and port
s_socket.listen()                                               # Have the server listen for client connections

clients_list = []                                               # A list to hold the client objects


# A class to hold the client connection and username
class Client:
    """A class to hold the client connection and username"""
    connection = None
    username = None


# End: Setup
#####################################################################################
# Start: Receiving/Sending

# Function to continuously listen for new client connections
def listen_for_clients():
    while True:
        connection, address = s_socket.accept()                 # wait for a new connecting client and accept

        try:  # Asks for username from client and assigns username
            connection.send("USERNAMEREQUEST".encode(utf8))
            username = connection.recv(1024).decode(utf8)
            client = Client()                                   # creates a Client object for the new client
            client.connection = connection                      # adds the attributes to object
            client.username = username
            clients_list.append(client)                         # adds new client to the list of connected clients
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
            if message != "":
                send_to_clients(client.username, message)
            else:
                print("Empty message, not sending")
                exit()
        except:
            print(f"Error in receiving from {client.username}. Disconnecting client ...")
            client.connection.close()                           # closes connection if unable to receive from client
            clients_list.remove(client)                         # removes client from list of connected clients

            # announces the disconnect to all remaining connected clients
            send_to_clients(server_username, f"{client.username} disconnected")
            print_clients()                                     # prints list of remaining connected clients
            break


# Function to broadcast new messages to all connected clients
def send_to_clients(sender, message):
    output_string = str(sender) + ": " + str(message)
    print(output_string)
    for client in clients_list:

        if client.username != sender:
            client.connection.send(output_string.encode(utf8))


# End: Receiving/Sending
#####################################################################################
# Start: User input send message with action

# function to print usernames of all connected clients
def print_clients():
    all_client_usernames = "Remaining clients usernames: "
    for client in clients_list:
        all_client_usernames += (client.username + " ")
    print(all_client_usernames)


# function to construct and assemble a random request. Verb can be user input
def construct_action_request(user_input):
    # lists of sentences
    sentence_list = ["Does anyone want to {}?", "Who's up for some {}ing?", "Let's {}!", "{}ing. Yay or nay?"]
    action_list = bots.action_list                              # gets list of defined actions from bots.py
    output_string = random.choice(sentence_list)                # picks a random sentence

    if user_input == "":                                        # without user input
        output_string = output_string.format(random.choice(action_list))
        return output_string

    try:
        if 4 >= int(user_input) >= 2:                           # without user input number between 2 and 4
            action_chain = ""                                   # prepares string to add all actions to
            for i in range(int(user_input)):
                action_chain += random.choice(action_list)
                if i < (int(user_input) - 2):                   # formats actions with ", " and " or "
                    action_chain += ", "
                elif i == (int(user_input) - 2):
                    action_chain += " or "

            output_string = output_string.format(action_chain)
            return output_string

        else:                                                   # if number is not between 2 and 4
            output_string = output_string.format(random.choice(action_list))

    except:
        output_string = output_string.format(user_input)        # with user input string

    return output_string


def user_input_send_action_request():
    # initial user instructions:
    print("Press 'ENTER' to send random action request OR type your own action\n"
          "Type 1 ... 4 to suggest 1 ... 4 random actions.\n")
    while True:
        user_input = input("")
        send_to_clients(server_username, construct_action_request(user_input))


user_input_thread = threading.Thread(target=user_input_send_action_request)
user_input_thread.start()

# End: User input send message with action
#####################################################################################

listen_for_clients()                                            # initiates the server by starting the listening-loop
