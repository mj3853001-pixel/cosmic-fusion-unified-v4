#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UCA Cosmic Fusion v5.2 — README Section Injector
Inject any content into README.md at specific markers
Usage: python3 inject_readme.py --after "## Section Name" --file new_section.md
"""

import sys
import argparse
import re

def inject_section(readme_path, content_path, after_marker, before_marker=None):
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme = f.read()

    with open(content_path, 'r', encoding='utf-8') as f:
        new_content = f.read().strip()

    # Find marker
    lines = readme.split('\n')
    inject_idx = None
    for i, line in enumerate(lines):
        if after_marker in line:
            inject_idx = i + 1
            break

    if inject_idx is None:
        print("❌ Marker not found: " + after_marker)
        return False

    if before_marker:
        for i in range(inject_idx, len(lines)):
            if before_marker in lines[i]:
                inject_idx = i
                break

    lines.insert(inject_idx, "\n" + new_content + "\n")

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print("✅ Injected after: " + after_marker)
    return True

def main():
    parser = argparse.ArgumentParser(description='Inject content into README.md')
    parser.add_argument('--readme', '-r', default='README.md', help='README file path')
    parser.add_argument('--file', '-f', required=True, help='File containing content to inject')
    parser.add_argument('--after', '-a', required=True, help='Marker line to inject after')
    parser.add_argument('--before', '-b', help='Optional: marker to inject before')
    args = parser.parse_args()

    success = inject_section(args.readme, args.file, args.after, args.before)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
