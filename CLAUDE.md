# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Leaderbird is a Python library for leaderboards and rankings, including ELO-based rankings between humans, AIs, and human-AI interactions. This is an early-stage project with minimal code structure.

## Development Commands

### Package Installation
```bash
# Install in development mode with virtual environment
pip3 install -e .

# Verify installation
python3 -c "import leaderbird; [print(f'{attr}: {getattr(leaderbird, attr)}') for attr in dir(leaderbird) if attr.startswith('__')]"
```

### Building and Distribution
```bash
# Build the package
python3 -m build

# Install build dependencies if needed
pip3 install build
```

## Project Structure

- `leaderbird/` - Main Python package directory
- `leaderbird/__init__.py` - Package initialization (currently minimal)
- `pyproject.toml` - Modern Python packaging configuration
- `README.md` - Project documentation and installation instructions

## Architecture Notes

This is a minimal Python package using modern `pyproject.toml` configuration with setuptools backend. The project follows the standard Python package structure but is in very early development stage with limited functionality implemented.

## Development Guidelines

From the README, the project follows these principles:
1. Keep code clean and maintainable
2. Ensure functionality "just works"
3. Refactor continuously rather than letting technical debt accumulate

## Package Information

- Package name: `leaderbird`
- Version: `0.1.0`
- Author: Robert James Toth (robert.toth@thetatech.ai)