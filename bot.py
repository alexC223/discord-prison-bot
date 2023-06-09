import discord
import responses
import credentials
import asyncio


# Send messages
async def send_message(message, user_message, is_private):
    try:
        if user_message.startswith('!jail'):
            mentioned_users = message.mentions
            if mentioned_users:
                jail_channel = discord.utils.get(message.guild.channels, name='jail')
                for i in range(15):
                    for user in mentioned_users:
                        if user.voice and user.voice.channel:
                            await user.move_to(jail_channel)
                    await asyncio.sleep(1)
                response = f" Inmate {', '.join([user.name for user in mentioned_users])} has served his 15 second sentence."
            else:
                response = "No user mentioned. Please mention a user using `@`."
        else:
            response = responses.handle_response(user_message)

        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = credentials.discordToken
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        # Make sure bot doesn't get stuck in an infinite loop
        if message.author == client.user:
            return

        # Get data about the user
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # Debug printing
        print(f"{username} said: '{user_message}' ({channel})")

        # If the user message contains a '?' in front of the text, it becomes a private message
        if len(user_message) > 0 and user_message[0] == '?':
            user_message = user_message[1:] # [1:] Removes the '?'
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    # Remember to run your bot with your personal TOKEN
    client.run(TOKEN)