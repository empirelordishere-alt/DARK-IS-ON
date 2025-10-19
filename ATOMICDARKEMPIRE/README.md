# 🌑 ATOMIC DARK EMPIRE BOT

A complete Discord server management system with economy, teams, marketplace, and moderation features.

## 🎯 FEATURES

### 💰 Economy System
- **5 Currencies**: Soul Fragments, Cursed Essence, Tombstone Coins, Lord's Blood, Void Crystals
- **XP & Leveling**: Gain 15 XP per message (60s cooldown), level up for rewards
- **Daily Rewards**: Claim daily with streak bonuses (up to +1,000 at Day 20+)
- **Leaderboards**: Track top 10 richest players

### 🎯 Team System (20 Teams)
- **20 Elite Teams**: Blood Vampires, Shadow Phantoms, Toxic Mutants, and 17 more
- **Team Hierarchy**: Lord → Lord Hand → Members
- **Team Vault**: Shared currency pool with donations
- **Join Requests**: Request system for joining teams
- **Team Commands**: 14 comprehensive team management commands

### 🛒 Marketplace
- **Buy/Sell System**: List items for sale with any currency
- **Admin Verification**: Trades require admin approval for safety
- **Listing Management**: View, cancel, and manage your listings

### 🔨 Moderation
- **Kick/Ban**: Full moderation with reason logging
- **Timeout System**: Mute members with flexible durations (60s to 28d)
- **Action Logging**: All mod actions saved to moderation.json

### 🏗 Server Building
- **!buildatomic**: Creates ALL 20 teams (~30 min, 180+ items)
  - 60 Roles (3 per team)
  - 20 Categories
  - 80 Text Channels (4 per team)
  - 20 Voice Channels
- **!quickbuild**: 3 test teams for testing
- **!simplebuild**: 1 team for quick testing

### 👑 Staff Roles
- **EMPEROR LORD**: Full administrator access
- **EMPEROR LORD HAND**: Administrator permissions
- **EMPEROR HELPER**: Moderation permissions

## 🚀 QUICK START

