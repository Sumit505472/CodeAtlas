
from app.core.config import settings
from app.ingestion.github_client import GitHubClient
from app.ingestion.github_loader import GitHubLoader
from app.ingestion.chunker import CodeChunker


github = GitHubClient(token=settings.GITHUB_TOKEN)

try:
    # Load source documents
    loader = GitHubLoader(
        github_client=github,
        owner="react",
        repo="react",
        max_files=2
    )

    # Initialize chunker
    chunker = CodeChunker(
        chunk_size=1200,
        chunk_overlap=150
    )

    # Generate chunks
    chunks = chunker.chunk_documents(
        loader.lazy_load()
    )

    for index, chunk in enumerate(chunks, start=1):

        print(f"\n{'=' * 50}")
        print(f"CHUNK {index}")
        print("=" * 50)

        print("Source:", chunk.metadata["source"])
        print("Chunk index:", chunk.metadata["chunk_index"])
        print("Start index:", chunk.metadata["start_index"])
        print("Characters:", len(chunk.page_content))

        print("\nContent:")
        print(chunk.page_content[:500])

finally:
    github.close()
