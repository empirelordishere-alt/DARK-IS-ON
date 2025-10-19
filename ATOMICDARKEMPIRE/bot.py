"""
🌑 ATOMIC DARK EMPIRE BOT
A complete Discord server management system with economy, teams, marketplace & moderation
"""

import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import asyncio
from typing import Optional

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID', 0))
PREFIX = os.getenv('PREFIX', '!')

# Bot setup with all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# Import data manager
from data_manager import DataManager
data = DataManager()

# XP cooldowns (user_id: last_message_time)
xp_cooldowns = {}

# 20 ELITE TEAMS CONFIGURATION
TEAMS = {
    'blood_vampires': {'name': '🩸 Blood Vampires', 'color': 0xFF0000, 'emoji': '🩸'},
    'shadow_phantoms': {'name': '👻 Shadow Phantoms', 'color': 0x2F4F4F, 'emoji': '👻'},
    'toxic_mutants': {'name': '🧪 Toxic Mutants', 'color': 0x00FF00, 'emoji': '🧪'},
    'soul_collectors': {'name': '💀 Soul Collectors', 'color': 0x808080, 'emoji': '💀'},
    'dark_warlocks': {'name': '🔮 Dark Warlocks', 'color': 0x9400D3, 'emoji': '🔮'},
    'hellfire_demons': {'name': '🔥 Hellfire Demons', 'color': 0xFF4500, 'emoji': '🔥'},
    'void_reapers': {'name': '⚫ Void Reapers', 'color': 0x000000, 'emoji': '⚫'},
    'ghost_apparitions': {'name': '⚪ Ghost Apparitions', 'color': 0xFFFFFF, 'emoji': '⚪'},
    'nightmare_creatures': {'name': '🌈 Nightmare Creatures', 'color': 0x8B00FF, 'emoji': '🌈'},
    'crystal_wraiths': {'name': '💎 Crystal Wraiths', 'color': 0x00FFFF, 'emoji': '💎'},
    'abyssal_horrors': {'name': '🌊 Abyssal Horrors', 'color': 0x0000FF, 'emoji': '🌊'},
    'volcanic_demons': {'name': '🌋 Volcanic Demons', 'color': 0xFF7F50, 'emoji': '🌋'},
    'storm_horrors': {'name': '⚡ Storm Horrors', 'color': 0xFFFF00, 'emoji': '⚡'},
    'cosmic_terrors': {'name': '🌌 Cosmic Terrors', 'color': 0x000080, 'emoji': '🌌'},
    'lunar_cults': {'name': '🌙 Lunar Cults', 'color': 0xC0C0C0, 'emoji': '🌙'},
    'eclipse_cults': {'name': '☀ Eclipse Cults', 'color': 0xFFA500, 'emoji': '☀'},
    'forest_haunts': {'name': '🌿 Forest Haunts', 'color': 0x228B22, 'emoji': '🌿'},
    'mountain_wraiths': {'name': '🏔 Mountain Wraiths', 'color': 0x696969, 'emoji': '🏔'},
    'inferno_lords': {'name': '🔥 Inferno Lords', 'color': 0xDC143C, 'emoji': '🔥'},
    'frost_specters': {'name': '❄ Frost Specters', 'color': 0xADD8E6, 'emoji': '❄'}
}

# 5 CURRENCIES
CURRENCIES = {
    'soul_fragments': {'name': '💀 Soul Fragments', 'emoji': '💀'},
    'cursed_essence': {'name': '🔮 Cursed Essence', 'emoji': '🔮'},
    'tombstone_coins': {'name': '🪙 Tombstone Coins', 'emoji': '🪙'},
    'lords_blood': {'name': '🩸 Lord\'s Blood', 'emoji': '🩸'},
    'void_crystals': {'name': '💎 Void Crystals', 'emoji': '💎'}
}

