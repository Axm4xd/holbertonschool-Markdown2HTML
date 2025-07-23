#!/usr/bin/python3
import sys
import os

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
        with open(input_file, 'r') as md_file:
            lines = md_file.readlines()

        with open(output_file, 'w') as html_file:
            in_list = False

            for line in lines:
                line = line.strip()

                if not line:
                    if in_list:
                        html_file.write("</ul>\n")
                        in_list = False
                    continue

                if line.startswith('- '):
                    if not in_list:
                        html_file.write("<ul>\n")
                        in_list = True
                    item = line[2:].strip()
                    html_file.write(f"<li>{item}</li>\n")
                    continue

                if in_list:
                    html_file.write("</ul>\n")
                    in_list = False

                if line.startswith('#'):
                    level = 0
                    while level < len(line) and line[level] == '#':
                        level += 1
                    if level > 0 and level <= 6 and line[level] == ' ':
                        content = line[level + 1:].strip()
                        html_file.write(f"<h{level}>{content}</h{level}>\n")

            if in_list:
                html_file.write("</ul>\n")

        sys.exit(0)

    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)
