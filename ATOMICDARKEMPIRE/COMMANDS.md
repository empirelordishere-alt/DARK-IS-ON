# 🌑 DARK EMPIRE BOT - COMMAND REFERENCE CARD

## 💰 ECONOMY COMMANDS

| Command | Aliases | Description | Example |
|---------|---------|-------------|---------|
| `!wealth [@user]` | balance, bal, money | Check wealth and currencies | `!wealth @User` |
| `!status [@user]` | profile, stats, me | View detailed profile | `!status` |
| `!daily` | claim | Claim daily rewards (24h cooldown) | `!daily` |
| `!leaderboard` | lb, top, rich | Top 10 richest players | `!leaderboard` |
| `!addmoney @user <amt> <curr>` | - | Add currency (Owner) | `!addmoney @User 1000 soul_fragments` |
| `!setlevel @user <level>` | - | Set user level (Owner) | `!setlevel @User 50` |

---

## 🎯 TEAM COMMANDS

| Command | Description | Who Can Use | Example |
|---------|-------------|-------------|---------|
| `!teams` | View all 20 teams | Everyone | `!teams` |
| `!join <team_id>` | Join a team | Everyone | `!join blood_vampires` |
| `!leaveteam` | Leave your team | Team Members | `!leaveteam` |
| `!teaminfo [team_id]` | View team details | Everyone | `!teaminfo dark_warlocks` |
| `!claimlord` | Claim vacant lordship | Team Members | `!claimlord` |
| `!appointhand @user` | Appoint Lord Hand | Team Lord | `!appointhand @User` |
| `!kickmember @user` | Kick team member | Team Lord | `!kickmember @User` |
| `!disbandteam` | Disband the team | Team Lord | `!disbandteam` |
| `!teamvault` | View team vault | Team Members | `!teamvault` |
| `!donate <amt> <curr>` | Donate to vault | Team Members | `!donate 500 soul_fragments` |
| `!teamleaderboard` | Team rankings | Everyone | `!teamleaderboard` |
| `!requests` | View join requests | Lord/Hand | `!requests` |
| `!approve @user` | Approve request | Lord/Hand | `!approve @User` |
| `!deny @user` | Deny request | Lord/Hand | `!deny @User` |

---

## 🛒 MARKETPLACE COMMANDS

| Command | Description | Example |
|---------|-------------|---------|
| `!sell <price> <curr> <item>` | List item for sale | `!sell 500 soul_fragments Dark Sword +10` |
| `!market` | Browse all listings | `!market` |
| `!mylistings` | View your listings | `!mylistings` |
| `!cancellisting <id>` | Cancel your listing | `!cancellisting 5` |
| `!buy <id>` | Purchase an item | `!buy 3` |
| `!verify <id>` | Verify listing (Admin) | `!verify 3` |
| `!completetrade <id>` | Complete trade (Admin) | `!completetrade 3` |

---

## 🔨 MODERATION COMMANDS

| Command | Permission Required | Description | Example |
|---------|---------------------|-------------|---------|
| `!kick @user [reason]` | Kick Members | Kick from server | `!kick @User Spamming` |
| `!ban @user [reason]` | Ban Members | Ban from server | `!ban @User Harassment` |
| `!unban <user_id> [reason]` | Ban Members | Unban user by ID | `!unban 123456789 Appeal` |
| `!mute @user <time> [reason]` | Moderate Members | Timeout member | `!mute @User 1h Spamming` |
| `!unmute @user [reason]` | Moderate Members | Remove timeout | `!unmute @User Time served` |

### Mute Duration Format:
- `60s` = 60 seconds
- `5m` = 5 minutes
- `2h` = 2 hours
- `1d` = 1 day
- `7d` = 7 days
- Max: `28d` = 28 days

---

## 🏗 SERVER BUILDING COMMANDS

| Command | Description | Time | Items Created | Owner Only |
|---------|-------------|------|---------------|------------|
| `!buildatomic` | Build ALL 20 teams | ~30 min | 180+ items | ✅ |
| `!quickbuild` | Build 3 test teams | ~5 min | 24 items | ✅ |
| `!simplebuild` | Build 1 team | ~1 min | 8 items | ✅ |
| `!cleanup` | Delete all teams | ~5 min | Deletes all | ✅ |
| `!setupwelcome` | Create welcome channel | <1 min | 1 channel | ✅ |
| `!setupstaff` | Create staff roles | <1 min | 3 roles | ✅ |
| `!serverstats` | View server stats | Instant | - | Everyone |

---

## 📚 HELP & ADMIN COMMANDS

| Command | Description | Who Can Use |
|---------|-------------|-------------|
| `!help` | Interactive help menu with buttons | Everyone |
| `!adminpanel` | Admin control panel | Owner |
| `!analytics` | Server analytics | Owner |

---

## 🎨 TEAM IDS (for !join command)

