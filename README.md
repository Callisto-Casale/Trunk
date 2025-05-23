# Trunk

Trunk is a modern, clean, and developer-friendly CLI tool to visualize your directory structure — like `tree`, but more Pythonic.

## Features

- Show folders and optionally files
- Limit depth of recursion with `--depth`
- Show file sizes with `--size`
- Automatically respects `.gitignore`
- Copy output to clipboard with `--copy`
- Save output to a file with `--output`
- Override `.gitignore` with `--break .gitignore`

## Installation

```bash
git clone https://github.com/Callisto-Casale/trunk.git
cd trunk
pip install .
```

Dependencies:

```bash
pip install pathspec pyperclip humanize
```

## Usage

```bash
trunk PATH [options]
```

### Examples

```bash
trunk .                          # Show only folders
trunk . --full                   # Show folders and files
trunk . --full --size            # Show file sizes
trunk . --depth 2                # Limit to 2 levels deep
trunk . --copy                   # Copy tree to clipboard
trunk . --output tree.txt        # Save output to a file
trunk . --break .gitignore       # Show everything, even ignored
```

## Output Example

```
my_project
├── trunk
│   ├── __init__.py (0 B)
│   └── cli.py (4.2 kB)
├── setup.py
└── README.md
```

## Notes

- Trunk respects `.gitignore` by default. To override this, you must explicitly run:

```bash
trunk . --break .gitignore
```

This prevents accidentally exposing ignored or sensitive files.
