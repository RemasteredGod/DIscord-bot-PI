# 🖥️ Raspberry Pi Discord System Monitor Bot

A Discord bot that monitors and reports Raspberry Pi system statistics including CPU temperature, CPU usage, RAM usage, and disk usage. The bot provides real-time system monitoring through Discord with customizable logging intervals and channels.

## ✨ Features

- **Real-time System Monitoring**: Continuously monitors CPU temperature, CPU usage, RAM, and disk space
- **Customizable Logging**: Configure logging interval and destination channel through Discord commands
- **Interactive UI**: User-friendly dropdown menus and buttons for configuration
- **Shell Command Execution**: Run shell commands remotely via Discord (use with caution!)
- **Rich Embeds**: Beautiful Discord embeds with proper formatting and timestamps
- **Automatic Updates**: Periodic system stats updates sent to configured channel

## 📋 Prerequisites

- Python 3.8 or higher
- Raspberry Pi (for temperature monitoring; other systems supported with limited features)
- Discord Bot Token ([Create one here](https://discord.com/developers/applications))

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/rasberry-pie-monitor.git
   cd rasberry-pie-monitor
   ```

2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot**
   
   Open `code.py` and update the following configuration:
   ```python
   TOKEN = "YOUR_DISCORD_BOT_TOKEN"  # Replace with your bot token
   DEFAULT_CHANNEL_ID = YOUR_CHANNEL_ID  # Replace with default channel ID
   DEFAULT_INTERVAL = 60  # Default logging interval in seconds
   ```

## 📦 Dependencies

Create a `requirements.txt` file with the following dependencies:

```txt
discord.py>=2.0.0
psutil>=5.9.0
humanize>=4.0.0
```

## 🚀 Usage

1. **Start the bot**
   ```bash
   python code.py
   ```

2. **Invite the bot to your Discord server**
   - Go to the Discord Developer Portal
   - Select your application
   - Navigate to OAuth2 → URL Generator
   - Select scopes: `bot`
   - Select permissions: `Send Messages`, `Embed Links`, `Read Message History`
   - Use the generated URL to invite the bot

3. **Available Commands**

   | Command | Description |
   |---------|-------------|
   | `!help` | Display all available commands |
   | `!setchannel` | Change the logging channel using a dropdown menu |
   | `!setinterval` | Change the logging interval (30s, 60s, 120s, 300s, 600s) |
   | `!getchannel` | Show the current logging channel |
   | `!run <command>` | Execute a shell command (⚠️ use with caution!) |

## ⚙️ Configuration

### Default Settings

- **Logging Interval**: 60 seconds
- **Channel ID**: Must be set in the code or via `!setchannel` command

### Bot Permissions Required

- Send Messages
- Embed Links
- Read Message History
- Use Slash Commands (optional)

## 🛡️ Security Considerations

⚠️ **WARNING**: The `!run` command allows execution of shell commands. This is a security risk if not properly restricted.

**Recommendations**:
- Only run this bot on private servers with trusted members
- Consider removing the `!run` command for production use
- Implement role-based permissions for sensitive commands
- Never share your bot token publicly

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guidelines for Python code
- Add comments for complex logic
- Update documentation for new features
- Test your changes thoroughly before submitting

## 📝 TODO / Future Enhancements

- [ ] Add slash commands support
- [ ] Implement role-based permission system
- [ ] Add network usage monitoring
- [ ] Create a web dashboard interface
- [ ] Add temperature alerts/warnings
- [ ] Support for multiple Raspberry Pi monitoring
- [ ] Docker containerization
- [ ] Database logging for historical data
- [ ] Graphs and charts for system metrics

## 🐛 Known Issues

- CPU temperature reading only works on Raspberry Pi (requires `vcgencmd`)
- Command timeout is fixed at 10 seconds for shell commands
- Maximum 25 channels displayed in dropdown (Discord limitation)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper
- [psutil](https://github.com/giampaolo/psutil) - System and process utilities
- [humanize](https://github.com/python-humanize/humanize) - Human-readable data formatting

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Note**: Remember to never commit your bot token to version control. Use environment variables or a separate configuration file that's added to `.gitignore`.
