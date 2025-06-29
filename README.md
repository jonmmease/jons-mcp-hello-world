# Jons MCP Hello World

A simple hello world MCP (Model Context Protocol) server built with FastMCP. This server demonstrates the basic structure and patterns for building MCP servers.

## Overview

The Jons MCP Hello World server provides tools for generating greetings in multiple languages with customizable templates. It's designed as a learning example for understanding MCP server development.

## Features

- **Multi-language greetings**: Generate hello messages in 9 different languages
- **Customizable names**: Greet anyone by name
- **Template support**: Create custom greetings with template strings
- **Configuration support**: Customize defaults via JSON configuration

## Installation

### Using uv (recommended)

```bash
# Clone the repository
git clone https://github.com/jonmmease/jons-mcp-hello-world
cd jons-mcp-hello-world

# Install with uv
uv pip install -e .

# Run the server
uv run jons-mcp-hello-world
```

### Using uvx (direct execution)

```bash
# Run directly from GitHub
uvx --from git+https://github.com/jonmmease/jons-mcp-hello-world jons-mcp-hello-world
```

### With Claude Code

Add to your Claude Code configuration:

```json
{
  "mcpServers": {
    "jons-mcp-hello-world": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/jonmmease/jons-mcp-hello-world",
        "jons-mcp-hello-world"
      ]
    }
  }
}
```

## Configuration

Create a `hello-config.json` file in your working directory:

```json
{
  "greeting_prefix": "Hello",
  "default_name": "World",
  "available_languages": {
    "en": "Hello",
    "es": "Hola",
    "fr": "Bonjour",
    "de": "Hallo",
    "it": "Ciao",
    "pt": "Olá",
    "ru": "Привет",
    "ja": "こんにちは",
    "zh": "你好"
  }
}
```

## Tools

### hello

Generate a greeting message.

**Parameters:**
- `name` (optional): The name to greet (defaults to "World")
- `language` (optional): Language code (e.g., 'en', 'es', 'fr')
- `uppercase` (optional): Return greeting in uppercase

**Example:**
```json
{
  "name": "Alice",
  "language": "es",
  "uppercase": false
}
```

**Response:**
```json
{
  "greeting": "Hola, Alice!",
  "language": "es",
  "name": "Alice",
  "uppercase": false
}
```

### list_languages

List all available languages for greetings.

**Example Response:**
```json
{
  "languages": {
    "en": "Hello",
    "es": "Hola",
    "fr": "Bonjour",
    ...
  },
  "count": 9
}
```

### custom_greeting

Create a custom greeting using a template.

**Parameters:**
- `template`: Template string with {name} and other {variables}
- `name` (optional): Name to use in template
- `variables` (optional): Additional template variables

**Example:**
```json
{
  "template": "Welcome {name} to {place}!",
  "name": "Bob",
  "variables": {
    "place": "MCP Server"
  }
}
```

**Response:**
```json
{
  "greeting": "Welcome Bob to MCP Server!",
  "template": "Welcome {name} to {place}!",
  "substitutions": {
    "name": "Bob",
    "place": "MCP Server"
  }
}
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/jonmmease/jons-mcp-hello-world
cd jons-mcp-hello-world

# Create virtual environment with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
uv pip install -e ".[dev,test]"
```

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black src tests

# Lint code
ruff check src tests
```

## Architecture

The server follows the FastMCP pattern:

1. **Configuration**: Loaded from `hello-config.json` with sensible defaults
2. **Tools**: Three tools demonstrating different patterns:
   - `hello`: Basic tool with optional parameters
   - `list_languages`: Simple query tool
   - `custom_greeting`: Advanced tool with error handling
3. **Logging**: Minimal logging to avoid MCP protocol interference
4. **Error Handling**: Graceful shutdown and error reporting

## Troubleshooting

### Server won't start
- Ensure you have Python 3.10+ installed
- Check that all dependencies are installed: `uv pip install -e .`
- Look for error messages in stderr output

### Configuration not loading
- Verify `hello-config.json` is in the working directory
- Check JSON syntax is valid
- Review server logs for configuration errors

## License

MIT License - see LICENSE file for details.