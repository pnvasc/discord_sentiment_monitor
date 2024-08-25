import discord
from discord.ext import commands
from .database import Session, Message

class DiscordCollector(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        session = Session()
        new_message = Message(content=message.content, user_id=str(message.author.id))
        session.add(new_message)
        session.commit()
        session.close()