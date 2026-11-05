
from pathlib import PurePosixPath


# Directories that should be ignored
IGNORED_DIRS = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "__pycache__",
    "dist",
    "build",
    "coverage",
    ".next",
    "vendor",
    "target",
}

# File extensions that we want to process
ALLOWED_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx",
    ".java", ".cpp", ".c", ".h", ".hpp",
    ".go", ".rs", ".php", ".rb",
    ".html", ".css", ".scss",
    ".json", ".yaml", ".yml", ".toml",
    ".md", ".txt", ".rst",
    ".sql", ".sh", ".bat",
    ".xml", ".graphql", ".proto",
    ".ipynb",
}

# Important extensionless files
ALLOWED_FILENAMES = {
    "Dockerfile",
    "Makefile",
    "LICENSE",
    "Procfile",
    ".gitignore",
    ".dockerignore",
}

# Files that usually contain generated or dependency data
IGNORED_FILENAMES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "poetry.lock",
    "uv.lock",
    "Cargo.lock",
    "go.sum",
}


def should_include_file(
    path: str,
    size: int | None = None,
    max_file_size: int = 1_000_000
) -> bool:

    file_path = PurePosixPath(path)

    # Only process files, not directories
    if not path or path.endswith("/"):
        return False

    # Ignore unwanted directories
    if any(part in IGNORED_DIRS for part in file_path.parts):
        return False

    filename = file_path.name

    # Ignore specific filenames
    if filename in IGNORED_FILENAMES:
        return False

    # Ignore minified files
    if ".min." in filename:
        return False

    # Ignore files larger than the limit
    if size is not None and size > max_file_size:
        return False

    # Allow selected extensionless files
    if filename in ALLOWED_FILENAMES:
        return True

    # Allow only selected file extensions
    return file_path.suffix.lower() in ALLOWED_EXTENSIONS
