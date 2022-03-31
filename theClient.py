import socket
import threading
import bots
import sys

#####################################################################################
# Start: Setup

utf8 = "utf-8"                                                  # defining encoding standard
IP = "127.0.0.21"                                              # getting IP and PORT from Server to ensure they ...
PORT = 7996                                     # ... are the same
print("Auto setup")

c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # creating client socket

# tries to connect, exits if unable to connect
try:
    c_socket.connect((IP, PORT))
    print("Connection successful!")
except:
    sys.exit("Unable to connect")


# End: Setup
#####################################################################################
# Start: Bot choice

# getting the list of all available bots from the bots.py file
bot_username_list = bots.run_bot(None, None, True)
client_is_bot = None                                            # currently unknown

while True:  # Loop to request bot choice
    bot_list_output = "Available bots: 0=[Manual input] "       # String to add all bot names to
    for idx, item in enumerate(bot_username_list):
        bot_list_output += f"{idx + 1}={item}  "                # adds each bot name to string

    while True:
        try:
            print(bot_list_output)
            bot_ID = int(input("Choose bot number > "))         # asks for bot name input
            break
        except:
            print("Not valid input. Only numbers please. Try again.\n")

    if len(bot_username_list) > bot_ID - 1 >= 0:                # checks if input is within range of bots
        print(f"You selected bot {bot_ID}: {bot_username_list[bot_ID - 1]}")
        client_is_bot = True
        break                                                   # stops loop after a bot is chosen
    elif bot_ID == 0:
        client_is_bot = False                                   # If input is 0 client is not set as a bot
        break                                                   # stops loop when manual input is chosen

    # Prints if user input is not valid
    print(f"{str(bot_ID)} is not an available choice. Please try again.\n")

# End: Bot choice
#####################################################################################
# Start: Sending/Receiving


def receive_from_server(client_username):
    while True:
        try:
            message = c_socket.recv(1024).decode(utf8)

            if message == "USERNAMEREQUEST":                    # If received message is a username request
                send_to_server(client_username)
            else:                                               # If received message is a normal message
                print(message)
                # replies to message if client is a bot and sender is not a bot
                if client_is_bot and check_to_reply(message):
                    bot_reply_message = bots.run_bot(message, bot_ID, False)    # prepares reply string
                    send_to_server(bot_reply_message)           # sends message to server
                    print(f"You: {bot_reply_message}")


        except:
            print("An error occured! You disconnected from the server")
            c_socket.close()
            break


def type_message():
    while True:
        message = input("")                                     # waits for input from the user
        send_to_server(message)                                 # sends user input as a message to server


def send_to_server(message):
    c_socket.send(message.encode(utf8))


# End: Sending/Receiving
#####################################################################################
# Start: Program ...

def check_to_reply(message):
    try:
        if "joined the server" in message:                      # bots will not respond to someone joining the server
            return False

        for name in bot_username_list:
            if name in message:
                return False                                    # False means bot should not reply
        return True                                             # True means bot should reply

    except:
        print("Failed to check for names")
        return False


# Defining username
if client_is_bot:
    username = bot_username_list[bot_ID - 1]                    # gets username of chosen bot from list
else:
    username = input("Type your username: ")                    # asks input for username if manual input is chosen

# receiving messages with following thread
receive_from_server_thread = threading.Thread(target=receive_from_server, args=(username,))
receive_from_server_thread.start()

# Taking input for messages with following thread if client is not set at a bot
if not client_is_bot:
    type_message_thread = threading.Thread(target=type_message)
    type_message_thread.start()
