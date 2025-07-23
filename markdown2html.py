#!/usr/bin/python3
"""
markdown2html.py - Simple markdown to HTML converter
"""

import sys
import os


def convert_markdown_to_html(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    with open(output_file, 'w') as f:
        in_ul = False

        for line in lines:
            line = line.rstrip()

            # skip empty lines
            if not line:
                if in_ul:
                    f.write("</ul>\n")
                    in_ul = False
                continue

            # handle headers
            if line.startswith('#'):
                level = 0
                while level < len(line) and line[level] == '#':
                    level += 1
                if 1 <= level <= 6 and line[level] == ' ':
                    content = line[level + 1:].strip()
                    f.write(f"<h{level}>{content}</h{level}>\n")
                continue

            # handle unordered list
            if line.startswith("* "):
                if not in_ul:
                    f.write("<ul>\n")
                    in_ul = True
                f.write(f"<li>{line[2:].strip()}</li>\n")
                continue
            else:
                if in_ul:
                    f.write("</ul>\n")
                    in_ul = False

        if in_ul:
            f.write("</ul>\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)

    try:
        convert_markdown_to_html(input_file, output_file)
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)
