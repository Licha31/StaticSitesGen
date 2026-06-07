import os
import shutil
import sys

from page_gen import generate_page

def copy_src_to_public(src_dir, public_dir):
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
        os.mkdir(public_dir)
    else:
        os.mkdir(public_dir)
    if os.path.exists(src_dir):
        for file in os.listdir(src_dir):
            if os.path.isfile(os.path.join(src_dir, file)):
                shutil.copy(os.path.join(src_dir, file), public_dir)
                print(f"Copied {file} to {public_dir}")
            else:
                os.mkdir(os.path.join(public_dir, file))
                copy_src_to_public(os.path.join(src_dir, file), os.path.join(public_dir, file))

def generate_pages_recursively(content_dir, template_path, dest_dir, basepath):
    if os.path.exists(content_dir):
        for file in os.listdir(content_dir):
            if os.path.isfile(os.path.join(content_dir, file)):
                generate_page(os.path.join(content_dir, file), template_path, os.path.join(dest_dir, file.replace(".md", ".html")), basepath)
            else:
                os.mkdir(os.path.join(dest_dir, file))
                generate_pages_recursively(os.path.join(content_dir, file), template_path, os.path.join(dest_dir, file),basepath)


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(f"Basepath: {basepath}")
    copy_src_to_public("static", "docs")
    generate_pages_recursively("content", "template.html", "docs", basepath)
    

if __name__ == "__main__":
    main()
