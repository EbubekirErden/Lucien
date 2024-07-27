from http import client
import nextcord
from nextcord.ext import commands
import sqlite3
import math
import random
from nextcord import Interaction, Embed, Color


class Leveling(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Leveling is online.")

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.author.bot:
            return
        
        connection = sqlite3.connect("./cogs/levels.db")
        cursor = connection.cursor()
        guild_id = message.guild.id
        user_id = message.author.id

        cursor.execute("SELECT * FROM Users WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
        result = cursor.fetchone()

        if result is None:
            cur_level = 0
            xp = 0
            level_up_xp = 100
            cursor.execute("INSERT INTO Users (guild_id, user_id, level, xp, level_up_xp) Values (?,?,?,?,?)", (guild_id, user_id, cur_level, xp, level_up_xp))
        else:
            cur_level = result[2]
            xp = result[3]
            level_up_xp = result[4]

            xp += random.randint(10, 25)

        if xp >= level_up_xp:
            cur_level += 1
            new_level_up_xp = math.ceil(50 * cur_level ** 2 + 100 * cur_level + 50)

            await message.channel.send(f"{message.author.mention}, {cur_level} seviye oldu!")

            cursor.execute("UPDATE Users SET level = ? , xp = ?, level_up_xp = ?, WHERE guild_id = ? AND user_id = ?", (cur_level, xp, level_up_xp, guild_id, user_id))

        cursor.execute("UPDATE Users SET xp = ? WHERE guild_id = ? AND user_id = ?", (xp, guild_id, user_id))

        connection.commit()
        connection.close()

    
    @nextcord.slash_command(name="level", description="Seviye istatistikleri.")
    async def level(self, interaction: Interaction, member: nextcord.Member=None):
        if member is None:
            member = interaction.user

        member_id = member.id
        guild_id = interaction.guild.id

        connection = sqlite3.connect("./cogs/levels.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE guild_id = ? AND user_id = ?", (guild_id, member_id))
        result = cursor.fetchone()

        if result is None:
            await interaction.response.send_message(f"Henüz bir seviyeye sahip değilsiniz.")
        else: 
            level = result[2]
            xp = result[3]
            level_up_xp = result[4]

            await interaction.response.send_message(f"{member.name} için seviye istatistikleri: \nLevel: {level} \nXP: {xp} \nXP To Level Up: {level_up_xp}")

        connection.close()


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
    client.add_cog(Leveling(client))
