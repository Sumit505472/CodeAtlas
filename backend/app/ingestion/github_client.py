
import httpx
import base64


class GitHubClient:

    BASE_URL = "https://api.github.com"

    def __init__(self, token: str):

        if not token or not token.strip():
            raise ValueError("GitHub token cannot be empty")

        self.headers = {
            "Authorization": f"Bearer {token.strip()}",
            "Accept": "application/vnd.github+json"
        }

        self.client = httpx.Client(
            base_url=self.BASE_URL,
            headers=self.headers,
            timeout=30.0,
            follow_redirects=True
        )

    def get_repository(self, owner: str, repo: str) -> dict:

        response = self.client.get(
            f"/repos/{owner}/{repo}"
        )

        response.raise_for_status()

        return response.json()

    def get_repository_tree(
        self,
        owner: str,
        repo: str,
        branch: str
    ) -> dict:

        commit_response = self.client.get(
            f"/repos/{owner}/{repo}/commits/{branch}"
        )
        commit_response.raise_for_status()

        commit_data = commit_response.json()

        tree_sha = commit_data["commit"]["tree"]["sha"]

        tree_response = self.client.get(
            f"/repos/{owner}/{repo}/git/trees/{tree_sha}",
            params={"recursive": "1"}
        )
        tree_response.raise_for_status()

        return tree_response.json()

    def get_file_content(
        self,
        owner: str,
        repo: str,
        file_sha: str
    ) -> str:

        response = self.client.get(
            f"/repos/{owner}/{repo}/git/blobs/{file_sha}"
        )

        response.raise_for_status()

        blob_data = response.json()

        encoded_content = blob_data["content"]

        decoded_content = base64.b64decode(
            encoded_content
        ).decode("utf-8", errors="replace")

        return decoded_content

    def close(self):
        self.client.close()
