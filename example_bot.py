import discord
import os
import subprocess
import json

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Name: ' + message.author.name)
        await message.channel.send('Display Name: ' + message.author.display_name)

    #turn into switch case
    #createUser
    if message.content.lower().startswith('$createuser'):
        await message.channel.send(message.mentions[0])
        
        os.system('curl -X POST http://localhost:7080/createuser -H "Content-Type: application/json" -d \'{"username": "' + str(message.mentions[0]) + '"}\'')
        #curl -X GET http://localhost:7080/getuser -H "Content-Type: application/json" -d '{"username": "Kalani Duran"}'
        await message.channel.send("User " + str(message.mentions[0]) + " created")


    #createGame
    if message.content.lower().startswith('$creategame'):
        await message.channel.send(message.content[12:])

        os.system('curl -X POST http://localhost:7080/creategame -H "Content-Type: application/json" -d \'{"title": "' + str(message.content[12:]) + '"}\'')
        await message.channel.send("Game " + str(message.content[12:]) + " created")


    #getUser
    if message.content.lower().startswith('$getuser'):
        await message.channel.send(message.mentions[0])

        result = subprocess.run('curl -X GET http://localhost:7080/getuser -H "Content-Type: application/json" -d \'{"username": "' + str(message.mentions[0]) + '"}\'', capture_output=True, text= True, shell=True)
        await message.channel.send(result.stdout)

        #await message.channel.send(json.loads(result.stdout)["username"] + " is the user I found")
        pass


    if message.content.lower().startswith('$assigngame'):
        await message.channel.send(message.content[12:])
        
        pass



client.run(os.environ['BOT_TOKEN']) 