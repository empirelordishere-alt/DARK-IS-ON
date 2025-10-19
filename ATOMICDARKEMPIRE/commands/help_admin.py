"""
📚 HELP & ADMIN COMMANDS
!help, !adminpanel, !analytics
Interactive help system with buttons and detailed command categories
"""

import discord
from discord.ext import commands
import os
from datetime import datetime


OWNER_ID = int(os.getenv('OWNER_ID', 0))
PREFIX = os.getenv('PREFIX', '!')


class HelpButton(discord.ui.Button):
    def __init__(self, label, emoji, category):
        super().__init__(label=label, emoji=emoji, style=discord.ButtonStyle.secondary)
        self.category = category
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=self.view.get_category_embed(self.category), ephemeral=True)


class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        
        # Add buttons for each category
        self.add_item(HelpButton("Economy", "💰", "economy"))
        self.add_item(HelpButton("Teams", "🎯", "teams"))
        self.add_item(HelpButton("Market", "🛒", "market"))
        self.add_item(HelpButton("Moderation", "🔨", "moderation"))
        self.add_item(HelpButton("Server", "🏗", "server"))
        self.add_item(HelpButton("Owner", "👑", "owner"))
    
    def get_category_embed(self, category):
        """Get embed for specific category"""
        if category == "economy":
            embed = discord.Embed(
                title="💰 ECONOMY COMMANDS",
                description="Manage your wealth and progression",
                color=0xFFD700
            )
            embed.add_field(
                name=f"`{PREFIX}wealth` / `{PREFIX}balance` / `{PREFIX}bal`",
                value="Check your or someone else's wealth and currencies",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}status` / `{PREFIX}profile` / `{PREFIX}stats`",
                value="View detailed profile with XP progress and rank",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}daily` / `{PREFIX}claim`",
                value="Claim daily rewards (24h cooldown, streak bonuses)",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}leaderboard` / `{PREFIX}lb`",
                value="See top 10 richest players in the server",
                inline=False
            )
            
        elif category == "teams":
            embed = discord.Embed(
                title="🎯 TEAM COMMANDS",
                description="Join teams and compete for glory",
                color=0x8B00FF
            )
            embed.add_field(
                name=f"`{PREFIX}teams`",
                value="View all 20 teams with stats",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}join <team_id>`",
                value="Join a team (become Lord if empty, or send request)",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}leaveteam`",
                value="Leave your current team",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}teaminfo [team_id]`",
                value="View team information and stats",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}teamvault`",
                value="Check your team's shared vault",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}donate <amount> <currency>`",
                value="Donate currency to your team vault",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}teamleaderboard`",
                value="See richest teams ranking",
                inline=False
            )
            
            embed.add_field(
                name="👑 Lord Commands",
                value=f"`{PREFIX}claimlord` - Claim lordship if vacant\n"
                      f"`{PREFIX}appointhand @user` - Appoint second-in-command\n"
                      f"`{PREFIX}kickmember @user` - Kick member from team\n"
                      f"`{PREFIX}disbandteam` - Disband the team\n"
                      f"`{PREFIX}requests` - View join requests\n"
                      f"`{PREFIX}approve @user` - Approve join request\n"
                      f"`{PREFIX}deny @user` - Deny join request",
                inline=False
            )
            
        elif category == "market":
            embed = discord.Embed(
                title="🛒 MARKETPLACE COMMANDS",
                description="Trade items and currency",
                color=0x00FFFF
            )
            embed.add_field(
                name=f"`{PREFIX}sell <price> <currency> <item_name>`",
                value="List an item for sale (requires admin verification)",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}market` / `{PREFIX}marketplace`",
                value="Browse all listings",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}mylistings`",
                value="View your active listings",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}cancellisting <id>`",
                value="Cancel your listing",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}buy <listing_id>`",
                value="Purchase an item from the marketplace",
                inline=False
            )
            embed.add_field(
                name="⚙️ Admin Commands",
                value=f"`{PREFIX}verify <trade_id>` - Verify listing is legitimate\n"
                      f"`{PREFIX}completetrade <trade_id>` - Complete verified trade",
                inline=False
            )
            
        elif category == "moderation":
            embed = discord.Embed(
                title="🔨 MODERATION COMMANDS",
                description="Server moderation tools",
                color=0xFF0000
            )
            embed.add_field(
                name=f"`{PREFIX}kick @user [reason]`",
                value="Kick member from server (requires Kick Members)",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}ban @user [reason]`",
                value="Ban member from server (requires Ban Members)",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}unban <user_id> [reason]`",
                value="Unban user by ID (requires Ban Members)",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}mute @user <duration> [reason]`",
                value="Timeout member (60s, 5m, 2h, 1d, 7d, max 28d)",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}unmute @user [reason]`",
                value="Remove timeout from member",
                inline=False
            )
            
        elif category == "server":
            embed = discord.Embed(
                title="🏗 SERVER BUILDING COMMANDS",
                description="Build the Dark Empire structure",
                color=0x8B0000
            )
            embed.add_field(
                name=f"`{PREFIX}buildatomic`",
                value="Build ALL 20 teams (~30 min, 180+ items) [Owner]",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}quickbuild`",
                value="Build 3 test teams [Owner]",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}simplebuild`",
                value="Build 1 team for testing [Owner]",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}cleanup`",
                value="Delete ALL team structures (DANGEROUS!) [Owner]",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}setupwelcome`",
                value="Create welcome channel [Owner]",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}setupstaff`",
                value="Create EMPEROR staff roles [Owner]",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}serverstats`",
                value="View server statistics",
                inline=False
            )
            
        elif category == "owner":
            embed = discord.Embed(
                title="👑 OWNER COMMANDS",
                description="Server owner only commands",
                color=0xFFD700
            )
            embed.add_field(
                name=f"`{PREFIX}addmoney @user <amount> <currency>`",
                value="Add currency to user\nCurrencies: soul_fragments, cursed_essence, tombstone_coins, lords_blood, void_crystals",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}setlevel @user <level>`",
                value="Set user level (1-1000)",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}adminpanel`",
                value="View admin control panel",
                inline=False
            )
            embed.add_field(
                name=f"`{PREFIX}analytics`",
                value="View server analytics",
                inline=False
            )
        
        else:
            embed = discord.Embed(title="Unknown Category", color=0xFF0000)
        
        embed.set_footer(text="🌑 Dark Empire Bot")
        return embed


class HelpAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        from data_manager import DataManager
        self.data = bot.data if hasattr(bot, 'data') else DataManager()
        if not hasattr(bot, 'data'):
            bot.data = self.data
    
    @commands.command(name='help')
    async def help(self, ctx):
        """Interactive help menu with buttons"""
        embed = discord.Embed(
            title="🌑 DARK EMPIRE BOT HELP",
            description=f"**Welcome to the Dark Empire!**\n\n"
                       f"Click the buttons below to explore each category:\n\n"
                       f"💰 **Economy** - Currencies, levels, daily rewards\n"
                       f"🎯 **Teams** - Join teams, compete, donate\n"
                       f"🛒 **Market** - Trade items and currency\n"
                       f"🔨 **Moderation** - Kick, ban, mute commands\n"
                       f"🏗 **Server** - Build team structures\n"
                       f"👑 **Owner** - Owner-only commands\n\n"
                       f"**Quick Start:**\n"
                       f"• `{PREFIX}teams` - View all teams\n"
                       f"• `{PREFIX}daily` - Claim daily rewards\n"
                       f"• `{PREFIX}wealth` - Check your balance\n"
                       f"• `{PREFIX}join <team_id>` - Join a team",
            color=0x000000
        )
        embed.set_footer(text=f"🌑 Dark Empire Bot | Prefix: {PREFIX}")
        
        view = HelpView()
        await ctx.send(embed=embed, view=view)
    
    @commands.command(name='adminpanel')
    async def adminpanel(self, ctx):
        """Admin control panel (Owner only)"""
        if ctx.author.id != OWNER_ID:
            await ctx.send("❌ Only the server owner can use this command!")
            return
        
        guild = ctx.guild
        
        # Server stats
        total_members = guild.member_count
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        roles = len(guild.roles)
        
        # Economy stats
        total_users = len(self.data.economy)
        total_wealth = sum(
            sum(user_data['currencies'].values()) 
            for user_data in self.data.economy.values()
        )
        
        # Team stats
        teams_with_lords = sum(1 for team in self.data.teams.values() if team['lord'] is not None)
        total_team_members = sum(len(team['members']) for team in self.data.teams.values())
        
        # Market stats
        total_listings = len(self.data.market['listings'])
        verified_listings = sum(1 for listing in self.data.market['listings'] if listing['verified'])
        
        embed = discord.Embed(
            title="👑 ADMIN CONTROL PANEL",
            description=f"**Server:** {guild.name}",
            color=0x8B0000
        )
        
        embed.add_field(
            name="📊 Server Stats",
            value=f"Members: {total_members}\n"
                  f"Channels: {text_channels + voice_channels}\n"
                  f"Roles: {roles}",
            inline=True
        )
        
        embed.add_field(
            name="💰 Economy Stats",
            value=f"Users: {total_users}\n"
                  f"Total Wealth: {total_wealth:,}\n"
                  f"Avg Wealth: {int(total_wealth/max(total_users, 1)):,}",
            inline=True
        )
        
        embed.add_field(
            name="🎯 Team Stats",
            value=f"Teams with Lords: {teams_with_lords}/20\n"
                  f"Total Members: {total_team_members}\n"
                  f"Avg per Team: {total_team_members/20:.1f}",
            inline=True
        )
        
        embed.add_field(
            name="🛒 Market Stats",
            value=f"Total Listings: {total_listings}\n"
                  f"Verified: {verified_listings}\n"
                  f"Pending: {total_listings - verified_listings}",
            inline=True
        )
        
        embed.add_field(
            name="📝 Mod Logs",
            value=f"Total Actions: {len(self.data.moderation['logs'])}",
            inline=True
        )
        
        embed.add_field(
            name="🤖 Bot Info",
            value=f"Servers: {len(self.bot.guilds)}\n"
                  f"Latency: {int(self.bot.latency * 1000)}ms\n"
                  f"Uptime: Since restart",
            inline=True
        )
        
        embed.add_field(
            name="⚡ Quick Commands",
            value=f"`{PREFIX}addmoney @user <amount> <currency>`\n"
                  f"`{PREFIX}setlevel @user <level>`\n"
                  f"`{PREFIX}buildatomic` - Build all teams\n"
                  f"`{PREFIX}cleanup` - Remove all teams\n"
                  f"`{PREFIX}setupwelcome` - Create welcome\n"
                  f"`{PREFIX}setupstaff` - Create staff roles",
            inline=False
        )
        
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.set_footer(text=f"🌑 Dark Empire Bot | Owner: {ctx.author.name}")
        embed.timestamp = datetime.now()
        
        await ctx.send(embed=embed)
    
    @commands.command(name='analytics')
    async def analytics(self, ctx):
        """Server analytics (Owner only)"""
        if ctx.author.id != OWNER_ID:
            await ctx.send("❌ Only the server owner can use this command!")
            return
        
        guild = ctx.guild
        
        # Member status breakdown
        online = len([m for m in guild.members if m.status == discord.Status.online])
        idle = len([m for m in guild.members if m.status == discord.Status.idle])
        dnd = len([m for m in guild.members if m.status == discord.Status.dnd])
        offline = len([m for m in guild.members if m.status == discord.Status.offline])
        
        total = guild.member_count
        bots = len([m for m in guild.members if m.bot])
        humans = total - bots
        
        # Calculate percentages
        online_pct = (online / max(total, 1)) * 100
        idle_pct = (idle / max(total, 1)) * 100
        dnd_pct = (dnd / max(total, 1)) * 100
        offline_pct = (offline / max(total, 1)) * 100
        
        embed = discord.Embed(
            title="📊 SERVER ANALYTICS",
            description=f"**{guild.name}**",
            color=0x8B00FF
        )
        
        embed.add_field(
            name="👥 Member Breakdown",
            value=f"Total: {total}\n"
                  f"Humans: {humans}\n"
                  f"Bots: {bots}",
            inline=True
        )
        
        embed.add_field(
            name="📈 Member Status",
            value=f"🟢 Online: {online} ({online_pct:.1f}%)\n"
                  f"🟡 Idle: {idle} ({idle_pct:.1f}%)\n"
                  f"🔴 DND: {dnd} ({dnd_pct:.1f}%)\n"
                  f"⚫ Offline: {offline} ({offline_pct:.1f}%)",
            inline=True
        )
        
        # Top 5 richest users
        leaderboard = self.data.get_leaderboard(5)
        top_users = ""
        for i, user_info in enumerate(leaderboard):
            try:
                user = await self.bot.fetch_user(user_info['user_id'])
                top_users += f"{i+1}. {user.name}: {user_info['total_wealth']:,}\n"
            except:
                top_users += f"{i+1}. User {user_info['user_id']}: {user_info['total_wealth']:,}\n"
        
        embed.add_field(
            name="💰 Top 5 Richest",
            value=top_users or "No data",
            inline=False
        )
        
        # Top 3 teams
        team_lb = self.data.get_team_leaderboard()[:3]
        top_teams = ""
        for i, team_info in enumerate(team_lb):
            from bot import TEAMS
            team_name = TEAMS[team_info['team_id']]['name']
            top_teams += f"{i+1}. {team_name}: {team_info['total_wealth']:,}\n"
        
        embed.add_field(
            name="🎯 Top 3 Teams",
            value=top_teams or "No data",
            inline=False
        )
        
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.set_footer(text="🌑 Dark Empire Analytics")
        embed.timestamp = datetime.now()
        
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpAdmin(bot))
