#!/usr/bin/python3
"""
markdown2html.py - Converts Markdown to HTML
"""

import sys
import os


def convert_md_to_html(input_path, output_path):
    in_ul = False
    with open(input_path, 'r') as input_file, open(output_path, 'w') as output_file:
        for line in input_file:
            line = line.rstrip()

            if not line:
                if in_ul:
                    output_file.write("</ul>\n")
                    in_ul = False
                continue

            # Headers
            if line.startswith("#"):
                count = 0
                while count < len(line) and line[count] == "#":
                    count += 1
                if count <= 6 and line[count] == ' ':
                    content = line[count+1:].strip()
                    output_file.write(f"<h{count}>{content}</h{count}>\n")
                    continue

            # List items
            if line.startswith("* "):
                if not in_ul:
                    output_file.write("<ul>\n")
                    in_ul = True
                content = line[2:].strip()
                output_file.write(f"<li>{content}</li>\n")
                continue
            else:
                if in_ul:
                    output_file.write("</ul>\n")
                    in_ul = False

        if in_ul:
            output_file.write("</ul>\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: ./markdown2html.py <input_file> <output_file>\n")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)

    try:
        convert_md_to_html(input_file, output_file)
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)
