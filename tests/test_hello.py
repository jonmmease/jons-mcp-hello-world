"""Tests for the jons-mcp-hello-world server."""
import pytest
from src.jons_mcp_hello_world import (
    hello, 
    list_languages,
    AVAILABLE_LANGUAGES,
    DEFAULT_NAME,
    GREETING_PREFIX
)


def test_hello_default():
    """Test hello function with default parameters."""
    result = hello()
    assert result["greeting"] == "Hello, World!"
    assert result["language"] == "en"
    assert result["name"] == "World"
    assert result["uppercase"] is False


def test_hello_with_name():
    """Test hello function with custom name."""
    result = hello(name="Alice")
    assert result["greeting"] == "Hello, Alice!"
    assert result["name"] == "Alice"


def test_hello_with_language():
    """Test hello function with different languages."""
    result = hello(name="Bob", language="es")
    assert result["greeting"] == "Hola, Bob!"
    assert result["language"] == "es"
    
    result = hello(name="Charlie", language="fr")
    assert result["greeting"] == "Bonjour, Charlie!"
    assert result["language"] == "fr"


def test_hello_uppercase():
    """Test hello function with uppercase option."""
    result = hello(name="David", uppercase=True)
    assert result["greeting"] == "HELLO, DAVID!"
    assert result["uppercase"] is True


def test_hello_invalid_language():
    """Test hello function with invalid language falls back to English."""
    result = hello(name="Eve", language="invalid")
    assert result["greeting"] == "Hello, Eve!"
    assert result["language"] == "invalid"


def test_list_languages():
    """Test list_languages function returns expected languages."""
    result = list_languages()
    assert "languages" in result
    assert "count" in result
    assert result["count"] == len(AVAILABLE_LANGUAGES)
    assert result["languages"] == AVAILABLE_LANGUAGES
    assert "en" in result["languages"]
    assert "es" in result["languages"]
    assert "fr" in result["languages"]


def test_constants():
    """Test that constants are properly defined."""
    assert DEFAULT_NAME == "World"
    assert GREETING_PREFIX == "Hello"
    assert isinstance(AVAILABLE_LANGUAGES, dict)
    assert len(AVAILABLE_LANGUAGES) == 9


def test_all_languages():
    """Test greeting in all available languages."""
    for lang_code, greeting_word in AVAILABLE_LANGUAGES.items():
        result = hello(name="Test", language=lang_code)
        expected = f"{greeting_word}, Test!"
        assert result["greeting"] == expected
        assert result["language"] == lang_code