#!/usr/bin/python3
"""
Markdown to HTML converter
Converts basic Markdown elements to HTML format
"""

import sys
import os
from typing import List, TextIO

if __name__ == "__main__":
    class MarkdownConverter:
        def __init__(self):
            self.in_ul = False
            self.in_ol = False
            self.in_paragraph = False
            self.paragraph_lines = []

        def reset_state(self):
            """Reset converter state"""
            self.in_ul = False
            self.in_ol = False
            self.in_paragraph = False
            self.paragraph_lines = []

        def close_lists(self, html_file: TextIO):
            """Close any open list tags"""
            if self.in_ul:
                html_file.write("</ul>\n")
                self.in_ul = False
            if self.in_ol:
                html_file.write("</ol>\n")
                self.in_ol = False

        def close_paragraph(self, html_file: TextIO):
            """Close current paragraph if open"""
            if self.in_paragraph and self.paragraph_lines:
                html_file.write("<p>\n")
                if len(self.paragraph_lines) >= 1:
                    html_file.write(f"    {self.paragraph_lines[0]}\n")
                if len(self.paragraph_lines) >= 2:
                    html_file.write("    <br/>\n")
                    html_file.write(f"    {self.paragraph_lines[1]}\n")
                if len(self.paragraph_lines) >= 3:
                    html_file.write(f"    {self.paragraph_lines[2]}\n")
                html_file.write("</p>\n")
                self.in_paragraph = False
                self.paragraph_lines = []

        def process_heading(self, line: str) -> str:
            """Process heading lines (# ## ### etc.)"""
            if not line.startswith('#'):
                return None
            count = 0
            while count < len(line) and line[count] == '#':
                count += 1
            if 1 <= count <= 6 and count < len(line) and line[count] == ' ':
                content = line[count + 1:].strip()
                return f"<h{count}>{content}</h{count}>\n"
            return None

        def process_unordered_list(self, line: str, html_file: TextIO) -> bool:
            """Process unordered list items (- item)"""
            if not line.startswith("- "):
                return False
            if not self.in_ul:
                self.close_lists(html_file)
                html_file.write("<ul>\n")
                self.in_ul = True
            content = line[2:].strip()
            html_file.write(f"    <li>{content}</li>\n")
            return True

        def process_ordered_list(self, line: str, html_file: TextIO) -> bool:
            """Process ordered list items (* item)"""
            if not line.startswith("* "):
                return False
            if not self.in_ol:
                self.close_lists(html_file)
                html_file.write("<ol>\n")
                self.in_ol = True
            content = line[2:].strip()
            html_file.write(f"<li>{content}</li>\n")
            return True

        def process_line(self, line: str, html_file: TextIO):
            """Process a single line of markdown"""
            line = line.rstrip()
            if not line:
                self.close_paragraph(html_file)
                self.close_lists(html_file)
                return
            heading_html = self.process_heading(line)
            if heading_html:
                self.close_paragraph(html_file)
                self.close_lists(html_file)
                html_file.write(heading_html)
                return
            if self.process_unordered_list(line, html_file):
                self.close_paragraph(html_file)
                return
            if self.process_ordered_list(line, html_file):
                self.close_paragraph(html_file)
                return
            self.close_lists(html_file)
            if not self.in_paragraph:
                self.in_paragraph = True
            self.paragraph_lines.append(line)

        def convert_file(self, input_path: str, output_path: str):
            """Convert markdown file to HTML"""
            try:
                with open(input_path, 'r', encoding='utf-8') as md_file:
                    lines = md_file.readlines()
                with open(output_path, 'w', encoding='utf-8') as html_file:
                    self.reset_state()
                    for line in lines:
                        self.process_line(line, html_file)
                    self.close_paragraph(html_file)
                    self.close_lists(html_file)
            except FileNotFoundError:
                raise FileNotFoundError(f"Input file '{input_path}' not found")
            except PermissionError:
                raise PermissionError(f"Permission denied accessing files")
            except Exception as e:
                raise Exception(f"Error during conversion: {str(e)}")

def main():
    """Main function"""
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
        print(f"Successfully converted {input_file} to {output_file}")        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
