# bot.py
import os
import discord
import pymysql
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
DB_IP="localhost"
DB_USER="root"
DB_PASSWORD="7755929"
DB_NAME="grizzo"
BAD_WORDS = []
arrayWords=[]
#SERVERID=" "

client = discord.Client()

#send custom querys
def DBQuery(queryStr):
    # Open database connection
    db = pymysql.connect(DB_IP,DB_USER,DB_PASSWORD,DB_NAME)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute(queryStr)

    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    #print ("Database version : %s " % data)

    # disconnect from server
    db.commit()
    db.close() 
   
#loads words into system   
def getWords():
    # Open database connection
    db = pymysql.connect(DB_IP,DB_USER,DB_PASSWORD,DB_NAME )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute("SELECT word FROM words WHERE serverID= '"+GUILD+"';")

    # Fetch a all rows using fetchall() method.
    BAD_WORDS = list(cursor.fetchall())
    
    #loads words from list to array
    for i in BAD_WORDS:
        arrayWords.append(i[-1])
        #print(i[-1])
    #print (BAD_WORDS)
    print(arrayWords)

    # disconnect from server
    db.commit()
    db.close() 

#check chack if value is in selected table and column
def has_value(table, column, value):
    # Open database connection
    db = pymysql.connect(DB_IP,DB_USER,DB_PASSWORD,DB_NAME )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    
    # execute SQL query using execute() method.
    cursor.execute("SELECT "+column+" from "+table+" WHERE "+column+" = '"+value+"' LIMIT 1")
    
    #query = "SELECT ID from grizzo WHERE ID = '".+GUILD+."' LIMIT 1"
    
    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    #print (data)
    db.commit()
    db.close()     
    return data is not None


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
            
    #SERVERID=str(guild.id)
    print("server id:::"+client.Server.id)
    #load words into array
    getWords()

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    
    #check if id is in database, if not, create it
    if not has_value("grizzo.grizzo", "ID", ""+GUILD+""):
        DBQuery("INSERT INTO grizzo VALUES('"+GUILD+"');")
    else:
        print("Server is already in database")
    
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    #censor word command, add words to censor list
    if message.content.strip().lower().startswith('!censorword '):
        badWord = message.content.strip().lower()[12:]
        if has_value("words", "word", badWord):
            await message.channel.send('{}, {} is already censored.'.format(message.author.mention, badWord))
        else:
            DBQuery("INSERT INTO words(words.serverID, word) VALUES('"+GUILD+"','"+badWord+"');")
            await message.channel.send('{}, has added "{}" to the censoring list'.format(message.author.mention, badWord))
            print("Censoring: "+badWord)
            getWords()
    
    #i=0
    #while i < len(arrayWords):
     #   if arrayWords[i] in message.content.strip().lower():
      #      await message.channel.send('{}, your message has been censored.'.format(message.author.mention))
       #     await message.delete() 
        #    print(arrayWords[i])
        #i += 1
     #uncensor word command, remove words from censor list   
    elif message.content.strip().lower().startswith('!uncensorword '):
        badWord = message.content.strip().lower()[14:]
        if not has_value("words", "word", badWord):
            await message.channel.send('{}, {} is not censored.'.format(message.author.mention, badWord))
        else:
            DBQuery("DELETE FROM words WHERE word='"+badWord+"';")
            await message.channel.send('{}, has been removed "{}" from the censoring list'.format(message.author.mention, badWord))
            print("Uncensoring: "+badWord)
            getWords()
    elif message.content.strip().lower().startswith('!censorhelp'):
        await message.channel.send('{}, !censorword [word/phrase to censor] \n\n!uncensorword [word/phrase to uncensor] \n\n!censorlist---- displays all cnesored words'.format(message.author.mention))
    elif message.content.strip().lower().startswith('!censorlist'):
        nicelist=""
        for x in arrayWords:
            nicelist+="["+x+"] "
        await message.channel.send('{}, Here is the list of censored words: {}'.format(message.author.mention, nicelist))
    else:    
        for x in arrayWords:
            print("List of censored words:")
            if x in message.content.strip().lower():
                await message.channel.send('{}, your message has been censored.'.format(message.author.mention))
                await message.delete() 
                print(x)
                break
            
client.run(TOKEN)























































