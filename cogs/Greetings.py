import nextcord
from nextcord.ext import commands
from nextcord import Interaction, Color, Embed


class Greetings(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(1257260297895415899)
        rules_channel = self.client.get_channel(1143490932126269480)
        await channel.send(
            "Hoş geldin " + member.mention + ", " + rules_channel.mention + " kanalından kuralları okuyabilirsin.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.client.get_channel(1257260297895415899)
        await channel.send("Güle Güle " + member.mention)

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
    client.add_cog(Greetings(client))
