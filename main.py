# Required imports
import discord
from discord.ext import commands
from discord.ui import View, Button
import os

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.invites = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Store invites
invite_tracker = {}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    for guild in bot.guilds:
        invite_tracker[guild.id] = await guild.invites()
    print("📌 Invite cache ready")

# View for the button
class CheckInvitesView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Check Invites", style=discord.ButtonStyle.secondary, emoji="📨")
    async def check_invites(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        guild = interaction.guild
        invites = await guild.invites()

        total_invites = sum(i.uses for i in invites if i.inviter and i.inviter.id == user.id)

        embed = discord.Embed(
            description=f"### <:1343331433753739316:1368676075978096661> Your Invitation Info\n{user.mention}, You have invited **{total_invites}** members to the server!",
            color=discord.Color.from_str("#fa002e")
        )

        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

# Command to trigger the invite checker
@bot.command()
async def invites(ctx):
    banner_url = "https://media.discordapp.net/attachments/1363516979138269395/1368580187708723330/checkyourinvites.png?format=webp&quality=lossless&width=1800&height=304"

    embed = discord.Embed(
        description="### <:1343321428266713089:1368676064095633561>  Check your invites:\n> **Click** the button below to check how many people you've invited!",
        color=discord.Color.from_str("#fa002e")
    )

    await ctx.send(content=banner_url)
    await ctx.send(embed=embed, view=CheckInvitesView())

# Running your bot
bot.run(os.getenv("DISCORD_TOKEN"))