# STAFF ROLES FOR SERVER
STAFF_ROLES = {
    'emperor_lord': {'name': '👑 EMPEROR LORD', 'color': 0x8B0000, 'permissions': discord.Permissions.all()},
    'emperor_lord_hand': {'name': '🗡️ EMPEROR LORD HAND', 'color': 0xFF0000, 'permissions': discord.Permissions(administrator=True)},
    'emperor_helper': {'name': '⚔️ EMPEROR HELPER', 'color': 0xFF4500, 'permissions': discord.Permissions(kick_members=True, ban_members=True, manage_messages=True, moderate_members=True)}
}


# ============================================================================
# EVENT HANDLERS
# ============================================================================

@bot.event
async def on_ready():
    """Bot startup"""
    print(f"""
    ╔═══════════════════════════════════════════════════════════════╗
    ║  🌑 ATOMIC DARK EMPIRE BOT IS ONLINE                         ║
    ║  Bot: {bot.user.name}                                        
    ║  ID: {bot.user.id}                                           
    ║  Servers: {len(bot.guilds)}                                  
    ║  Prefix: {PREFIX}                                            
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="🌑 Dark Empire | !help"))


@bot.event
async def on_member_join(member):
    """Welcome new members with starter currency"""
    # Initialize user data
    data.init_user(member.id)
    user_data = data.get_user(member.id)
    user_data['currencies']['soul_fragments'] += 1000
    data.save_economy()
    
    # Send welcome message
    welcome_channel = discord.utils.get(member.guild.text_channels, name='welcome')
    if welcome_channel:
        embed = discord.Embed(
            title=f"🌑 Welcome to the Dark Empire, {member.name}!",
            description=f"You have been granted **1,000 💀 Soul Fragments** to begin your journey.\n\n"
                       f"Type `{PREFIX}help` to see all commands\n"
                       f"Type `{PREFIX}teams` to view teams\n"
                       f"Type `{PREFIX}daily` to claim daily rewards",
            color=0x000000
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="🌑 Dark Empire Bot")
        await welcome_channel.send(embed=embed)


@bot.event
async def on_message(message):
    """Auto XP gain from messages"""
    if message.author.bot:
        await bot.process_commands(message)
        return
    
    user_id = message.author.id
    current_time = datetime.now()
    
    # XP cooldown check (60 seconds)
    if user_id in xp_cooldowns:
        time_diff = (current_time - xp_cooldowns[user_id]).total_seconds()
        if time_diff < 60:
            await bot.process_commands(message)
            return
    
    # Grant XP
    data.init_user(user_id)
    user_data = data.get_user(user_id)
    
    old_level = user_data['level']
    user_data['xp'] += 15
    user_data['messages'] += 1
    
    # Level up check
    xp_needed = 100 * (old_level ** 1.5)
    if user_data['xp'] >= xp_needed:
        user_data['level'] += 1
        user_data['xp'] = 0
        
        # Level up rewards
        rewards = {
            'soul_fragments': 100 * user_data['level'],
            'cursed_essence': 10 * user_data['level'],
            'tombstone_coins': 50 * user_data['level']
        }
        
        for currency, amount in rewards.items():
            user_data['currencies'][currency] += amount
        
        # Send level up message
        embed = discord.Embed(
            title="⬆️ LEVEL UP!",
            description=f"🎉 {message.author.mention} reached **Level {user_data['level']}**!\n\n"
                       f"**Rewards:**\n"
                       f"💀 {rewards['soul_fragments']:,} Soul Fragments\n"
                       f"🔮 {rewards['cursed_essence']:,} Cursed Essence\n"
                       f"🪙 {rewards['tombstone_coins']:,} Tombstone Coins",
            color=0x8B00FF
        )
        await message.channel.send(embed=embed)
    
    data.save_economy()
    xp_cooldowns[user_id] = current_time
    
    await bot.process_commands(message)


# Load all command cogs
async def load_extensions():
    """Load all command modules"""
    extensions = [
        'commands.economy',
        'commands.teams',
        'commands.marketplace',
        'commands.moderation',
        'commands.server_build',
        'commands.help_admin'
    ]
    
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            print(f"✅ Loaded {ext}")
        except Exception as e:
            print(f"❌ Failed to load {ext}: {e}")


# Run bot
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
