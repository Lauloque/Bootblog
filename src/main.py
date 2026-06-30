import shutil
from os import getcwd, listdir, mkdir, path


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


def generate_site() -> None:
    cwd = getcwd()
    static_dir = path.join(cwd, "static")
    public_dir = path.join(cwd, "public")

    copy_files_in_dir(static_dir, public_dir)


def main():
    generate_site()


if __name__ == "__main__":
    main()
