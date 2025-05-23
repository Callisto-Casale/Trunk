import os
import argparse
import pyperclip
from pathlib import Path

try:
    from humanize import naturalsize
    use_humanize = True
except ImportError:
    use_humanize = False

try:
    import pathspec
except ImportError:
    print("❌ Missing required dependency: pathspec\nInstall it with: pip install pathspec")
    exit(1)


def load_gitignore(path):
    gitignore_path = os.path.join(path, ".gitignore")
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            return pathspec.PathSpec.from_lines("gitwildmatch", f.readlines())
    return None


def should_ignore(path, spec, root):
    if not spec:
        return False
    rel_path = os.path.relpath(path, root)
    return spec.match_file(rel_path)


def format_size(size):
    if use_humanize:
        return naturalsize(size)
    else:
        return f"{size} B"


def print_tree(path, show_files=False, show_size=False, depth=None, prefix="", output_func=print, root=None, spec=None, level=0):
    try:
        items = sorted(os.listdir(path))
    except PermissionError:
        output_func(prefix + "└── [Permission Denied]")
        return

    if depth is not None and level >= depth:
        return

    entries = []
    for item in items:
        full_path = os.path.join(path, item)
        if should_ignore(full_path, spec, root):
            continue
        if show_files or os.path.isdir(full_path):
            entries.append(item)

    for index, name in enumerate(entries):
        full_path = os.path.join(path, name)
        connector = "└── " if index == len(entries) - 1 else "├── "
        display_name = name
        if show_size and os.path.isfile(full_path):
            try:
                display_name += f" ({format_size(os.path.getsize(full_path))})"
            except:
                display_name += " (?)"
        output_func(prefix + connector + display_name)

        if os.path.isdir(full_path):
            extension = "    " if index == len(entries) - 1 else "│   "
            print_tree(full_path, show_files, show_size, depth,
                       prefix + extension, output_func, root, spec, level + 1)


def main():
    parser = argparse.ArgumentParser(
        description="📁 Trunk - Directory tree visualizer.")
    parser.add_argument("path", help="Path to directory")
    parser.add_argument("--full", "-f", action="store_true",
                        help="Show files as well as folders")
    parser.add_argument("--size", "-s", action="store_true",
                        help="Show file sizes")
    parser.add_argument("--depth", type=int, help="Limit recursion depth")
    parser.add_argument("--output", "-o", type=str,
                        help="Write output to a file")
    parser.add_argument("--copy", "-cp", action="store_true",
                        help="Copy output to clipboard")
    parser.add_argument("--break", dest="break_gitignore", nargs=1, metavar="WHAT",
                        help="Override .gitignore (must be exactly: .gitignore)")

    args = parser.parse_args()

    # ✅ Normalize relative path
    input_path = args.path.lstrip("/\\")
    path = os.path.abspath(os.path.join(os.getcwd(), input_path))

    if not os.path.exists(path):
        print(f"❌ Error: Path '{path}' does not exist.")
        return

    # ✅ Handle .gitignore
    use_gitignore = True
    if args.break_gitignore and args.break_gitignore[0] == ".gitignore":
        print("⚠️  Ignoring .gitignore as requested.")
        use_gitignore = False

    spec = load_gitignore(path) if use_gitignore else None

    output_lines = [path]
    print_tree(
        path,
        show_files=args.full,
        show_size=args.size,
        depth=args.depth,
        output_func=output_lines.append,
        root=path,
        spec=spec
    )

    output_text = "\n".join(output_lines)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output_text)
            print(f"✅ Tree written to {args.output}")
        except Exception as e:
            print(f"❌ Failed to write to {args.output}: {e}")

    if args.copy:
        try:
            pyperclip.copy(output_text)
            print("📋 Tree copied to clipboard!")
        except Exception as e:
            print(f"❌ Failed to copy to clipboard: {e}")

    if not args.output and not args.copy:
        print(output_text)


if __name__ == "__main__":
    main()
