# Contributing to Raspberry Pi Discord Monitor Bot

First off, thank you for considering contributing to this project! 🎉

## Code of Conduct

Please be respectful and constructive in all interactions. We're all here to learn and improve the project together.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** to demonstrate the steps
- **Describe the behavior you observed** and what you expected to see
- **Include screenshots** if relevant
- **Specify your environment**: OS, Python version, discord.py version

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful**
- **List any potential drawbacks or considerations**

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the coding standards below
3. **Test your changes thoroughly**
4. **Update documentation** if you're adding or changing functionality
5. **Write clear commit messages**
6. **Submit a pull request** with a comprehensive description

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use 4 spaces for indentation (no tabs)
- Maximum line length of 100 characters
- Use descriptive variable and function names

### Code Quality

- **Add comments** for complex logic
- **Write docstrings** for functions and classes
- **Handle exceptions** appropriately
- **Avoid hardcoding** values; use configuration where possible

### Example Code Style

```python
def get_system_stats() -> dict:
    """
    Retrieve current system statistics.
    
    Returns:
        dict: Dictionary containing CPU temp, usage, RAM, and disk stats
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        print(f"Error getting system stats: {e}")
        return {}
```

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/your-username/rasberry-pie-monitor.git
   cd rasberry-pie-monitor
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a test bot and configuration:
   - Set up a test Discord server
   - Create a test bot token
   - Update configuration for testing

## Testing

- Test all commands manually before submitting
- Ensure the bot starts without errors
- Verify new features work as expected
- Test edge cases and error handling

## Commit Message Guidelines

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests when relevant

### Example Commit Messages

```
Add temperature alert feature

- Implement threshold checking
- Add notification embeds
- Update documentation
```

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

Thank you for contributing! 🚀
