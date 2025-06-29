#!/usr/bin/env python3
"""
FastMCP server that provides a simple hello world functionality.
"""
import sys
import os
import logging
import atexit
import signal
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

# Configure logging - reduce to WARNING to avoid MCP protocol interference
logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "WARNING"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastMCP server instance
mcp = FastMCP("jons-mcp-hello-world")


# Default configuration values
DEFAULT_NAME = "World"
GREETING_PREFIX = "Hello"
AVAILABLE_LANGUAGES = {
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
    target_name = name or DEFAULT_NAME
    
    # Determine greeting based on language
    if language and language in AVAILABLE_LANGUAGES:
        greeting_word = AVAILABLE_LANGUAGES[language]
    else:
        greeting_word = GREETING_PREFIX
    
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
        "languages": AVAILABLE_LANGUAGES,
        "count": len(AVAILABLE_LANGUAGES)
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