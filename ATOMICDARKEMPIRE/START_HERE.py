"""
🌑 ATOMIC DARK EMPIRE BOT - INSTALLATION & USAGE GUIDE
═══════════════════════════════════════════════════════════════

This is your complete Python Discord bot for the Dark Empire server!
"""

print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     🌑 DARK EMPIRE BOT - READY TO LAUNCH! 🌑                 ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

📦 WHAT YOU HAVE:
═════════════════
✅ Complete Discord bot with 44 commands
✅ 20 elite teams (Blood Vampires, Shadow Phantoms, etc.)
✅ 5 currency economy system
✅ Team management with Lord hierarchy
✅ Marketplace with trade verification
✅ Full moderation suite
✅ XP & leveling system
✅ Daily rewards with streaks
✅ Auto-save data system
✅ Complete documentation

📁 FILE STRUCTURE:
══════════════════
QODU/
├── bot.py                 ← Main bot file (START HERE)
├── data_manager.py        ← Data handling
├── requirements.txt       ← Dependencies
├── .env.example           ← Configuration template
│
├── commands/              ← All bot commands
│   ├── economy.py         (8 commands)
│   ├── teams.py           (14 commands)
│   ├── marketplace.py     (7 commands)
│   ├── moderation.py      (5 commands)
│   ├── server_build.py    (7 commands)
│   └── help_admin.py      (3 commands)
│
├── data/                  ← Auto-created on first run
│   ├── economy.json       (User wealth & levels)
│   ├── teams.json         (Team data & vaults)
│   ├── market.json        (Marketplace listings)
│   └── moderation.json    (Mod action logs)
│
└── Documentation/
    ├── README.md          ← Full documentation
    ├── FEATURES.md        ← Feature overview
    ├── COMMANDS.md        ← Command reference
    ├── SETUP_GUIDE.py     ← Setup instructions
    └── PROJECT_SUMMARY.md ← Project summary

🚀 QUICK START (3 STEPS):
══════════════════════════

STEP 1: GET YOUR DISCORD BOT TOKEN
-----------------------------------
1. Go to: https://discord.com/developers/applications
2. Click "New Application"
3. Go to "Bot" → "Add Bot"
4. Copy the token

STEP 2: CONFIGURE THE BOT
--------------------------
1. Copy .env.example to .env:
   
   On Windows:
   copy .env.example .env
   
   On Linux/Mac:
   cp .env.example .env

2. Edit .env file and add:
   
   DISCORD_TOKEN=your_bot_token_here
   OWNER_ID=your_discord_user_id_here
   PREFIX=!

   How to get your Discord User ID:
   - Enable Developer Mode (Settings → Advanced → Developer Mode)
   - Right-click your name → Copy ID

STEP 3: RUN THE BOT
-------------------
Windows:
  Double-click start.bat

Linux/Mac:
  chmod +x start.sh
  ./start.sh

OR manually:
  pip install -r requirements.txt
  python bot.py

🎮 FIRST COMMANDS TO USE:
══════════════════════════
In your Discord server:

!help              # View all commands (interactive menu)
!setupwelcome      # Create welcome channel
!setupstaff        # Create EMPEROR staff roles
!serverstats       # Check bot permissions
!simplebuild       # Test with 1 team (Blood Vampires)
!buildatomic       # Build all 20 teams (~30 min)

💡 WHAT !buildatomic DOES:
═══════════════════════════
Creates for EACH of the 20 teams:
  • 3 Roles (Member, Lord, Lord Hand)
  • 1 Category (with permissions)
  • 4 Text Channels (chat, strategy, commands, stats)
  • 1 Voice Channel (team voice)

TOTAL: 180+ items created automatically!

🎯 THE 20 TEAMS:
════════════════
🩸 Blood Vampires        👻 Shadow Phantoms
🧪 Toxic Mutants         💀 Soul Collectors
🔮 Dark Warlocks         🔥 Hellfire Demons
⚫ Void Reapers          ⚪ Ghost Apparitions
🌈 Nightmare Creatures   💎 Crystal Wraiths
🌊 Abyssal Horrors       🌋 Volcanic Demons
⚡ Storm Horrors         🌌 Cosmic Terrors
🌙 Lunar Cults           ☀ Eclipse Cults
🌿 Forest Haunts         🏔 Mountain Wraiths
🔥 Inferno Lords         ❄ Frost Specters

