#!/usr/bin/env python3
"""
FastMCP server that provides a simple hello world functionality.
"""
import sys
import os
import logging
import atexit
import signal
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Configure logging - reduce to WARNING to avoid MCP protocol interference
logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "WARNING"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastMCP server instance
mcp = FastMCP("jons-mcp-hello-world")


@dataclass
class Config:
    """Configuration for Hello MCP server"""
    greeting_prefix: str = "Hello"
    default_name: str = "World"
    available_languages: Dict[str, str] = field(default_factory=lambda: {
        "en": "Hello",
        "es": "Hola",
        "fr": "Bonjour",
        "de": "Hallo",
        "it": "Ciao",
        "pt": "Olá",
        "ru": "Привет",
        "ja": "こんにちは",
        "zh": "你好"
    })


def load_config() -> Config:
    """Load configuration from config.json if it exists"""
    config_path = Path("hello-config.json")
    if config_path.exists():
        try:
            with open(config_path) as f:
                data = json.load(f)
            return Config(**data)
        except Exception as e:
            logger.warning(f"Failed to load config: {e}")
    return Config()


# Global config instance
config = load_config()


@mcp.tool()
def hello(
    name: Optional[str] = None,
    language: Optional[str] = None,
    uppercase: bool = False
) -> Dict[str, Any]:
    """Generate a hello world greeting.
    
    Args:
        name: The name to greet (defaults to "World")
        language: Language code for the greeting (e.g., 'en', 'es', 'fr')
        uppercase: Whether to return the greeting in uppercase
    
    Returns:
        A dictionary containing the greeting and metadata
    """
    # Use default name if not provided
    target_name = name or config.default_name
    
    # Determine greeting based on language
    if language and language in config.available_languages:
        greeting_word = config.available_languages[language]
    else:
        greeting_word = config.greeting_prefix
    
    # Build the greeting
    greeting = f"{greeting_word}, {target_name}!"
    
    # Apply uppercase if requested
    if uppercase:
        greeting = greeting.upper()
    
    return {
        "greeting": greeting,
        "language": language or "en",
        "name": target_name,
        "uppercase": uppercase
    }


@mcp.tool()
def list_languages() -> Dict[str, Any]:
    """List all available languages for greetings.
    
    Returns:
        A dictionary containing available languages and their greetings
    """
    return {
        "languages": config.available_languages,
        "count": len(config.available_languages)
    }


@mcp.tool()
def custom_greeting(
    template: str,
    name: Optional[str] = None,
    variables: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """Create a custom greeting using a template.
    
    Args:
        template: A template string with {name} and other {variables}
        name: The name to use in the template
        variables: Additional variables to substitute in the template
    
    Returns:
        A dictionary containing the formatted greeting
    """
    # Prepare substitution dictionary
    subs = {"name": name or config.default_name}
    if variables:
        subs.update(variables)
    
    try:
        # Format the template
        greeting = template.format(**subs)
        return {
            "greeting": greeting,
            "template": template,
            "substitutions": subs
        }
    except KeyError as e:
        return {
            "error": f"Missing variable in template: {e}",
            "template": template,
            "available_variables": list(subs.keys())
        }
    except Exception as e:
        return {
            "error": f"Template formatting error: {str(e)}",
            "template": template
        }


def cleanup():
    """Cleanup function to be called on exit."""
    logger.info("Hello MCP server shutting down gracefully")


# Register cleanup handler
atexit.register(cleanup)


def main():
    """Initialize and run the FastMCP server."""
    # Handle signals gracefully
    def signal_handler(sig, frame):
        cleanup()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Log startup
        logger.info("Starting Hello MCP server...")
        
        # Run the server
        mcp.run()
    except Exception as e:
        # Log any startup errors to stderr
        import traceback
        print(f"MCP server error: {e}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()