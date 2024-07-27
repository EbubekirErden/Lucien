import asyncio
import datetime
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, Color
from nextcord.utils import get

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="mute", description="Üyeyi susturur")
    @commands.has_permissions(moderate_members=True)
    async def mute(
            self,
            interaction: Interaction,
            member: nextcord.Member = nextcord.SlashOption(
                name="member",
                description="Lütfen bir üye seçiniz."
            ),
            seconds: int = nextcord.SlashOption(name="seconds", description="saniye", required=False),
            minutes: int = nextcord.SlashOption(name="minutes", description="dakika", required=False),
            hours: int = nextcord.SlashOption(name="hours", description="saat", required=False),
            days: int = nextcord.SlashOption(name="days", description="gün", required=False),
    ):
        role = get(interaction.guild.roles, name="muted")
        if not seconds: seconds = 0
        if not minutes: minutes = 0
        if not hours: hours = 0
        if not days: days = 0

        if role not in interaction.guild.roles:
            role = await interaction.guild.create_role(name="muted", permissions=nextcord.Permissions(send_messages=False))

        await member.add_roles(role)
        await interaction.response.send_message(f"{member.mention} susturuldu.")

        await asyncio.sleep(seconds + minutes * 60 + hours * 3600 + days * 86400)
        await member.remove_roles(role)

    @nextcord.slash_command(name="unmute", description="Üye susturmasını kaldırır.")
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, interaction: Interaction, member: nextcord.Member = nextcord.SlashOption(name="member", description="Lütfen bir üye seçiniz.")):
        role = get(interaction.guild.roles, name="muted")
        await member.remove_roles(role)
        await interaction.response.send_message(f"{member.mention} susturulması kaldırıldı.")

    @nextcord.slash_command(name="timeout", description="Üyeyi zaman aşımına uğratır.")
    @commands.has_permissions(moderate_members=True)
    async def timeout(
            self,
            interaction: Interaction,
            member: nextcord.Member = nextcord.SlashOption(
                name="member",
                description="Lütfen bir üye seçiniz."
            ),
            seconds: int = nextcord.SlashOption(name="seconds", description="saniye", required=False),
            minutes: int = nextcord.SlashOption(name="minutes", description="dakika", required=False),
            hours: int = nextcord.SlashOption(name="hours", description="saat", required=False),
            days: int = nextcord.SlashOption(name="days", description="gün", required=False),
            reason: str = nextcord.SlashOption(
                name="reason",
                description="Lütfen bir sebep belirtiniz.",
                required=False
            )
    ):
        if not reason: reason = "sebepsiz"
        if not seconds: seconds = 0
        if not minutes: minutes = 0
        if not hours: hours = 0
        if not days: days = 0
        duration = datetime.timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)
        await member.timeout(duration, reason=reason)
        await interaction.response.send_message(f"{member.mention}, {reason} sebebiyle zaman aşımına uğratıldı.")

    @nextcord.slash_command(name="kick", description="Üyeyi sunucudan atar")
    @commands.has_permissions(kick_members=True)
    async def kick(
            self,
            interaction: Interaction,
            member: nextcord.Member = nextcord.SlashOption(
                name="member",
                description="Lütfen bir üye seçiniz."
            ),
            reason: str = nextcord.SlashOption(
                name="reason",
                description="Lütfen bir sebep belirtiniz.",
                required=False
            )
    ):
        if not reason: reason = "sebepsiz"
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member.mention} sunucudan {reason} sebebiyle atıldı.")

    @nextcord.slash_command(name="ban", description="Üyeyi sunucudan yasaklar")
    @commands.has_permissions(ban_members=True)
    async def ban(
            self,
            interaction: Interaction,
            member: nextcord.Member = nextcord.SlashOption(
                name="member",
                description="Lütfen bir üye seçiniz."
            ),
            reason: str = nextcord.SlashOption(
                name="reason",
                description="Lütfen bir sebep belirtiniz.",
                required=False
            )
    ):
        if not reason: reason = "sebepsiz"
        if member == interaction.user:
            await interaction.channel.response.send_message("Kendini sunucudan yasaklayamazsın!")
            return
        await member.ban(reason=reason)
        await interaction.channel.response.send_message(f"{member.mention}, sunucudan {reason} sebebiyle yasaklandı.")

    @nextcord.slash_command(name="unban", description="Üye yasaklamasını kaldırır")
    @commands.has_permissions(ban_members=True)
    async def unban(
            self,
            interaction: Interaction,
            user: nextcord.User = nextcord.SlashOption(
                name="user",
                description="Lütfen geçerli bir üye ID'si belirtiniz."
            )):
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"{user.mention}'nın yasaklaması kaldırıldı.")

    @nextcord.slash_command(name="clear", description="Mesajları siler.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, interaction: Interaction,
                    number_of_messages: int = nextcord.SlashOption(name="number_of_messages",
                                                                   description="Silinecek mesaj sayısı"),
                    ):
        await interaction.channel.purge(limit=number_of_messages)
        await interaction.response.send_message(f"{number_of_messages} mesaj silindi.")
        await interaction.channel.purge(limit=1)

    @nextcord.slash_command(name="serverinfo", description="Sunucu istatistiklerini görün.")
    async def guild_info(self, interaction: Interaction):
        member_count = len(interaction.guild.members)
        roles_count = len(interaction.guild.roles)
        inline = False
        embed = nextcord.Embed(title=interaction.guild.name, colour=0x0080ff)
        embed.set_thumbnail(url=interaction.guild.icon.url)
        embed.add_field(name="ID: ", value=str(interaction.guild.id), inline=inline)
        embed.add_field(name="Owner: ", value=str(interaction.guild.owner), inline=inline)
        embed.add_field(name='Created at: ', value=interaction.guild.created_at.strftime("%b %d, %Y, %T"),
                        inline=inline)
        embed.add_field(name='Region: ', value=interaction.guild.region, inline=inline)
        embed.add_field(name='Total Members: ', value=str(member_count), inline=inline)
        embed.add_field(name='Total Roles: ', value=str(roles_count), inline=inline)
        embed.add_field(name="Total Channels: ", value=len(interaction.guild.channels), inline=inline)
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="userinfo", description="Üye bilgilerini görün.")
    async def user_info(self, interaction: Interaction, member: nextcord.Member = None):
        if member is None: member = interaction.user
        print(member.name)
        inline = False
        embed = nextcord.Embed(title=member.name, colour=0x0080ff, description=member.mention)
        embed.set_thumbnail(member.display_avatar)
        embed.add_field(name="ID: ", value=member.id, inline=inline)
        embed.add_field(name="Name: ", value=member.name, inline=inline)
        embed.add_field(name="Joined Discord: ", value=member.created_at.strftime("%b %d, %Y, %T"), inline=inline)
        embed.add_field(name="Joined Server: ", value=member.joined_at.strftime("%b %d, %Y, %T"), inline=inline)
        if len(member.roles) > 1:
            role_string = ' '.join([r.mention for r in member.roles][1:])
            embed.add_field(name="Roles [{}]".format(len(member.roles) - 1), value=role_string, inline=inline)
        embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="lock", description="Kanalı yazı yazmaya kapatır")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, interaciton: Interaction, channel : nextcord.TextChannel=None):
        if channel is None:
            channel = interaciton.channel
        await channel.set_permissions(interaciton.guild.default_role, reason=f"{channel.name} erişime kapatıldı.", send_messages=False)
        await interaciton.response.send_message("Kanal erişime kapatıldı.")

    @nextcord.slash_command(name="unlock", description="Kanalı yazı yazmaya açar.")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, interaciton: Interaction, channel : nextcord.TextChannel=None):
        if channel is None:
            channel = interaciton.channel
        await channel.set_permissions(interaciton.guild.default_role, reason=f"{channel.name} erişime açıldı.", send_messages=True)
        await interaciton.response.send_message("Kanal erişime açıldı.")

    @nextcord.slash_command(name="slowmode", description="Yavaş mod süresini belirler.")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, interaction: Interaction, time_delay=0, channel: nextcord.TextChannel=None):
        if channel is None:
            channel = interaction.channel
        await channel.edit(slowmode_delay=time_delay)
        await interaction.response.send_message(f"{channel.name} yavaş mod ayarları değiştirildi.")

    @nextcord.slash_command(name="giverole", description="Bir veya daha fazla üyeye rol verir.")
    @commands.has_permissions(moderate_members=True)
    async def giverole(self, interaction: Interaction, role: nextcord.Role, members: commands.Greedy[nextcord.Member]):
        for m in members:
            await m.add_roles(role)
            await asyncio.sleep(1)
        await interaction.response.send_message(f"Rol verildi!")

    @nextcord.slash_command(name="takerole", description="Üyeden belirli rolü alır.")
    @commands.has_permissions(moderate_members=True)
    async def giverole(self, interaction: Interaction, role: nextcord.Role, member: nextcord.Member):
        await member.remove_roles(role)
        await interaction.response.send_message(f"Rol geri alındı!")

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
    client.add_cog(Moderation(client))