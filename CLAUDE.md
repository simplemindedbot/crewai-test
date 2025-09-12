# Python Project with UV and PyEnv

This is a Python project using modern tooling:

## Development Environment
- **Python Version Management**: PyEnv
- **Package Management**: UV (ultra-fast)  
- **Project Structure**: src-layout with pyproject.toml
- **Testing**: pytest
- **Code Formatting**: black, ruff
- **Virtual Environments**: Automatic with UV
- **Memory System**: in-memoria MCP server for coding conventions
- **IDE Integration**: MCP tools for VS Code diagnostics and Jupyter code execution

## Custom Commands Available
- `new-python-project <name>` - Create new Python project
- `add-dep <package>` - Add production dependency
- `add-dep <package> --dev` - Add development dependency
- `remove-dep <package>` - Remove dependency
- `update-deps` - Update all dependencies
- `uv-run <command>` - Run command in virtual environment

## Code Style Preferences
- Line length: 88 characters
- Use type hints where appropriate
- Follow PEP 8 guidelines
- Write comprehensive tests
- Use descriptive function and variable names

## Project Structure
```
src/           # Source code
tests/         # Test files  
pyproject.toml # Project configuration
uv.lock        # Dependency lockfile
```

## When Helping
- Suggest using the custom UV-based commands
- Respect the existing project structure
- Generate tests alongside code changes
- Use modern Python features and best practices
