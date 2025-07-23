#!/usr/bin/python3
import sys
import os


def convert_markdown_to_html(input_file, output_file):
    with open(input_file, 'r') as md_file:
        lines = md_file.readlines()

    with open(output_file, 'w') as html_file:
        in_ul = False
        in_ol = False

        for line in lines:
            line = line.strip()

            if not line:
                if in_ul:
                    html_file.write("</ul>\n")
                    in_ul = False
                if in_ol:
                    html_file.write("</ol>\n")
                    in_ol = False
                continue

            if line.startswith('* '):
                if not in_ol:
                    if in_ul:
                        html_file.write("</ul>\n")
                        in_ul = False
                    html_file.write("<ol>\n")
                    in_ol = True
                item = line[2:].strip()
                html_file.write(f"<li>{item}</li>\n")
                continue

            if line.startswith('- '):
                if not in_ul:
                    if in_ol:
                        html_file.write("</ol>\n")
                        in_ol = False
                    html_file.write("<ul>\n")
                    in_ul = True
                item = line[2:].strip()
                html_file.write(f"<li>{item}</li>\n")
                continue

            if in_ul:
                html_file.write("</ul>\n")
                in_ul = False
            if in_ol:
                html_file.write("</ol>\n")
                in_ol = False

            if line.startswith('#'):
                level = 0
                while level < len(line) and line[level] == '#':
                    level += 1
                if 1 <= level <= 6 and line[level] == ' ':
                    content = line[level + 1:].strip()
                    html_file.write(f"<h{level}>{content}</h{level}>\n")

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
