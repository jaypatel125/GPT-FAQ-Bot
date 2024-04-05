"""
Authorship Statement: I Jay Patel, 000881881 certify that this material is my original work. No other person's work has been used without due acknowledgement. I have not made my work available to anyone else.
Date: 19 March 2024
Description: A Discord bot that provides information on diet, health, and wellness using OpenAI services.
"""

import discord
from WellnessWhiz import *


class MyClient(discord.Client):
    """
    Class to represent the Client (bot user)
    """

    def __init__(self):
        """
        This is the constructor. Sets the default 'intents' for the bot.
        """
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self):
        """
        Called when the bot is fully logged in.
        """
        print('Logged on as', self.user)

    async def on_message(self, message):
        """
        Called whenever the bot receives a message. The 'message' object
        contains all the pertinent information.
        """

        # don't respond to ourselves
        if message.author == self.user:
            return

        # Check if the message mentions the bot's name
        if self.user.mention in message.content:
            user_input = message.content
            response1, response2 = generate_response(user_input)
            best_response = choose_best_response(response1, response2)

            # send the response
            await message.channel.send(best_response)


## Set up and log in
client = MyClient()
with open("bot_token.txt") as file:
    token = file.read()
client.run(token)
