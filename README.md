# leaderbird
For leaderboards and rankings.

## Overview
Helper library for leaderboards and rankings, such as ELO-based rankings between humans, AI's, and between humans and AI's.

## Rules
1. Don't let the code get sloppy.
2. It should "just work".
3. Don't procrastinate on refactoring; refactor as you go.

## Installation
We recommending always using a virtual environment such as venv or Conda.

First install leaderbird and check it's installed (the second command will either show information about the package or throw an error).
```bash
pip3 install leaderbird
python3 -c "import leaderbird; [print(f'{attr}: {getattr(leaderbird, attr)}') for attr in dir(leaderbird) if attr.startswith('__')]"
```
