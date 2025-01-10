import discord
from discord.ext import commands
import config
import discord.ui
from discord.ui import Button, View, Select
import datetime
from datetime import datetime, timedelta
import json
import os
import random
import requests
from discord.ext.commands import CheckFailure
import asyncio


intents = discord.Intents.all()

bot = commands.Bot(command_prefix = 'a!', intents= intents)
# Load or create scrims file
if os.path.exists("data/scrims.json"):
    with open("data/scrims.json", "r") as f:
        scrims = json.load(f)
else:
    scrims = {}

# Load or create ban list file
if os.path.exists("data/banlist.json"):
    with open("data/banlist.json", "r") as f:
        banlist = json.load(f)
else:
    banlist = []

# Save scrims to file
def save_scrims():
    with open("data/scrims.json", "w") as f:
        json.dump(scrims, f)


# Save ban list to file
def save_banlist():
    with open("banlist.json", "w") as f:
        json.dump(banlist, f)


# Load or create submissions file
if os.path.exists("data/submissions.json"):
    with open("data/submissions.json", "r") as f:
        submissions = json.load(f)
else:
    submissions = {}

# Save submissions to file
def save_submissions():
    with open("data/submissions.json", "w") as f:
        json.dump(submissions, f)


# Load or create balances file
if os.path.exists("data/mainbank.json"):
    with open("data/mainbank.json", "r") as f:
        balances = json.load(f)
else:
    balances = {}


@bot.event
async def on_ready():
    print("Bot ready ho chuka hai! Discord par jaakar check kar sakte ho :)")
    await bot.tree.sync()
    await bot.change_presence(activity=discord. Activity(type=discord.ActivityType.listening, name='/help'))
    
    
    
@bot.event
async def on_command_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.CommandOnCooldown): #checks if on cooldown
        msg = 'You are on **cooldown**. \nWait `{:.2f}s'.format(error.retry_after)
        await interaction.response.send(msg)
# Save balances to file
def save_balances():
    with open("mainbank.json", "w") as f:
        json.dump(balances, f)


#-------------------------------------------------------------------------------
#                          MISC COMMANDS
#-------------------------------------------------------------------------------

@bot.tree.command()
async def ping(interaction: discord.Interaction):
    """Pong!"""
    await interaction.response.send_message(f"Bot: `{round(bot.latency*1000)}`ms")

