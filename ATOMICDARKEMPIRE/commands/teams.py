"""
🎯 TEAM COMMANDS
!teams, !join, !leaveteam, !teaminfo, !claimlord, !appointhand, !kickmember, !disbandteam
!teamvault, !donate, !teamleaderboard, !requests, !approve, !deny
"""

import discord
from discord.ext import commands
from typing import Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot import TEAMS, CURRENCIES

OWNER_ID = int(os.getenv('OWNER_ID', 0))


class Teams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        from data_manager import DataManager
        self.data = bot.data if hasattr(bot, 'data') else DataManager()
        if not hasattr(bot, 'data'):
            bot.data = self.data
    
    @commands.command(name='teams')
    async def teams(self, ctx):
        """View all 20 teams"""
        embed = discord.Embed(
            title="🌑 DARK EMPIRE TEAMS",
            description="Join a team to unlock exclusive features!\nUse `!join <team_id>` to join",
            color=0x000000
        )
        
        teams_text = ""
        for team_id, team_info in TEAMS.items():
            team_data = self.data.get_team(team_id)
            member_count = len(team_data['members']) if team_data else 0
            lord = team_data['lord'] if team_data else None
            lord_name = f"<@{lord}>" if lord else "No Lord"
            
            teams_text += f"{team_info['emoji']} **{team_info['name']}**\n"
            teams_text += f"   ID: `{team_id}` | Members: {member_count}/20 | Lord: {lord_name}\n\n"
        
        embed.description = teams_text
        embed.set_footer(text="Use !join <team_id> to join a team")
        await ctx.send(embed=embed)
    
    @commands.command(name='join')
    async def join(self, ctx, team_id: str):
        """Join or request to join a team"""
        if team_id not in TEAMS:
            await ctx.send(f"❌ Invalid team ID! Use `!teams` to see all teams.")
            return
        
        # Check if user already in a team
        current_team = self.data.get_user_team(ctx.author.id)
        if current_team:
            await ctx.send(f"❌ You're already in a team! Use `!leaveteam` first.")
            return
        
        team_data = self.data.get_team(team_id)
        team_info = TEAMS[team_id]
        
        # Check if team is full
        if len(team_data['members']) >= 20:
            await ctx.send(f"❌ {team_info['name']} is full (20/20 members)!")
            return
        
        # If no lord, user becomes lord
        if team_data['lord'] is None:
            team_data['lord'] = ctx.author.id
            self.data.join_team(ctx.author.id, team_id)
            
            # Assign lord role
            guild = ctx.guild
            lord_role = discord.utils.get(guild.roles, name=f"{team_info['emoji']} {team_info['name']} Lord")
            if lord_role:
                await ctx.author.add_roles(lord_role)
            
            embed = discord.Embed(
                title=f"👑 You are now the Lord of {team_info['name']}!",
                description=f"You have claimed leadership of {team_info['emoji']} **{team_info['name']}**\n\n"
                           f"**Lord Commands:**\n"
                           f"`!appointhand @user` - Appoint second-in-command\n"
                           f"`!kickmember @user` - Kick members\n"
                           f"`!disbandteam` - Disband the team",
                color=team_info['color']
            )
            await ctx.send(embed=embed)
        else:
            # Send join request
            self.data.add_join_request(ctx.author.id, team_id)
            
            lord_user = await self.bot.fetch_user(team_data['lord'])
            
            embed = discord.Embed(
                title=f"📨 Join Request Sent",
                description=f"Your request to join {team_info['emoji']} **{team_info['name']}** has been sent to {lord_user.mention}",
                color=team_info['color']
            )
            await ctx.send(embed=embed)
            
            # Notify lord
            try:
                lord_embed = discord.Embed(
                    title=f"📨 New Join Request",
                    description=f"{ctx.author.mention} wants to join **{team_info['name']}**\n\n"
                               f"Use `!approve @{ctx.author.name}` or `!deny @{ctx.author.name}`",
                    color=team_info['color']
                )
                await lord_user.send(embed=lord_embed)
            except:
                pass
    
    @commands.command(name='leaveteam')
    async def leaveteam(self, ctx):
        """Leave your current team"""
        current_team_id = self.data.get_user_team(ctx.author.id)
        
        if not current_team_id:
            await ctx.send("❌ You're not in a team!")
            return
        
        team_data = self.data.get_team(current_team_id)
        team_info = TEAMS[current_team_id]
        
        # Lords can't leave (must disband)
        if team_data['lord'] == ctx.author.id:
            await ctx.send("❌ Lords cannot leave their team! Use `!disbandteam` to disband.")
            return
        
        # Remove from team
        self.data.leave_team(ctx.author.id, current_team_id)
        
        # Remove roles
        guild = ctx.guild
        member_role = discord.utils.get(guild.roles, name=f"{team_info['emoji']} {team_info['name']}")
        hand_role = discord.utils.get(guild.roles, name=f"{team_info['emoji']} {team_info['name']} Hand")
        
        if member_role and member_role in ctx.author.roles:
            await ctx.author.remove_roles(member_role)
        if hand_role and hand_role in ctx.author.roles:
            await ctx.author.remove_roles(hand_role)
            team_data['lord_hand'] = None
            self.data.save_teams()
        
        embed = discord.Embed(
            title="👋 Left Team",
            description=f"You have left **{team_info['name']}**",
            color=0x808080
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='teaminfo')
    async def teaminfo(self, ctx, team_id: str = None):
        """View team information"""
        if not team_id:
            team_id = self.data.get_user_team(ctx.author.id)
            if not team_id:
                await ctx.send("❌ Specify a team ID or join a team! Use `!teams`")
                return
        
        if team_id not in TEAMS:
            await ctx.send(f"❌ Invalid team ID! Use `!teams` to see all teams.")
            return
        
        team_data = self.data.get_team(team_id)
        team_info = TEAMS[team_id]
        
        # Get lord and hand info
        lord_mention = f"<@{team_data['lord']}>" if team_data['lord'] else "None"
        hand_mention = f"<@{team_data['lord_hand']}>" if team_data['lord_hand'] else "None"
        
        embed = discord.Embed(
            title=f"{team_info['emoji']} {team_info['name']}",
            color=team_info['color']
        )
        
        embed.add_field(name="👑 Lord", value=lord_mention, inline=True)
        embed.add_field(name="🗡️ Lord Hand", value=hand_mention, inline=True)
        embed.add_field(name="👥 Members", value=f"{len(team_data['members'])}/20", inline=True)
        
        # Vault info
        vault_total = sum(team_data['vault'].values())
        embed.add_field(name="💰 Vault Total", value=f"{vault_total:,}", inline=True)
        embed.add_field(name="📨 Pending Requests", value=len(team_data['join_requests']), inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='claimlord')
    async def claimlord(self, ctx):
        """Become Lord if team has no Lord"""
        current_team_id = self.data.get_user_team(ctx.author.id)
        
        if not current_team_id:
            await ctx.send("❌ You must be in a team to claim lordship!")
            return
        
        team_data = self.data.get_team(current_team_id)
        team_info = TEAMS[current_team_id]
        
        if team_data['lord'] is not None:
            await ctx.send(f"❌ This team already has a Lord!")
            return
        
        team_data['lord'] = ctx.author.id
        self.data.save_teams()
        
        # Assign lord role
        guild = ctx.guild
        lord_role = discord.utils.get(guild.roles, name=f"{team_info['emoji']} {team_info['name']} Lord")
        if lord_role:
            await ctx.author.add_roles(lord_role)
        
        embed = discord.Embed(
            title=f"👑 Lord Claimed!",
            description=f"You are now the Lord of **{team_info['name']}**!",
            color=team_info['color']
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='appointhand')
    async def appointhand(self, ctx, member: discord.Member):
        """Appoint Lord Hand (second-in-command)"""
        current_team_id = self.data.get_user_team(ctx.author.id)
        
        if not current_team_id:
            await ctx.send("❌ You must be in a team!")
            return
        
        team_data = self.data.get_team(current_team_id)
        team_info = TEAMS[current_team_id]
        
        # Check if user is lord
        if team_data['lord'] != ctx.author.id:
            await ctx.send("❌ Only the Lord can appoint a Hand!")
            return
        
        # Check if member is in team
        if member.id not in team_data['members']:
            await ctx.send(f"❌ {member.mention} is not in your team!")
            return
        
        team_data['lord_hand'] = member.id
        self.data.save_teams()
        
        # Assign hand role
        guild = ctx.guild
        hand_role = discord.utils.get(guild.roles, name=f"{team_info['emoji']} {team_info['name']} Hand")
        if hand_role:
            await member.add_roles(hand_role)
        
        embed = discord.Embed(
            title=f"🗡️ Lord Hand Appointed",
            description=f"{member.mention} is now the Lord Hand of **{team_info['name']}**!",
            color=team_info['color']
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='kickmember')
    async def kickmember(self, ctx, member: discord.Member):
        """Kick member from your team"""
        current_team_id = self.data.get_user_team(ctx.author.id)
        
        if not current_team_id:
            await ctx.send("❌ You must be in a team!")
            return
        
        team_data = self.data.get_team(current_team_id)
        team_info = TEAMS[current_team_id]
        
        # Check if user is lord
        if team_data['lord'] != ctx.author.id:
            await ctx.send("❌ Only the Lord can kick members!")
            return
        
        # Check if member is in team
        if member.id not in team_data['members']:
            await ctx.send(f"❌ {member.mention} is not in your team!")
            return
        
        # Can't kick self
        if member.id == ctx.author.id:
            await ctx.send("❌ You can't kick yourself! Use `!disbandteam` instead.")
            return
        
        # Remove from team
        self.data.leave_team(member.id, current_team_id)
        
        # Remove roles
        guild = ctx.guild
        member_role = discord.utils.get(guild.roles, name=f"{team_info['emoji']} {team_info['name']}")
        hand_role = discord.utils.get(guild.roles, name=f"{team_info['emoji']} {team_info['name']} Hand")
        
        if member_role and member_role in member.roles:
            await member.remove_roles(member_role)
        if hand_role and hand_role in member.roles:
            await member.remove_roles(hand_role)
            team_data['lord_hand'] = None
            self.data.save_teams()
        
        embed = discord.Embed(
            title="⚔️ Member Kicked",
            description=f"{member.mention} has been kicked from **{team_info['name']}**",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='disbandteam')
    async def disbandteam(self, ctx):
        """Delete your team completely"""
        current_team_id = self.data.get_user_team(ctx.author.id)
        
        if not current_team_id:
            await ctx.send("❌ You must be in a team!")
            return
        
        team_data = self.data.get_team(current_team_id)
        team_info = TEAMS[current_team_id]
        
        # Check if user is lord
        if team_data['lord'] != ctx.author.id:
            await ctx.send("❌ Only the Lord can disband the team!")
            return
        
        # Confirmation
        embed = discord.Embed(
            title="⚠️ Confirm Team Disbandment",
            description=f"Are you sure you want to disband **{team_info['name']}**?\n\n"
                       f"This will:\n"
                       f"• Remove all {len(team_data['members'])} members\n"
                       f"• Clear the team vault\n"
                       f"• Remove all team roles\n\n"
                       f"Type `confirm` to proceed or `cancel` to abort.",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['confirm', 'cancel']
        
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)
            
            if msg.content.lower() == 'cancel':
                await ctx.send("❌ Disbandment cancelled.")
                return
            
            # Disband team
            for member_id in team_data['members'][:]:
                self.data.leave_team(member_id, current_team_id)
            
            # Reset team data
            team_data['lord'] = None
            team_data['lord_hand'] = None
            team_data['members'] = []
            team_data['join_requests'] = []
            team_data['vault'] = {k: 0 for k in team_data['vault']}
            self.data.save_teams()
            
            embed = discord.Embed(
                title="💀 Team Disbanded",
                description=f"**{team_info['name']}** has been disbanded.",
                color=0x000000
            )
            await ctx.send(embed=embed)
            
        except TimeoutError:
            await ctx.send("⏰ Disbandment cancelled (timeout).")
    
    @commands.command(name='teamvault')
    async def teamvault(self, ctx):
        """Check team's shared vault"""
        current_team_id = self.data.get_user_team(ctx.author.id)
        
        if not current_team_id:
            await ctx.send("❌ You must be in a team!")
            return
        
        team_data = self.data.get_team(current_team_id)
        team_info = TEAMS[current_team_id]
        
        embed = discord.Embed(
            title=f"💰 {team_info['name']} Vault",
            color=team_info['color']
        )
        
        for currency_id, currency_info in CURRENCIES.items():
            amount = team_data['vault'][currency_id]
            embed.add_field(
                name=currency_info['name'],
                value=f"{currency_info['emoji']} {amount:,}",
                inline=True
            )
        
        total = sum(team_data['vault'].values())
        embed.add_field(name="📊 Total", value=f"{total:,}", inline=False)
        embed.set_footer(text="Use !donate <amount> <currency> to donate")
        
        await ctx.send(embed=embed)
    
    @commands.command(name='donate')
    async def donate(self, ctx, amount: int, currency: str):
        """Donate to team vault"""
        if amount <= 0:
            await ctx.send("❌ Amount must be positive!")
            return
        
        if currency not in CURRENCIES:
            await ctx.send(f"❌ Invalid currency! Use: {', '.join(CURRENCIES.keys())}")
            return
        
        current_team_id = self.data.get_user_team(ctx.author.id)
        
        if not current_team_id:
            await ctx.send("❌ You must be in a team!")
            return
        
        # Check user balance
        user_data = self.data.get_user(ctx.author.id)
        if user_data['currencies'][currency] < amount:
            await ctx.send(f"❌ You don't have enough {CURRENCIES[currency]['name']}!")
            return
        
        # Transfer to vault
        user_data['currencies'][currency] -= amount
        team_data = self.data.get_team(current_team_id)
        team_data['vault'][currency] += amount
        
        self.data.save_economy()
        self.data.save_teams()
        
        team_info = TEAMS[current_team_id]
        emoji = CURRENCIES[currency]['emoji']
        name = CURRENCIES[currency]['name']
        
        embed = discord.Embed(
            title=f"💝 Donation Received",
            description=f"{ctx.author.mention} donated **{emoji} {amount:,} {name}** to **{team_info['name']}**!",
            color=team_info['color']
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='teamleaderboard', aliases=['teamlb'])
    async def teamleaderboard(self, ctx):
        """See richest teams ranking"""
        leaderboard = self.data.get_team_leaderboard()
        
        embed = discord.Embed(
            title="🏆 TEAM WEALTH LEADERBOARD",
            description="Top 10 Richest Teams",
            color=0xFFD700
        )
        
        medals = ['🥇', '🥈', '🥉']
        description_text = ""
        
        for i, team_info_data in enumerate(leaderboard[:10]):
            team_id = team_info_data['team_id']
            team_info = TEAMS[team_id]
            medal = medals[i] if i < 3 else f"`{i+1}.`"
            lord = f"<@{team_info_data['lord']}>" if team_info_data['lord'] else "No Lord"
            
            description_text += f"{medal} **{team_info['name']}**\n"
            description_text += f"   💰 {team_info_data['total_wealth']:,} | 👥 {team_info_data['members']} members | Lord: {lord}\n\n"
        
        embed.description = description_text
        embed.set_footer(text="🌑 Dark Empire Teams")
        await ctx.send(embed=embed)
    
    @commands.command(name='requests')
    async def requests(self, ctx):
        """View pending join requests (Lord/Lord Hand only)"""
        current_team_id = self.data.get_user_team(ctx.author.id)
        
        if not current_team_id:
            await ctx.send("❌ You must be in a team!")
            return
        
        team_data = self.data.get_team(current_team_id)
        team_info = TEAMS[current_team_id]
        
        # Check if lord or hand
        if team_data['lord'] != ctx.author.id and team_data['lord_hand'] != ctx.author.id:
            await ctx.send("❌ Only the Lord or Lord Hand can view requests!")
            return
        
        if not team_data['join_requests']:
            await ctx.send("✅ No pending join requests!")
            return
        
        embed = discord.Embed(
            title=f"📨 Join Requests for {team_info['name']}",
            color=team_info['color']
        )
        
        request_text = ""
        for user_id in team_data['join_requests']:
            request_text += f"• <@{user_id}>\n"
        
        embed.description = request_text
        embed.set_footer(text="Use !approve @user or !deny @user")
        await ctx.send(embed=embed)
    
    @commands.command(name='approve')
    async def approve(self, ctx, member: discord.Member):
        """Approve join request"""
        current_team_id = self.data.get_user_team(ctx.author.id)
        
        if not current_team_id:
            await ctx.send("❌ You must be in a team!")
            return
        
        team_data = self.data.get_team(current_team_id)
        team_info = TEAMS[current_team_id]
        
        # Check if lord or hand
        if team_data['lord'] != ctx.author.id and team_data['lord_hand'] != ctx.author.id:
            await ctx.send("❌ Only the Lord or Lord Hand can approve requests!")
            return
        
        if member.id not in team_data['join_requests']:
            await ctx.send(f"❌ {member.mention} doesn't have a pending request!")
            return
        
        # Check if team is full
        if len(team_data['members']) >= 20:
            await ctx.send(f"❌ Team is full (20/20 members)!")
            return
        
        # Approve
        self.data.remove_join_request(member.id, current_team_id)
        self.data.join_team(member.id, current_team_id)
        
        # Assign role
        guild = ctx.guild
        member_role = discord.utils.get(guild.roles, name=f"{team_info['emoji']} {team_info['name']}")
        if member_role:
            await member.add_roles(member_role)
        
        embed = discord.Embed(
            title="✅ Join Request Approved",
            description=f"{member.mention} has joined **{team_info['name']}**!",
            color=0x00FF00
        )
        await ctx.send(embed=embed)
        
        # Notify member
        try:
            notify_embed = discord.Embed(
                title="✅ Request Approved!",
                description=f"Your request to join **{team_info['name']}** has been approved!",
                color=team_info['color']
            )
            await member.send(embed=notify_embed)
        except:
            pass
    
    @commands.command(name='deny')
    async def deny(self, ctx, member: discord.Member):
        """Deny join request"""
        current_team_id = self.data.get_user_team(ctx.author.id)
        
        if not current_team_id:
            await ctx.send("❌ You must be in a team!")
            return
        
        team_data = self.data.get_team(current_team_id)
        team_info = TEAMS[current_team_id]
        
        # Check if lord or hand
        if team_data['lord'] != ctx.author.id and team_data['lord_hand'] != ctx.author.id:
            await ctx.send("❌ Only the Lord or Lord Hand can deny requests!")
            return
        
        if member.id not in team_data['join_requests']:
            await ctx.send(f"❌ {member.mention} doesn't have a pending request!")
            return
        
        # Deny
        self.data.remove_join_request(member.id, current_team_id)
        
        embed = discord.Embed(
            title="❌ Join Request Denied",
            description=f"{member.mention}'s request to join **{team_info['name']}** was denied.",
            color=0xFF0000
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Teams(bot))
