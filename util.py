import discord
import random
import praw
import config
import pymysql

#sql database login
DB_IP="localhost"
DB_USER="root"
DB_PASSWORD="password"
DB_NAME="grizzo"

#arrays for loading data
BAD_WORDS = []
arrayWords=[]
arrayPinned =[]
arrayCensoredWords =[]

guildID=discord.Guild.id

# reddit = praw.Reddit(client_id=config.REDDIT_ID, client_secret=config.REDDIT_SECRET,user_agent=config.USER_AGENT)

# multireddit = 'memes'
# sub = reddit.subreddit(multireddit)


def dice_roller(ctx, arg):
    # contents = arg.content[len("!r"):]
    contents = arg.lower()  # make the contents of the argument lowercase
    # word_list = contents.split(" ")

    output = ctx.author.mention  # Start output with user name
    output += " `" + contents.replace(" ", "") + "` "  # Add the arguments to the output
    summation = 0  # Establish a sum  counter track the sum of the rolls
    # for word in word_list:
    roll_word = contents.split('d')  # Split argument into two parts at the d
    if len(roll_word) > 1:  # If there are more than one components
        output += "("
        for x in range(0, int(roll_word[0])):  # Loop it based on the number of dice
            rand_int = random.randint(1, int(roll_word[1]))  # Create a random integer based on the number of sides
            output += str(rand_int)  # Add the roll to the output addition section
            if x is not int(roll_word[0]) - 1:  # Add a + if we are not at the end of the loop
                output += ' + '
            summation += rand_int  # Add the new int to the total sum
        output += ") "
    else:
        if roll_word[0].isdigit() is True:
            output = output.strip()
            output += ' + ' + str(roll_word[0])
            summation += int(roll_word[0])
    output += " = " + str(summation)  # Add the sum to the output string
    return output


def test(ctx):
    output = "test1234"
    return output


# def meme(ctx):
# post = sub.random()
# msg = "{}\nSource: {}".format(post.url, post.permalink)
# return msg

# define function for creating initial vote
def vote_start(question, choices_arr, emojis):
    print("Vote is being made...")

    # create embed
    vote_announce = discord.Embed(title="Time for a vote!")
    vote_announce.add_field(name="Question", value=question)  # add question field to embed

    # assign emojis to choices as a string and add to embed
    choices_string = ""
    i = 0
    while i < len(choices_arr):  # until all choices have been assigned
        choices_string += (emojis[i] + "" + choices_arr[i] + "\n")
        i += 1  # concatenate string that will be displayed in embed
    vote_announce.add_field(name="Choices", value=choices_string)

    # return embedded vote announcement
    return vote_announce


# define function for counting the votes
def tally_up(question, choices_arr, message):
    vote_string = "vote"  # singular or plural amount of votes?
    tie_flag = 0  # was there a tie?

    # tally dictionary
    tallies = {react.emoji: react.count for react in message.reactions}

    # check for a tie
    tallies_sorted = sorted(tallies.values(), reverse=True)  # sort highest numbers
    if tallies_sorted[0] != tallies_sorted[1]:  # if there is only one maximum, find the winner
        winner_count = max(tallies.values()) - 1  # assign winner count
        winner_emoji = max(tallies, key=tallies.get)  # assign winner emoji

        winner = choices_arr[list(tallies.keys()).index(winner_emoji)]  # assign winner using the index of winner_emoji

        # if more than one vote or no votes, change string to votes
        if winner_count > 1 or winner_count == 0:  #
            vote_string = "votes"

    else:  # there's a tie
        tie_flag = 1

    vote_winner = discord.Embed(title="We have a winner!")
    if tie_flag == 0:  # add field based on whether there's a tie or not
        vote_winner.add_field(name="And your winner is...", value=
        "__**" + winner + "**__ (" + winner_emoji + ")" +
        " with __**" + str(winner_count) + "**__ " + vote_string + "!")
    else:
        vote_winner.add_field(name="And your winner is...", value=
        "No one! It's a tie!")

    return vote_winner


# define function for pulling a certain amount of messages
def pull(ctx, message_list, num):  # context, channel, number of messages
    random.shuffle(message_list)  # randomize message list
    message_list = message_list[0:num]  # strip to number of inputted messages

    pulled_messages_string = ""  # string to place in embed
    for message in message_list:
        pulled_messages_string += message + "\n"  # concatenate messages

    # create embed
    pulled_messages_embed = discord.Embed(title=None)
    pulled_messages_embed.add_field(name="Messages:", value=pulled_messages_string)

    return pulled_messages_embed


def cmd_help(prefix):
    output = prefix
    output += "\nCommand: test ---- Arguments: None. ---- Function: Sends a test post."
    output += "\nCommand: roll or r ---- Arguments: XdY. X = # of dice, Y = # or sides per die. ---- Function: rolls " \
              "dice."
    output += "\nCommand: meme ---- Arguments: None. ---- Function: Posts a meme from Redit."
    output += "\nCommand: join or j ---- Arguments: None. ---- Function: Joins current voice channel of the author of" \
              " the command."
    output += "\nCommand: disconnect or d ---- Arguments: None. ---- Function: Disconnects from voice."
    output += "\nCommand: youtube, yt, or y ---- Arguments: Youtube search query. ---- Function: Plays audio to a" \
              " voice channel."
    output += "\nCommand: volume or v ---- Arguments: Number between 0 and 1. ---- Function: Changes bot audio volume."
    output += "\nCommand: censor or censorword ---- Arguments: a word to censor. ---- Function: censors a word from the chat channel."
    output += "\nCommand: uncensor or uncensorword ---- Arguments: a word to uncensor. ---- Function: removes word from the censor list."
    output += "\nCommand: censorlist or listcensors ---- Arguments: none. ---- Function: displays all censored words."
    output += "\nCommand: pins or pinnedlist ---- Arguments: none. ---- Function: shows all items pinned by gizzo."
    output += "\nTo pin messages in chat, add a 📌 reaction to the message ---- Function: pins message to view later"
    return output


