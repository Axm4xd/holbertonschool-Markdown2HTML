#!/usr/bin/python3
"""
markdown2html.py - Convert Markdown to HTML

This script reads a Markdown file and outputs its HTML representation.
Supports headings and both unordered (-) and ordered (*) lists.

Usage:
    ./markdown2html.py input.md output.html
"""

import sys
import os


def convert_markdown_to_html(input_path, output_path):
    with open(input_path, 'r') as md_file:
        lines = md_file.readlines()

    with open(output_path, 'w') as html_file:
        in_ul = False
        in_ol = False

        for line in lines:
            line = line.rstrip()

            if not line:
                if in_ul:
                    html_file.write("</ul>\n")
                    in_ul = False
                if in_ol:
                    html_file.write("</ol>\n")
                    in_ol = False
                continue

            # Unordered list item (- )
            if line.startswith("- "):
                if not in_ul:
                    if in_ol:
                        html_file.write("</ol>\n")
                        in_ol = False
                    html_file.write("<ul>\n")
                    in_ul = True
                html_file.write(f"<li>{line[2:].strip()}</li>\n")
                continue

            # Ordered list item (* )
            if line.startswith("* "):
                if not in_ol:
                    if in_ul:
                        html_file.write("</ul>\n")
                        in_ul = False
                    html_file.write("<ol>\n")
                    in_ol = True
                html_file.write(f"<li>{line[2:].strip()}</li>\n")
                continue

            # If not list, close any open list
            if in_ul:
                html_file.write("</ul>\n")
                in_ul = False
            if in_ol:
                html_file.write("</ol>\n")
                in_ol = False

            # Headers (# up to ######)
            if line.startswith("#"):
                count = 0
                while count < len(line) and line[count] == "#":
                    count += 1
                if 1 <= count <= 6 and line[count] == ' ':
                    content = line[count + 1:].strip()
                    html_file.write(f"<h{count}>{content}</h{count}>\n")

        # Final cleanup (if list still open at end of file)
        if in_ul:
            html_file.write("</ul>\n")
        if in_ol:
            html_file.write("</ol>\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)

    try:
        convert_markdown_to_html(input_file, output_file)
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)
