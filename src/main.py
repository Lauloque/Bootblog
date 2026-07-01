import re
import shutil
import sys
from os import getcwd, listdir, makedirs, mkdir, path

from markdown_converters import markdown_to_html_node


def copy_files_in_dir(basePath: str, outputPath: str) -> None:
    # Cleanup outputPath
    if path.exists(outputPath):
        shutil.rmtree(outputPath)
    mkdir(outputPath)

    for item in listdir(basePath):
        itemPath = path.join(basePath, item)

        if path.isdir(itemPath):
            copy_files_in_dir(itemPath, path.join(outputPath, item))
        else:
            print(f"copying '{itemPath}' to '{outputPath}'")
            shutil.copy(itemPath, outputPath)


def extract_title(markdown: str) -> str:
    header = re.search(r"^#\s*(.+)$", markdown, flags=re.MULTILINE)
    if not header:
        raise Exception("No title in the provided markdown file.")
    return header.group(1).strip()


def get_file_content_str(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def generate_pages_recursive(
    dir_path_content, template_path, dest_dir_path, basepath
) -> None:

    dir_content = listdir(dir_path_content)
    for content in dir_content:
        from_path = path.join(dir_path_content, content)
        dest_path = path.join(dest_dir_path, content)
        if path.isfile(from_path):
            root, ext = path.splitext(dest_path)
            if ext == ".md":
                generate_page(from_path, template_path, root + ".html", basepath)
            else:
                continue
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)


def generate_page(from_path, template_path, dest_path, basepath) -> None:
    print(
        f"Generating page from '{from_path}' to '{dest_path}' using '{template_path}'"
    )

    md_str = get_file_content_str(from_path)
    template_str = get_file_content_str(template_path)

    html_node = markdown_to_html_node(md_str)
    html_str = html_node.to_html()

    title = extract_title(md_str)

    template_str = template_str.replace("{{ Title }}", title)
    template_str = template_str.replace("{{ Content }}", html_str)
    template_str = template_str.replace('href="/', f'href="{basepath}')
    template_str = template_str.replace('src="/', f'src="{basepath}')

    makedirs(path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template_str)


def main():
    cwd = getcwd()
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    static_dir = path.join(cwd, "static")
    public_dir = path.join(cwd, "docs")

    copy_files_in_dir(static_dir, public_dir)

    # generate index
    from_path = path.join(cwd, "content")
    dset_path = path.join(cwd, "docs")
    template__path = path.join(cwd, "template.html")

    generate_pages_recursive(from_path, template__path, dset_path, basepath)


if __name__ == "__main__":
    main()
