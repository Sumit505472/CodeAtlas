
from collections.abc import Iterable, Iterator

from langchain_core.documents import Document
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    Language
)


LANGUAGE_MAP = {
    "py": Language.PYTHON,

    "js": Language.JS,
    "jsx": Language.JS,

    "ts": Language.TS,
    "tsx": Language.TS,

    "java": Language.JAVA,

    "cpp": Language.CPP,
    "hpp": Language.CPP,
    "h": Language.CPP,

    "c": Language.C,
    "go": Language.GO,
    "rs": Language.RUST,

    "html": Language.HTML,
    "md": Language.MARKDOWN,
}


class CodeChunker:

    def __init__(
        self,
        chunk_size: int = 1200,
        chunk_overlap: int = 150
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Generic fallback for unsupported languages
        self.default_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=True
        )

    def get_splitter(self, document: Document):

        language_name = document.metadata.get(
            "language", ""
        ).lower()

        language = LANGUAGE_MAP.get(language_name)

        if language is None:
            return self.default_splitter

        return RecursiveCharacterTextSplitter.from_language(
            language=language,
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            add_start_index=True
        )

    def chunk_documents(
        self,
        documents: Iterable[Document]
    ) -> Iterator[Document]:

        for document in documents:

            splitter = self.get_splitter(document)

            chunks = splitter.split_documents([document])

            for index, chunk in enumerate(chunks):

                chunk.metadata["chunk_index"] = index

                yield chunk
