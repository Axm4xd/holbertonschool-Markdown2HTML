#!/usr/bin/python3
"""
Markdown to HTML converter with paragraphs, bold/emphasis, md5 and c-removal
"""

import sys
import os
import hashlib
import re
from typing import TextIO

class MarkdownConverter:
    def __init__(self):
        self.in_ul = False
        self.in_ol = False
        self.paragraph_lines = []

    def reset_state(self):
        self.in_ul = False
        self.in_ol = False
        self.paragraph_lines = []

    def close_lists(self, html_file: TextIO):
        if self.in_ul:
            html_file.write("</ul>\n")
            self.in_ul = False
        if self.in_ol:
            html_file.write("</ol>\n")
            self.in_ol = False

    def process_heading(self, line: str) -> str:
        if not line.startswith('#'):
            return None
        count = 0
        while count < len(line) and line[count] == '#':
            count += 1
        if 1 <= count <= 6 and count < len(line) and line[count] == ' ':
            content = line[count+1:].strip()
            return f"<h{count}>{self.apply_inline_formatting(content)}</h{count}>\n"
        return None

    def process_unordered_list(self, line: str, html_file: TextIO) -> bool:
        if not line.startswith("- "):
            return False
        if not self.in_ul:
            self.close_lists(html_file)
            html_file.write("<ul>\n")
            self.in_ul = True
        content = line[2:].strip()
        html_file.write(f"<li>{self.apply_inline_formatting(content)}</li>\n")
        return True

    def process_ordered_list(self, line: str, html_file: TextIO) -> bool:
        if not line.startswith("* "):
            return False
        if not self.in_ol:
            self.close_lists(html_file)
            html_file.write("<ol>\n")
            self.in_ol = True
        content = line[2:].strip()
        html_file.write(f"<li>{self.apply_inline_formatting(content)}</li>\n")
        return True

    def apply_inline_formatting(self, text: str) -> str:
        # bold
        text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
        # emphasis
        text = re.sub(r"__(.+?)__", r"<em>\1</em>", text)
        # [[text]] → md5
        def md5_replace(match):
            hashed = hashlib.md5(match.group(1).encode()).hexdigest()
            return hashed
        text = re.sub(r"\[\[(.+?)\]\]", md5_replace, text)

        # ((text)) → remove 'c' and 'C'
        def remove_c(match):
            return re.sub(r"[cC]", "", match.group(1))
        text = re.sub(r"\(\((.+?)\)\)", remove_c, text)
        return text

    def flush_paragraph(self, html_file: TextIO):
        if not self.paragraph_lines:
            return
        html_file.write("<p>\n")
        for i, line in enumerate(self.paragraph_lines):
            html_file.write(f"{'    ' if i == 0 else '    <br/>\n    '}{self.apply_inline_formatting(line)}\n")
        html_file.write("</p>\n")
        self.paragraph_lines = []

    def process_line(self, line: str, html_file: TextIO):
        line = line.rstrip()
        if not line:
            self.flush_paragraph(html_file)
            self.close_lists(html_file)
            return
        heading = self.process_heading(line)
        if heading:
            self.flush_paragraph(html_file)
            self.close_lists(html_file)
            html_file.write(heading)
            return
        if self.process_unordered_list(line, html_file):
            self.flush_paragraph(html_file)
            return
        if self.process_ordered_list(line, html_file):
            self.flush_paragraph(html_file)
            return
        self.close_lists(html_file)
        self.paragraph_lines.append(line)

    def convert_file(self, input_path: str, output_path: str):
        try:
            with open(input_path, 'r', encoding='utf-8') as md_file:
                lines = md_file.readlines()
            with open(output_path, 'w', encoding='utf-8') as html_file:
                self.reset_state()
                for line in lines:
                    self.process_line(line, html_file)
                self.flush_paragraph(html_file)
                self.close_lists(html_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file '{input_path}' not found")
        except PermissionError:
            raise PermissionError("Permission denied accessing files")
        except Exception as e:
            raise Exception(f"Error during conversion: {str(e)}")

def main():
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py <input.md> <output.html>", file=sys.stderr)
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)
    try:
        converter = MarkdownConverter()
        converter.convert_file(input_file, output_file)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
