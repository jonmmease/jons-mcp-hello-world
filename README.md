# Jons MCP Hello World

A simple hello world MCP (Model Context Protocol) server built with FastMCP. This server demonstrates the basic structure and patterns for building MCP servers.

## Overview

The Jons MCP Hello World server provides tools for generating greetings in multiple languages with customizable templates. It's designed as a learning example for understanding MCP server development.

## Features

- **Multi-language greetings**: Generate hello messages in 9 different languages
- **Customizable names**: Greet anyone by name

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

### Adding to Claude Code as MCP Server

To use this with Claude Code, add it using the CLI:

```bash
claude mcp add jons-mcp-hello-world uvx -- --from git+https://github.com/jonmmease/jons-mcp-hello-world jons-mcp-hello-world
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

Using uv to run tests with the virtual environment:

```bash
# Run all tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run a specific test file
uv run pytest tests/test_hello.py

# Run tests with coverage
uv run pytest --cov=src
```

The test suite includes examples of:
- Importing functions and constants from the module
- Testing the `hello` function with various parameters
- Testing the `list_languages` function
- Verifying all language translations work correctly

### Code Quality

```bash
# Format code
black src tests

# Lint code
ruff check src tests
```

## Architecture

The server follows the FastMCP pattern:

1. **Tools**: Two tools demonstrating different patterns:
   - `hello`: Basic tool with optional parameters
   - `list_languages`: Simple query tool
2. **Logging**: Minimal logging to avoid MCP protocol interference
3. **Error Handling**: Graceful shutdown and error reporting

## Troubleshooting

### Server won't start
- Ensure you have Python 3.10+ installed
- Check that all dependencies are installed: `uv pip install -e .`
- Look for error messages in stderr output

## License

MIT License - see LICENSE file for details.