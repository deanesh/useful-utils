import os
import pandas as pd

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


# ---------------------------------------------------------
# Detect Git Repositories (recursive)
# ---------------------------------------------------------
def find_repos(root):

    repos = []

    for dirpath, dirnames, filenames in os.walk(root):

        if ".git" in dirnames:
            repos.append(dirpath)

            # do not go deeper once repo found
            dirnames[:] = []

    # if none found treat root as repo
    if not repos:
        repos.append(root)

    return repos


# ---------------------------------------------------------
# Compress Python Code
# ---------------------------------------------------------
def compress_code(content):

    lines = []

    for line in content.splitlines():
        stripped = line.strip()

        if stripped:
            lines.append(" ".join(stripped.split()))

    return "\n".join(lines)


# ---------------------------------------------------------
# Build Folder Structure
# ---------------------------------------------------------
def build_structure(repo):

    structure = []

    for root, dirs, files in os.walk(repo):

        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        level = root.replace(repo, "").count(os.sep)
        indent = "    " * level

        structure.append(f"{indent}{os.path.basename(root)}/")

        subindent = "    " * (level + 1)

        for f in sorted(files):
            structure.append(f"{subindent}{f}")

    return "\n".join(structure)


# ---------------------------------------------------------
# Extract Python Files
# ---------------------------------------------------------
def extract_python(repo):

    results = []

    for root, dirs, files in os.walk(repo):

        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:

            if file.endswith(".py"):

                path = os.path.join(root, file)

                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = compress_code(f.read())

                    results.append((root, file, content))

                except:
                    pass

    return results


# ---------------------------------------------------------
# README Analysis
# ---------------------------------------------------------
def read_readme(repo):

    for file in os.listdir(repo):

        if file.lower() == "readme.md":

            path = os.path.join(repo, file)

            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()

            if not content:
                return "README.md exists but is empty. Objective could not be inferred."

            lines = content.splitlines()

            return "\n".join(lines[:20])

    return "README.md not found. Repository objective analysis could not be done."


# ---------------------------------------------------------
# Data Sample Extraction
# ---------------------------------------------------------
def extract_data_samples(repo):

    data_dirs = ["data", "dataset", "datasets"]

    samples = []

    for d in data_dirs:

        path = os.path.join(repo, d)

        if not os.path.exists(path):
            continue

        for file in os.listdir(path):

            file_path = os.path.join(path, file)

            try:

                if file.endswith(".csv"):
                    df = pd.read_csv(file_path)

                elif file.endswith(".xlsx"):
                    df = pd.read_excel(file_path)

                else:
                    continue

                headers = list(df.columns)
                row = df.iloc[0].to_dict()

                samples.append(
f"""
Sample File: {file}
Headers : {headers}
Row(1 row): {row}
"""
                )

            except:
                pass

    if not samples:
        return "No readable dataset samples found."

    return "\n".join(samples)


# ---------------------------------------------------------
# Write Repo Output
# ---------------------------------------------------------
def write_repo_output(repo):

    repo_name = os.path.basename(repo)

    file_name = f"output_{repo_name}.txt1"

    structure = build_structure(repo)

    python_files = extract_python(repo)

    with open(file_name, "w", encoding="utf-8") as out:

        out.write("===========================================================\n")
        out.write("Folder Structure\n")
        out.write("===========================================================\n\n")

        out.write(structure)

        out.write("\n\n=======================================================================\n")
        out.write("Python Files\n")
        out.write("========================================================================\n\n")

        for folder, fname, content in python_files:

            out.write(f"# Folder Location: {folder}\n")
            out.write(f"File Name: {fname}\n")
            out.write("------------------------------------\n")

            out.write(content)
            out.write("\n\n")


# ---------------------------------------------------------
# Repo Objective File
# ---------------------------------------------------------
def write_repo_objective(repos):

    with open("repo_objective.txt1", "w", encoding="utf-8") as out:

        for repo in repos:

            repo_name = os.path.basename(repo)

            out.write("===========================================================\n")
            out.write(f"Repository: {repo_name}\n")
            out.write("===========================================================\n\n")

            out.write("README Summary\n")
            out.write("------------------------\n")

            out.write(read_readme(repo))

            out.write("\n\nData Sample\n")
            out.write("------------------------\n")

            out.write(extract_data_samples(repo))

            out.write("\n\n")


# ---------------------------------------------------------
# Folder Summary
# ---------------------------------------------------------
def write_folder_summary(root, repos):

    with open("folder_summary.txt1", "w", encoding="utf-8") as out:

        out.write(f"Main Folder: {root}\n\n")

        out.write("Repositories Found:\n")

        for r in repos:
            out.write(f"- {os.path.basename(r)}\n")

        out.write(f"\nTotal Git Repos count: {len(repos)}\n")


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():

    root = input("Enter main folder path: ").strip()

    repos = find_repos(root)

    write_folder_summary(root, repos)

    for repo in repos:
        write_repo_output(repo)

    write_repo_objective(repos)

    print("\nAll files generated successfully.\n")


if __name__ == "__main__":
    main()