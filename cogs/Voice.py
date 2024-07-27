import nextcord
from nextcord.ext import commands
from nextcord import Interaction, Color, Embed, VoiceClient
from youtube_dl import YoutubeDL


class Voice(commands.Cog):

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="join", description="Bot ses kanalına katılır.")
    async def join(self, interaction: Interaction):
        if interaction.user.voice:
            if interaction.guild.voice_client:
                await interaction.response.send_message("Zaten bir ses kanalına bağlıyım.")
                return
            channel = interaction.user.voice.channel
            await interaction.response.send_message("Ses kanalına bağlandım.")
            await channel.connect()
        else:
            await interaction.response.send_message("Bu komutu kullanmak için bir ses kanalına bağlanmalısın.")

    @nextcord.slash_command(name="leave", description="Bot ses kanalından ayrılır.")
    async def leave(self, interaction: Interaction):
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message("Bağlantı kesildi.")
        else:
            await interaction.response.send_message("Bir ses kanalına bağlı değilim.")


    @commands.Cog.listener()
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            print(type(error))
            print(error)
            em = nextcord.Embed(title="Yavaşla!", description=f"{error.retry_after:.2f}s sonra tekrar deneyin.", color=Color.red())
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
    client.add_cog(Voice(client))