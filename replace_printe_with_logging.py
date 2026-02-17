#!/usr/bin/env python3
"""
Script to replace printe.output(...) with logger.info(...)
Adds 'import logging' and 'logger = logging.getLogger(__name__)' if not exists.
Removes 'import printe' and 'from ... import printe' if not used anymore.
"""

import re
import sys
from pathlib import Path


def get_python_files():
    """Get all Python files in the project."""
    return list(Path(".").rglob("*.py"))


def has_printe_output(content):
    """Check if file contains printe.output( usage."""
    return "printe.output(" in content


def has_logging_setup(content):
    """Check if file already has logging setup."""
    return "logging.getLogger(__name__)" in content or "logging.getLogger(__name__)" in content


def has_import_logging(content):
    """Check if file already imports logging."""
    return re.search(r'^import logging\s*$', content, re.MULTILINE) is not None


def process_file(file_path):
    """Process a single Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

    content = original_content
    modified = False

    # Check if file uses printe.output(
    if not has_printe_output(content):
        return False

    # Replace printe.output(...) with logger.info(...)
    # Handle multi-line calls by using a regex that matches balanced parentheses
    def replace_printe_call(match):
        # Get the content inside printe.output(...)
        inner = match.group(1)
        return f"logger.info({inner})"

    # Pattern to match printe.output(...) with balanced parentheses
    # This regex handles nested parentheses
    pattern = r'printe\.output\((.*?)\)(?!\s*\()'

    # Use a more robust approach: find all printe.output( occurrences and replace
    new_content = []
    i = 0
    while i < len(content):
        idx = content.find('printe.output(', i)
        if idx == -1:
            new_content.append(content[i:])
            break

        new_content.append(content[i:idx])

        # Find matching closing parenthesis
        start = idx + len('printe.output(')
        depth = 1
        j = start
        while j < len(content) and depth > 0:
            if content[j] == '(':
                depth += 1
            elif content[j] == ')':
                depth -= 1
            j += 1

        if depth == 0:
            # Extract arguments
            args = content[start:j-1]
            new_content.append(f'logger.info({args})')
            modified = True
        else:
            # Malformed, keep as is
            new_content.append(content[idx:j])

        i = j

    content = ''.join(new_content)

    if not modified:
        return False

    # Add logging import if not present
    if not has_import_logging(content):
        # Find a good place to add import
        lines = content.split('\n')
        import_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                import_idx = i + 1
        lines.insert(import_idx, 'import logging')
        content = '\n'.join(lines)

    # Add logger = logging.getLogger(__name__) if not present
    if not has_logging_setup(content):
        lines = content.split('\n')
        # Find position after imports
        last_import_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                last_import_idx = i + 1
        lines.insert(last_import_idx, 'logger = logging.getLogger(__name__)')
        content = '\n'.join(lines)

    # Remove unused printe imports
    # Check if printe is still used in the file
    if 'printe.' not in content:
        # Remove 'import printe' lines
        content = re.sub(r'^import printe\s*$', '', content, flags=re.MULTILINE)
        # Remove 'from ... import printe' lines
        content = re.sub(r'^from\s+\S+\s+import\s+.*\bprinte\b.*$', '', content, flags=re.MULTILINE)
        # Remove 'from ... import ..., printe' - keep other imports
        content = re.sub(r'^from\s+(\S+)\s+import\s+(.*?),\s*printe\s*$', r'from \1 import \2', content, flags=re.MULTILINE)
        content = re.sub(r'^from\s+(\S+)\s+import\s+printe,\s*(.*?)$', r'from \1 import \2', content, flags=re.MULTILINE)

    # Clean up extra blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Modified: {file_path}")
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return False

    return False


def main():
    print("Starting replacement of printe.output with logger.info...")

    files = get_python_files()
    print(f"Found {len(files)} Python files")

    modified_count = 0
    for file_path in files:
        # Skip the script itself
        if file_path.name == 'replace_printe_with_logging.py':
            continue
        if process_file(file_path):
            modified_count += 1

    print(f"\nDone! Modified {modified_count} files.")


if __name__ == "__main__":
    main()
