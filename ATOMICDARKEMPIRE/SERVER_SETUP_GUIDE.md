# 🌑 COMPLETE DARK EMPIRE SERVER SETUP GUIDE

## 🚀 QUICK SETUP (5 COMMANDS)

Run these commands **IN ORDER** to set up your complete Dark Empire server:

```bash
# 1. Create staff roles (EMPEROR LORD, EMPEROR LORD HAND, EMPEROR HELPER)
!setupstaff

# 2. Create main server channels (announcements, general, staff rooms, etc.)
!setupchannels

# 3. Create welcome channel
!setupwelcome

# 4. Build all 20 team structures
!buildatomic

# 5. Fix team permissions (only team members + owners can access)
!fixteampermissions
```

---

## 📋 WHAT EACH COMMAND CREATES

### 1. `!setupstaff` - Creates Staff Roles

**Creates 3 EMPEROR staff roles:**

- **👑 EMPEROR LORD**
  - Role for: Server Owner & Co-Owners
  - Permissions: Full Administrator
  - Color: Dark Red (#8B0000)
  - Can access: Everything

- **🗡️ EMPEROR LORD HAND**
  - Role for: Admins
  - Permissions: Administrator
  - Color: Red (#FF0000)
  - Can access: All channels, moderation commands

- **⚔️ EMPEROR HELPER**
  - Role for: Moderators/Helpers
  - Permissions: Moderation (kick, ban, mute, etc.)
  - Color: Orange (#FF4500)
  - Can access: Staff channels, moderation commands

---

### 2. `!setupchannels` - Creates Main Server Structure

**Creates 4 categories with channels:**

#### 📁 SERVER INFO (Read-only for members)
- **#📢-announcements** - Only owners can post
- **#📜-rules** - Server rules (read-only)
- **#📰-updates** - Server updates (read-only)

#### 📁 GENERAL (Everyone can chat)
- **#💬-general** - General chat
- **#🎮-gaming** - Gaming discussions
- **#🤖-bot-commands** - Bot command usage

#### 📁 VOICE
- **🔊 General Voice** - General voice chat
- **🎤 Gaming Voice** - Gaming voice chat

#### 📁 STAFF (Private - Staff only)
- **#👑-emperor-council** - EMPEROR LORD only
- **#⚔-mod-chat** - All staff can chat
- **#📋-mod-logs** - Moderation logs

---

### 3. `!setupwelcome` - Creates Welcome Channel

Creates **#👋-welcome** with:
- Auto-welcome messages for new members
- Bot commands guide
- Team information
- Getting started instructions

---

### 4. `!buildatomic` - Creates 20 Team Structures

**For EACH of the 20 teams, creates:**
- 3 Roles (Member, Lord, Lord Hand)
- 1 Category
- 4 Text Channels (chat, strategy, commands, stats)
- 1 Voice Channel

**Total:** 180+ Discord items

**Teams:** Blood Vampires, Shadow Phantoms, Toxic Mutants, Soul Collectors, Dark Warlocks, Hellfire Demons, Void Reapers, Ghost Apparitions, Nightmare Creatures, Crystal Wraiths, Abyssal Horrors, Volcanic Demons, Storm Horrors, Cosmic Terrors, Lunar Cults, Eclipse Cults, Forest Haunts, Mountain Wraiths, Inferno Lords, Frost Specters

---

### 5. `!fixteampermissions` - Fixes Team Channel Access

**What it does:**
- ✅ Only team members can access their team channels
- ✅ EMPEROR LORD & EMPEROR LORD HAND can access all teams
- ✅ Adds **#👑-lord-commands** channel to each team (Lord & Hand only)
- ✅ Non-team members **CANNOT** see team channels

**Lord Commands Channel:**
- Only Lord, Lord Hand, and EMPEROR roles can access
- Perfect for team management discussions
- Receive join requests here

---

## 🔒 PERMISSION STRUCTURE

### Channel Access:

| Channel Type | @everyone | Team Member | Lord/Hand | EMPEROR LORD | EMPEROR LORD HAND | EMPEROR HELPER |
|--------------|-----------|-------------|-----------|--------------|-------------------|----------------|
| **Announcements** | Read | Read | Read | Read & Post | Read & Post | Read |
| **Rules/Updates** | Read | Read | Read | Read & Post | Read & Post | Read |
| **General Channels** | Chat | Chat | Chat | Chat | Chat | Chat |
| **Team Channels** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **Lord Commands** | ❌ No | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **Emperor Council** | ❌ No | ❌ No | ❌ No | ✅ Yes | ❌ No | ❌ No |
| **Mod Chat** | ❌ No | ❌ No | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |

---

## 🎯 COMPLETE SERVER STRUCTURE

After running all 5 commands, your server will have:

```
DARK EMPIRE SERVER
│
├── 📁 SERVER INFO
│   ├── 📢 announcements (Owner can post)
│   ├── 📜 rules (Read-only)
│   └── 📰 updates (Owner can post)
│
├── 📁 GENERAL
│   ├── 💬 general
│   ├── 🎮 gaming
│   └── 🤖 bot-commands
│
├── 📁 VOICE
│   ├── 🔊 General Voice
│   └── 🎤 Gaming Voice
│
├── 📁 STAFF (Private)
│   ├── 👑 emperor-council (EMPEROR LORD only)
│   ├── ⚔ mod-chat (All staff)
│   └── 📋 mod-logs (All staff)
│
├── 🩸 BLOOD VAMPIRES (Team 1)
│   ├── 👑 lord-commands (Lord/Hand/EMPEROR only)
│   ├── 💬 chat
│   ├── ⚔ strategy
│   ├── 🎮 commands
│   ├── 📊 stats
│   └── 🎤 Blood Vampires Voice
│
├── 👻 SHADOW PHANTOMS (Team 2)
│   └── ... (same structure)
│
└── ... (18 more teams)
```

---

## 📝 HOW TO USE

### For Server Owner:

1. **Run setup commands** (see Quick Setup above)
2. **Assign staff roles:**
   - Right-click member → Roles
   - Give 👑 EMPEROR LORD to co-owners
   - Give 🗡️ EMPEROR LORD HAND to admins
   - Give ⚔️ EMPEROR HELPER to moderators

3. **Post server rules** in #📜-rules
4. **Make announcements** in #📢-announcements
5. **Manage teams** with `!adminpanel`

### For Members:

1. **Read #👋-welcome** for getting started
2. **Type `!help`** to see all commands
3. **Type `!teams`** to view all teams
4. **Type `!join <team_id>`** to join a team
5. **Only your team channels will be visible**

### For Team Lords:

1. **Check `#👑-lord-commands`** in your team category
2. **Use `!requests`** to see join requests
3. **Use `!approve @user`** to accept members
4. **Use `!appointhand @user`** to appoint second-in-command
5. **Only you, your Hand, and EMPEROR roles can see lord-commands**

---

## ⚡ IMPORTANT NOTES

### Team Channel Privacy:
- ✅ Team members can ONLY see their own team channels
- ✅ EMPEROR LORD & EMPEROR LORD HAND can see ALL teams
- ✅ EMPEROR HELPER cannot see team channels (unless they're a member)
- ❌ Non-members cannot see team channels at all

### Staff Channels:
- **#👑-emperor-council** - ONLY for EMPEROR LORD role
- **#⚔-mod-chat** - All staff (LORD, HAND, HELPER)
- **#📋-mod-logs** - Auto logs all moderation actions

### Join Requests:
- When someone uses `!join <team>`, the Lord gets notified
- Lord/Hand can see requests in `#👑-lord-commands`
- Use `!requests` to view pending requests
- Use `!approve` or `!deny` to manage requests

---

## 🛠️ TROUBLESHOOTING

**If channels don't appear:**
- Make sure you ran `!setupstaff` first
- Check bot has Administrator permission
- Bot's role must be above all created roles

**If permissions don't work:**
- Run `!fixteampermissions` again
- Check role hierarchy (Bot → EMPEROR LORD → Others)
- Verify bot has "Manage Roles" and "Manage Channels"

**If team channels are visible to everyone:**
- Run `!fixteampermissions` to fix
- This command updates all team channel permissions

---

## 🎮 COMMANDS SUMMARY

| Command | What It Does | Owner Only |
|---------|--------------|------------|
| `!setupstaff` | Create 3 EMPEROR staff roles | ✅ |
| `!setupchannels` | Create main server structure | ✅ |
| `!setupwelcome` | Create welcome channel | ✅ |
| `!buildatomic` | Build all 20 teams | ✅ |
| `!fixteampermissions` | Fix team channel access | ✅ |

---

## 🌑 YOU'RE ALL SET!

Your Dark Empire server now has:
- ✅ Staff hierarchy (EMPEROR LORD, HAND, HELPER)
- ✅ Main channels (announcements, general, staff)
- ✅ 20 complete team structures
- ✅ Proper permissions on all channels
- ✅ Private team channels
- ✅ Lord command channels

**Rise to Power in the Dark Empire! 🌑💀**