class Prompt1(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

@bot.tree.command()
async def help(interaction: discord.Interaction):
    """Get some help."""
    view = Prompt1()
    view.add_item(
        discord.ui.Button(
            label = "Support Server",
            url = "https://discord.gg/CxJdyezkyx"
        )
        )
    view.add_item(
        discord.ui.Button(
            label = "Invite Me",
            url = "https://discord.com/oauth2/authorize?client_id=1324800678174130186&permissions=8&integration_type=0&scope=bot+applications.commands"
        )
    )
    embed = discord.Embed(description="[Support Server](<https://discord.gg/CxJdyezkyx>) **|** [Invite Me](<https://discord.com/oauth2/authorize?client_id=1324800678174130186&permissions=8&integration_type=0&scope=bot+applications.commands>) **|** [Privacy Policy](<https://www.youtube.com/@Aryan_singh022>)",color=0xf8504c)
    embed.add_field(name="Esports",value="`idp`, `smanager`, `register_scrim`, `upcoming_scrims`, `past_scrims`, `slotmanager`",inline=False)
    embed.add_field(name = "Mod", value="`clear`, `kick`, `ban`, `warn`",inline=False)
    embed.add_field(name = "ArsMisc", value="`source`, `invite`, `ping`, `about`, `prefix`",inline=False)
    embed.add_field(name="Utility",value="`embed`, `botinfo`, `userinfo`, `serverinfo`, `avatar`, `roleinfo`, `serverstats`",inline=False)
    embed.add_field(name="Economy",value="`qobalance`, `earn`, `spend`, `leaderboard`, `daily`, `transfer`, `gamble`, `work`, `shop`, `buy`, `rob`, `deposit`, `withdraw`, `payday`, `bet`, `inventory`, `give`, `steal`, `lottery`, `draw_lottery` ",inline=False)
    embed.add_field(name="Fun",value="`roll`, `flip`, `joke`, `eightball`",inline=False)
    embed.add_field(name="Giveaways",value="`start_giveaway`, `end_giveaway`, `enter_giveaway`",inline=False)
    embed.add_field(name="Tickets",value="`ticket`, `ticket_use_info`",inline=False)
    embed.add_field(name="SSVerification",value="`submit_screenshot`, `view_submissions`, `manage_submission`",inline=False)
    await interaction.response.send_message(embed=embed,view=view)


@bot.tree.command()
async def source(interaction: discord.Interaction):
    """Gets the source"""
    await interaction.response.send_message("https://www.youtube.com/@Aryan_singh022")

@bot.tree.command()
async def invite(interaction: discord.Interaction):
    """Gets the invite link"""
    embed = discord.Embed(description=
                          "[Invite Me](<https://discord.com/oauth2/authorize?client_id=1324800678174130186&permissions=8&integration_type=0&scope=bot+applications.commands>)"
                          ,color=0xf8504c
                          )
    await interaction.response.send_message(embed=embed)

@bot.tree.command()
async def prefix(interaction: discord.Interaction):
    """Says the prefix"""
    embed = discord.Embed(description="I support slash(/) commands! write /help to start with me",color=0xf8504c)
    await interaction.response.send_message(embed=embed)



@bot.tree.command()
async def about(interaction: discord.Interaction):
    """Tells about itself"""
    embed = discord.Embed(
        description="[ArstoCate Official Discord Server](<https://discord.gg/CxJdyezkyx>)",color=0xf8504c
    )
    embed.add_field(name="Stats",value=f"Ping: {bot.latency}ms \n Shard: {bot.shard_count}")
    embed.set_footer(text="Made with discord.py v2.3.0",icon_url="https://images-ext-1.discordapp.net/external/0KeQjRAKFJfVMXhBKPc4RBRNxlQSiieQtbSxuPuyfJg/http/i.imgur.com/5BFecvA.png")
    await interaction.response.send_message(embed=embed)

#-------------------------------------------------------------------------------
#                          UTILITY COMMANDS
#-------------------------------------------------------------------------------


@bot.tree.command()
async def embed(interaction: discord.Interaction, title:str,*,description:str):
    """Sends an embed"""
    embed = discord.Embed(title=title, description=description, color = 0xf8504c)
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/853174868551532564/860464565338898472/embed_thumbnail.png?ex=6779b3d3&is=67786253&hm=8bb1e16e1c4ebb1c417b801ae8f2f69cceda19c5af45e1ac289f06bf826659fd&=&format=webp&quality=lossless")
    embed.set_image(url="https://cdn.discordapp.com/attachments/853174868551532564/860462053063393280/embed_image.png?ex=6779b17c&is=67785ffc&hm=a73c68e2925e20a3ce2f18de4aa1c6b0b268507ce3484345aa735bde55beec71&")
    embed.set_footer(text="Footer Message",icon_url="https://media.discordapp.net/attachments/853174868551532564/860464989164535828/embed_footer.png?ex=6779b438&is=677862b8&hm=e96b9bb01fca7b09acdc6cf116f2bb9fc68852da2a15db09a09811ce43e8abdb&")
    await interaction.response.send_message(embed=embed)

@bot.tree.command()
async def serverinfo(interaction: discord.Interaction):
    """Displays information about the server."""
    guild = interaction.guild
    embed = discord.Embed(title=f"{guild.name} Server Information", color=0xf8504c)
    embed.add_field(name="Server Name:", value=guild.name, inline=True)
    embed.add_field(name="Server ID:", value=guild.id, inline=True)
    embed.add_field(name="Owner:", value=guild.owner, inline=True)
    embed.add_field(name="Member Count:", value=guild.member_count, inline=True)
    embed.add_field(name="Created At:", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    embed.set_thumbnail(url=guild.icon.url)
    await interaction.response.send_message(embed=embed)


@bot.tree.command()
async def userinfo(interaction: discord.Interaction, member: discord.Member=None):
    """Says about the mentioned user."""
    if member is None:
        member = interaction.author
    elif member is not None:
        member = member

    embed = discord.Embed(title=f"`{member.name}'s` Information:",color=0xf8504c)
    embed.add_field(
        name="Name:",
        value=member.name,
        inline=True
    )
    embed.add_field(
        name="ID",
        value=member.id,
        inline=True
    )
    embed.add_field(
        name="Nick name",
        value=member.display_name,
        inline=True
    )
    embed.add_field(
        name="Discrimination",
        value=member.discriminator,
        inline=True
    )
    embed.add_field(
        name="Top Role",
        value=member.top_role,
        inline=True
    )
    embed.add_field(
        name="Status",
        value=member.status,
        inline=True
    )
    embed.add_field(
        name="Bot User?",
        value=member.bot,
        inline=True
    )
    embed.add_field(
        name="Created on",
        value=member.created_at.__format__("%A, %d. %B %Y @ %H:%M:%S"),
        inline=True
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command()
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    """Get the avatar of a user"""
    if member is None:
        member = interaction.user
    embed = discord.Embed(title=f"{member.name}'s Avatar", color=0xf8504c)
    embed.set_image(url=member.avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command()
async def botinfo(interaction: discord.Interaction):
    """Get information about the bot"""
    embed = discord.Embed(title="Bot Information", color=0xf8504c)
    embed.add_field(name="Name", value=bot.user.name, inline=True)
    embed.add_field(name="ID", value=bot.user.id, inline=True)
    embed.add_field(name="Latency", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="Servers", value=f"{len(bot.guilds)}", inline=True)
    embed.set_thumbnail(url=bot.user.avatar.url)
    await interaction.response.send_message(embed=embed)



@bot.tree.command()
async def roleinfo(interaction: discord.Interaction, role: discord.Role):
    """Get information about a role"""
    embed = discord.Embed(title=f"Role Information: {role.name}", color=role.color)
    embed.add_field(name="ID", value=role.id, inline=True)
    embed.add_field(name="Name", value=role.name, inline=True)
    embed.add_field(name="Color", value=str(role.color), inline=True)
    embed.add_field(name="Position", value=role.position, inline=True)
    embed.add_field(name="Mentionable", value=role.mentionable, inline=True)
    embed.add_field(name="Created At", value=role.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command()
async def serverstats(interaction: discord.Interaction):
    """Get server statistics"""
    guild = interaction.guild
    total_members = guild.member_count
    online_members = sum(1 for member in guild.members if member.status != discord.Status.offline)
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    roles = len(guild.roles)
    embed = discord.Embed(title=f"{guild.name} Server Statistics", color=0xf8504c)
    embed.add_field(name="Total Members", value=total_members, inline=True)
    embed.add_field(name="Online Members", value=online_members, inline=True)
    embed.add_field(name="Text Channels", value=text_channels, inline=True)
    embed.add_field(name="Voice Channels", value=voice_channels, inline=True)
    embed.add_field(name="Roles", value=roles, inline=True)
    await interaction.response.send_message(embed=embed)

#-------------------------------------------------------------------------------
#                          MODERATION COMMANDS
#-------------------------------------------------------------------------------

@bot.tree.command()
@commands.has_permissions(kick_members=True)
@commands.bot_has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, *, reason: str):
    """Kick a member."""
    if interaction.user.guild_permissions.kick_members:
        await member.kick(reason=reason)
        embed = discord.Embed(description=f"<:tick:1323972567924740169> | {member} has been successfully kicked out!",color=0xf8504c)
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(description="You lack `Kick Members` permissions to run this command.",color=0xFF0000)
        await interaction.response.send_message(embed=embed)

@bot.tree.command()
@commands.has_permissions(ban_members=True)
@commands.bot_has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, *, reason: str):
    """Ban a member."""
    if interaction.user.guild_permissions.ban_members:
        await member.ban(reason=reason)
        embed = discord.Embed(description=f"<:tick:1323972567924740169> | {member} has been successfully banned.",color=0xf8504c)
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(description="You lack `Ban Members` permissions to run this command.",color=0xFF0000)
        await interaction.response.send_message(embed=embed)

@bot.tree.command()
@commands.has_permissions(ban_members=True)
async def warn(interaction: discord.Interaction, member: discord.Member, *, reason: str):
    """Warns a member."""
    if interaction.user.guild_permissions.ban_members:
        embed = discord.Embed(description=f"<:tick:1323972567924740169> | {member} has been warned",color=0xf8504c)
        await interaction.response.send_message(embed=embed,ephemeral=True)
        embed2 = discord.Embed(title="Be Careful!",description=f"You have been warned for `{reason}`.",color=0xf8504c)
        await member.send(embed=embed2)
    else:
        embed = discord.Embed(description="You lack `Ban Members` permissions to run this command.",color=0xf8504c)
        await interaction.response.send_message(embed=embed)



@bot.tree.command()
@commands.has_permissions(manage_messages=True)
@commands.bot_has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    """Clear a amount of messages"""
    if interaction.user.guild_permissions.manage_messages:
        await interaction.response.defer(thinking=True,ephemeral=True)
        await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"{amount} messages were removed",ephemeral=True)
    else:
        embed = discord.Embed(description="You lack `Manage Messages` permissions to run this command.",color=0xFF0000)
        await interaction.response.send_message(embed=embed)


@clear.error
async def on_error(interaction: discord.Interaction, error: commands.CommandError):
    if isinstance(error, commands.MissingPermissions):
        embed=discord.Embed(description="You lack `Manage Messages` permissions to run this command.",color=0xFF0000)
        await interaction.response.send_message(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        await interaction.response.send_message("Merepe Permission nhi hai :(")





#-------------------------------------------------------------------------------
#                          ESPORTS COMMAND
#-------------------------------------------------------------------------------

@bot.tree.command()
async def idp(interaction: discord.Interaction, room_id: int, password: int, *, map:str, roles: discord.Role):
    """Shares Id/pass with embed quickly."""
    icon_url = interaction.guild.icon.url
    embed = discord.Embed(title="ArstoCate `IDP` Manager. ",color=0xf8504c)
    embed.add_field(
        name = "Room ID",
        value = room_id,
        inline=True
    )
    embed.add_field(
        name = "Password",
        value=password,
        inline = True
    )
    embed.add_field(
        name = "Map",
        value=map,
        inline=True
    )
    embed.set_thumbnail(url=icon_url)
    await interaction.response.send_message(roles.mention , embed=embed)




#-------------------------------------------------------------------------------
#                          ECONOMY COMMANDS
#-------------------------------------------------------------------------------

@bot.tree.command()
async def qobalance(interaction: discord.Interaction):
    """Check your balance"""
    user_id = str(interaction.user.id)
    bal = balances.get(user_id, 0)
    embed = discord.Embed(title=f"{interaction.user.name}'s QoBalance Book",description=f"Balance: `{bal}` coins",color=0xf8504c)
    await interaction.response.send_message(embed=embed)


@bot.tree.command()
async def earn(interaction: discord.Interaction):
    """Earn some coins"""
    user_id = str(interaction.user.id)
    amount = random.randint(10, 100)
    balances[user_id] = balances.get(user_id, 0) + amount
    save_balances()
    await interaction.response.send_message(f"You earned {amount} coins! Your new balance is: {balances[user_id]} coins")

@bot.tree.command()
async def spend(interaction: discord.Interaction, amount: int):
    """Spend some coins"""
    user_id = str(interaction.user.id)
    if balances.get(user_id, 0) >= amount:
        balances[user_id] -= amount
        save_balances()
        await interaction.response.send_message(f"You spent {amount} coins! Your new balance is: {balances[user_id]} coins")
    else:
        await interaction.response.send_message("You don't have enough coins!")


@bot.tree.command()
async def leaderboard(interaction: discord.Interaction):
    """Show the top 10 users by balance"""
    try:
        # Filter out invalid balances
        valid_balances = {user_id: bal for user_id, bal in balances.items() if isinstance(bal, int)}
        sorted_balances = sorted(valid_balances.items(), key=lambda x: x[1], reverse=True)
        top_users = sorted_balances[:10]
        embed = discord.Embed(title="Leaderboard", description="Top 10 users by balance", color=0xf8504c)
        for i, (user_id, bal) in enumerate(top_users, start=1):
            try:
                user = await bot.fetch_user(int(user_id))
                embed.add_field(name=f"{i}. {user.name}", value=f"{bal} coins", inline=False)
            except discord.NotFound:
                embed.add_field(name=f"{i}. Unknown User (ID: {user_id})", value=f"{bal} coins", inline=False)
            except Exception as e:
                embed.add_field(name=f"{i}. Error fetching user (ID: {user_id})", value=f"{bal} coins", inline=False)
                print(f"Error fetching user {user_id}: {str(e)}")
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred while fetching the leaderboard: {str(e)}", ephemeral=True)
        print(f"Error in leaderboard command: {str(e)}")

@bot.tree.command()
@commands.cooldown(1,86400,commands.BucketType.user)
async def daily(interaction: discord.Interaction):
    """Claim your daily reward"""
    user_id = str(interaction.user.id)
    now = datetime.utcnow()
    last_claim = balances.get(f"{user_id}_last_claim", None)
    if last_claim:
        last_claim = datetime.strptime(last_claim, "%Y-%m-%d %H:%M:%S")
        if now - last_claim < timedelta(days=1):
            await interaction.response.send_message("You have already claimed your daily reward. Try again later.")
            return
    balances[user_id] = balances.get(user_id, 0) + 100
    balances[f"{user_id}_last_claim"] = now.strftime("%Y-%m-%d %H:%M:%S")
    save_balances()
    await interaction.response.send_message("You have claimed your daily reward of 100 coins!")

@bot.tree.command()
async def transfer(interaction: discord.Interaction, member: discord.Member, amount: int):
    """Transfer coins to another user"""
    user_id = str(interaction.user.id)
    target_id = str(member.id)
    if balances.get(user_id, 0) >= amount:
        balances[user_id] -= amount
        balances[target_id] = balances.get(target_id, 0) + amount
        save_balances()
        await interaction.response.send_message(f"You transferred {amount} coins to {member.name}. Your new balance is: {balances[user_id]} coins")
    else:
        await interaction.response.send_message("You don't have enough coins!")


@bot.tree.command()
async def gamble(interaction: discord.Interaction, amount: int):
    """Gamble your coins"""
    user_id = str(interaction.user.id)
    if balances.get(user_id, 0) < amount:
        await interaction.response.send_message("You don't have enough coins to gamble!")
        return
    if random.random() < 0.5:
        balances[user_id] += amount
        result = f"You won {amount} coins! Your new balance is: {balances[user_id]} coins"
    else:
        balances[user_id] -= amount
        result = f"You lost {amount} coins! Your new balance is: {balances[user_id]} coins"
    save_balances()
    await interaction.response.send_message(result)

@bot.tree.command()
async def work(interaction: discord.Interaction):
    """Work to earn coins"""
    user_id = str(interaction.user.id)
    amount = random.randint(50, 200)
    balances[user_id] = balances.get(user_id, 0) + amount
    save_balances()
    await interaction.response.send_message(f"You worked hard and earned {amount} coins! Your new balance is: {balances[user_id]} coins")

# Shop system
shop_items = {
    "Wodden Log": {"price": 100, "description": "This is  Wooden log used for making houses"},
    "Marble Slabs": {"price": 200, "description": "This is used in kitchens"},
    "Windows": {"price": 300, "description": "This is used in decorating"},
}

@bot.tree.command()
async def shop(interaction: discord.Interaction):
    """Show available items in the shop"""
    embed = discord.Embed(title="Shop", description="Available items for purchase", color=0xf8504c)
    for item, details in shop_items.items():
        embed.add_field(name=item, value=f"Price: {details['price']} coins\nDescription: {details['description']}", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command()
async def buy(interaction: discord.Interaction, item: str):
    """Buy an item from the shop"""
    user_id = str(interaction.user.id)
    if item not in shop_items:
        await interaction.response.send_message("This item does not exist in the shop!")
        return
    item_price = shop_items[item]["price"]
    if balances.get(user_id, 0) >= item_price:
        balances[user_id] -= item_price
        save_balances()
        await interaction.response.send_message(f"You bought {item} for {item_price} coins! Your new balance is: {balances[user_id]} coins")
    else:
        await interaction.response.send_message("You don't have enough coins to buy this item!")

@bot.tree.command()
async def rob(interaction: discord.Interaction, member: discord.Member):
    """Attempt to rob another user"""
    user_id = str(interaction.user.id)
    target_id = str(member.id)
    if user_id == target_id:
        await interaction.response.send_message("You cannot rob yourself!")
        return
    if balances.get(target_id, 0) < 100:
        await interaction.response.send_message(f"{member.name} does not have enough coins to rob!")
        return
    if random.random() < 0.5:
        amount = random.randint(50, balances[target_id] // 2)
        balances[user_id] += amount
        balances[target_id] -= amount
        save_balances()
        await interaction.response.send_message(f"You successfully robbed {amount} coins from {member.name}! Your new balance is: {balances[user_id]} coins")
    else:
        amount = random.randint(20, 50)
        balances[user_id] = max(0, balances[user_id] - amount)
        save_balances()
        await interaction.response.send_message(f"You got caught and lost {amount} coins! Your new balance is: {balances[user_id]} coins")

@bot.tree.command()
async def deposit(interaction: discord.Interaction, amount: int):
    """Deposit coins into your bank"""
    user_id = str(interaction.user.id)
    if balances.get(user_id, 0) >= amount:
        balances[user_id] -= amount
        balances[f"{user_id}_bank"] = balances.get(f"{user_id}_bank", 0) + amount
        save_balances()
        await interaction.response.send_message(f"You deposited {amount} coins into your bank! Your new balance is: {balances[user_id]} coins")
    else:
        await interaction.response.send_message("You don't have enough coins to deposit!")
@bot.tree.command()
async def withdraw(interaction: discord.Interaction, amount: int):
    """Withdraw coins from your bank"""
    user_id = str(interaction.user.id)
    if balances.get(f"{user_id}_bank", 0) >= amount:
        balances[f"{user_id}_bank"] -= amount
        balances[user_id] += amount
        save_balances()
        await interaction.response.send_message(f"You withdrew {amount} coins from your bank! Your new balance is: {balances[user_id]} coins")
    else:
        await interaction.response.send_message("You don't have enough coins in your bank to withdraw!")


@bot.tree.command()
@commands.cooldown(1,86400,commands.BucketType.user)
async def payday(interaction: discord.Interaction):
    """Claim your payday reward"""
    user_id = str(interaction.user.id)
    now = datetime.utcnow()
    last_claim = balances.get(f"{user_id}_last_claim", None)
    if last_claim:
        last_claim = datetime.strptime(last_claim, "%Y-%m-%d %H:%M:%S")
        if now - last_claim < timedelta(days=1):
            await interaction.response.send_message("You have already claimed your payday. Try again later.")
            return
    balances[user_id] = balances.get(user_id, 0) + 500
    balances[f"{user_id}_last_claim"] = now.strftime("%Y-%m-%d %H:%M:%S")
    save_balances()
    await interaction.response.send_message("You have claimed your payday of 500 coins!")

        
        
     
@bot.tree.command()
async def bet(interaction: discord.Interaction, amount: int, choice: str):
    """Bet on heads or tails"""
    user_id = str(interaction.user.id)
    if balances.get(user_id, 0) < amount:
        await interaction.response.send_message("You don't have enough coins to bet!")
        return
    if choice.lower() not in ["heads", "tails"]:
        await interaction.response.send_message("Invalid choice! Choose 'heads' or 'tails'.")
        return
    result = "heads" if random.random() < 0.5 else "tails"
    if result == choice.lower():
        balances[user_id] += amount
        await interaction.response.send_message(f"You won the bet! The coin landed on {result}. Your new balance is: {balances[user_id]} coins")
    else:
        balances[user_id] -= amount
        await interaction.response.send_message(f"You lost the bet! The coin landed on {result}. Your new balance is: {balances[user_id]} coins")
    save_balances()

@bot.tree.command()
async def inventory(interaction: discord.Interaction):
    """Show your inventory"""
    user_id = str(interaction.user.id)
    inventory = balances.get(f"{user_id}_inventory", {})
    if not inventory:
        await interaction.response.send_message("Your inventory is empty!")
        return
    embed = discord.Embed(title=f"{interaction.user.name}'s Inventory", color=0xf8504c)
    for item, quantity in inventory.items():
        embed.add_field(name=item, value=f"Quantity: {quantity}", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command()
async def give(interaction: discord.Interaction, member: discord.Member, item: str, quantity: int):
    """Give an item to another user"""
    user_id = str(interaction.user.id)
    target_id = str(member.id)
    inventory = balances.get(f"{user_id}_inventory", {})
    if item not in inventory or inventory[item] < quantity:
        await interaction.response.send_message("You don't have enough of this item to give!")
        return
    inventory[item] -= quantity
    if inventory[item] == 0:
        del inventory[item]
    balances[f"{user_id}_inventory"] = inventory
    target_inventory = balances.get(f"{target_id}_inventory", {})
    target_inventory[item] = target_inventory.get(item, 0) + quantity
    balances[f"{target_id}_inventory"] = target_inventory
    save_balances()
    await interaction.response.send_message(f"You gave {quantity} {item}(s) to {member.name}!")

@bot.tree.command()
async def steal(interaction: discord.Interaction, member: discord.Member):
    """Attempt to steal an item from another user"""
    user_id = str(interaction.user.id)
    target_id = str(member.id)
    if user_id == target_id:
        await interaction.response.send_message("You cannot steal from yourself!")
        return
    target_inventory = balances.get(f"{target_id}_inventory", {})
    if not target_inventory:
        await interaction.response.send_message(f"{member.name} has nothing to steal!")
        return
    item, quantity = random.choice(list(target_inventory.items()))
    if random.random() < 0.5:
        target_inventory[item] -= 1
        if target_inventory[item] == 0:
            del target_inventory[item]
        balances[f"{target_id}_inventory"] = target_inventory
        user_inventory = balances.get(f"{user_id}_inventory", {})
        user_inventory[item] = user_inventory.get(item, 0) + 1
        balances[f"{user_id}_inventory"] = user_inventory
        save_balances()
        await interaction.response.send_message(f"You successfully stole 1 {item} from {member.name}!")
    else:
        await interaction.response.send_message(f"You got caught trying to steal from {member.name}!")


@bot.tree.command()
async def lottery(interaction: discord.Interaction, amount: int):
    """Enter the lottery"""
    user_id = str(interaction.user.id)
    if balances.get(user_id, 0) < amount:
        await interaction.response.send_message("You don't have enough coins to enter the lottery!")
        return
    balances[user_id] -= amount
    lottery_pool = balances.get("lottery_pool", 0) + amount
    balances["lottery_pool"] = lottery_pool
    participants = balances.get("lottery_participants", [])
    participants.append(user_id)
    balances["lottery_participants"] = participants
    save_balances()
    await interaction.response.send_message(f"You entered the lottery with {amount} coins! The current pool is {lottery_pool} coins.")

@bot.tree.command()
async def draw_lottery(interaction: discord.Interaction):
    """Draw a winner for the lottery"""
    if "lottery_participants" not in balances or not balances["lottery_participants"]:
        await interaction.response.send_message("No one has entered the lottery yet!")
        return
    winner_id = random.choice(balances["lottery_participants"])
    lottery_pool = balances.get("lottery_pool", 0)
    balances[winner_id] = balances.get(winner_id, 0) + lottery_pool
    balances["lottery_pool"] = 0
    balances["lottery_participants"] = []
    save_balances()
    winner = await bot.fetch_user(int(winner_id))
    await interaction.response.send_message(f"The lottery winner is {winner.name}! They have won {lottery_pool} coins!")





#-------------------------------------------------------------------------------
#                          FUN COMMANDS
#-------------------------------------------------------------------------------
@bot.tree.command()
async def roll(interaction: discord.Interaction, sides: int = 6):
    """Roll a dice"""
    result = random.randint(1, sides)
    await interaction.response.send_message(f"You rolled a {result} on a {sides}-sided dice.")

@bot.tree.command()
async def flip(interaction: discord.Interaction):
    """Flip a coin"""
    result = random.choice(["Heads", "Tails"])
    await interaction.response.send_message(f"The coin landed on {result}.")

@bot.tree.command()
async def joke(interaction: discord.Interaction):
    """Tell a random joke"""
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    if response.status_code == 200:
        joke = response.json()
        await interaction.response.send_message(f"{joke['setup']} - {joke['punchline']}")
    else:
        await interaction.response.send_message("Couldn't fetch a joke at the moment. Try again later.")

@bot.tree.command()
async def meme(interaction: discord.Interaction):
    """Send a random meme"""
    response = requests.get("https://meme-api.herokuapp.com/gimme")
    if response.status_code == 200:
        meme = response.json()
        embed = discord.Embed(title=meme['title'])
        embed.set_image(url=meme['url'])
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message("Couldn't fetch a meme at the moment. Try again later.")

@bot.tree.command()
async def eightball(interaction: discord.Interaction, question: str):
    """Ask the magic 8-ball a question"""
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes – definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    answer = random.choice(responses)
    await interaction.response.send_message(f"Question: {question}\nAnswer: {answer}")


#-------------------------------------------------------------------------------
#                          GIVEAWAY COMMANDS
#-------------------------------------------------------------------------------

giveaways = {}

@bot.tree.command()
@commands.has_permissions(manage_guild=True)
async def start_giveaway(interaction: discord.Interaction, prize: str, duration: int):
    """Start a giveaway"""
    if interaction.user.guild_permissions.manage_guild:
        embed = discord.Embed(title="Giveaway", description=f"Prize: {prize}\nDuration: {duration} minutes", color=0xf8504c)
        embed.set_footer(text="React with 🎉 to enter!")
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()
        await message.add_reaction("🎉")

        giveaways[message.id] = {
            "prize": prize,
            "end_time": discord.utils.utcnow() + timedelta(minutes=duration),
            "message_id": message.id,
            "channel_id": interaction.channel_id,
            "guild_id": interaction.guild_id
        }

        await asyncio.sleep(duration * 60)

        message = await interaction.channel.fetch_message(message.id)
        reaction = discord.utils.get(message.reactions, emoji="🎉")
        users = [user async for user in reaction.users() if user != bot.user]

        if len(users) > 0:
            winner = random.choice(users)
            await interaction.channel.send(f"Congratulations {winner.mention}! You won the giveaway for {prize}!")
        else:
            await interaction.channel.send("No one entered the giveaway.")
    else:
        embed = discord.Embed(description="You lack `Manage Guild` permissions to use this command.", color=0xFF0000)
        await interaction.response.send_message(embed=embed)


@bot.tree.command()
@commands.has_permissions(manage_guild=True)
async def end_giveaway(interaction: discord.Interaction, message_id: int):
    """End a giveaway early"""
    if message_id in giveaways:
        giveaway = giveaways[message_id]
        channel = bot.get_channel(giveaway["channel_id"])
        message = await channel.fetch_message(giveaway["message_id"])
        users = await message.reactions[0].users().flatten()
        users.remove(bot.user)

        if len(users) > 0:
            winner = random.choice(users)
            await channel.send(f"Congratulations {winner.mention}! You won the giveaway for {giveaway['prize']}!")
        else:
            await channel.send("No one entered the giveaway.")
        
        del giveaways[message_id]
    else:
        await interaction.response.send_message("Giveaway not found.")

@bot.tree.command()
async def enter_giveaway(interaction: discord.Interaction, message_id: int):
    """Enter a giveaway"""
    if message_id in giveaways:
        message = await interaction.channel.fetch_message(message_id)
        await message.add_reaction("🎉")
        await interaction.response.send_message("You have entered the giveaway!")
    else:
        await interaction.response.send_message("Giveaway not found.")


#-------------------------------------------------------------------------------
#                          TICKET SYSTEM
#-------------------------------------------------------------------------------

ticket_category_name = "Tickets"

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(CreateTicketButton())

class CreateTicketButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="🎫 Create Ticket", style=discord.ButtonStyle.green)

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name=ticket_category_name)
        if category is None:
            category = await guild.create_category(ticket_category_name)

        ticket_channel = await category.create_text_channel(f"ticket-{interaction.user.name}")
        await ticket_channel.set_permissions(interaction.guild.default_role, read_messages=False)
        await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        embed = discord.Embed(title="Ticket Created", description="Be Patient! \n A staff member will be with you shortly. \n Commnicate with them and feel free to close this ticket wheneever you want.", color=0xf8504c)
        await ticket_channel.send(f"{interaction.user.mention}", embed=embed, view=CloseTicketView())
        await interaction.response.send_message(f"Ticket created: {ticket_channel.mention}", ephemeral=True)

class CloseTicketButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="🔒 Close Ticket", style=discord.ButtonStyle.red)

    async def callback(self, interaction: discord.Interaction):
        if interaction.channel.category and interaction.channel.category.name == ticket_category_name:
            await interaction.channel.delete()
        else:
            await interaction.response.send_message("This command can only be used in a ticket channel.", ephemeral=True)

class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(CloseTicketButton())

@bot.tree.command()
@commands.has_guild_permissions(manage_channels=True)
async def ticket(interaction: discord.Interaction):
    """Send a message with a button to create a ticket"""
    if interaction.user.guild_permissions.manage_messages:
        embed = discord.Embed(title="Support Ticket", description="Click the `🎫 Create Ticket` button to create a ticket and contact with an admin/mod of this server. \n You can close the ticket whenever you want.", color=0xf8504c)
        await interaction.response.send_message(embed=embed, view=TicketView())
    else:
        embed = discord.Embed(description="You lack `Manage Messages` permission to use this command.", color=0xFF0000)
        await interaction.response.send_message(embed=embed) 

@bot.tree.command()
async def ticket_use_info(interaction: discord.Interaction):
    """Tells how to use tickets"""
    embed = discord.Embed(
        title="To Use tickets",
        description="click the button below to create a ticket and a ticket will be created and a staff member will be with you shortly. \n\n For Staffs: Create a category named: `Tickets` and inside it make a channel and type `/ticket` to `get started`",
        color = 0xf8504c
    )
    await interaction.response.send_message(embed=embed)


#-------------------------------------------------------------------------------
#                          VERIFICATION COMMANDS
#-------------------------------------------------------------------------------

class VerificationView(discord.ui.View):
    def __init__(self, submission_id):
        super().__init__(timeout=None)
        self.submission_id = submission_id

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green)
    async def approve(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.submission_id in submissions:
            submissions[self.submission_id]["status"] = "Approved"
            save_submissions()
            await interaction.response.send_message(f"Submission '{self.submission_id}' has been approved!", ephemeral=True)
        else:
            await interaction.response.send_message("Submission not found.", ephemeral=True)

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red)
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.submission_id in submissions:
            submissions[self.submission_id]["status"] = "Rejected"
            save_submissions()
            await interaction.response.send_message(f"Submission '{self.submission_id}' has been rejected!", ephemeral=True)
        else:
            await interaction.response.send_message("Submission not found.", ephemeral=True)

@bot.tree.command(name="submit_screenshot", description="Submit a screenshot for verification")
async def submit_screenshot(interaction: discord.Interaction, screenshot: discord.Attachment):
    """Submit a screenshot for verification"""
    submission_id = str(len(submissions) + 1)
    submissions[submission_id] = {
        "user_id": str(interaction.user.id),
        "screenshot_url": screenshot.url,
        "status": "Pending"
    }
    save_submissions()
    await interaction.response.send_message(f"Screenshot submitted successfully! Submission ID: {submission_id}")

@bot.tree.command(name="view_submissions", description="View all submissions")
@commands.has_permissions(administrator=True)
async def view_submissions(interaction: discord.Interaction):
    """View all submissions"""
    if interaction.user.guild_permissions.administrator:
        if not submissions:
            await interaction.response.send_message("No submissions found.")
            return

        embed = discord.Embed(title="Submissions", color=0xf8504c)
        for submission_id, submission in submissions.items():
            user = await bot.fetch_user(int(submission["user_id"]))
            embed.add_field(name=f"Submission ID: {submission_id}", value=f"User: {user.name}\nStatus: {submission['status']}\n[View Screenshot]({submission['screenshot_url']})", inline=False)
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(description="You lack `Administrator` permissions to use this command.", color=0xFF0000)
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="manage_submission", description="Manage a submission")
@commands.has_permissions(administrator=True)
async def manage_submission(interaction: discord.Interaction, submission_id: str):
    """Manage a submission"""
    if interaction.user.guild_permissions.administrator:
        if submission_id in submissions:
            submission = submissions[submission_id]
            user = await bot.fetch_user(int(submission["user_id"]))
            embed = discord.Embed(title=f"Manage Submission: {submission_id}", color=0xf8504c)
            embed.add_field(name="User", value=user.name, inline=False)
            embed.add_field(name="Status", value=submission["status"], inline=False)
            embed.add_field(name="Screenshot", value=f"[View Screenshot]({submission['screenshot_url']})", inline=False)
            view = VerificationView(submission_id)
            await interaction.response.send_message(embed=embed, view=view)
        else:
            await interaction.response.send_message("Submission not found.")
    else:
        embed = discord.Embed(description="You lack `Administrator` permissions to use this command.", color=0xFF0000)
        await interaction.response.send_message(embed=embed)

#-------------------------------------------------------------------------------
#                          SCRIMS MANAGER
#-------------------------------------------------------------------------------

class ScrimsManager(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Scrim", style=discord.ButtonStyle.green)
    async def create_scrim(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CreateScrimModal())

    @discord.ui.button(label="Edit Settings", style=discord.ButtonStyle.blurple)
    async def edit_settings(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EditSettingsModal())

    @discord.ui.button(label="Start/Stop Registration", style=discord.ButtonStyle.green)
    async def start_stop_reg(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(StartStopRegModal())

    @discord.ui.button(label="Reserve Slots", style=discord.ButtonStyle.green)
    async def reserve_slots(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ReserveSlotsModal())

    @discord.ui.button(label="Close Scrim", style=discord.ButtonStyle.red)
    async def close_scrim(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CloseScrimModal())

class CreateScrimModal(discord.ui.Modal, title="Create Scrim"):
    scrim_name = discord.ui.TextInput(label="Scrim Name", placeholder="Enter the scrim name")
    scrim_date = discord.ui.TextInput(label="Scrim Date", placeholder="Enter the scrim date")

    async def on_submit(self, interaction: discord.Interaction):
        server_id = str(interaction.guild.id)
        if server_id not in scrims:
            scrims[server_id] = {}
        scrim_id = str(len(scrims[server_id]) + 1)
        scrims[server_id][scrim_id] = {
            "name": self.scrim_name.value,
            "date": self.scrim_date.value,
            "participants": [],
            "started": False,
            "ended": False
        }
        save_scrims()
        await interaction.response.send_message(f"Scrim '{self.scrim_name.value}' created successfully! \nYour Scrim ID: `{scrim_id}` \n⚠️ **KEEP IT PRIVATE AND NOTED! IT WILL BE REQUIRED IN FUTURE!**", ephemeral=True)

class EditSettingsModal(discord.ui.Modal, title="Edit Scrim Settings"):
    scrim_id = discord.ui.TextInput(label="Scrim ID", placeholder="Enter the scrim ID")
    scrim_name = discord.ui.TextInput(label="Scrim Name", placeholder="Enter the new scrim name", required=False)
    scrim_date = discord.ui.TextInput(label="Scrim Date", placeholder="Enter the new scrim date", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        server_id = str(interaction.guild.id)
        if server_id in scrims and self.scrim_id.value in scrims[server_id]:
            if self.scrim_name.value:
                scrims[server_id][self.scrim_id.value]["name"] = self.scrim_name.value
            if self.scrim_date.value:
                scrims[server_id][self.scrim_id.value]["date"] = self.scrim_date.value
            save_scrims()
            await interaction.response.send_message(f"Scrim '{self.scrim_id.value}' updated successfully!", ephemeral=True)
        else:
            await interaction.response.send_message("Scrim not found.", ephemeral=True)

class StartStopRegModal(discord.ui.Modal, title="Start/Stop Registration"):
    scrim_id = discord.ui.TextInput(label="Scrim ID", placeholder="Enter the scrim ID")

    async def on_submit(self, interaction: discord.Interaction):
        server_id = str(interaction.guild.id)
        if server_id in scrims and self.scrim_id.value in scrims[server_id]:
            scrims[server_id][self.scrim_id.value]["started"] = not scrims[server_id][self.scrim_id.value]["started"]
            save_scrims()
            status = "started" if scrims[server_id][self.scrim_id.value]["started"] else "stopped"
            await interaction.response.send_message(f"Registration for scrim '{self.scrim_id.value}' has been {status}.", ephemeral=True)
        else:
            await interaction.response.send_message("Scrim not found.", ephemeral=True)

class ReserveSlotsModal(discord.ui.Modal, title="Reserve Slots"):
    scrim_id = discord.ui.TextInput(label="Scrim ID", placeholder="Enter the scrim ID")
    slots = discord.ui.TextInput(label="Slots", placeholder="Enter the number of slots to reserve")

    async def on_submit(self, interaction: discord.Interaction):
        server_id = str(interaction.guild.id)
        if server_id in scrims and self.scrim_id.value in scrims[server_id]:
            scrims[server_id][self.scrim_id.value]["reserved_slots"] = int(self.slots.value)
            save_scrims()
            await interaction.response.send_message(f"{self.slots.value} slots reserved for scrim '{self.scrim_id.value}'.", ephemeral=True)
        else:
            await interaction.response.send_message("Scrim not found.", ephemeral=True)

class CloseScrimModal(discord.ui.Modal, title="Close Scrim"):
    scrim_id = discord.ui.TextInput(label="Scrim ID", placeholder="Enter the scrim ID")

    async def on_submit(self, interaction: discord.Interaction):
        server_id = str(interaction.guild.id)
        if server_id in scrims and self.scrim_id.value in scrims[server_id]:
            scrims[server_id][self.scrim_id.value]["ended"] = True
            save_scrims()
            await interaction.response.send_message(f"Scrim '{self.scrim_id.value}' has been closed.", ephemeral=True)
        else:
            await interaction.response.send_message("Scrim not found.", ephemeral=True)

class ScrimDropdown(discord.ui.Select):
    def __init__(self, server_id):
        options = [
            discord.SelectOption(label=scrim["name"], description=scrim["date"], value=scrim_id)
            for scrim_id, scrim in scrims.get(server_id, {}).items()
        ]
        super().__init__(placeholder="Select a scrim...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        scrim_id = self.values[0]
        server_id = str(interaction.guild.id)
        scrim = scrims[server_id][scrim_id]
        embed = discord.Embed(title=f"Scrim: {scrim['name']}", color=0xf8504c)
        embed.add_field(name="Date", value=scrim["date"], inline=False)
        embed.add_field(name="Participants", value=f"{len(scrim['participants'])}", inline=False)
        embed.add_field(name="Started", value="Yes" if scrim["started"] else "No", inline=False)
        embed.add_field(name="Ended", value="Yes" if scrim["ended"] else "No", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class ScrimDropdownView(discord.ui.View):
    def __init__(self, server_id):
        super().__init__(timeout=None)
        self.add_item(ScrimDropdown(server_id))

@bot.tree.command(name="smanager", description="Smart Scrims Manager")
async def smanager(interaction: discord.Interaction):
    """Smart Scrims Manager"""
    if interaction.user.guild_permissions.manage_messages:
        view = ScrimsManager()
        dropdown_view = ScrimDropdownView(str(interaction.guild.id))
        server_id = str(interaction.guild.id)
        total = sum(1 for scrim in scrims.get(server_id, {}).values())
        embed = discord.Embed(description="[**ArstoCate's Smart Scrims Manager**](<https://discord.gg/CxJdyezkyx>)", color=0xf8504c)
        embed.set_footer(text=f"Total Scrims in this server: {total}", icon_url=interaction.user.avatar.url)
        embed.add_field(name="`Scrims Channel:`", value=f"{interaction.channel.mention}", inline=False)
        await interaction.response.send_message(embed=embed, view=view)
        await interaction.followup.send("Select a scrim to view details:", view=dropdown_view, ephemeral=True)
    else:
        embed = discord.Embed(description="You lack `Manage Messages` permission to use this command.", color=0xFF0000)
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="register_scrim", description="Register for a scrim")
async def register_scrim(interaction: discord.Interaction, scrim_id: str):
    """Register for a scrim"""
    server_id = str(interaction.guild.id)
    if scrim_id in scrims.get(server_id, {}):
        scrim = scrims[server_id][scrim_id]
        if scrim["started"] and not scrim["ended"]:
            if interaction.user.id not in scrim["participants"]:
                if interaction.user.id not in banlist:
                    scrim["participants"].append(interaction.user.id)
                    save_scrims()
                    await interaction.response.send_message(f"You have successfully registered for scrim '{scrim['name']}'!", ephemeral=True)
                else:
                    await interaction.response.send_message("You are banned from participating in scrims.", ephemeral=True)
            else:
                await interaction.response.send_message("You are already registered for this scrim.", ephemeral=True)
        else:
            await interaction.response.send_message("Registration for this scrim is not open.", ephemeral=True)
    else:
        await interaction.response.send_message("Scrim not found.", ephemeral=True)

@bot.tree.command(name="upcoming_scrims", description="List upcoming scrims")
async def upcoming_scrims(interaction: discord.Interaction):
    """List upcoming scrims"""
    server_id = str(interaction.guild.id)
    upcoming = [scrim for scrim in scrims.get(server_id, {}).values() if not scrim["ended"]]
    if not upcoming:
        await interaction.response.send_message("No upcoming scrims found.", ephemeral=True)
        return

    embed = discord.Embed(title="Upcoming Scrims", color=0xf8504c)
    for scrim in upcoming:
        embed.add_field(name=scrim["name"], value=f"Date: {scrim['date']}\nParticipants: {len(scrim['participants'])}", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="past_scrims", description="List past scrims")
async def past_scrims(interaction: discord.Interaction):
    """List past scrims"""
    server_id = str(interaction.guild.id)
    past = [scrim for scrim in scrims.get(server_id, {}).values() if scrim["ended"]]
    if not past:
        await interaction.response.send_message("No past scrims found.", ephemeral=True)
        return

    embed = discord.Embed(title="Past Scrims", color=0xf8504c)
    for scrim in past:
        embed.add_field(name=scrim["name"], value=f"Date: {scrim['date']}\nParticipants: {len(scrim['participants'])}", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="slotmanager", description="Manage slots for a scrim")
async def slotmanager(interaction: discord.Interaction, scrim_id: str, action: str, slots: int = 0):
    """Manage slots for a scrim"""
    if interaction.user.guild_permissions.manage_messages:
        server_id = str(interaction.guild.id)
        if scrim_id in scrims.get(server_id, {}):
            scrim = scrims[server_id][scrim_id]
            if action == "view":
                reserved_slots = scrim.get("reserved_slots", 0)
                await interaction.response.send_message(f"Scrim '{scrim['name']}' has {reserved_slots} reserved slots.", ephemeral=True)
            elif action == "add":
                scrim["reserved_slots"] = scrim.get("reserved_slots", 0) + slots
                save_scrims()
                await interaction.response.send_message(f"Added {slots} slots to scrim '{scrim['name']}'. Total reserved slots: {scrim['reserved_slots']}", ephemeral=True)
            elif action == "remove":
                scrim["reserved_slots"] = max(0, scrim.get("reserved_slots", 0) - slots)
                save_scrims()
                await interaction.response.send_message(f"Removed {slots} slots from scrim '{scrim['name']}'. Total reserved slots: {scrim['reserved_slots']}", ephemeral=True)
            else:
                await interaction.response.send_message("Invalid action. Use 'view', 'add', or 'remove'.", ephemeral=True)
        else:
            await interaction.response.send_message("Scrim not found.", ephemeral=True)
    else:
        embed = discord.Embed(description="You lack `Manage Messages` permission to use this command.", color=0xFF0000)
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="banlogs", description="View the ban logs of the server")
@commands.has_permissions(administrator=True)
async def banlogs(interaction: discord.Interaction):
    """View the ban logs of the server"""
    bans = await interaction.guild.bans()
    if not bans:
        await interaction.response.send_message("No bans found.", ephemeral=True)
        return

    embed = discord.Embed(title="Ban Logs", color=0xFF0000)
    for ban_entry in bans:
        user = ban_entry.user
        reason = ban_entry.reason if ban_entry.reason else "No reason provided"
        embed.add_field(name=user.name, value=f"Reason: {reason}", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="ban_from_scrims", description="Ban a user from participating in scrims")
@commands.has_permissions(administrator=True)
async def ban_from_scrims(interaction: discord.Interaction, user: discord.User):
    """Ban a user from participating in scrims"""
    if user.id not in banlist:
        banlist.append(user.id)
        save_banlist()
        await interaction.response.send_message(f"{user.name} has been banned from participating in scrims.", ephemeral=True)
    else:
        await interaction.response.send_message(f"{user.name} is already banned from participating in scrims.", ephemeral=True)

@bot.tree.command(name="total_scrims", description="Count the total number of scrims hosted in this server")
async def total_scrims(interaction: discord.Interaction):
    """Count the total number of scrims hosted in this server"""
    server_id = str(interaction.guild.id)
    total = sum(1 for scrim in scrims.get(server_id, {}).values())
    await interaction.response.send_message(f"Total scrims hosted in this server: {total}", ephemeral=True)

@bot.tree.command(name="start_scrim", description="Start a scrim and ping the scrims role")
@commands.has_permissions(manage_messages=True)
async def start_scrim(interaction: discord.Interaction, scrim_id: str):
    """Start a scrim and ping the scrims role"""
    server_id = str(interaction.guild.id)
    if scrim_id in scrims.get(server_id, {}):
        scrim = scrims[server_id][scrim_id]
        if not scrim["started"] and not scrim["ended"]:
            scrim["started"] = True
            save_scrims()
            scrims_channel = discord.utils.get(interaction.guild.text_channels, name="scrims")
            scrims_role = discord.utils.get(interaction.guild.roles, name="Scrims")
            if scrims_channel and scrims_role:
                await scrims_channel.send(f"{scrims_role.mention} Scrim '{scrim['name']}' has started! Join now!")
                await interaction.response.send_message(f"Scrim '{scrim['name']}' has been started and the scrims role has been pinged.", ephemeral=True)
            else:
                await interaction.response.send_message("Scrims channel or Scrims role not found.", ephemeral=True)
        else:
            await interaction.response.send_message("Scrim has already started or ended.", ephemeral=True)
    else:
        await interaction.response.send_message("Scrim not found.", ephemeral=True)


@bot.tree.command(name="end_scrim", description="End a scrim and ping the scrims role")
@commands.has_permissions(manage_messages=True)
async def end_scrim(interaction: discord.Interaction, scrim_id: str):
    """End a scrim and ping the scrims role"""
    server_id = str(interaction.guild.id)
    if scrim_id in scrims.get(server_id, {}):
        scrim = scrims[server_id][scrim_id]
        if scrim["started"] and not scrim["ended"]:
            scrim["ended"] = True
            save_scrims()
            scrims_channel = discord.utils.get(interaction.guild.text_channels, name="scrims")
            scrims_role = discord.utils.get(interaction.guild.roles, name="Scrims")
            if scrims_channel and scrims_role:
                await scrims_channel.send(f"{scrims_role.mention} Scrim '{scrim['name']}' has ended. Thank you for participating!")
                await interaction.response.send_message(f"Scrim '{scrim['name']}' has been ended and the scrims role has been pinged.", ephemeral=True)
            else:
                await interaction.response.send_message("Scrims channel or Scrims role not found.", ephemeral=True)


#-------------------------------------------------------------------------------
#                          DISCORD_BOT_TOKEN
#-------------------------------------------------------------------------------

bot.run(config.DISCORD_TOKEN)
