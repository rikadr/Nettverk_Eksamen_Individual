import random

#####################################################################################
# Start: Bots

# list of known actions
action_list = ["clean", "fight", "cook", "fish", "sing", "relax", "cheat", "ski", "talk", "shit", "listen", "eat",
               "sleep", "fuck"]


def extract_actions(raw_message):
    if raw_message is None:
        return None

    message_lowercase = raw_message.lower()
    actions = []

    for action in action_list:  # for every known action
        if action in message_lowercase:  # check if known action is mentioned in message
            actions.append(action)  # adds action if known action is found mentioned in message

    return actions  # returns list of found known actions


def bot_peder(actions):
    name = "Peder"
    if actions is None:
        return name

    action_count = len(actions)
    reply_0_actions = ["Don't really wanna do that.",
         "Lame! Would much rather {}".format(random.choice(action_list)),
         "What did you suggest just now?!",
         "Do not expect to see me there...",
         "I can think of {} better things to do".format(random.randrange(0, 100)),
         "Even {}-{}ing sounds more fun".format(random.choice(action_list), random.choice(action_list))]

    if action_count >= 1:
        reply_1_action = ["Of all things to do in this world you really want to "
                          "do some stupid {}ing?".format(actions[0]),
                          "I'll think about it. {}ing isn't really my thing ...".format(random.choice(actions)),
                          "I'm down to {} if you give me ${}".format(random.choice(actions), random.randrange(1, 1500))]

    if action_count >= 2:
        reply_multiple_actions = ["Make your mind up, {} or {}?".format(actions[1], actions[0]),
                            "How about some {}-{}ing?".format(random.choice(actions), random.choice(action_list)),
                            "You can go {} and i'll go {}".format(random.choice(actions), random.choice(action_list)),
                            "You can go {} and i'll go {}".format(actions[0], actions[1])]

    if action_count == 0:
        return random.choice(reply_0_actions)

    elif action_count == 1:
        return random.choice([random.choice(reply_0_actions), random.choice(reply_1_action)])

    elif action_count >= 2:
        return random.choice([random.choice(reply_0_actions), random.choice(reply_1_action),
                             random.choice(reply_multiple_actions)])
    else:
        return "Unknown action count"


def bot_fredrik(actions):
    name = "Fredrik"
    if actions is None:
        return name

    reply_0_actions = ["Have not tried that before, but im down to try it!", "Alright, let's do it"]
    reply_multiple_actions = ["OK, {}ing it is!".format(random.choice(actions)),
                              "I LOVE {}ing".format(random.choice(actions))]
    return random.choice([random.choice(reply_0_actions), random.choice(reply_multiple_actions)])


def bot_rikard(actions):
    name = "Rikard"
    if actions is None:
        return name

    reply_0_actions = ["How about next week?",
                       "Sorry, can't. Have spent {} hours gaming, "
                       "need to catch up on school".format(random.randrange(1, 100))]
    reply_multiple_actions = ["... {}ing is more fun".format(random.choice(action_list)),
                              "{}ing is cool and all, but have you tried {}?!"
                              .format(random.choice(actions), random.choice(action_list))]
    return random.choice([random.choice(reply_0_actions), random.choice(reply_multiple_actions)])


def bot_maren(actions):
    name = "Maren"
    if actions is None:
        return name
    return random.choice(["No", "Nah", "Never", "Next year maybe", "Why am i even in this chat?"])


def run_bot(message, bot_id, get_usernames):
    actions = extract_actions(message)  # extract actions from message
    # a switch case to run the correct bot function based on selected bot_ID
    switcher = {
        1: lambda: bot_peder(actions),
        2: lambda: bot_fredrik(actions),
        3: lambda: bot_rikard(actions),
        4: lambda: bot_maren(actions)
    }

    # code to return all bot usernames if boolean get_usernames is true
    if get_usernames:
        bot_username_list = []  # prepares list to append all usernames
        i = 1
        while True:  # runs through all switch functions.
            try:
                bot_username_list.append(switcher.get(i, )())  # runs bot-functions with no parameter to get username
                i += 1
            except:
                break  # stops when through all switch cases.
        return bot_username_list

    if message is None:
        actions = None
        return switcher.get(bot_id, )()

    actions = extract_actions(message)

    # runs chosen lambda function, returns username from bot function
    return switcher.get(bot_id, )()

# End: Bots
#####################################################################################