💎 THE 5 CURRENCIES:
════════════════════
💀 Soul Fragments    - Main currency
🔮 Cursed Essence    - Rare currency
🪙 Tombstone Coins   - Trading currency
🩸 Lord's Blood      - Prestige currency
💎 Void Crystals     - Ultra rare currency

👑 THE 3 STAFF ROLES:
═════════════════════
👑 EMPEROR LORD        - Full Administrator
🗡️ EMPEROR LORD HAND   - Administrator
⚔️ EMPEROR HELPER      - Moderation

📚 ALL 44 COMMANDS:
═══════════════════

💰 ECONOMY (8):
  !wealth, !status, !daily, !leaderboard
  !addmoney, !setlevel

🎯 TEAMS (14):
  !teams, !join, !leaveteam, !teaminfo
  !claimlord, !appointhand, !kickmember, !disbandteam
  !teamvault, !donate, !teamleaderboard
  !requests, !approve, !deny

🛒 MARKETPLACE (7):
  !sell, !market, !mylistings, !cancellisting
  !buy, !verify, !completetrade

🔨 MODERATION (5):
  !kick, !ban, !unban, !mute, !unmute

🏗 SERVER BUILDING (7):
  !buildatomic, !quickbuild, !simplebuild
  !cleanup, !setupwelcome, !setupstaff, !serverstats

📚 HELP & ADMIN (3):
  !help, !adminpanel, !analytics

⚙️ AUTO SYSTEMS:
════════════════
✅ XP Gain: 15 XP per message (60s cooldown)
✅ Level Up: Auto rewards & notifications
✅ Daily Rewards: 500+ currency with streak bonuses
✅ Welcome: New members get 1,000 Soul Fragments
✅ Auto-Save: All data saves to JSON files

🔒 BOT PERMISSIONS NEEDED:
═══════════════════════════
Required:
  ✅ Administrator (RECOMMENDED)

OR individually:
  ✅ Manage Roles
  ✅ Manage Channels
  ✅ Kick Members
  ✅ Ban Members
  ✅ Moderate Members
  ✅ Send Messages
  ✅ Embed Links
  ✅ Read Message History
  ✅ Add Reactions
  ✅ Connect & Speak (for voice)

📖 DOCUMENTATION:
═════════════════
README.md          - Complete guide (start here!)
FEATURES.md        - All features explained
COMMANDS.md        - Command reference card
SETUP_GUIDE.py     - Step-by-step setup
PROJECT_SUMMARY.md - Project overview

❓ TROUBLESHOOTING:
═══════════════════
Bot doesn't start:
  → Check .env file exists and has correct token
  → Verify Python 3.8+ is installed
  → Run: pip install -r requirements.txt

Commands don't work:
  → Check bot is online in server
  → Verify bot has Administrator permission
  → Ensure prefix is correct (default: !)

Build commands fail:
  → Bot needs Manage Roles & Manage Channels
  → Bot's role must be higher than created roles
  → Wait for rate limits (1 sec between operations)

Data not saving:
  → data/ folder will be created automatically
  → Check file permissions
  → Look for error messages in console

🎉 YOU'RE READY!
════════════════
1. ✅ Configure .env
2. ✅ Run python bot.py
3. ✅ Use !setupwelcome
4. ✅ Use !setupstaff
5. ✅ Use !buildatomic
6. ✅ Rise to power in the Dark Empire! 🌑

═══════════════════════════════════════════════════════════════
For full documentation, see README.md
For questions, check SETUP_GUIDE.py
For command list, see COMMANDS.md
═══════════════════════════════════════════════════════════════

🌑 RISE TO POWER IN THE DARK EMPIRE! 🌑💀

""")

# Additional info
print("\n📌 NEXT STEPS:")
print("1. Create .env file with your bot token")
print("2. Run: python bot.py")
print("3. Invite bot to your Discord server")
print("4. Use !help to see all commands")
print("\n🌑 Ready to dominate Discord! 🌑\n")