def npc(ctx):
    strength = [random.randint(1, 6) for _ in range(4)]  # creates array with 4 random numbers
    strength.sort()  # sorts array
    a = strength[1] + strength[2] + strength[3]  # adds 3 highest values

    dex = [random.randint(1, 6) for _ in range(4)]
    dex.sort()
    b = dex[1] + dex[2] + dex[3]

    constitution = [random.randint(1, 6) for _ in range(4)]
    constitution.sort()
    c = constitution[1] + constitution[2] + constitution[3]

    intellligence = [random.randint(1, 6) for _ in range(4)]
    intellligence.sort()
    d = intellligence[1] + intellligence[2] + intellligence[3]

    wisdom = [random.randint(1, 6) for _ in range(4)]
    wisdom.sort()
    e = wisdom[1] + wisdom[2] + wisdom[3]

    charisma = [random.randint(1, 6) for _ in range(4)]
    wisdom.sort()
    f = charisma[1] + charisma[2] + charisma[3]

    output = "Strength: " + str(a) + "\nDexterity: " + str(b) + "\nConstitution: " + str(c) + "\nIntelligence: " + str(
        d) + "\nWisdom: " + str(e) + "\nCharisma: " + str(f)
    return output

#sql
# loads words into system from database
def getWords():
    # Open database connection
    db = pymysql.connect(DB_IP, DB_USER, DB_PASSWORD, DB_NAME)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute("SELECT word FROM words WHERE serverID= '" + guildID + "';")

    # Fetch a all rows using fetchall() method.
    BAD_WORDS = list(cursor.fetchall())

    # loads words from list to array
    for i in BAD_WORDS:
        arrayWords.append(i[-1])
        # print(i[-1])
    # print (BAD_WORDS)
    print(arrayWords)

    # disconnect from server
    db.commit()
    db.close()

#sql
# check chack if value is in selected table and column
"""
def has_value(table, column, value):
    # Open database connection
    db = pymysql.connect(DB_IP, DB_USER, DB_PASSWORD, DB_NAME)
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute("SELECT " + column + " from " + table + " WHERE " + column + " = '" + value + "' LIMIT 1")
    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    # print (data)
    db.commit()
    db.close()
    return data is not None
"""

#profanity filter
def censorword(phrase, message):
    phrase=phrase.lower()
    phrase+=""
    output=""
    #sql
    #if has_value("words", "word", phrase):
    if phrase in arrayCensoredWords:
        output=('{}, {} is already censored.'.format(message.author.mention, phrase))
    else:
        #sql
        #DBQuery("INSERT INTO words(words.serverID, word) VALUES('"+GUILD+"','"+phrase+"');")
        arrayCensoredWords.append(phrase)
        output=('{}, has added "{}" to the censoring list'.format(message.author.mention, phrase))
        print("Censoring: "+phrase)
        #sql
        #getWords()
    return output

#profanity filter
def uncensorword(phrase, message):
    phrase=phrase.lower()
    phrase+=""
    output=""
    #sql
    #if has_value("words", "word", phrase):
    if phrase not in arrayCensoredWords:
        output=('{}, {} is not censored.'.format(message.author.mention, phrase))
    else:
        #sql
        #DBQuery("DELETE FROM words WHERE word='"+badWord+"';")
        arrayCensoredWords.remove(phrase)
        output=('{}, has uncensored "{}"'.format(message.author.mention, phrase))
        print("Uncensoring: "+phrase)
        #sql
        #getWords()
    return output

"""
async def filter(message):
    output=""
    for x in arrayCensoredWords:
        # print("List of censored words:")
        if x in message.content.strip().lower():
            #await message.channel.send('{}, your message has been censored.'.format(message.author.mention))
            output='{}, your message has been censored.'.format(message.author.mention)
            await message.delete()
            print(x)
            break
    return output"""

# profanity filter
def censorlist(message):
    if not arrayCensoredWords:
        return '{}, Nothing is censored yet.'.format(message.author.mention)
    arrayCensoredWords.sort()
    censoredwords = ""
    for x in arrayCensoredWords:
        if arrayCensoredWords.index(x)>0:
            censoredwords+= "\t|\t "
        censoredwords += x +""
    output='{}, Here is the list of censored words: \n{}'.format(message.author.mention, censoredwords)
    return output

#display pins
def pins(message):
    output = message.author.mention+", pinned messages: (date in UTC)"
    for i in range(len(arrayPinned)):
        output+="\n"+str(i)+": "+arrayPinned[i][0].message.author.name+" "+arrayPinned[i][0].message.created_at.strftime("%m-%d-%Y %I:%M %p") +", 📌 by "+ arrayPinned[i][1].name+\
                "\n"+arrayPinned[i][0].message.content+"\n"
    return output

def unpin(message, id):
    output=""
    print(int(id))
    #sql
    #if has_value("words", "word", phrase):
    if int(id)>len(arrayPinned) or int(id)<0:
        output=('{}, {} out of index.'.format(message.author.mention, str(id)))
    else:
        #sql
        #DBQuery("DELETE FROM words WHERE word='"+badWord+"';")
        output=('{}, has unpinned "{}"'.format(message.author.mention, arrayPinned[int(id)][0].message.content))
        del arrayPinned[int(id)]
        #sql
        #getWords()
    return output
