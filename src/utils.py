import os

IGNORE_DIRS = {".git", "__pycache__", "venv", ".venv", ".mypy_cache", ".pytest_cache"}


def compress_content(content: str) -> str:
    """Lightweight compression without regex"""
    lines = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped:
            lines.append(" ".join(stripped.split()))
    return "\n".join(lines)


def process_repository(root_folder, output_file="output.txt1"):
    py_entries = []
    structure_lines = []
    counter = 1

    root_folder = os.path.abspath(root_folder)

    with open(output_file, "w", encoding="utf-8") as out:

        for root, dirs, files in os.walk(root_folder):

            # Remove ignored directories in-place (important optimization)
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            level = root.replace(root_folder, "").count(os.sep)
            indent = "    " * level
            structure_lines.append(f"{indent}{os.path.basename(root)}/")

            subindent = "    " * (level + 1)

            for file in sorted(files):

                structure_lines.append(f"{subindent}{file}")

                if file.endswith(".py"):

                    file_path = os.path.join(root, file)

                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = compress_content(f.read())

                        py_entries.append(
                            (
                                counter,
                                root,
                                file,
                                content
                            )
                        )

                        counter += 1

                    except Exception as e:
                        print(f"Skipping {file_path}: {e}")

        # Write python file data
        for num, folder, fname, content in py_entries:
            out.write(f"{num})\n")
            out.write(f"Folder Location: {folder}\n")
            out.write(f"File Name: {fname}\n")
            out.write("-------------------\n")
            out.write(content + "\n\n")

        # Write folder structure
        out.write("\n===== Folder Structure =====\n")
        out.write("\n".join(structure_lines))


if __name__ == "__main__":
    folder = input("Enter root folder path: ").strip()
    process_repository(folder)
    print("Output written to output.txt")