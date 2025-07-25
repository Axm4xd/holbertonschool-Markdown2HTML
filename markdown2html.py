#!/usr/bin/python3
"""
Markdown to HTML converter with advanced features.

- Argument checking and file existence
- Headings (# to ######)
- Unordered lists (-)
- Ordered lists (*)
- Paragraphs with <p>, including <br/> for line breaks
- Bold (**text**) and emphasis (__text__)
- Special syntax:
  - [[text]] → MD5 hash (lowercase)
  - ((text)) → remove all 'c' or 'C' from text
"""

import sys
import os
import hashlib
import re


def md5_hash(text):
    """Return lowercase MD5 hash of the input text."""
    return hashlib.md5(text.encode()).hexdigest()


def remove_c(text):
    """Remove all 'c' or 'C' characters from the input text."""
    return re.sub(r"[cC]", "", text)


def replace_bold_emphasis(text):
    """
    Replace **bold** with <b>bold</b>
    Replace __emphasis__ with <em>emphasis</em>
    """
    # Bold first
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    # Emphasis next
    text = re.sub(r"__(.+?)__", r"<em>\1</em>", text)
    return text


def replace_special(text):
    """
    Replace [[text]] with MD5 hash,
    Replace ((text)) by removing 'c' or 'C' characters.
    """

    def md5_repl(match):
        content = match.group(1)
        return md5_hash(content)

    def remove_c_repl(match):
        content = match.group(1)
        return remove_c(content)

    text = re.sub(r"\[\[(.+?)\]\]", md5_repl, text)
    text = re.sub(r"\(\((.+?)\)\)", remove_c_repl, text)
    return text


def process_line(line):
    """
    Process a line of text for bold, emphasis, and special replacements.
    """
    line = replace_bold_emphasis(line)
    line = replace_special(line)
    return line


def main():
    """Main function to convert markdown file to HTML."""
    if len(sys.argv) < 3:
        print(
            "Usage: ./markdown2html.py README.md README.html",
            file=sys.stderr,
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_file, "r") as infile, \
               open(output_file, "w") as outfile:

            in_ul = False  # inside unordered list
            in_ol = False  # inside ordered list
            paragraph_lines = []  # accumulate paragraph lines

            def close_paragraph():
                """Write and clear any accumulated paragraph lines."""
                if paragraph_lines:
                    if len(paragraph_lines) == 1:
                        content = process_line(paragraph_lines[0])
                        outfile.write("<p>\n" + content + "\n</p>\n")
                    else:
                        processed_lines = [
                            process_line(line) for line in paragraph_lines
                        ]
                        joined = "<br/>\n".join(processed_lines)
                        outfile.write("<p>\n" + joined + "\n</p>\n")
                    paragraph_lines.clear()

            def close_ul():
                """Close unordered list if open."""
                nonlocal in_ul
                if in_ul:
                    outfile.write("</ul>\n")
                    in_ul = False

            def close_ol():
                """Close ordered list if open."""
                nonlocal in_ol
                if in_ol:
                    outfile.write("</ol>\n")
                    in_ol = False

            for raw_line in infile:
                line = raw_line.rstrip("\n")
                stripped = line.strip()

                if stripped == "":
                    close_paragraph()
                    close_ul()
                    close_ol()
                    continue

                # Headings
                if stripped.startswith("#"):
                    close_paragraph()
                    close_ul()
                    close_ol()

                    count = 0
                    for char in stripped:
                        if char == "#":
                            count += 1
                        else:
                            break

                    if count <= 6 and \
                        len(stripped) > count and \
                            stripped[count] == " ":
                        content = stripped[count + 1:]
                        content = process_line(content)
                        outfile.write(f"<h{count}>{content}</h{count}>\n")
                    continue

                # Unordered list
                if stripped.startswith("- "):
                    close_paragraph()
                    close_ol()
                    if not in_ul:
                        outfile.write("<ul>\n")
                        in_ul = True

                    content = stripped[2:]
                    content = process_line(content)
                    outfile.write(f"<li>{content}</li>\n")
                    continue

                # Ordered list
                if stripped.startswith("* "):
                    close_paragraph()
                    close_ul()
                    if not in_ol:
                        outfile.write("<ol>\n")
                        in_ol = True

                    content = stripped[2:]
                    content = process_line(content)
                    outfile.write(f"<li>{content}</li>\n")
                    continue

                # Paragraph lines
                close_ul()
                close_ol()
                paragraph_lines.append(line)

            # Close any open blocks at the end
            close_paragraph()
            close_ul()
            close_ol()

        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
