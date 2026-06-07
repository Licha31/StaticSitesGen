import re
import os
from block_functions import markdown_to_html_code

def extract_title(markdown):
    if not markdown:
        raise Exception("markdown is None")
    else:
        title = re.search(r'^# (.*)\n?', markdown, re.MULTILINE)
        if title:
            return title.group(1)
        else:
            raise Exception("H1 not present")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        markdown = f.read()
        page_title = extract_title(markdown)
        html_node = markdown_to_html_code(markdown).to_html()
        with open(template_path, 'r') as template:
            template_content = template.read()
            full_html = template_content.replace("{{ Content }}", html_node).replace("{{ Title }}", page_title)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, 'w') as dest:
                dest.write(full_html)
