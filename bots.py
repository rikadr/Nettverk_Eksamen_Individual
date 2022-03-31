import random

#####################################################################################
# Start: Setup

# list of known actions
action_list = ["clean", "fight", "cook", "fish", "sing", "relax", "cheat", "ski", "talk", "listen", "eat", "sleep"]
# End: Setup
#####################################################################################
# Start: Bots


def bot_peder(actions):
    name = "Peder"
    if actions is None:                                         # returns name if actions is None
        return name

    action_count = len(actions)
    reply_sentences = []

    reply_0_actions = ["Don't really wanna do that.",
         "Lame! Would much rather {}".format(random.choice(action_list)),
         "What did you suggest just now?!",
         "Do not expect to see me there...",
         "I can think of {} better things to do".format(random.randrange(0, 100)),
         "Even {}-{}ing sounds more fun".format(random.choice(action_list), random.choice(action_list))]
    for reply in reply_0_actions:
        reply_sentences.append(reply)

    if action_count >= 1:
        reply_1_action = ["Of all things to do in this world you really want to "
                          "do some stupid {}ing?".format(actions[0]),
                          "I'll think about it. {}ing isn't really my thing ...".format(random.choice(actions)),
                          "I'm down to {} if you give me ${}".format(random.choice(actions), random.randrange(1, 1500))]
        for reply in reply_1_action:
            reply_sentences.append(reply)

    if action_count >= 2:
        reply_multiple_actions = ["Make your mind up, {} or {}?".format(actions[1], actions[0]),
                            "How about some {}-{}ing?".format(random.choice(actions), random.choice(action_list)),
                            "You can go {} and i'll go {}".format(random.choice(actions), random.choice(action_list)),
                            "You can go {} and i'll go {}".format(actions[0], actions[1])]
        for reply in reply_multiple_actions:
            reply_sentences.append(reply)

    return random.choice(reply_sentences)


def bot_fredrik(actions):
    name = "Fredrik"
    if actions is None:                                         # returns name if actions is None
        return name

    reply_0_actions = ["Have not tried that before, but im down to try it!", "Alright, let's do it"]

    if len(actions) > 0:
        reply_multiple_actions = ["OK, {}ing it is!".format(random.choice(actions)),
                                  "I LOVE {}ing".format(random.choice(actions))]
        return random.choice([random.choice(reply_0_actions), random.choice(reply_multiple_actions)])
    return random.choice(reply_0_actions)


def bot_rikard(actions):
    name = "Rikard"
    if actions is None:                                         # returns name if actions is None
        return name

    reply_0_actions = ["How about next week?",
                       "Sorry, can't. Have spent {} hours gaming, "
                       "need to catch up on school".format(random.randrange(1, 100))]

    if len(actions) > 0:
        reply_multiple_actions = ["... {}ing is more fun".format(random.choice(action_list)),
                                  "{}ing is cool and all, but have you tried {}?!"
                                  .format(random.choice(actions), random.choice(action_list))]
        return random.choice([random.choice(reply_0_actions), random.choice(reply_multiple_actions)])
    return random.choice(reply_0_actions)


def bot_maren(actions):
    name = "Maren"
    if actions is None:                                         # returns name if actions is None
        return name

    return random.choice(["No", "Nah", "Never", "Next year maybe", "Why am I even in this chat?"])


# End: Bots
#####################################################################################
# Start: Functions

def extract_actions(raw_message):
    if raw_message is None:
        return None

    message_lowercase = raw_message.lower()                     # sets all characters to lowercase to match action_list
    actions = []                                                # prepares list to add matches to and return

    for action in action_list:                                  # for every known action
        if action in message_lowercase:                         # check if known action is mentioned in message
            actions.append(action)                              # adds action if found mentioned in message
    return actions                                              # returns list of found known actions


def run_bot(message, bot_id, get_usernames):
    actions = extract_actions(message)                          # extract actions from message
    # a switch case to run the correct bot function based on selected bot_ID
    switcher = {
        1: lambda: bot_peder(actions),
        2: lambda: bot_fredrik(actions),
        3: lambda: bot_rikard(actions),
        4: lambda: bot_maren(actions)
    }

    # code to return all bot usernames if boolean get_usernames is true
    if get_usernames:
        bot_username_list = []                                  # prepares list to append all usernames
        for idx, lam in enumerate(switcher):                    # runs through all switch functions.
            bot_username_list.append(switcher.get(idx + 1, )())  # runs bot functions with no parameter to get username
        return bot_username_list

    return switcher.get(bot_id, )()                             # runs chosen bot, returns generated reply string

# End: Functions
#####################################################################################
