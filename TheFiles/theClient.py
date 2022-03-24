import socket
import threading
import argparse
import random

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

setupMode = input("Setup mode: (0) Normal, (1) Auto")

if setupMode == "1":
    print("Auto setup")
    IP = "127.0.0.1"
    PORT = 7976
elif setupMode == "0":
    print("Manual Setup")
    # Getting command line parameters
    IP = input("What IP do you want to connect to? > ")
    PORT = input("At what port? > ")
    print(f"{IP}:{PORT} confirmed\n")
else:
    print("No Setup")

bots = ["Peder", "Fredrik", "Rikard", "Maren"]  # List of available bots to choose from

while True:  # Loop to request bot choice
    botList = "Available bots: "    # String to add all bot names to
    for idx, item in enumerate(bots):
        botList += f"{idx + 1}={item}  "    # adds each bot name to string
    print(botList)

    bot_ID = int(input("Choose bot number > "))  # asks for bot name input
    if len(bots) > bot_ID - 1 >= 0:  # checks if input is within range of bots
        print(f"You selected bot {bot_ID}: {bots[bot_ID - 1]}")
        break  # stops loop after a bot is chosen

    # Prints if user input is not valid
    print(f"{str(bot_ID)} is not an available choice. Please try again.\n")

# End: Setup
#####################################################################################
# Start: Sending/Receiving


def recieve_from_server():
    print("Recieving now <<<")

    # if recieve "USERNAME?":
        # send_to_server(username)


def send_to_server(message):
    print(f"Sending {message} now >>>")


# End: Sending/Receiving
#####################################################################################
# Bots

action_list = ["clean", "fight", "cook", "fish", "sing", "relax", "cheat", "ski", "talk", "shit", "listen", "eat",
               "sleep", "fuck", "fuck", "fuck", "fuck", "fuck", "fuck", "fuck", "fuck", "fuck", "fuck"]


def bot_peder(actions):
    name = "Peder"
    print(f"Now running bot: {name}")
    action_count = len(actions)
    print("Number og actions recieved: " + str(action_count))

    reply_0 = ["Don't really wanna do that.",
               "Lame! Would much rather {}".format(random.choice(action_list)),
               "What did you suggest just now?!",
               "Do not expect to see me there...",
               "I can think of {} better things to do".format(random.randrange(0, 100)),
               "Even {}-{}ing sounds more fun".format(random.choice(action_list), random.choice(action_list))]

    reply_1 = ["Of all the things to do in this world you really want to do some stupid {}ing?".format(actions[0]),
               "I'll think about it. {}ing isn't really my thing ...".format(random.choice(actions)),
               "I'm down to {} if you give me ${}".format(random.choice(actions), random.randrange(1, 1500))]

    reply_2 = ["Make your mind up, {} or {}?".format(actions[1], actions[0]),
               "How about some {}-{}ing?".format(random.choice(actions), random.choice(action_list)),
               "You can go {} and i'll go {}".format(random.choice(actions), random.choice(action_list)),
               "You can go {} and i'll go {}".format(actions[0], actions[1])]

    if action_count == 0:
        print("0 actions")
        print(random.choice(reply_0))

    elif action_count == 1:
        print("1 actions")
        print(random.choice([random.choice(reply_0), random.choice(reply_1)]))

    elif action_count >= 2:
        print("2 or more actions")
        print(random.choice([random.choice(reply_0), random.choice(reply_1), random.choice(reply_2)]))

    else:
        print("Unknown action count")


def bot_fredrik(actions):
    print("Bot is fredrik hallo")


def bot_rikard(actions):
    print("Bot is rikard hallo")


def bot_maren(actions):
    print("Bot is maren hallo")


def bot_default():
    print("Unable to run selected bot. Default bot is id 1, starting now...")
    run_bot(1)


def run_bot(actions):
    # a switch case to run the correct bot function based on selected bot_ID
    switcher = {
        1: lambda: bot_peder(actions),
        2: lambda: bot_fredrik(actions),
        3: lambda: bot_rikard(actions),
        4: lambda: bot_maren(actions)
    }
    switcher.get(bot_ID, lambda: bot_default())()

# End: Bots
#####################################################################################
# Start: Program ...


run_bot([random.choice(action_list), random.choice(action_list), random.choice(action_list)])



