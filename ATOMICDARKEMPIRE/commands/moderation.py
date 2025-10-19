"""
🔨 MODERATION COMMANDS
!kick, !ban, !unban, !mute, !unmute
"""

import discord
from discord.ext import commands
from datetime import timedelta
from typing import Optional
import re


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        from data_manager import DataManager
        self.data = bot.data if hasattr(bot, 'data') else DataManager()
        if not hasattr(bot, 'data'):
            bot.data = self.data
    
    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
        """Kick member from server"""
        if member.id == ctx.author.id:
            await ctx.send("❌ You can't kick yourself!")
            return
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ You can't kick someone with a higher or equal role!")
            return
        
        if member.top_role >= ctx.guild.me.top_role:
            await ctx.send("❌ I can't kick someone with a higher or equal role than me!")
            return
        
        # Log moderation action
        self.data.log_moderation('kick', ctx.author.id, member.id, reason)
        
        # Send DM to member
        try:
            dm_embed = discord.Embed(
                title="⚠️ You were kicked",
                description=f"**Server:** {ctx.guild.name}\n"
                           f"**Moderator:** {ctx.author.name}\n"
                           f"**Reason:** {reason}",
                color=0xFF0000
            )
            await member.send(embed=dm_embed)
        except:
            pass
        
        # Kick member
        await member.kick(reason=f"[{ctx.author.name}] {reason}")
        
        # Send confirmation
        embed = discord.Embed(
            title="👢 Member Kicked",
            description=f"**Member:** {member.mention} ({member.name})\n"
                       f"**Moderator:** {ctx.author.mention}\n"
                       f"**Reason:** {reason}",
            color=0xFF4500
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
        """Ban member from server"""
        if member.id == ctx.author.id:
            await ctx.send("❌ You can't ban yourself!")
            return
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ You can't ban someone with a higher or equal role!")
            return
        
        if member.top_role >= ctx.guild.me.top_role:
            await ctx.send("❌ I can't ban someone with a higher or equal role than me!")
            return
        
        # Log moderation action
        self.data.log_moderation('ban', ctx.author.id, member.id, reason)
        
        # Send DM to member
        try:
            dm_embed = discord.Embed(
                title="🔨 You were banned",
                description=f"**Server:** {ctx.guild.name}\n"
                           f"**Moderator:** {ctx.author.name}\n"
                           f"**Reason:** {reason}",
                color=0xFF0000
            )
            await member.send(embed=dm_embed)
        except:
            pass
        
        # Ban member
        await member.ban(reason=f"[{ctx.author.name}] {reason}", delete_message_days=0)
        
        # Send confirmation
        embed = discord.Embed(
            title="🔨 Member Banned",
            description=f"**Member:** {member.mention} ({member.name})\n"
                       f"**Moderator:** {ctx.author.mention}\n"
                       f"**Reason:** {reason}",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: int, *, reason: Optional[str] = "No reason provided"):
        """Unban user by ID"""
        try:
            user = await self.bot.fetch_user(user_id)
        except:
            await ctx.send(f"❌ User with ID {user_id} not found!")
            return
        
        # Check if user is banned
        try:
            await ctx.guild.unban(user, reason=f"[{ctx.author.name}] {reason}")
        except discord.NotFound:
            await ctx.send(f"❌ {user.name} is not banned!")
            return
        
        # Log moderation action
        self.data.log_moderation('unban', ctx.author.id, user.id, reason)
        
        # Send confirmation
        embed = discord.Embed(
            title="✅ Member Unbanned",
            description=f"**Member:** {user.mention} ({user.name})\n"
                       f"**Moderator:** {ctx.author.mention}\n"
                       f"**Reason:** {reason}",
            color=0x00FF00
        )
        await ctx.send(embed=embed)
    
    def parse_duration(self, duration_str: str) -> Optional[timedelta]:
        """Parse duration string like '60s', '5m', '2h', '1d', '7d'"""
        pattern = r'^(\d+)([smhd])$'
        match = re.match(pattern, duration_str)
        
        if not match:
            return None
        
        amount, unit = match.groups()
        amount = int(amount)
        
        if unit == 's':
            return timedelta(seconds=amount)
        elif unit == 'm':
            return timedelta(minutes=amount)
        elif unit == 'h':
            return timedelta(hours=amount)
        elif unit == 'd':
            return timedelta(days=amount)
        
        return None
    
    @commands.command(name='mute')
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, duration: str, *, reason: Optional[str] = "No reason provided"):
        """Timeout member"""
        if member.id == ctx.author.id:
            await ctx.send("❌ You can't mute yourself!")
            return
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ You can't mute someone with a higher or equal role!")
            return
        
        if member.top_role >= ctx.guild.me.top_role:
            await ctx.send("❌ I can't mute someone with a higher or equal role than me!")
            return
        
        # Parse duration
        duration_td = self.parse_duration(duration)
        
        if not duration_td:
            await ctx.send("❌ Invalid duration! Use format like: `60s`, `5m`, `2h`, `1d`, `7d`")
            return
        
        # Max duration is 28 days
        if duration_td > timedelta(days=28):
            await ctx.send("❌ Maximum timeout duration is 28 days!")
            return
        
        # Log moderation action
        self.data.log_moderation('mute', ctx.author.id, member.id, f"{duration} - {reason}")
        
        # Timeout member
        await member.timeout(duration_td, reason=f"[{ctx.author.name}] {reason}")
        
        # Send DM to member
        try:
            dm_embed = discord.Embed(
                title="🔇 You were muted",
                description=f"**Server:** {ctx.guild.name}\n"
                           f"**Moderator:** {ctx.author.name}\n"
                           f"**Duration:** {duration}\n"
                           f"**Reason:** {reason}",
                color=0xFFA500
            )
            await member.send(embed=dm_embed)
        except:
            pass
        
        # Send confirmation
        embed = discord.Embed(
            title="🔇 Member Muted",
            description=f"**Member:** {member.mention} ({member.name})\n"
                       f"**Moderator:** {ctx.author.mention}\n"
                       f"**Duration:** {duration}\n"
                       f"**Reason:** {reason}",
            color=0xFFA500
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='unmute')
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
        """Remove timeout"""
        if not member.is_timed_out():
            await ctx.send(f"❌ {member.mention} is not muted!")
            return
        
        # Log moderation action
        self.data.log_moderation('unmute', ctx.author.id, member.id, reason)
        
        # Remove timeout
        await member.timeout(None, reason=f"[{ctx.author.name}] {reason}")
        
        # Send DM to member
        try:
            dm_embed = discord.Embed(
                title="🔊 You were unmuted",
                description=f"**Server:** {ctx.guild.name}\n"
                           f"**Moderator:** {ctx.author.name}\n"
                           f"**Reason:** {reason}",
                color=0x00FF00
            )
            await member.send(embed=dm_embed)
        except:
            pass
        
        # Send confirmation
        embed = discord.Embed(
            title="🔊 Member Unmuted",
            description=f"**Member:** {member.mention} ({member.name})\n"
                       f"**Moderator:** {ctx.author.mention}\n"
                       f"**Reason:** {reason}",
            color=0x00FF00
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
