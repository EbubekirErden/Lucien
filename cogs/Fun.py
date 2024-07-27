import nextcord
from nextcord.ext import commands
import random
from nextcord import Interaction, Color, Embed
import requests
import asyncpraw as praw
from random import choice
from apikeys import *



class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.reddit = praw.Reddit(client_id=ClIENT_ID, client_secret=CLIENT_SECRET,
                                  user_agent="script:Lucien:v1.0 {by u/Potential_Break_6125}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        elif message.content.startswith("!"):
            return
        elif message.content == "Yüzükleri neden kartallar götürmedi":
            await message.delete()
            await message.channel.send("Bunu burda sormuyoruz!")

        elif message.content.lower() == "vymir":
            message_list = ["tamam", "güzel", "E bu bekir nerede?", "https://tenor.com/view/vinland-saga-gif-24421210"]
            await message.channel.send(random.choice(message_list))

        await self.client.process_commands(message)

    @nextcord.slash_command(name="meme", description="Send memes")
    async def meme(self, interaction: Interaction):
        subreddit = await self.reddit.subreddit("memes", "meme")
        posts_list = []

        async for post in subreddit.hot(limit=30):
            if not post.over_18 and post.author is not None and any(
                    post.url.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif"]):
                author_name = post.author.name
                posts_list.append((post.url, author_name))
            if post.author is None:
                posts_list.append((post.url, "N/A"))

        if posts_list:
            random_post = choice(posts_list)

            meme_embed = Embed(title="Random Meme", color=0x0080ff, url=random_post[0])
            meme_embed.set_author(name=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url)
            meme_embed.set_image(url=random_post[0])
            meme_embed.set_footer(text=f"Post created by {random_post[1]}.", icon_url=None)
            await interaction.response.send_message(embed=meme_embed)

        else:
            await interaction.response.send_message("Gönderi bulunamadı. Lütfen daha sonra tekrar deneyiniz.")

    def cog_unload(self):
        self.client.loop.create_task(self.reddit.close())

    @nextcord.slash_command(name="dog", description="Köpek fotoğrafı gönderir!")
    async def dog(self, interaction: Interaction):
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        image_link = response.json()["message"]
        embed = nextcord.Embed(title="🐶Woof!", url=image_link, colour=0x0080ff)
        embed.set_image(url=image_link)
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="cat", description="Kedi fotoğrafı gönderir!")
    async def cat(self, interaction: Interaction):
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        data = response.json()
        embed = nextcord.Embed(title="🐱Meoww!", url=data[0]['url'], color=0x0080ff)
        embed.set_image(url=data[0]['url'])
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="avatar", description="Üyenin profil fotoğrafını gösterir.")
    async def avatar(self, interaction: Interaction, member: nextcord.Member = nextcord.SlashOption(name="member", required=False)):
        if not member:
            member = interaction.user
        if member.avatar is None:
            await interaction.response.send_message(f"{member.mention} profil fotosu bulunamadı.")
            return
        pfp_embed = nextcord.Embed(title="Avatar's Link", url=member.avatar.url, colour=0x0080ff)
        pfp_embed.set_image(member.avatar.url)
        pfp_embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=pfp_embed)


    @commands.Cog.listener()
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            print(type(error))
            print(error)
            em = nextcord.Embed(title="Yavaşla!",
                                description=f"{error.retry_after:.2f}s sonra tekrar deneyin.", color=Color.red())
            await ctx.send(embed=em)
        elif isinstance(error, commands.MissingRequiredArgument):
            print(type(error))
            print(error)
            await ctx.send('Lütfen gerekli bütün argümanları giriniz.')
        elif isinstance(error, commands.MissingPermissions):
            print(type(error))
            print(error)
            await ctx.send("Bu komutu kullanmaya yetkiniz yok!")
        elif isinstance(error, commands.MemberNotFound):
            print(type(error))
            print(error)
            await ctx.send("Üye bulunamadı.")
        else:
            print(type(error))
            print(error)


def setup(client):
    client.add_cog(Fun(client))