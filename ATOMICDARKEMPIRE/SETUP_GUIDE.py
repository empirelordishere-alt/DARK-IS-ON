"""
🌑 QUICK SETUP GUIDE - DARK EMPIRE BOT
Follow these steps to get your bot running!
"""

# STEP 1: GET A DISCORD BOT TOKEN
# ================================
# 1. Go to https://discord.com/developers/applications
# 2. Click "New Application" and give it a name (e.g., "Dark Empire Bot")
# 3. Go to the "Bot" section in the left sidebar
# 4. Click "Add Bot" → "Yes, do it!"
# 5. Under "Token", click "Copy" to copy your bot token
# 6. IMPORTANT: Keep this token secret! Never share it!

# STEP 2: GET YOUR DISCORD USER ID
# =================================
# 1. Open Discord
# 2. Go to Settings → Advanced → Enable "Developer Mode"
# 3. Right-click your username anywhere → Copy ID
# 4. This is your User ID (a long number)

# STEP 3: INVITE THE BOT TO YOUR SERVER
# ======================================
# 1. In Discord Developer Portal, go to "OAuth2" → "URL Generator"
# 2. Select these scopes:
#    - bot
#    - applications.commands
# 3. Select these bot permissions:
#    - Administrator (recommended)
#    OR select individually:
#    - Manage Roles
#    - Manage Channels
#    - Kick Members
#    - Ban Members
#    - Moderate Members
#    - Send Messages
#    - Manage Messages
#    - Embed Links
#    - Read Message History
#    - Add Reactions
#    - Connect
#    - Speak
# 4. Copy the generated URL at the bottom
# 5. Paste it in your browser and select your server
# 6. Click "Authorize"

# STEP 4: CONFIGURE THE BOT
# ==========================
# 1. Copy .env.example to .env
# 2. Edit .env and fill in:
#    DISCORD_TOKEN=paste_your_bot_token_here
#    OWNER_ID=paste_your_user_id_here
#    PREFIX=!

# STEP 5: INSTALL PYTHON (if not installed)
# ==========================================
# 1. Go to https://www.python.org/downloads/
# 2. Download Python 3.8 or higher
# 3. Run installer
# 4. IMPORTANT: Check "Add Python to PATH" during installation

# STEP 6: RUN THE BOT
# ===================
# Windows:
#   Double-click start.bat
#
# Linux/Mac:
#   chmod +x start.sh
#   ./start.sh
#
# OR manually:
#   pip install -r requirements.txt
#   python bot.py

# STEP 7: TEST THE BOT
# =====================
# In your Discord server, type:
#   !help         - View all commands
#   !setupwelcome - Create welcome channel
#   !setupstaff   - Create staff roles
#   !simplebuild  - Test with 1 team
#   !serverstats  - Check bot permissions

# STEP 8: BUILD YOUR EMPIRE
# ==========================
# When ready, use:
#   !buildatomic  - Build all 20 teams (~30 minutes)
#
# This creates:
#   - 60 Roles (3 per team)
#   - 20 Categories
#   - 80 Text Channels (4 per team)
#   - 20 Voice Channels
#   TOTAL: 180+ items!

# TROUBLESHOOTING
# ===============
# Bot doesn't respond:
#   - Check bot is online in server
#   - Verify token in .env is correct
#   - Make sure bot has permissions
#
# Build commands fail:
#   - Ensure bot has "Manage Roles" permission
#   - Ensure bot has "Manage Channels" permission
#   - Bot's role must be above created roles
#
# Commands show errors:
#   - Check you have correct permissions
#   - Make sure you're using correct prefix (default: !)
#
# Data not saving:
#   - Make sure data/ folder exists
#   - Check bot has write permissions

# SUPPORT
# =======
# Check README.md for full documentation
# All commands are listed in !help

print("""
╔═══════════════════════════════════════════════════════════╗
║  🌑 DARK EMPIRE BOT SETUP COMPLETE!                      ║
║                                                           ║
║  Next Steps:                                              ║
║  1. Configure your .env file                              ║
║  2. Run start.bat (Windows) or start.sh (Linux/Mac)       ║
║  3. Invite bot to your server                             ║
║  4. Use !setupwelcome and !setupstaff                     ║
║  5. Use !simplebuild to test                              ║
║  6. Use !buildatomic when ready for full build            ║
║                                                           ║
║  Rise to Power in the Dark Empire! 🌑                     ║
╚═══════════════════════════════════════════════════════════╝
""")
