# Claude Code Migration Guide

This guide explains how to migrate from the standard Anthropic API to Claude Code for your Replay system.

## Overview

Claude Code provides enhanced capabilities including:
- Custom base URL configuration for enterprise deployments
- Advanced authentication mechanisms
- Integration with local Claude Code settings
- Better debugging and monitoring capabilities

## Migration Summary

The migration has been implemented with **backward compatibility** - your existing setup using `ANTHROPIC_API_KEY` will continue to work. The system now supports both:

1. **Claude Code** (preferred): Uses `ANTHROPIC_AUTH_TOKEN` + `ANTHROPIC_BASE_URL`
2. **Standard Anthropic API** (fallback): Uses `ANTHROPIC_API_KEY`

## Configuration Methods

### Method 1: Environment Variables (Recommended)

Set these environment variables for Claude Code:

```bash
export ANTHROPIC_AUTH_TOKEN="your-auth-token-here"
export ANTHROPIC_BASE_URL="your-claude-code-base-url-here"
```

### Method 2: Claude Code Settings File

Create or update `~/.claude/settings.json`:

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your-auth-token-here"
  }
}
```

Note: `ANTHROPIC_BASE_URL` should still be set as an environment variable.

### Method 3: Fallback to Standard API

If Claude Code is not configured, the system will automatically fall back to:

```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

## Configuration Priority

The system checks authentication in this order:

1. `ANTHROPIC_AUTH_TOKEN` environment variable (Claude Code)
2. `ANTHROPIC_AUTH_TOKEN` from `~/.claude/settings.json` (Claude Code)
3. `ANTHROPIC_API_KEY` environment variable (standard Anthropic API - fallback)
4. API key helper from `~/.claude/settings.json` (future enhancement)

For base URL configuration:

1. `ANTHROPIC_BASE_URL` environment variable
2. `ANTHROPIC_BASE_URL` from `~/.claude/settings.json`

## What Changed

### New Files

- `core/backend/claude_code_config.py` - Configuration loader for Claude Code
- `test_claude_code_migration.py` - Test script to verify migration
- `CLAUDE_CODE_MIGRATION.md` - This documentation file

### Modified Files

- `core/backend/replay.py` - Updated `_init_client()` method to support Claude Code

### Dependencies

- `claude_code_sdk` is already listed in `pyproject.toml`
- No additional dependencies needed

## Testing the Migration

Run the test script to verify your configuration:

```bash
python test_claude_code_migration.py
```

This will:
- Check your Claude Code configuration
- Show current environment variable status
- Test Replay initialization with mock client
- Provide setup guidance

## Example Setup for Your Environment

Based on your description of having Claude Code configured in `~/.claude/settings.json`, you likely need to:

1. **Check your current settings file:**
   ```bash
   cat ~/.claude/settings.json
   ```

2. **Extract the values and set environment variables:**
   ```bash
   # Replace with your actual values from ~/.claude/settings.json
   export ANTHROPIC_AUTH_TOKEN="your-token-from-settings"
   export ANTHROPIC_BASE_URL="your-base-url-from-settings"
   ```

3. **Test the configuration:**
   ```bash
   python test_claude_code_migration.py
   ```

## Production Deployment

### Option 1: Environment Variables

Add to your deployment configuration:

```bash
# Claude Code configuration
export ANTHROPIC_AUTH_TOKEN="${CLAUDE_CODE_AUTH_TOKEN}"
export ANTHROPIC_BASE_URL="${CLAUDE_CODE_BASE_URL}"
```

### Option 2: Settings File

Ensure `~/.claude/settings.json` is properly configured on the deployment target:

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "${CLAUDE_CODE_AUTH_TOKEN}"
  }
}
```

## Debugging

### Configuration Status

The system will log detailed configuration information when initializing:

```
=== Claude Code Configuration Status ===
Settings file loaded: True
Auth token available: True
Base URL configured: True
Claude Code configured: True
Settings keys: ['env', 'permissions']
Environment variables from settings: ['ANTHROPIC_AUTH_TOKEN']
==========================================
```

### Common Issues

1. **Missing ANTHROPIC_BASE_URL**: Ensure this is set as an environment variable
2. **Settings file not found**: Check that `~/.claude/settings.json` exists and is readable
3. **Permission issues**: Ensure the settings file has proper permissions (readable by the application)

## Benefits of Migration

1. **Enterprise Support**: Integration with corporate proxy and custom endpoints
2. **Enhanced Authentication**: Support for dynamic token generation via API key helpers
3. **Better Monitoring**: Integration with Claude Code's built-in observability
4. **Future-Proof**: Access to Claude Code's advanced features as they're released

## Rollback Plan

If you need to rollback:

1. Remove or unset Claude Code environment variables:
   ```bash
   unset ANTHROPIC_AUTH_TOKEN
   unset ANTHROPIC_BASE_URL
   ```

2. Ensure `ANTHROPIC_API_KEY` is set:
   ```bash
   export ANTHROPIC_API_KEY="your-standard-api-key"
   ```

The system will automatically fall back to the standard Anthropic API.

## Support

- Run `python test_claude_code_migration.py` for configuration diagnostics
- Check the logs for detailed configuration status during client initialization
- Refer to Claude Code documentation for advanced configuration options 