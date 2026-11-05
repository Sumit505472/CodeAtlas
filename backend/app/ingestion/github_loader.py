
from collections.abc import Iterator
from pathlib import PurePosixPath

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

from app.ingestion.github_client import GitHubClient
from app.ingestion.file_filter import should_include_file


class GitHubLoader(BaseLoader):

    def __init__(
        self,
        github_client: GitHubClient,
        owner: str,
        repo: str,
        branch: str | None = None,
        max_files: int | None = None
    ):
        self.github_client = github_client
        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.max_files = max_files

    def lazy_load(self) -> Iterator[Document]:

        # Step 1: Get repository information
        repo_data = self.github_client.get_repository(
            self.owner,
            self.repo
        )

        branch = self.branch or repo_data["default_branch"]

        # Step 2: Get repository tree
        tree_data = self.github_client.get_repository_tree(
            self.owner,
            self.repo,
            branch
        )

        if tree_data.get("truncated"):
            raise RuntimeError(
                "GitHub returned a truncated repository tree."
            )

        # Step 3: Process eligible files
        processed_files = 0

        for entry in tree_data["tree"]:

            if entry["type"] != "blob":
                continue

            if not should_include_file(
                path=entry["path"],
                size=entry.get("size")
            ):
                continue

            # Step 4: Fetch file content
            content = self.github_client.get_file_content(
                self.owner,
                self.repo,
                entry["sha"]
            )

            file_path = entry["path"]

            # Step 5: Create metadata
            metadata = {
                "source": file_path,
                "repository": f"{self.owner}/{self.repo}",
                "branch": branch,
                "file_sha": entry["sha"],
                "language": (
                    PurePosixPath(file_path).suffix.lstrip(".")
                    or "text"
                )
            }

            # Step 6: Convert into LangChain Document
            yield Document(
                page_content=content,
                metadata=metadata
            )

            processed_files += 1

            if (
                self.max_files is not None
                and processed_files >= self.max_files
            ):
                break