| Team Name | Team ID | Emoji |
|-----------|---------|-------|
| Blood Vampires | `blood_vampires` | 🩸 |
| Shadow Phantoms | `shadow_phantoms` | 👻 |
| Toxic Mutants | `toxic_mutants` | 🧪 |
| Soul Collectors | `soul_collectors` | 💀 |
| Dark Warlocks | `dark_warlocks` | 🔮 |
| Hellfire Demons | `hellfire_demons` | 🔥 |
| Void Reapers | `void_reapers` | ⚫ |
| Ghost Apparitions | `ghost_apparitions` | ⚪ |
| Nightmare Creatures | `nightmare_creatures` | 🌈 |
| Crystal Wraiths | `crystal_wraiths` | 💎 |
| Abyssal Horrors | `abyssal_horrors` | 🌊 |
| Volcanic Demons | `volcanic_demons` | 🌋 |
| Storm Horrors | `storm_horrors` | ⚡ |
| Cosmic Terrors | `cosmic_terrors` | 🌌 |
| Lunar Cults | `lunar_cults` | 🌙 |
| Eclipse Cults | `eclipse_cults` | ☀ |
| Forest Haunts | `forest_haunts` | 🌿 |
| Mountain Wraiths | `mountain_wraiths` | 🏔 |
| Inferno Lords | `inferno_lords` | 🔥 |
| Frost Specters | `frost_specters` | ❄ |

---

## 💎 CURRENCY IDS (for !sell, !donate, !addmoney)

| Currency Name | Currency ID | Emoji |
|---------------|-------------|-------|
| Soul Fragments | `soul_fragments` | 💀 |
| Cursed Essence | `cursed_essence` | 🔮 |
| Tombstone Coins | `tombstone_coins` | 🪙 |
| Lord's Blood | `lords_blood` | 🩸 |
| Void Crystals | `void_crystals` | 💎 |

---

## 🚀 QUICK START COMMANDS

### First Time Setup (Owner):
```
!setupwelcome          # Create welcome channel
!setupstaff            # Create staff roles
!simplebuild           # Test with 1 team
!serverstats           # Check bot permissions
!buildatomic           # Build all 20 teams (when ready)
```

### For New Users:
```
!help                  # View all commands
!teams                 # See all teams
!join blood_vampires   # Join a team
!daily                 # Claim daily rewards
!wealth                # Check your balance
```

### For Team Lords:
```
!requests              # View join requests
!approve @user         # Accept member
!appointhand @user     # Appoint second-in-command
!teamvault             # Check team wealth
!kickmember @user      # Remove member
```

### For Moderators:
```
!kick @user reason     # Kick member
!ban @user reason      # Ban member
!mute @user 1h reason  # Timeout member
!verify 123            # Verify marketplace trade
```

---

## ⚡ KEYBOARD SHORTCUTS & TIPS

### Command Aliases (Shorter versions):
- `!bal` instead of `!wealth`
- `!lb` instead of `!leaderboard`
- `!me` instead of `!status`

### Pro Tips:
1. **Daily Streaks**: Claim daily every 24h to build streak bonus
2. **Team Vault**: Donate to help your team compete
3. **XP Farming**: Chat every 60s to maximize XP gain
4. **Marketplace**: Get admin verification before listing valuable items
5. **Team Size**: Max 20 members per team - join early!

---

## 🔥 COMMON WORKFLOWS

### Joining & Managing a Team:
```
1. !teams                    # View all teams
2. !join blood_vampires      # Join team
3. !teaminfo                 # Check team stats
4. !donate 100 soul_fragments # Donate to vault
5. !teamleaderboard          # See rankings
```

### Selling Items:
```
1. !sell 500 soul_fragments Dark Sword +10  # List item
2. Wait for admin: !verify 1                # Admin verifies
3. Buyers use: !buy 1                       # Purchase
```

### Moderating:
```
1. !mute @spammer 1h Spamming chat         # Timeout
2. !kick @troll Breaking rules             # Kick
3. !ban @hacker Hacking attempts           # Ban
4. !unban 123456789 Appeal accepted        # Unban
```

---

## 📊 STATUS CODES & ERRORS

| Message | Meaning | Solution |
|---------|---------|----------|
| "❌ Only the server owner..." | Not the owner | Must be server owner |
| "❌ You don't have permission..." | Missing perms | Get required permission |
| "❌ You must be in a team!" | Not in team | Join a team first |
| "⏰ Daily Reward on Cooldown" | Too soon | Wait 24h from last claim |
| "❌ Team is full (20/20)" | Team maxed | Join different team |
| "⚠️ Not Verified" | Trade not verified | Ask admin to verify |

---

## 🌑 REMEMBER

- **Prefix**: Default is `!` (configurable in .env)
- **Case Sensitive**: Team IDs are lowercase with underscores
- **Currency IDs**: Use underscores (e.g., `soul_fragments`)
- **Mentions**: Use @username for user commands
- **Cooldowns**: 60s for XP, 24h for daily
- **Auto-Save**: All data saves automatically

---

**🌑 Rise to Power in the Dark Empire! 🌑**

**For full documentation, see [`README.md`](README.md)**
