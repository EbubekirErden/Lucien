import nextcord
from nextcord.ext import commands
from nextcord import Interaction, File, ButtonStyle, Embed, Color
from nextcord.ui import Button, View
import os
import json

from apikeys import *

intent = nextcord.Intents.all()
client = commands.Bot(command_prefix="fd!", intents=intent, case_insensitive=True, help_command=None)
client.remove_command("help")


@client.event
async def on_ready():
    await client.change_presence(status=nextcord.Status.online,
                                activity=nextcord.Activity(type=nextcord.ActivityType.competing, name="Valinor"))
    print("The bot is now ready for use")
    print("----------------------------")


help_guide = json.load(open("help.json"))


def create_help_embed(interaction: Interaction, page_num=0, inline=False):
    page_num = page_num % len(list(help_guide))
    page_title = list(help_guide)[page_num]
    embed = Embed(colour=0x0080ff, title=page_title)
    embed.set_thumbnail(interaction.guild.icon.url)
    for key, val in help_guide[page_title].items():
        embed.add_field(name="/" + key, value=val, inline=inline)
        embed.set_footer(text=f"Page {page_num + 1} of {len(list(help_guide))}")
    return embed


@client.slash_command(name="help")
async def help(ctx):
    current_page = 0

    async def next_callback(interaction):
        nonlocal current_page, sent_msg
        current_page += 1
        await sent_msg.edit(embed=create_help_embed(interaction, page_num=current_page), view=my_view)

    async def previous_callback(interaction):
        nonlocal current_page, sent_msg
        current_page -= 1
        await sent_msg.edit(embed=create_help_embed(interaction, page_num=current_page), view=my_view)

    previous_button = Button(label="<", style=ButtonStyle.blurple)
    next_button = Button(label=">", style=ButtonStyle.blurple)
    previous_button.callback = previous_callback
    next_button.callback = next_callback

    my_view = View(timeout=180)
    my_view.add_item(previous_button)
    my_view.add_item(next_button)


    sent_msg = await ctx.response.send_message(embed=create_help_embed(ctx), view=my_view)



initial_extensions = []
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        initial_extensions.append("cogs." + filename[:-3])

if __name__ == "__main__":
    for extension in initial_extensions:
        client.load_extension(extension)

client.run(TOKEN)