### 1. Prerequisites
- Python 3.8 or higher
- Discord Bot Token ([Get one here](https://discord.com/developers/applications))
- Your Discord User ID

### 2. Installation

```bash
# Clone or download this repository
cd QODU

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in the root directory:

```env
DISCORD_TOKEN=your_bot_token_here
OWNER_ID=your_discord_user_id_here
PREFIX=!
```

**How to get your Discord User ID:**
1. Enable Developer Mode in Discord (Settings → Advanced → Developer Mode)
2. Right-click your username → Copy ID

### 4. Run the Bot

```bash
python bot.py
```

## 📋 COMMAND LIST

### 💰 Economy Commands (8)
- `!wealth` / `!balance` / `!bal` / `!money` - Check wealth
- `!status` / `!profile` / `!stats` / `!me` - View profile
- `!daily` / `!claim` - Claim daily rewards
- `!leaderboard` / `!lb` / `!top` / `!rich` - View leaderboard
- `!addmoney @user <amount> <currency>` - Add money (Owner)
- `!setlevel @user <level>` - Set level (Owner)

### 🎯 Team Commands (14)
- `!teams` - View all 20 teams
- `!join <team_id>` - Join a team
- `!leaveteam` - Leave your team
- `!teaminfo [team_id]` - View team info
- `!claimlord` - Become Lord if vacant
- `!appointhand @user` - Appoint Lord Hand (Lord only)
- `!kickmember @user` - Kick member (Lord only)
- `!disbandteam` - Disband team (Lord only)
- `!teamvault` - Check team vault
- `!donate <amount> <currency>` - Donate to vault
- `!teamleaderboard` - Team wealth rankings
- `!requests` - View join requests (Lord/Hand)
- `!approve @user` - Approve request (Lord/Hand)
- `!deny @user` - Deny request (Lord/Hand)

### 🛒 Marketplace Commands (6)
- `!sell <price> <currency> <item_name>` - List item
- `!market` / `!marketplace` - Browse listings
- `!mylistings` - View your listings
- `!cancellisting <id>` - Cancel listing
- `!buy <listing_id>` - Purchase item
- `!verify <trade_id>` - Verify trade (Admin)
- `!completetrade <trade_id>` - Complete trade (Admin)

### 🔨 Moderation Commands (5)
- `!kick @user [reason]` - Kick member
- `!ban @user [reason]` - Ban member
- `!unban <user_id> [reason]` - Unban user
- `!mute @user <duration> [reason]` - Timeout member
- `!unmute @user [reason]` - Remove timeout

### 🏗 Server Building Commands (7)
- `!buildatomic` - Build ALL 20 teams (Owner)
- `!quickbuild` - Build 3 test teams (Owner)
- `!simplebuild` - Build 1 team (Owner)
- `!cleanup` - Delete all teams (Owner)
- `!setupwelcome` - Create welcome channel (Owner)
- `!setupstaff` - Create staff roles (Owner)
- `!serverstats` - View server statistics

### 📚 Help & Admin Commands (3)
- `!help` - Interactive help menu
- `!adminpanel` - Admin control panel (Owner)
- `!analytics` - Server analytics (Owner)

## 🎨 THE 20 TEAMS

| Team Name | Emoji | Color | Team ID |
|-----------|-------|-------|---------|
| Blood Vampires | 🩸 | Red | blood_vampires |
| Shadow Phantoms | 👻 | Dark Gray | shadow_phantoms |
| Toxic Mutants | 🧪 | Green | toxic_mutants |
| Soul Collectors | 💀 | Gray | soul_collectors |
| Dark Warlocks | 🔮 | Purple | dark_warlocks |
| Hellfire Demons | 🔥 | Orange | hellfire_demons |
| Void Reapers | ⚫ | Black | void_reapers |
| Ghost Apparitions | ⚪ | White | ghost_apparitions |
| Nightmare Creatures | 🌈 | Violet | nightmare_creatures |
| Crystal Wraiths | 💎 | Cyan | crystal_wraiths |
| Abyssal Horrors | 🌊 | Blue | abyssal_horrors |
| Volcanic Demons | 🌋 | Coral | volcanic_demons |
| Storm Horrors | ⚡ | Yellow | storm_horrors |
| Cosmic Terrors | 🌌 | Navy | cosmic_terrors |
| Lunar Cults | 🌙 | Silver | lunar_cults |
| Eclipse Cults | ☀ | Orange | eclipse_cults |
| Forest Haunts | 🌿 | Green | forest_haunts |
| Mountain Wraiths | 🏔 | Gray | mountain_wraiths |
| Inferno Lords | 🔥 | Crimson | inferno_lords |
| Frost Specters | ❄ | Light Blue | frost_specters |

## 💎 THE 5 CURRENCIES

| Currency | Emoji | Description |
|----------|-------|-------------|
| Soul Fragments | 💀 | Main currency (most common) |
| Cursed Essence | 🔮 | Rare currency |
| Tombstone Coins | 🪙 | Trading currency |
| Lord's Blood | 🩸 | Team/prestige currency |
| Void Crystals | 💎 | Ultra rare currency |

## ⚙️ AUTO SYSTEMS

### XP Gain
- **15 XP per message** (60-second cooldown)
- Automatic level-up notifications
- Currency rewards on level up

### Daily Rewards
- **Base**: 500 Soul Fragments + other currencies
- **Streak Bonus**: Up to +1,000 at Day 20+
- 24-hour cooldown

### Welcome System
- New members get **1,000 Soul Fragments** starter bonus
- Automatic welcome message in #welcome channel

### Data Saving
- All data auto-saves to JSON files
- Files stored in `/data` directory

## 📁 FILE STRUCTURE

```
QODU/
├── bot.py                    # Main bot file
├── data_manager.py           # Data handling & JSON operations
├── requirements.txt          # Python dependencies
├── .env                      # Configuration (create this)
├── .env.example              # Environment template
├── README.md                 # This file
├── commands/
│   ├── economy.py            # Economy commands
│   ├── teams.py              # Team commands
│   ├── marketplace.py        # Market commands
│   ├── moderation.py         # Moderation commands
│   ├── server_build.py       # Server building commands
│   └── help_admin.py         # Help & admin commands
└── data/
    ├── economy.json          # User wealth & levels
    ├── teams.json            # Team data & vaults
    ├── market.json           # Marketplace listings
    └── moderation.json       # Mod action logs
```

## 🔧 BOT PERMISSIONS

The bot requires these permissions:
- **Administrator** (recommended) OR:
  - Manage Roles
  - Manage Channels
  - Manage Messages
  - Kick Members
  - Ban Members
  - Moderate Members (for timeouts)
  - Send Messages
  - Embed Links
  - Attach Files
  - Read Message History
  - Add Reactions
  - Connect (voice)
  - Speak (voice)

## 🎮 GETTING STARTED (For Users)

1. **Check your wealth**: `!wealth`
2. **View teams**: `!teams`
3. **Join a team**: `!join blood_vampires`
4. **Claim daily**: `!daily`
5. **View profile**: `!status`
6. **See help**: `!help`

## 👑 GETTING STARTED (For Server Owner)

1. **Setup welcome**: `!setupwelcome`
2. **Create staff roles**: `!setupstaff`
3. **Test with 1 team**: `!simplebuild`
4. **Build all teams**: `!buildatomic` (takes ~30 min)
5. **View admin panel**: `!adminpanel`

## 🛡️ MODERATION

All moderation actions are logged to `data/moderation.json` with:
- Action type (kick/ban/mute/etc)
- Moderator ID
- Target user ID
- Reason
- Timestamp

## 📊 DATA FILES

### economy.json
Stores user data:
- Currencies (all 5 types)
- Level & XP
- Messages sent
- Daily streak
- Team membership

### teams.json
Stores team data:
- Lord & Lord Hand
- Member list
- Team vault currencies
- Join requests

### market.json
Stores marketplace:
- Active listings
- Seller info
- Prices & currencies
- Verification status

### moderation.json
Stores mod logs:
- All moderation actions
- Timestamps
- Reasons

## ⚠️ IMPORTANT NOTES

### Rate Limits
- Discord has rate limits for creating channels/roles
- `!buildatomic` takes ~30 minutes to avoid rate limits
- Uses 1-second delays between creations

### Team Limits
- Max 20 members per team
- Lords cannot leave (must disband)
- Lord Hands can be replaced

### Marketplace Safety
- All trades require admin verification
- Use `!verify <id>` before buyers can purchase
- Prevents scams and fraud

## 🐛 TROUBLESHOOTING

**Bot doesn't respond:**
- Check bot is online
- Verify token in `.env` is correct
- Ensure bot has permissions

**Commands don't work:**
- Check prefix is correct (default `!`)
- Ensure you have required permissions
- Check bot can see the channel

**Build commands fail:**
- Ensure bot has Manage Roles & Manage Channels
- Check bot's role is high enough in hierarchy
- Wait for rate limits (1 sec between operations)

**Data not saving:**
- Check `/data` folder exists
- Ensure bot has write permissions
- Check JSON files aren't corrupted

## 📝 LICENSE

MIT License - Feel free to use and modify!

## 🌑 CREDITS

Created for the Dark Empire Discord Server
Bot Version: 1.0.0
Discord.py Version: 2.3.2

---

**🌑 Rise to Power in the Dark Empire! 🌑**
