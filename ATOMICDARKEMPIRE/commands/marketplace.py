"""
🛒 MARKETPLACE COMMANDS
!sell, !market, !mylistings, !cancellisting, !buy, !verify, !completetrade
"""

import discord
from discord.ext import commands
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot import CURRENCIES

OWNER_ID = int(os.getenv('OWNER_ID', 0))


class Marketplace(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        from data_manager import DataManager
        self.data = bot.data if hasattr(bot, 'data') else DataManager()
        if not hasattr(bot, 'data'):
            bot.data = self.data
    
    @commands.command(name='sell')
    async def sell(self, ctx, price: int, currency: str, *, item_name: str):
        """List item for sale"""
        if price <= 0:
            await ctx.send("❌ Price must be positive!")
            return
        
        if currency not in CURRENCIES:
            await ctx.send(f"❌ Invalid currency! Use: {', '.join(CURRENCIES.keys())}")
            return
        
        if len(item_name) > 100:
            await ctx.send("❌ Item name too long (max 100 characters)!")
            return
        
        # Create listing
        listing_id = self.data.create_listing(ctx.author.id, price, currency, item_name)
        
        emoji = CURRENCIES[currency]['emoji']
        currency_name = CURRENCIES[currency]['name']
        
        embed = discord.Embed(
            title="🛒 Item Listed for Sale",
            description=f"**Item:** {item_name}\n"
                       f"**Price:** {emoji} {price:,} {currency_name}\n"
                       f"**Listing ID:** #{listing_id}\n\n"
                       f"⚠️ **IMPORTANT:** An admin must verify this trade with `!verify {listing_id}` before buyers can purchase!",
            color=0x00FF00
        )
        embed.set_footer(text=f"Seller: {ctx.author.name}")
        await ctx.send(embed=embed)
    
    @commands.command(name='market', aliases=['marketplace'])
    async def market(self, ctx):
        """Browse all listings"""
        listings = self.data.market['listings']
        
        if not listings:
            await ctx.send("🛒 The marketplace is empty!")
            return
        
        # Show last 10 listings
        recent_listings = listings[-10:]
        
        embed = discord.Embed(
            title="🛒 DARK EMPIRE MARKETPLACE",
            description=f"Showing {len(recent_listings)} most recent listings",
            color=0x8B00FF
        )
        
        for listing in recent_listings:
            try:
                seller = await self.bot.fetch_user(listing['seller_id'])
                seller_name = seller.name
            except:
                seller_name = f"User {listing['seller_id']}"
            
            emoji = CURRENCIES[listing['currency']]['emoji']
            currency_name = CURRENCIES[listing['currency']]['name']
            verified = "✅ Verified" if listing['verified'] else "⚠️ Not Verified"
            
            embed.add_field(
                name=f"#{listing['id']} - {listing['item_name']}",
                value=f"**Price:** {emoji} {listing['price']:,} {currency_name}\n"
                      f"**Seller:** {seller_name}\n"
                      f"**Status:** {verified}",
                inline=False
            )
        
        embed.set_footer(text="Use !buy <id> to purchase | Use !mylistings to see your listings")
        await ctx.send(embed=embed)
    
    @commands.command(name='mylistings')
    async def mylistings(self, ctx):
        """View your active listings"""
        listings = self.data.get_user_listings(ctx.author.id)
        
        if not listings:
            await ctx.send("📭 You have no active listings!")
            return
        
        embed = discord.Embed(
            title="📋 Your Marketplace Listings",
            color=0x8B00FF
        )
        
        for listing in listings:
            emoji = CURRENCIES[listing['currency']]['emoji']
            currency_name = CURRENCIES[listing['currency']]['name']
            verified = "✅ Verified" if listing['verified'] else "⚠️ Not Verified"
            
            embed.add_field(
                name=f"#{listing['id']} - {listing['item_name']}",
                value=f"**Price:** {emoji} {listing['price']:,} {currency_name}\n"
                      f"**Status:** {verified}",
                inline=False
            )
        
        embed.set_footer(text="Use !cancellisting <id> to cancel a listing")
        await ctx.send(embed=embed)
    
    @commands.command(name='cancellisting')
    async def cancellisting(self, ctx, listing_id: int):
        """Cancel your listing"""
        listing = self.data.get_listing(listing_id)
        
        if not listing:
            await ctx.send(f"❌ Listing #{listing_id} not found!")
            return
        
        if listing['seller_id'] != ctx.author.id:
            await ctx.send("❌ You can only cancel your own listings!")
            return
        
        # Remove listing
        self.data.remove_listing(listing_id)
        
        embed = discord.Embed(
            title="🗑️ Listing Cancelled",
            description=f"Listing #{listing_id} for **{listing['item_name']}** has been cancelled.",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='buy')
    async def buy(self, ctx, listing_id: int):
        """Purchase an item"""
        listing = self.data.get_listing(listing_id)
        
        if not listing:
            await ctx.send(f"❌ Listing #{listing_id} not found!")
            return
        
        if listing['seller_id'] == ctx.author.id:
            await ctx.send("❌ You can't buy your own listing!")
            return
        
        # Check if verified
        if not listing['verified']:
            await ctx.send("⚠️ This listing hasn't been verified by an admin yet! Ask an admin to use `!verify {listing_id}`")
            return
        
        # Check buyer balance
        self.data.init_user(ctx.author.id)
        buyer_data = self.data.get_user(ctx.author.id)
        
        currency = listing['currency']
        price = listing['price']
        
        if buyer_data['currencies'][currency] < price:
            emoji = CURRENCIES[currency]['emoji']
            currency_name = CURRENCIES[currency]['name']
            await ctx.send(f"❌ You don't have enough {emoji} {currency_name}! You need {price:,} but have {buyer_data['currencies'][currency]:,}")
            return
        
        # Get seller
        try:
            seller = await self.bot.fetch_user(listing['seller_id'])
        except:
            await ctx.send("❌ Seller not found!")
            return
        
        # Transfer currency
        buyer_data['currencies'][currency] -= price
        
        seller_data = self.data.get_user(listing['seller_id'])
        seller_data['currencies'][currency] += price
        
        # Remove listing
        self.data.remove_listing(listing_id)
        self.data.save_economy()
        
        emoji = CURRENCIES[currency]['emoji']
        currency_name = CURRENCIES[currency]['name']
        
        # Notify buyer
        embed = discord.Embed(
            title="✅ Purchase Complete!",
            description=f"You purchased **{listing['item_name']}** for {emoji} {price:,} {currency_name}\n\n"
                       f"**Seller:** {seller.mention}\n"
                       f"**Contact them to arrange delivery!**",
            color=0x00FF00
        )
        await ctx.send(embed=embed)
        
        # Notify seller
        try:
            seller_embed = discord.Embed(
                title="💰 Item Sold!",
                description=f"Your **{listing['item_name']}** was sold for {emoji} {price:,} {currency_name}!\n\n"
                           f"**Buyer:** {ctx.author.mention} ({ctx.author.name})\n"
                           f"**Contact them to arrange delivery!**",
                color=0x00FF00
            )
            await seller.send(embed=seller_embed)
        except:
            pass
    
    @commands.command(name='verify')
    @commands.has_permissions(administrator=True)
    async def verify(self, ctx, listing_id: int):
        """Verify trade is legitimate (Admin only)"""
        listing = self.data.get_listing(listing_id)
        
        if not listing:
            await ctx.send(f"❌ Listing #{listing_id} not found!")
            return
        
        if listing['verified']:
            await ctx.send(f"✅ Listing #{listing_id} is already verified!")
            return
        
        # Verify listing
        listing['verified'] = True
        self.data.save_market()
        
        embed = discord.Embed(
            title="✅ Listing Verified",
            description=f"Listing #{listing_id} for **{listing['item_name']}** has been verified!\n"
                       f"Buyers can now purchase this item.",
            color=0x00FF00
        )
        await ctx.send(embed=embed)
        
        # Notify seller
        try:
            seller = await self.bot.fetch_user(listing['seller_id'])
            seller_embed = discord.Embed(
                title="✅ Your Listing Was Verified!",
                description=f"Your listing for **{listing['item_name']}** (#{listing_id}) has been verified by {ctx.author.mention}!\n"
                           f"It can now be purchased by buyers.",
                color=0x00FF00
            )
            await seller.send(embed=seller_embed)
        except:
            pass
    
    @commands.command(name='completetrade')
    @commands.has_permissions(administrator=True)
    async def completetrade(self, ctx, listing_id: int):
        """Complete verified trade (Admin only)"""
        listing = self.data.get_listing(listing_id)
        
        if not listing:
            await ctx.send(f"❌ Listing #{listing_id} not found!")
            return
        
        # Remove listing
        self.data.remove_listing(listing_id)
        
        embed = discord.Embed(
            title="✅ Trade Completed",
            description=f"Listing #{listing_id} has been marked as complete and removed.",
            color=0x00FF00
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Marketplace(bot))
