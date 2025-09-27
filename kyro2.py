import discord
from discord.ext import commands
from discord import Interaction, app_commands
import random
from discord.ext import commands
import json
import os
from discord import app_commands
import datetime

class Client(commands.Bot):
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
    
        try:
            guild = discord.Object(id=1398401093809213504)
            synced =  await self.tree.sync()
            print(f'Synced {len(synced)} global command(s).')
        except Exception as e:
            print(f'Error syncing commands: {e}')



    
        




intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = Client(command_prefix="!", intents=intents)


reaction_file = "reaction.json"


@bot.tree.command(name="auto_message", description="Select a message to automatically send as a reaction to a message of your choosing")
async def auto_message(interaction: discord.Interaction, triggerword: str = "", message: str = ""):
    if triggerword == "":
        await interaction.response.send_message("Please provide a trigger word.", ephemeral=True)
        return
    if message == "":
        await interaction.response.send_message("Please provide a message to send.", ephemeral=True)
        return

    try:
        if os.path.exists(reaction_file):
            with open(reaction_file, "r", encoding="utf-8") as file:
                try:
                    reactions = json.load(file)
                except json.JSONDecodeError:
                    reactions = {}
        else:
            reactions = {}

        user_id = str(interaction.user.id)
        if user_id not in reactions:
            reactions[user_id] = {}

        reactions[user_id][triggerword] = message

        with open(reaction_file, "w", encoding="utf-8") as file:
            json.dump(reactions, file, indent=4)

        await interaction.response.send_message(f"Auto message set for trigger '{triggerword}'.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message("An error occurred while saving the message.", ephemeral=True)


react_file = "react.json"

@bot.tree.command(name="auto_react", description="Select a reaction to automatically send as a reaction to a message of your choosing")
async def auto_react(interaction: discord.Interaction, triggerword2: str, reaction: str):
    if triggerword2 == "":
        await interaction.response.send_message("Please provide a trigger word.", ephemeral=True)
        return
    if reaction == "":
        await interaction.response.send_message("Please provide a reaction to send.", ephemeral=True)
        return

    try:
        if os.path.exists(react_file):
            with open(react_file, "r", encoding="utf-8") as file:
                try:
                    react = json.load(file)
                except json.JSONDecodeError:
                    react = {}
        else:
            react = {}

        user_id = str(interaction.user.id)
        if user_id not in react:
            react[user_id] = {}

        react[user_id][triggerword2] = reaction

        with open(react_file, "w", encoding="utf-8") as file:
            json.dump(react, file, indent=4)

        await interaction.response.send_message(f"Auto reaction set for trigger '{triggerword2}' with reaction '{reaction}'.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message("An error occurred while saving the reaction.", ephemeral=True)

@bot.listen("on_message")
async def check_auto_message(message: discord.Message):
    if message.author == bot.user:
        return

    
    if os.path.exists(reaction_file):
        with open(reaction_file, "r", encoding="utf-8") as file:
            try:
                reactions = json.load(file)
            except json.JSONDecodeError:
                reactions = {}
    else:
        reactions = {}

    user_id = str(message.author.id)
    if user_id in reactions:
        for trigger, response in reactions[user_id].items():
            if trigger in message.content:
                await message.channel.send(response)
                break

    
    if os.path.exists(react_file):
        with open(react_file, "r", encoding="utf-8") as file:
            try:
                react = json.load(file)
            except json.JSONDecodeError:
                react = {}
    else:
        react = {}

    if user_id in react:
        for trigger2, emoji in react[user_id].items():
            if trigger2 in message.content:
                try:
                    await message.add_reaction(emoji)
                except Exception as e:
                    print(f"Failed to react with '{emoji}' for trigger '{trigger2}': {e}")
                break
            
empty = {}
@bot.tree.command(name= "clear-all-auto_message", description="Clears all your auto_message commands")
async def clear_message(interaction: discord.Interaction):
    with open (reaction_file, "w") as f:
        json.dump(empty, f)
    await interaction.response.send_message("All your auto message, messages have been cleared")

@bot.tree.command(name= "clear-all-auto_react", description= "Clears all your auto_react commands")
async def clear_react(interaction: discord.Interaction):
    with open (react_file, "w") as f:
        json.dump(empty, f)
    await interaction.response.send_message("All your auto react messages have been cleared")


@bot.tree.command(name="delete-auto_message", description="Delete a specific auto message by its trigger word")
async def delete_auto_message(interaction: discord.Interaction, triggerword: str):
    if not os.path.exists(reaction_file):
        await interaction.response.send_message("No auto messages found.", ephemeral=True)
        return
    try: 
        with open(reaction_file, "r", encoding="utf-8") as file:
            reactions_data = json.load(file)
            
        if triggerword in reactions_data:
            del reactions_data[triggerword]
            with open(reaction_file, "w", encoding="utf-8") as file:
                json.dump(reactions_data, file)
            await interaction.response.send_message(f"Auto message with trigger '{triggerword}' has been deleted.", ephemeral=True)
        else:
            await interaction.response.send_message(f' No auto message found with trigger "{triggerword}".', ephemeral=True)
    
    except Exception as e:
        await interaction.response.send_message("An error occurred while deleting the auto message.", ephemeral=True)

@bot.tree.command(name= "delete-auto_react", description = "Delete a specific auto reaction by its trigger word")
async def delete_auto_react(interaction: discord.Interaction, triggerword2: str):
    if not os.path.exists(react_file):
        await interaction.response.send_message("No auto reaction found.", ephemeral=True)
        return
    try:
        with open(react_file, "r", encoding="utf-8") as file:
            react_data = json.load(file)
        
        if triggerword2 in react_data:
            del react_data[triggerword2]
            with open(react_file, "w", encoding="utf-8") as file:
                json.dump(react_data, file)
            await interaction.response.send_message(f"Auto reaction with trigger '{triggerword2}' has been deleted.", ephemeral=True)
        else:
             await interaction.response.send_message(f' No auto reaction found with trigger "{triggerword2}".', ephemeral=True)
    
    except Exception as e:
        await interaction.response.send_message(f'An error occurred while deleting the auto reaction')

@bot.tree.command(name= "list-all-auto-message", description= "Lists all current auto message and react commands")
async def list_auto_message(interaction: discord.Interaction):

    if not os.path.exists(reaction_file) and not os.path.exists(react_file):
        await interaction.response.send_message("No auto messages found.", ephemeral=True)
        return
    
    data = {}

    if os.path.exists(reaction_file):
        with open(reaction_file, "r", encoding = "utf-8") as file:
            try:
                data.update(json.load(file))
            except json.JSONDecodeError:
                pass

    if os.path.exists(react_file):
        with open(react_file, "r", encoding = "utf-8") as file:
            try:
                data.update(json.load(file))
            except json.JSONDecodeError:
                pass
    
    if not data:
        await interaction.response.send_message("No auto messages found.", ephemeral=True)
        return

    else:
        message_lines = ["Current Auto Messages and Reactions:"]
        for trigger, response in data.items():
            message_lines.append(f"Trigger: '{trigger}' -> Response: '{response}'")
        
        message = "\n".join(message_lines)
        if len(message) > 2000:
            message = message[:1997] + "..."
        
        await interaction.response.send_message(message, ephemeral=True)

    
    
        



bot.run('')

