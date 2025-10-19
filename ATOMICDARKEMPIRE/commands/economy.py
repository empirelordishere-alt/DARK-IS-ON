"""
💰 ECONOMY COMMANDS
!wealth, !status, !daily, !leaderboard, !addmoney, !setlevel
"""

import discord
from discord.ext import commands
from datetime import datetime, timedelta
import os
from typing import Optional

OWNER_ID = int(os.getenv('OWNER_ID', 0))

CURRENCIES = {
    'soul_fragments': {'name': '💀 Soul Fragments', 'emoji': '💀'},
    'cursed_essence': {'name': '🔮 Cursed Essence', 'emoji': '🔮'},
    'tombstone_coins': {'name': '🪙 Tombstone Coins', 'emoji': '🪙'},
    'lords_blood': {'name': '🩸 Lord\'s Blood', 'emoji': '🩸'},
    'void_crystals': {'name': '💎 Void Crystals', 'emoji': '💎'}
}


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = bot.data if hasattr(bot, 'data') else None
        # Import data manager if not available
        if not self.data:
            from data_manager import DataManager
            self.data = DataManager()
            bot.data = self.data
    
    @commands.command(name='wealth', aliases=['balance', 'bal', 'money'])
    async def wealth(self, ctx, member: Optional[discord.Member] = None):
        """Check your or someone else's wealth"""
        target = member or ctx.author
        self.data.init_user(target.id)
        user_data = self.data.get_user(target.id)
        
        embed = discord.Embed(
            title=f"💰 {target.display_name}'s Wealth",
            description=f"**Level:** {user_data['level']} | **Messages:** {user_data['messages']} | **Daily Streak:** {user_data['daily_streak']} days",
            color=0x8B00FF
        )
        
        # Add currencies
        for currency_id, currency_info in CURRENCIES.items():
            amount = user_data['currencies'][currency_id]
            embed.add_field(
                name=currency_info['name'],
                value=f"{currency_info['emoji']} {amount:,}",
                inline=True
            )
        
        # Calculate total wealth
        total = sum(user_data['currencies'].values())
        embed.add_field(name="📊 Total Wealth", value=f"{total:,}", inline=False)
        
        # XP Progress
        xp_needed = int(100 * (user_data['level'] ** 1.5))
        progress = int((user_data['xp'] / xp_needed) * 20)
        progress_bar = f"[{'█' * progress}{'░' * (20 - progress)}]"
        embed.add_field(
            name="⚡ XP Progress",
            value=f"{progress_bar} {user_data['xp']}/{xp_needed}",
            inline=False
        )
        
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.set_footer(text="🌑 Dark Empire Economy")
        await ctx.send(embed=embed)
    
    @commands.command(name='status', aliases=['profile', 'stats', 'me'])
    async def status(self, ctx, member: Optional[discord.Member] = None):
        """View detailed profile"""
        target = member or ctx.author
        self.data.init_user(target.id)
        user_data = self.data.get_user(target.id)
        
        # Find rank in leaderboard
        leaderboard = self.data.get_leaderboard(1000)
        rank = next((i+1 for i, u in enumerate(leaderboard) if u['user_id'] == target.id), "Unranked")
        
        # Find richest currency
        richest_currency = max(user_data['currencies'].items(), key=lambda x: x[1])
        
        embed = discord.Embed(
            title=f"📊 {target.display_name}'s Profile",
            color=0x000000
        )
        
        # Basic stats
        embed.add_field(name="🎯 Level", value=user_data['level'], inline=True)
        embed.add_field(name="🏆 Server Rank", value=f"#{rank}", inline=True)
        embed.add_field(name="⭐ Prestige", value=user_data['prestige'], inline=True)
        
        # XP Progress Bar
        xp_needed = int(100 * (user_data['level'] ** 1.5))
        progress = int((user_data['xp'] / xp_needed) * 20)
        progress_bar = f"[{'█' * progress}{'░' * (20 - progress)}]"
        embed.add_field(
            name="⚡ XP Progress",
            value=f"{progress_bar}\n{user_data['xp']}/{xp_needed} XP",
            inline=False
        )
        
        # Richest currency
        currency_name = CURRENCIES[richest_currency[0]]['name']
        embed.add_field(
            name="💎 Richest Currency",
            value=f"{currency_name}: {richest_currency[1]:,}",
            inline=False
        )
        
        # Activity
        embed.add_field(name="💬 Messages Sent", value=user_data['messages'], inline=True)
        embed.add_field(name="🔥 Daily Streak", value=f"{user_data['daily_streak']} days", inline=True)
        
        # Team info
        team_name = user_data.get('team', 'None')
        if team_name:
            from bot import TEAMS
            team_name = TEAMS.get(team_name, {}).get('name', 'None')
        embed.add_field(name="🎯 Team", value=team_name or "No Team", inline=True)
        
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.set_footer(text="🌑 Dark Empire Bot")
        await ctx.send(embed=embed)
    
    @commands.command(name='daily', aliases=['claim'])
    async def daily(self, ctx):
        """Claim daily rewards"""
        self.data.init_user(ctx.author.id)
        user_data = self.data.get_user(ctx.author.id)
        
        now = datetime.now()
        last_daily = user_data.get('last_daily')
        
        # Check cooldown
        if last_daily:
            last_daily_dt = datetime.fromisoformat(last_daily)
            time_diff = now - last_daily_dt
            
            if time_diff < timedelta(hours=24):
                time_left = timedelta(hours=24) - time_diff
                hours = int(time_left.total_seconds() // 3600)
                minutes = int((time_left.total_seconds() % 3600) // 60)
                
                embed = discord.Embed(
                    title="⏰ Daily Reward on Cooldown",
                    description=f"You can claim again in **{hours}h {minutes}m**",
                    color=0xFF0000
                )
                await ctx.send(embed=embed)
                return
            
            # Check streak
            if time_diff < timedelta(hours=48):
                user_data['daily_streak'] += 1
            else:
                user_data['daily_streak'] = 1
        else:
            user_data['daily_streak'] = 1
        
        # Calculate rewards
        base_rewards = {
            'soul_fragments': 500,
            'cursed_essence': 50,
            'tombstone_coins': 250,
            'lords_blood': 10,
            'void_crystals': 5
        }
        
        # Streak bonus
        streak_bonus = min(user_data['daily_streak'] * 50, 1000)
        
        # Apply rewards
        for currency, amount in base_rewards.items():
            user_data['currencies'][currency] += amount
        
        user_data['currencies']['soul_fragments'] += streak_bonus
        user_data['last_daily'] = now.isoformat()
        self.data.save_economy()
        
        # Create embed
        embed = discord.Embed(
            title="🎁 Daily Reward Claimed!",
            description=f"🔥 **Streak:** {user_data['daily_streak']} days",
            color=0x00FF00
        )
        
        for currency, amount in base_rewards.items():
            emoji = CURRENCIES[currency]['emoji']
            name = CURRENCIES[currency]['name']
            embed.add_field(name=name, value=f"{emoji} +{amount:,}", inline=True)
        
        if streak_bonus > 0:
            embed.add_field(
                name="🔥 Streak Bonus",
                value=f"💀 +{streak_bonus:,} Soul Fragments",
                inline=False
            )
        
        embed.set_footer(text=f"Come back in 24 hours! | Streak: {user_data['daily_streak']} days")
        await ctx.send(embed=embed)
    
    @commands.command(name='leaderboard', aliases=['lb', 'top', 'rich'])
    async def leaderboard(self, ctx):
        """See top 10 richest players"""
        leaderboard = self.data.get_leaderboard(10)
        
        if not leaderboard:
            await ctx.send("No data available yet!")
            return
        
        embed = discord.Embed(
            title="🏆 DARK EMPIRE LEADERBOARD",
            description="Top 10 Richest Players",
            color=0xFFD700
        )
        
        medals = ['🥇', '🥈', '🥉']
        
        description_text = ""
        for i, user_info in enumerate(leaderboard):
            try:
                user = await self.bot.fetch_user(user_info['user_id'])
                name = user.name
            except:
                name = f"User {user_info['user_id']}"
            
            medal = medals[i] if i < 3 else f"`{i+1}.`"
            description_text += f"{medal} **{name}**\n"
            description_text += f"   💰 Total: {user_info['total_wealth']:,} | 💀 {user_info['soul_fragments']:,} | 🎯 Lvl {user_info['level']}\n\n"
        
        embed.description = description_text
        
        # Find user's rank
        all_users = self.data.get_leaderboard(1000)
        user_rank = next((i+1 for i, u in enumerate(all_users) if u['user_id'] == ctx.author.id), None)
        
        if user_rank and user_rank > 10:
            user_data = self.data.get_user(ctx.author.id)
            total_wealth = sum(user_data['currencies'].values())
            embed.add_field(
                name="Your Rank",
                value=f"#{user_rank} | 💰 {total_wealth:,}",
                inline=False
            )
        
        embed.set_footer(text="🌑 Dark Empire Economy")
        await ctx.send(embed=embed)
    
    @commands.command(name='addmoney')
    async def addmoney(self, ctx, member: discord.Member, amount: int, currency: str):
        """Add currency to user (Owner only)"""
        if ctx.author.id != OWNER_ID:
            await ctx.send("❌ Only the server owner can use this command!")
            return
        
        if currency not in CURRENCIES:
            await ctx.send(f"❌ Invalid currency! Use: {', '.join(CURRENCIES.keys())}")
            return
        
        self.data.init_user(member.id)
        user_data = self.data.get_user(member.id)
        user_data['currencies'][currency] += amount
        self.data.save_economy()
        
        emoji = CURRENCIES[currency]['emoji']
        name = CURRENCIES[currency]['name']
        
        embed = discord.Embed(
            title="💰 Money Added",
            description=f"Added **{emoji} {amount:,} {name}** to {member.mention}",
            color=0x00FF00
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='setlevel')
    async def setlevel(self, ctx, member: discord.Member, level: int):
        """Set user level (Owner only)"""
        if ctx.author.id != OWNER_ID:
            await ctx.send("❌ Only the server owner can use this command!")
            return
        
        if level < 1 or level > 1000:
            await ctx.send("❌ Level must be between 1 and 1000!")
            return
        
        self.data.init_user(member.id)
        user_data = self.data.get_user(member.id)
        user_data['level'] = level
        user_data['xp'] = 0
        self.data.save_economy()
        
        embed = discord.Embed(
            title="🎯 Level Set",
            description=f"Set {member.mention}'s level to **{level}**",
            color=0x8B00FF
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Economy(bot))
