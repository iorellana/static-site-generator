import os
from os.path import exists, join, isfile
from shutil import copy, rmtree
from converter import extract_title, markdown_to_html_node

def main():
    # copy everything from static to public
    static_dir = "static"
    public_dir = "public"
    if exists(public_dir):
        rmtree(public_dir)
    os.mkdir(public_dir)
    copy_recursive(static_dir, public_dir)
    # generate index.html
    generate_pages_recursive("content", "template.html", "public")

def copy_recursive(src, dst):
    if isfile(src):
        copy(src, dst)
    else:
        if not exists(dst):
            os.mkdir(dst)
        for l in os.listdir(src):
            copy_recursive(join(src, l), join(dst, l))

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, encoding="utf-8") as f:
        markdown_from_path = f.read()
    with open(template_path, encoding="utf-8") as f:
        template_html = f.read()
    title = extract_title(markdown_from_path)
    template_html = template_html.replace("{{ Title }}", title)
    template_html = template_html.replace("{{ Content }}", markdown_to_html_node(markdown_from_path).to_html())
    # Create folder in the dest_path if it doesn't exist
    if not exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template_html)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for l in os.listdir(dir_path_content):
        if isfile(join(dir_path_content, l)) and l.endswith(".md"):
            generate_page(join(dir_path_content, l), template_path, join(dest_dir_path, l.replace(".md", ".html")))
        else:
            generate_pages_recursive(join(dir_path_content, l), template_path, join(dest_dir_path, l))

if __name__ == "__main__":
    main()