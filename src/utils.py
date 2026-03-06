import os

IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    ".mypy_cache",
    ".pytest_cache",
    "node_modules",
    ".idea",
    ".vscode"
}


def is_git_repo(path):
    """Check if directory is a git repository"""
    return os.path.isdir(os.path.join(path, ".git"))


def compress_python(content):
    """Compress python file content"""
    lines = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped:
            lines.append(" ".join(stripped.split()))
    return "\n".join(lines)


def find_git_repos(root_folder):
    """
    Detect git repos inside root.
    If none found, treat root as repo.
    """
    repos = []

    for item in os.listdir(root_folder):
        full_path = os.path.join(root_folder, item)

        if os.path.isdir(full_path) and is_git_repo(full_path):
            repos.append(full_path)

    if not repos:
        repos.append(root_folder)

    return repos


def process_repo(repo_path):
    repo_name = os.path.basename(repo_path.rstrip(os.sep))
    output_file = f"output_{repo_name}.txt1"

    structure_lines = []
    python_entries = []

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        level = root.replace(repo_path, "").count(os.sep)
        indent = "    " * level
        structure_lines.append(f"{indent}{os.path.basename(root)}/")

        subindent = "    " * (level + 1)

        for file in sorted(files):

            structure_lines.append(f"{subindent}{file}")

            if file.endswith(".py"):

                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = compress_python(f.read())

                    python_entries.append(
                        (root, file, content)
                    )

                except Exception as e:
                    print(f"Skipping {file_path}: {e}")

    with open(output_file, "w", encoding="utf-8") as out:

        out.write("-----------------------------------------------------------\n")
        out.write("Folder Structure\n")
        out.write("-----------------------------------------------------------\n\n")

        out.write("\n".join(structure_lines))
        out.write("\n\n")

        out.write("----------------------------------------------------------------\n")
        out.write("Python Files (Compressed)\n")
        out.write("----------------------------------------------------------------\n\n")

        for folder, fname, content in python_entries:

            out.write(f"# Folder Location: {folder}\n")
            out.write(f"File Name: {fname}\n")
            out.write("------------------------------------\n")
            out.write(content)
            out.write("\n\n")

    print(f"Generated: {output_file}")


def main():

    root_folder = input("Enter root folder path: ").strip()

    repos = find_git_repos(root_folder)

    print(f"\nDetected {len(repos)} repository(s)\n")

    for repo in repos:
        process_repo(repo)


if __name__ == "__main__":
    main()