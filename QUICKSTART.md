# Quick Start Guide

Get your Raspberry Pi Discord Monitor Bot up and running in minutes!

## Prerequisites Checklist

- [ ] Raspberry Pi (or any Linux/Windows system)
- [ ] Python 3.8 or higher installed
- [ ] Discord account
- [ ] Discord server where you have admin permissions

## Step 1: Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**
3. Give it a name (e.g., "System Monitor")
4. Go to the **"Bot"** section in the left sidebar
5. Click **"Add Bot"**
6. Under the bot's username, click **"Reset Token"** and copy it (you'll need this later)
7. Enable these **Privileged Gateway Intents**:
   - Message Content Intent

## Step 2: Invite Bot to Your Server

1. In the Developer Portal, go to **"OAuth2"** → **"URL Generator"**
2. Select these **Scopes**:
   - `bot`
3. Select these **Bot Permissions**:
   - Send Messages
   - Embed Links
   - Read Message History
4. Copy the generated URL at the bottom
5. Paste it in your browser and select your server
6. Click **"Authorize"**

## Step 3: Get Your Channel ID

1. Open Discord and enable **Developer Mode**:
   - User Settings → Advanced → Developer Mode (toggle ON)
2. Right-click the channel where you want logs to appear
3. Click **"Copy Channel ID"**
4. Save this ID for the next step

## Step 4: Install the Bot

### On Raspberry Pi / Linux:

```bash
# Clone the repository
git clone https://github.com/yourusername/rasberry-pie-monitor.git
cd rasberry-pie-monitor

# Run the setup script
chmod +x setup.sh
./setup.sh
```

### On Windows:

```cmd
# Clone the repository
git clone https://github.com/yourusername/rasberry-pie-monitor.git
cd rasberry-pie-monitor

# Run the setup script
setup.bat
```

### Manual Setup (All Platforms):

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

## Step 5: Configure Your Bot

1. Open the `.env` file in a text editor
2. Add your bot token and channel ID:

```env
DISCORD_TOKEN=your_bot_token_here
DEFAULT_CHANNEL_ID=your_channel_id_here
DEFAULT_INTERVAL=60
```

3. Save the file

## Step 6: Run Your Bot

```bash
# Make sure virtual environment is activated
# Then run:
python code.py
```

You should see:
```
Logged in as YourBotName#1234
```

## Step 7: Test Your Bot

In your Discord server, try these commands:

1. `!help` - See all available commands
2. `!getchannel` - Verify the logging channel
3. Wait for the first automatic system stats message!

## Common Issues

### Bot doesn't start
- Check that your token is correct in `.env`
- Make sure all dependencies are installed: `pip install -r requirements.txt`

### Bot can't send messages
- Verify the bot has "Send Messages" permission in your channel
- Check that the channel ID is correct
- Use `!setchannel` to configure a different channel

### Temperature shows "N/A"
- This is normal on non-Raspberry Pi systems
- The `vcgencmd` tool is Raspberry Pi specific

### "Module not found" errors
- Make sure you activated the virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

## What's Next?

- Customize the logging interval with `!setinterval`
- Change the logging channel with `!setchannel`
- **Important**: Remove or secure the `!run` command (see [SECURITY.md](SECURITY.md))
- Explore the code and add your own features!

## Getting Help

- Check the [README.md](README.md) for detailed documentation
- Review [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Open an issue on GitHub if you need help

---

**Important Security Note**: The `!run` command allows shell access. For production use, remove this command or implement strict role-based permissions. See [SECURITY.md](SECURITY.md) for details.
