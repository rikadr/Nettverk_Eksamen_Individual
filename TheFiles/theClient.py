import socket
import threading
import argparse
import random
import sys

# The help documentation
# DESCRIPTION
# parser = argparse.ArgumentParser(description="This chat client connects to a chat server and "
#                                             "lets a bot of your choosing reply to messages in the chat. It takes"
#                                             "three command line parameters: IP, PORT and BOT.")
# parser.add_argument('IP', type=str, help="The IP address you want to connect to.")  # IP parameter
# parser.add_argument('PORT', type=str, help="The PORT you want to connect to.")      # PORT parameter
# parser.add_argument('BOT', type=str, help="The BOT you want to run.")               # BOT parameter
# args = parser.parse_args()

#####################################################################################
# Start: Setup

# defining encoding standard
utf8 = "utf-8"

if input("Setup mode: (0) Normal, (1) Auto") == "1":
    print("Auto setup")
    IP = "127.0.0.1"
    PORT = 7976
else:
    print("Manual Setup")
    # Getting command line parameters
    IP = input("What IP do you want to connect to? > ")
    PORT = input("At what port? > ")
    print(f"{IP}:{PORT} confirmed\n")

# creating client socket
c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# tries to connect, exits if unable to connect
try:
    c_socket.connect((IP, PORT))
    print("Connection successful!")
except:
    sys.exit("Unable to connect")


# End: Setup
#####################################################################################
# Start: Bot choice

bots = ["Peder", "Fredrik", "Rikard", "Maren"]  # List of available bots to choose from
client_is_bot = True

while True:  # Loop to request bot choice
    botList = "0=[Manual input] \nAvailable bots: "    # String to add all bot names to
    for idx, item in enumerate(bots):
        botList += f"{idx + 1}={item}  "    # adds each bot name to string

    while True:
        try:
            print(botList)
            bot_ID = int(input("Choose bot number > "))  # asks for bot name input
            break
        except:
            print("Not valid input. Only numbers please. Try again.\n")

    if len(bots) > bot_ID - 1 >= 0:  # checks if input is within range of bots
        print(f"You selected bot {bot_ID}: {bots[bot_ID - 1]}")
        break  # stops loop after a bot is chosen
    elif bot_ID == 0:
        client_is_bot = False  # If input is 0 client is not set as a bot
        break  # stops loop when manual input is chosen

    # Prints if user input is not valid
    print(f"{str(bot_ID)} is not an available choice. Please try again.\n")

# End: Bot choice
#####################################################################################
# Start: Sending/Receiving


def receive_from_server(username):
    print("Recieving now <<<")
    while True:
        try:
            message = c_socket.recv(1024).decode(utf8)
            if message == "USERNAMEREQUEST":
                print("SENDING USERNAME")
                c_socket.send(username.encode(utf8))
            else:
                print(message)

        except:
            sys.exit("Unable to receive from server")


def type_message():
    while True:
        message = input("")
        send_to_server(message)


def send_to_server(message):
    print(f"Sending {message} now >>>")
    c_socket.send(message.encode(utf8))


# End: Sending/Receiving
#####################################################################################
# Start: Bots

action_list = ["clean", "fight", "cook", "fish", "sing", "relax", "cheat", "ski", "talk", "shit", "listen", "eat",
               "sleep", "fuck", "fuck", "fuck", "fuck", "fuck", "fuck", "fuck", "fuck", "fuck", "fuck"]


def extract_actions(raw_message):
    print(f"in extract_actions {raw_message}")
    return raw_message


def bot_peder(actions):
    name = "Peder"
    if actions is None:
        return name

    print(f"Now running bot: {name}")
    action_count = len(actions)
    print("Number og actions received: " + str(action_count))

    reply_0_actions = ["Don't really wanna do that.",
                       "Lame! Would much rather {}".format(random.choice(action_list)),
                       "What did you suggest just now?!",
                       "Do not expect to see me there...",
                       "I can think of {} better things to do".format(random.randrange(0, 100)),
                       "Even {}-{}ing sounds more fun".format(random.choice(action_list), random.choice(action_list))]

    reply_1_action = ["Of all things to do in this world you really want to do some stupid {}ing?".format(actions[0]),
                      "I'll think about it. {}ing isn't really my thing ...".format(random.choice(actions)),
                      "I'm down to {} if you give me ${}".format(random.choice(actions), random.randrange(1, 1500))]

    reply_multiple_actions = ["Make your mind up, {} or {}?".format(actions[1], actions[0]),
                              "How about some {}-{}ing?".format(random.choice(actions), random.choice(action_list)),
                              "You can go {} and i'll go {}".format(random.choice(actions), random.choice(action_list)),
                              "You can go {} and i'll go {}".format(actions[0], actions[1])]

    if action_count == 0:
        print("0 actions")
        print(random.choice(reply_0_actions))

    elif action_count == 1:
        print("1 actions")
        print(random.choice([random.choice(reply_0_actions), random.choice(reply_1_action)]))

    elif action_count >= 2:
        print("2 or more actions")
        print(random.choice([random.choice(reply_0_actions), random.choice(reply_1_action),
                             random.choice(reply_multiple_actions)]))

    else:
        print("Unknown action count")


def bot_fredrik(actions):
    name = "Fredrik"
    if actions is None:
        return name
    print("Bot is fredrik hallo")


def bot_rikard(actions):
    name = "Rikard"
    if actions is None:
        return name
    print("Bot is rikard hallo")


def bot_maren(actions):
    name = "Maren"
    if actions is None:
        return name
    print("Bot is maren hallo")


def bot_default():
    print("Unable to run selected bot. Default bot is id 1, starting now...")
    run_bot(1)


def run_bot(message):
    actions = extract_actions(message)

    # a switch case to run the correct bot function based on selected bot_ID
    switcher = {
        1: lambda: bot_peder(actions),
        2: lambda: bot_fredrik(actions),
        3: lambda: bot_rikard(actions),
        4: lambda: bot_maren(actions)
    }
    # runs chosen lambda function, returns username from bot function
    return switcher.get(bot_ID, lambda: bot_default())()

# End: Bots
#####################################################################################
# Start: Program ...


# Defining username and retrieving it if from a bot
get_username = ""
if client_is_bot:
    get_username = run_bot(None)    # returns username of chosen bot
else:
    get_username = input("Type your username: ")    # asks input for username if manual input is chosen


# receiving messages with following thread
receive_from_server_thread = threading.Thread(target=receive_from_server, args=(get_username,))
receive_from_server_thread.start()

# Taking input for messages with following thread if client is not set at a bot
if not client_is_bot:
    type_message_thread = threading.Thread(target=type_message)
    type_message_thread.start()

print("ALL THROUGH")
# run_bot([random.choice(action_list), random.choice(action_list), random.choice(action_list)])



