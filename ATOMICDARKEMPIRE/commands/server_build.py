"""
🏗 SERVER BUILDING COMMANDS
!buildatomic, !quickbuild, !simplebuild, !cleanup, !setupwelcome, !serverstats
Creates the complete 20-team Dark Empire structure with roles, channels, and permissions
"""

import discord
from discord.ext import commands
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot import TEAMS, STAFF_ROLES

OWNER_ID = int(os.getenv('OWNER_ID', 0))


class ServerBuild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        from data_manager import DataManager
        self.data = bot.data if hasattr(bot, 'data') else DataManager()
        if not hasattr(bot, 'data'):
            bot.data = self.data
    
    async def create_team_structure(self, guild: discord.Guild, team_id: str, team_info: dict, status_msg=None):
        """Create complete structure for a single team"""
        try:
            # Update status
            if status_msg:
                await status_msg.edit(content=f"🏗️ Building {team_info['name']}...")
            
            # Create 3 roles: Member, Lord, Lord Hand
            member_role = await guild.create_role(
                name=f"{team_info['emoji']} {team_info['name']}",
                color=discord.Color(team_info['color']),
                hoist=True,
                mentionable=True
            )
            await asyncio.sleep(1)  # Rate limit protection
            
            lord_role = await guild.create_role(
                name=f"{team_info['emoji']} {team_info['name']} Lord",
                color=discord.Color(team_info['color']),
                hoist=True,
                mentionable=True
            )
            await asyncio.sleep(1)
            
            hand_role = await guild.create_role(
                name=f"{team_info['emoji']} {team_info['name']} Hand",
                color=discord.Color(team_info['color']),
                hoist=True,
                mentionable=True
            )
            await asyncio.sleep(1)
            
            # Create category with permissions
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True),
                lord_role: discord.PermissionOverwrite(
                    read_messages=True, 
                    send_messages=True, 
                    manage_messages=True,
                    manage_channels=True,
                    connect=True,
                    move_members=True
                ),
                hand_role: discord.PermissionOverwrite(
                    read_messages=True, 
                    send_messages=True, 
                    manage_messages=True,
                    connect=True,
                    move_members=True
                ),
                guild.me: discord.PermissionOverwrite(
                    read_messages=True, 
                    send_messages=True, 
                    manage_channels=True
                )
            }
            
            category = await guild.create_category(
                name=f"{team_info['emoji']} {team_info['name'].upper()}",
                overwrites=overwrites
            )
            await asyncio.sleep(1)
            
            # Create 4 text channels
            await guild.create_text_channel(
                name="💬-chat",
                category=category,
                topic=f"General chat for {team_info['name']}"
            )
            await asyncio.sleep(1)
            
            await guild.create_text_channel(
                name="⚔-strategy",
                category=category,
                topic=f"Team planning and strategy for {team_info['name']}"
            )
            await asyncio.sleep(1)
            
            await guild.create_text_channel(
                name="🎮-commands",
                category=category,
                topic=f"Bot commands for {team_info['name']}"
            )
            await asyncio.sleep(1)
            
            await guild.create_text_channel(
                name="📊-stats",
                category=category,
                topic=f"Team statistics and leaderboards for {team_info['name']}"
            )
            await asyncio.sleep(1)
            
            # Create 1 voice channel
            await guild.create_voice_channel(
                name=f"🎤 {team_info['name']} Voice",
                category=category
            )
            await asyncio.sleep(1)
            
            return True
            
        except Exception as e:
            print(f"Error creating {team_info['name']}: {e}")
            return False
    
    @commands.command(name='buildatomic')
    async def buildatomic(self, ctx):
        """Build ALL 20 teams (Owner only)"""
        if ctx.author.id != OWNER_ID:
            await ctx.send("❌ Only the server owner can use this command!")
            return
        
        # Confirmation
        embed = discord.Embed(
            title="⚠️ BUILD ATOMIC DARK EMPIRE",
            description=f"This will create:\n"
                       f"• **60 Roles** (20 teams × 3 roles each)\n"
                       f"• **20 Categories** (one per team)\n"
                       f"• **80 Text Channels** (4 per team)\n"
                       f"• **20 Voice Channels** (1 per team)\n\n"
                       f"**TOTAL: 180+ items**\n\n"
                       f"⏱️ **Estimated time: 25-30 minutes** (due to Discord rate limits)\n\n"
                       f"Type `confirm` to proceed or `cancel` to abort.",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['confirm', 'cancel']
        
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60.0)
            
            if msg.content.lower() == 'cancel':
                await ctx.send("❌ Build cancelled.")
                return
            
            # Start building
            start_embed = discord.Embed(
                title="🏗️ ATOMIC BUILD INITIATED",
                description="Building 20 complete team structures...\nThis will take approximately 25-30 minutes.",
                color=0x8B00FF
            )
            status_msg = await ctx.send(embed=start_embed)
            
            success_count = 0
            failed = []
            
            for team_id, team_info in TEAMS.items():
                result = await self.create_team_structure(ctx.guild, team_id, team_info, status_msg)
                if result:
                    success_count += 1
                else:
                    failed.append(team_info['name'])
                
                # Update progress
                progress = f"🏗️ Progress: {success_count}/20 teams built"
                await status_msg.edit(content=progress)
            
            # Build complete
            complete_embed = discord.Embed(
                title="✅ ATOMIC BUILD COMPLETE!",
                description=f"**Successfully built {success_count}/20 teams!**\n\n"
                           f"Created:\n"
                           f"• {success_count * 3} Roles\n"
                           f"• {success_count} Categories\n"
                           f"• {success_count * 4} Text Channels\n"
                           f"• {success_count} Voice Channels\n\n"
                           f"Total: {success_count * 8} items created!",
                color=0x00FF00
            )
            
            if failed:
                complete_embed.add_field(
                    name="⚠️ Failed Teams",
                    value="\n".join(failed),
                    inline=False
                )
            
            await ctx.send(embed=complete_embed)
            
        except asyncio.TimeoutError:
            await ctx.send("⏰ Build cancelled (timeout).")
    
    @commands.command(name='quickbuild')
    async def quickbuild(self, ctx):
        """Build 3 test teams (Owner only)"""
        if ctx.author.id != OWNER_ID:
            await ctx.send("❌ Only the server owner can use this command!")
            return
        
        # Build first 3 teams
        test_teams = ['blood_vampires', 'shadow_phantoms', 'toxic_mutants']
        
        embed = discord.Embed(
            title="🏗️ QUICK BUILD",
            description="Building 3 test teams...",
            color=0x8B00FF
        )
        status_msg = await ctx.send(embed=embed)
        
        success_count = 0
        for team_id in test_teams:
            team_info = TEAMS[team_id]
            result = await self.create_team_structure(ctx.guild, team_id, team_info, status_msg)
            if result:
                success_count += 1
        
        complete_embed = discord.Embed(
            title="✅ QUICK BUILD COMPLETE!",
            description=f"Built {success_count}/3 test teams!",
            color=0x00FF00
        )
        await ctx.send(embed=complete_embed)
    
    @commands.command(name='simplebuild')
    async def simplebuild(self, ctx):
        """Build 1 team for testing (Owner only)"""
        if ctx.author.id != OWNER_ID:
            await ctx.send("❌ Only the server owner can use this command!")
            return
        
        # Build Blood Vampires
        team_id = 'blood_vampires'
        team_info = TEAMS[team_id]
        
        embed = discord.Embed(
            title="🏗️ SIMPLE BUILD",
            description=f"Building {team_info['name']}...",
            color=team_info['color']
        )
        await ctx.send(embed=embed)
        
        result = await self.create_team_structure(ctx.guild, team_id, team_info)
        
        if result:
            complete_embed = discord.Embed(
                title="✅ BUILD COMPLETE!",
                description=f"{team_info['name']} has been created!",
                color=0x00FF00
            )
            await ctx.send(embed=complete_embed)
        else:
            await ctx.send("❌ Build failed!")
    
    @commands.command(name='cleanup')
    async def cleanup(self, ctx):
        """Delete ALL team structures (Owner only)"""
        if ctx.author.id != OWNER_ID:
            await ctx.send("❌ Only the server owner can use this command!")
            return
        
        # Confirmation
        embed = discord.Embed(
            title="⚠️ DANGER: CLEANUP ALL TEAMS",
            description=f"This will **DELETE**:\n"
                       f"• All team roles\n"
                       f"• All team categories\n"
                       f"• All team channels\n\n"
                       f"**THIS CANNOT BE UNDONE!**\n\n"
                       f"Type `confirm` to proceed or `cancel` to abort.",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['confirm', 'cancel']
        
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)
            
            if msg.content.lower() == 'cancel':
                await ctx.send("❌ Cleanup cancelled.")
                return
            
            # Start cleanup
            status_msg = await ctx.send("🗑️ Cleaning up...")
            
            deleted_channels = 0
            deleted_roles = 0
            deleted_categories = 0
            
            # Delete channels in team categories
            for category in ctx.guild.categories:
                if any(team_info['emoji'] in category.name for team_info in TEAMS.values()):
                    for channel in category.channels:
                        await channel.delete()
                        deleted_channels += 1
                        await asyncio.sleep(0.5)
                    
                    await category.delete()
                    deleted_categories += 1
                    await asyncio.sleep(0.5)
            
            # Delete team roles
            for role in ctx.guild.roles:
                if any(team_info['emoji'] in role.name for team_info in TEAMS.values()):
                    await role.delete()
                    deleted_roles += 1
                    await asyncio.sleep(0.5)
            
            complete_embed = discord.Embed(
                title="✅ CLEANUP COMPLETE",
                description=f"Deleted:\n"
                           f"• {deleted_channels} channels\n"
                           f"• {deleted_categories} categories\n"
                           f"• {deleted_roles} roles",
                color=0x00FF00
            )
            await ctx.send(embed=complete_embed)
            
        except asyncio.TimeoutError:
            await ctx.send("⏰ Cleanup cancelled (timeout).")
    
    @commands.command(name='setupwelcome')
    async def setupwelcome(self, ctx):
        """Create welcome channel (Owner only)"""
        if ctx.author.id != OWNER_ID:
            await ctx.send("❌ Only the server owner can use this command!")
            return
        
        # Check if welcome channel exists
        existing = discord.utils.get(ctx.guild.text_channels, name='welcome')
        if existing:
            await ctx.send("❌ Welcome channel already exists!")
            return
        
        # Create welcome channel
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        welcome_channel = await ctx.guild.create_text_channel(
            name='welcome',
            overwrites=overwrites,
            topic='🌑 Welcome to the Dark Empire',
            position=0
        )
        
        # Send welcome message
        welcome_embed = discord.Embed(
            title="🌑 WELCOME TO THE DARK EMPIRE",
            description=f"**Welcome to {ctx.guild.name}!**\n\n"
                       f"📜 **Get Started:**\n"
                       f"• Type `!help` to see all commands\n"
                       f"• Type `!teams` to view all teams\n"
                       f"• Type `!daily` to claim daily rewards\n"
                       f"• Type `!wealth` to check your balance\n\n"
                       f"🎯 **Join a Team:**\n"
                       f"• Use `!join <team_id>` to join a team\n"
                       f"• Compete for wealth and glory!\n\n"
                       f"💰 **Earn Currency:**\n"
                       f"• Chat to gain XP and level up\n"
                       f"• Claim daily rewards\n"
                       f"• Trade in the marketplace\n\n"
                       f"🌑 **Rise to Power in the Dark Empire!**",
            color=0x000000
        )
        welcome_embed.set_footer(text="🌑 Dark Empire Bot")
        await welcome_channel.send(embed=welcome_embed)
        
        await ctx.send(f"✅ Welcome channel created: {welcome_channel.mention}")
    
    @commands.command(name='serverstats')
    async def serverstats(self, ctx):
        """View server statistics"""
        guild = ctx.guild
        
        # Count channels
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        
        # Count members
        total_members = guild.member_count
        bots = len([m for m in guild.members if m.bot])
        humans = total_members - bots
        
        # Bot permissions
        bot_perms = guild.me.guild_permissions
        admin = "✅" if bot_perms.administrator else "❌"
        manage_roles = "✅" if bot_perms.manage_roles else "❌"
        manage_channels = "✅" if bot_perms.manage_channels else "❌"
        
        embed = discord.Embed(
            title=f"📊 {guild.name} Statistics",
            color=0x8B00FF
        )
        
        embed.add_field(
            name="👥 Members",
            value=f"Total: {total_members}\nHumans: {humans}\nBots: {bots}",
            inline=True
        )
        
        embed.add_field(
            name="📁 Channels",
            value=f"Text: {text_channels}\nVoice: {voice_channels}\nCategories: {categories}",
            inline=True
        )
        
        embed.add_field(
            name="🎭 Roles",
            value=f"{len(guild.roles)} roles",
            inline=True
        )
        
        embed.add_field(
            name="🤖 Bot Permissions",
            value=f"Admin: {admin}\nManage Roles: {manage_roles}\nManage Channels: {manage_channels}",
            inline=True
        )
        
        embed.add_field(
            name="📅 Server Created",
            value=guild.created_at.strftime("%Y-%m-%d"),
            inline=True
        )
        
        embed.add_field(
            name="👑 Owner",
            value=guild.owner.mention if guild.owner else "Unknown",
            inline=True
        )
        
        # Limits
        embed.add_field(
            name="📊 Discord Limits",
            value=f"Roles: {len(guild.roles)}/250\nChannels: {len(guild.channels)}/500",
            inline=False
        )
        
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.set_footer(text="🌑 Dark Empire Bot")
        
        await ctx.send(embed=embed)
    
    @commands.command(name='setupstaff')
    async def setupstaff(self, ctx):
        """Create EMPEROR staff roles (Owner only)"""
        if ctx.author.id != OWNER_ID:
            await ctx.send("❌ Only the server owner can use this command!")
            return
        
        created = []
        
        for role_id, role_info in STAFF_ROLES.items():
            # Check if role exists
            existing = discord.utils.get(ctx.guild.roles, name=role_info['name'])
            if existing:
                continue
            
            # Create role
            role = await ctx.guild.create_role(
                name=role_info['name'],
                color=discord.Color(role_info['color']),
                permissions=role_info['permissions'],
                hoist=True,
                mentionable=True
            )
            created.append(role.name)
            await asyncio.sleep(1)
        
        if created:
            embed = discord.Embed(
                title="👑 Staff Roles Created",
                description=f"Created:\n• " + "\n• ".join(created),
                color=0x8B0000
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("✅ All staff roles already exist!")


    @commands.command(name='setupchannels')
    async def setupchannels(self, ctx):
        """Create main server channels with proper permissions (Owner only)"""
        if ctx.author.id != OWNER_ID:
            await ctx.send("❌ Only the server owner can use this command!")
            return
        
        guild = ctx.guild
        
        # Get staff roles
        emperor_lord = discord.utils.get(guild.roles, name='👑 EMPEROR LORD')
        emperor_hand = discord.utils.get(guild.roles, name='🗡️ EMPEROR LORD HAND')
        emperor_helper = discord.utils.get(guild.roles, name='⚔️ EMPEROR HELPER')
        
        if not emperor_lord:
            await ctx.send("❌ Please run `!setupstaff` first to create staff roles!")
            return
        
        status_msg = await ctx.send("🏗️ Creating server channels...")
        created = []
        
        # ===== SERVER INFO CATEGORY =====
        info_overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
            emperor_lord: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            emperor_hand: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        info_category = await guild.create_category("📁 SERVER INFO", overwrites=info_overwrites)
        created.append("📁 SERVER INFO category")
        await asyncio.sleep(1)
        
        # Announcements (Read-only)
        await guild.create_text_channel(
            name="📢-announcements",
            category=info_category,
            topic="🌑 Official Dark Empire announcements"
        )
        created.append("#📢-announcements")
        await asyncio.sleep(1)
        
        # Rules (Read-only)
        await guild.create_text_channel(
            name="📜-rules",
            category=info_category,
            topic="🌑 Dark Empire server rules - Read carefully"
        )
        created.append("#📜-rules")
        await asyncio.sleep(1)
        
        # Updates (Read-only)
        await guild.create_text_channel(
            name="📰-updates",
            category=info_category,
            topic="🌑 Server updates and changes"
        )
        created.append("#📰-updates")
        await asyncio.sleep(1)
        
        # ===== GENERAL CATEGORY =====
        general_overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        general_category = await guild.create_category("📁 GENERAL", overwrites=general_overwrites)
        created.append("📁 GENERAL category")
        await asyncio.sleep(1)
        
        await guild.create_text_channel(
            name="💬-general",
            category=general_category,
            topic="🌑 General chat for the Dark Empire"
        )
        created.append("#💬-general")
        await asyncio.sleep(1)
        
        await guild.create_text_channel(
            name="🎮-gaming",
            category=general_category,
            topic="🌑 Gaming discussions"
        )
        created.append("#🎮-gaming")
        await asyncio.sleep(1)
        
        await guild.create_text_channel(
            name="🤖-bot-commands",
            category=general_category,
            topic="🌑 Use bot commands here | Type !help"
        )
        created.append("#🤖-bot-commands")
        await asyncio.sleep(1)
        
        # ===== VOICE CATEGORY =====
        voice_category = await guild.create_category("📁 VOICE", overwrites=general_overwrites)
        created.append("📁 VOICE category")
        await asyncio.sleep(1)
        
        await guild.create_voice_channel(
            name="🔊 General Voice",
            category=voice_category
        )
        created.append("🔊 General Voice")
        await asyncio.sleep(1)
        
        await guild.create_voice_channel(
            name="🎤 Gaming Voice",
            category=voice_category
        )
        created.append("🎤 Gaming Voice")
        await asyncio.sleep(1)
        
        # ===== STAFF CATEGORY (PRIVATE) =====
        staff_overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            emperor_lord: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            emperor_hand: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            emperor_helper: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        staff_category = await guild.create_category("📁 STAFF", overwrites=staff_overwrites)
        created.append("📁 STAFF category (Private)")
        await asyncio.sleep(1)
        
        # Emperor Council (Owner/Co-owner only)
        emperor_overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            emperor_lord: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        emperor_council = await guild.create_text_channel(
            name="👑-emperor-council",
            category=staff_category,
            overwrites=emperor_overwrites,
            topic="🌑 EMPEROR LORD only - Highest council"
        )
        created.append("#👑-emperor-council (Owner only)")
        await asyncio.sleep(1)
        
        # Mod Chat (All staff)
        await guild.create_text_channel(
            name="⚔-mod-chat",
            category=staff_category,
            topic="🌑 Staff discussion and coordination"
        )
        created.append("#⚔-mod-chat")
        await asyncio.sleep(1)
        
        # Mod Logs
        await guild.create_text_channel(
            name="📋-mod-logs",
            category=staff_category,
            topic="🌑 Moderation action logs"
        )
        created.append("#📋-mod-logs")
        await asyncio.sleep(1)
        
        # Complete
        embed = discord.Embed(
            title="✅ Server Channels Created!",
            description=f"Successfully created {len(created)} items:\n\n" + "\n".join([f"• {item}" for item in created]),
            color=0x00FF00
        )
        embed.add_field(
            name="📊 Summary",
            value=f"**Categories:** 4\n**Text Channels:** {len([c for c in created if '#' in c])}\n**Voice Channels:** {len([c for c in created if '🔊' in c or '🎤' in c])}",
            inline=False
        )
        embed.set_footer(text="🌑 Dark Empire Bot")
        await status_msg.delete()
        await ctx.send(embed=embed)
    
    @commands.command(name='generalbuild')
    async def generalbuild(self, ctx):
        """Build general server channels - TALK WITH EMPIRE + COMMANDS categories (Owner only)"""
        if ctx.author.id != OWNER_ID:
            await ctx.send("❌ Only the server owner can use this command!")
            return
        
        guild = ctx.guild
        
        # Get staff roles
        emperor_lord = discord.utils.get(guild.roles, name='👑 EMPEROR LORD')
        emperor_hand = discord.utils.get(guild.roles, name='🗡️ EMPEROR LORD HAND')
        emperor_helper = discord.utils.get(guild.roles, name='⚔️ EMPEROR HELPER')
        
        # Confirmation
        embed = discord.Embed(
            title="🏗️ GENERAL BUILD",
            description=f"This will create:\n"
                       f"• **TALK WITH EMPIRE** category (3 text channels)\n"
                       f"• **COMMANDS** category (2 text channels)\n\n"
                       f"**TOTAL: 2 categories + 5 channels**\n\n"
                       f"Type `confirm` to proceed or `cancel` to abort.",
            color=0x8B00FF
        )
        await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['confirm', 'cancel']
        
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60.0)
            
            if msg.content.lower() == 'cancel':
                await ctx.send("❌ Build cancelled.")
                return
            
            status_msg = await ctx.send("🏗️ Building general channels...")
            created = []
            
            # ===== TALK WITH EMPIRE CATEGORY =====
            await status_msg.edit(content="🏗️ Creating TALK WITH EMPIRE...")
            
            talk_overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
            }
            
            talk_category = await guild.create_category("💬 TALK WITH EMPIRE", overwrites=talk_overwrites)
            created.append("📁 TALK WITH EMPIRE category")
            await asyncio.sleep(1)
            
            # Announcements (Read-only for everyone except admins)
            announce_overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
                emperor_lord: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True) if emperor_lord else None,
                emperor_hand: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True) if emperor_hand else None,
                emperor_helper: discord.PermissionOverwrite(read_messages=True, send_messages=True) if emperor_helper else None,
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
            }
            announce_overwrites = {k: v for k, v in announce_overwrites.items() if v is not None}
            
            await guild.create_text_channel(
                name="📢-announcements",
                category=talk_category,
                overwrites=announce_overwrites,
                topic="🌑 Official Empire announcements - Staff only can post"
            )
            created.append("#📢-announcements")
            await asyncio.sleep(1)
            
            # Rules (Read-only for everyone except admins)
            rules_overwrites = announce_overwrites.copy()
            await guild.create_text_channel(
                name="📜-rules",
                category=talk_category,
                overwrites=rules_overwrites,
                topic="🌑 Empire rules - Read carefully"
            )
            created.append("#📜-rules")
            await asyncio.sleep(1)
            
            # General Chat (Open for everyone)
            await guild.create_text_channel(
                name="💬-general-chat",
                category=talk_category,
                topic="🌑 Talk with the Empire - Open discussion"
            )
            created.append("#💬-general-chat")
            await asyncio.sleep(1)
            
            # ===== COMMANDS CATEGORY =====
            await status_msg.edit(content="🏗️ Creating COMMANDS category...")
            
            commands_overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                emperor_lord: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True) if emperor_lord else None,
                emperor_hand: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True) if emperor_hand else None,
                emperor_helper: discord.PermissionOverwrite(read_messages=True, send_messages=True) if emperor_helper else None,
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
            }
            commands_overwrites = {k: v for k, v in commands_overwrites.items() if v is not None}
            
            commands_category = await guild.create_category("⚔️ COMMANDS", overwrites=commands_overwrites)
            created.append("📁 COMMANDS category (Admin only)")
            await asyncio.sleep(1)
            
            # Lord Commands (OWNER/EMPEROR LORD ONLY)
            lord_only_overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                emperor_lord: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True) if emperor_lord else None,
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
            }
            lord_only_overwrites = {k: v for k, v in lord_only_overwrites.items() if v is not None}
            
            await guild.create_text_channel(
                name="👑-lord-commands",
                category=commands_category,
                overwrites=lord_only_overwrites,
                topic="🌑 Emperor Lord ONLY - Highest authority commands"
            )
            created.append("#👑-lord-commands (Owner Only)")
            await asyncio.sleep(1)
            
            # Admin Commands (All staff can access)
            await guild.create_text_channel(
                name="⚔-admin-commands",
                category=commands_category,
                topic="🌑 Admin commands and tools - All staff"
            )
            created.append("#⚔-admin-commands (All Staff)")
            await asyncio.sleep(1)
            
            # Build complete
            complete_embed = discord.Embed(
                title="✅ GENERAL BUILD COMPLETE!",
                description=f"Successfully created {len(created)} items!\n\n" + "\n".join([f"• {item}" for item in created]),
                color=0x00FF00
            )
            complete_embed.add_field(
                name="📊 Summary",
                value=f"**Categories:** 2\n"
                     f"**Text Channels:** 5\n"
                     f"• Announcements (Read-only)\n"
                     f"• Rules (Read-only)\n"
                     f"• General Chat (Open)\n"
                     f"• Lord Commands (Owner Only)\n"
                     f"• Admin Commands (All Staff)",
                inline=False
            )
            complete_embed.set_footer(text="🌑 Dark Empire Bot")
            
            await status_msg.delete()
            await ctx.send(embed=complete_embed)
            
        except asyncio.TimeoutError:
            await ctx.send("⏰ Build cancelled (timeout).")
    
    @commands.command(name='empirebuild')
    async def empirebuild(self, ctx):
        """Build Empire communication channels (Owner only)"""
        if ctx.author.id != OWNER_ID:
            await ctx.send("❌ Only the server owner can use this command!")
            return
        
        guild = ctx.guild
        
        # Get staff roles
        emperor_lord = discord.utils.get(guild.roles, name='👑 EMPEROR LORD')
        emperor_hand = discord.utils.get(guild.roles, name='🗡️ EMPEROR LORD HAND')
        emperor_helper = discord.utils.get(guild.roles, name='⚔️ EMPEROR HELPER')
        
        # Confirmation
        embed = discord.Embed(
            title="🏗️ BUILD EMPIRE CHANNELS",
            description=f"This will create:\n"
                       f"• **TALK WITH EMPIRE** category (3 channels)\n"
                       f"• **COMMANDS** category (2 channels)\n"
                       f"• **OPEN VOICE** category (10 voice channels)\n"
                       f"• **SQUAD VOICE** category (6 voice channels, max 4 players)\n\n"
                       f"**TOTAL: 4 categories + 21 channels**\n\n"
                       f"Type `confirm` to proceed or `cancel` to abort.",
            color=0x8B00FF
        )
        await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['confirm', 'cancel']
        
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60.0)
            
            if msg.content.lower() == 'cancel':
                await ctx.send("❌ Build cancelled.")
                return
            
            status_msg = await ctx.send("🏗️ Building Empire channels...")
            created = []
            
            # ===== TALK WITH EMPIRE CATEGORY =====
            await status_msg.edit(content="🏗️ Creating TALK WITH EMPIRE...")
            
            talk_overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
            }
            
            talk_category = await guild.create_category("💬 TALK WITH EMPIRE", overwrites=talk_overwrites)
            created.append("📁 TALK WITH EMPIRE category")
            await asyncio.sleep(1)
            
            # Announcements (Read-only for everyone except admins)
            announce_overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
                emperor_lord: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True) if emperor_lord else None,
                emperor_hand: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True) if emperor_hand else None,
                emperor_helper: discord.PermissionOverwrite(read_messages=True, send_messages=True) if emperor_helper else None,
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
            }
            announce_overwrites = {k: v for k, v in announce_overwrites.items() if v is not None}
            
            await guild.create_text_channel(
                name="📢-announcements",
                category=talk_category,
                overwrites=announce_overwrites,
                topic="🌑 Official Empire announcements - Staff only can post"
            )
            created.append("#📢-announcements")
            await asyncio.sleep(1)
            
            # Rules (Read-only for everyone except admins)
            rules_overwrites = announce_overwrites.copy()
            await guild.create_text_channel(
                name="📜-rules",
                category=talk_category,
                overwrites=rules_overwrites,
                topic="🌑 Empire rules - Read carefully"
            )
            created.append("#📜-rules")
            await asyncio.sleep(1)
            
            # General Chat (Open for everyone)
            await guild.create_text_channel(
                name="💬-general-chat",
                category=talk_category,
                topic="🌑 Talk with the Empire - Open discussion"
            )
            created.append("#💬-general-chat")
            await asyncio.sleep(1)
            
            # ===== COMMANDS CATEGORY =====
            await status_msg.edit(content="🏗️ Creating COMMANDS category...")
            
            commands_overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                emperor_lord: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True) if emperor_lord else None,
                emperor_hand: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True) if emperor_hand else None,
                emperor_helper: discord.PermissionOverwrite(read_messages=True, send_messages=True) if emperor_helper else None,
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
            }
            commands_overwrites = {k: v for k, v in commands_overwrites.items() if v is not None}
            
            commands_category = await guild.create_category("⚔️ COMMANDS", overwrites=commands_overwrites)
            created.append("📁 COMMANDS category (Admin only)")
            await asyncio.sleep(1)
            
            # Lord Commands (OWNER/EMPEROR LORD ONLY)
            lord_only_overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                emperor_lord: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True) if emperor_lord else None,
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
            }
            lord_only_overwrites = {k: v for k, v in lord_only_overwrites.items() if v is not None}
            
            await guild.create_text_channel(
                name="👑-lord-commands",
                category=commands_category,
                overwrites=lord_only_overwrites,
                topic="🌑 Emperor Lord ONLY - Highest authority commands"
            )
            created.append("#👑-lord-commands (Owner Only)")
            await asyncio.sleep(1)
            
            # Admin Commands (All staff can access)
            await guild.create_text_channel(
                name="⚔-admin-commands",
                category=commands_category,
                topic="🌑 Admin commands and tools - All staff"
            )
            created.append("#⚔-admin-commands (All Staff)")
            await asyncio.sleep(1)
            
            # ===== OPEN VOICE CATEGORY =====
            await status_msg.edit(content="🏗️ Creating OPEN VOICE channels...")
            
            open_voice_overwrites = {
                guild.default_role: discord.PermissionOverwrite(connect=True, speak=True),
                guild.me: discord.PermissionOverwrite(connect=True, speak=True, manage_channels=True)
            }
            
            open_voice_category = await guild.create_category("🔊 OPEN VOICE", overwrites=open_voice_overwrites)
            created.append("📁 OPEN VOICE category")
            await asyncio.sleep(1)
            
            # Create 10 open voice channels
            for i in range(1, 11):
                await guild.create_voice_channel(
                    name=f"🔊 Open Voice {i}",
                    category=open_voice_category
                )
                created.append(f"🔊 Open Voice {i}")
                await asyncio.sleep(1)
            
            # ===== SQUAD VOICE CATEGORY =====
            await status_msg.edit(content="🏗️ Creating SQUAD VOICE channels...")
            
            squad_voice_overwrites = {
                guild.default_role: discord.PermissionOverwrite(connect=True, speak=True),
                guild.me: discord.PermissionOverwrite(connect=True, speak=True, manage_channels=True)
            }
            
            squad_voice_category = await guild.create_category("🎯 SQUAD VOICE", overwrites=squad_voice_overwrites)
            created.append("📁 SQUAD VOICE category")
            await asyncio.sleep(1)
            
            # Create 6 squad voice channels with max 4 players
            for i in range(1, 7):
                await guild.create_voice_channel(
                    name=f"🎯 Squad {i}",
                    category=squad_voice_category,
                    user_limit=4
                )
                created.append(f"🎯 Squad {i} (Max 4 players)")
                await asyncio.sleep(1)
            
            # Build complete
            complete_embed = discord.Embed(
                title="✅ EMPIRE BUILD COMPLETE!",
                description=f"Successfully created {len(created)} items!\n\n" + "\n".join([f"• {item}" for item in created]),
                color=0x00FF00
            )
            complete_embed.add_field(
                name="📊 Summary",
                value=f"**Categories:** 4\n"
                     f"**Text Channels:** 5\n"
                     f"**Open Voice Channels:** 10\n"
                     f"**Squad Voice Channels:** 6 (Max 4 players each)",
                inline=False
            )
            complete_embed.set_footer(text="🌑 Dark Empire Bot")
            
            await status_msg.delete()
            await ctx.send(embed=complete_embed)
            
        except asyncio.TimeoutError:
            await ctx.send("⏰ Build cancelled (timeout).")
    
    @commands.command(name='fixteampermissions')
    async def fixteampermissions(self, ctx):
        """Fix team channel permissions - Only team members + owners can access (Owner only)"""
        if ctx.author.id != OWNER_ID:
            await ctx.send("❌ Only the server owner can use this command!")
            return
        
        guild = ctx.guild
        
        # Get staff roles
        emperor_lord = discord.utils.get(guild.roles, name='👑 EMPEROR LORD')
        emperor_hand = discord.utils.get(guild.roles, name='🗡️ EMPEROR LORD HAND')
        
        if not emperor_lord:
            await ctx.send("❌ Please run `!setupstaff` first!")
            return
        
        status_msg = await ctx.send("🔧 Fixing team permissions...")
        fixed_count = 0
        
        # Process each team
        for team_id, team_info in TEAMS.items():
            # Find team category
            category = discord.utils.get(guild.categories, name=f"{team_info['emoji']} {team_info['name'].upper()}")
            if not category:
                continue
            
            # Get team roles
            member_role = discord.utils.get(guild.roles, name=f"{team_info['emoji']} {team_info['name']}")
            lord_role = discord.utils.get(guild.roles, name=f"{team_info['emoji']} {team_info['name']} Lord")
            hand_role = discord.utils.get(guild.roles, name=f"{team_info['emoji']} {team_info['name']} Hand")
            
            if not member_role:
                continue
            
            # Set category permissions
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True),
                emperor_lord: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True, connect=True),
                emperor_hand: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True, connect=True),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
            }
            
            if lord_role:
                overwrites[lord_role] = discord.PermissionOverwrite(
                    read_messages=True, send_messages=True, manage_messages=True, connect=True, move_members=True
                )
            
            if hand_role:
                overwrites[hand_role] = discord.PermissionOverwrite(
                    read_messages=True, send_messages=True, manage_messages=True, connect=True, move_members=True
                )
            
            await category.edit(overwrites=overwrites)
            fixed_count += 1
            await asyncio.sleep(0.5)
            
            # Create Lord Command Channel if it doesn't exist
            lord_channel_name = "👑-lord-commands"
            lord_channel = discord.utils.get(category.channels, name=lord_channel_name)
            
            if not lord_channel:
                # Lord-only channel permissions
                lord_overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    member_role: discord.PermissionOverwrite(read_messages=False),
                    lord_role: discord.PermissionOverwrite(read_messages=True, send_messages=True) if lord_role else None,
                    hand_role: discord.PermissionOverwrite(read_messages=True, send_messages=True) if hand_role else None,
                    emperor_lord: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True),
                    emperor_hand: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                }
                
                # Remove None values
                lord_overwrites = {k: v for k, v in lord_overwrites.items() if v is not None}
                
                await guild.create_text_channel(
                    name=lord_channel_name,
                    category=category,
                    overwrites=lord_overwrites,
                    topic=f"🌑 {team_info['name']} - Lord & Hand only"
                )
                await asyncio.sleep(1)
        
        embed = discord.Embed(
            title="✅ Team Permissions Fixed!",
            description=f"Updated permissions for **{fixed_count} teams**\n\n"
                       f"**Changes:**\n"
                       f"• Only team members can access team channels\n"
                       f"• 👑 EMPEROR LORD & 🗡️ EMPEROR LORD HAND can access all teams\n"
                       f"• Added 👑-lord-commands channel to each team\n"
                       f"• Lord & Hand have full team permissions",
            color=0x00FF00
        )
        embed.set_footer(text="🌑 Dark Empire Bot")
        await status_msg.delete()
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ServerBuild(bot))

