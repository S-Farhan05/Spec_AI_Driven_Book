"""
Text chunking utility for the Documentation Ingestion Pipeline
"""
import re
from typing import List, Tuple
from models import DocumentChunk, CrawledPage
from utils import count_tokens_cohere
import logging
import time
import hashlib


logger = logging.getLogger(__name__)


class TextChunker:
    """Text chunking utility with sentence-aware splitting"""

    def __init__(self, min_chunk_size: int = 200, max_chunk_size: int = 1000, overlap: int = 50):
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap

    def split_by_sentence(self, text: str) -> List[str]:
        """
        Split text by sentences while preserving semantic boundaries
        """
        # Split by sentence endings, keeping the punctuation
        sentences = re.split(r'(?<=[.!?])\s+', text)

        # Clean up any empty strings
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences

    def create_chunks_from_sentences(self, sentences: List[str], source_url: str, module: str, section: str) -> List[DocumentChunk]:
        """
        Create chunks from sentences, ensuring they meet size requirements
        """
        chunks = []
        current_chunk = ""
        current_tokens = 0

        for i, sentence in enumerate(sentences):
            sentence_tokens = count_tokens_cohere(sentence)

            # If a single sentence is too large, split it by paragraphs or fixed length
            if sentence_tokens > self.max_chunk_size:
                sub_chunks = self.split_large_sentence(sentence)
                for sub_chunk in sub_chunks:
                    chunk_id = f"chunk_{hashlib.md5((source_url + sub_chunk[:50]).encode()).hexdigest()[:12]}_{int(time.time())}"
                    chunk = DocumentChunk(
                        chunk_id=chunk_id,
                        content=sub_chunk,
                        url=source_url,
                        module=module,
                        section=section,
                        token_count=count_tokens_cohere(sub_chunk)
                    )
                    chunks.append(chunk)
                continue

            # Check if adding this sentence would exceed max chunk size
            if current_tokens + sentence_tokens > self.max_chunk_size and current_chunk:
                # Save the current chunk
                chunk_id = f"chunk_{hashlib.md5((source_url + current_chunk[:50]).encode()).hexdigest()[:12]}_{int(time.time())}"
                chunk = DocumentChunk(
                    chunk_id=chunk_id,
                    content=current_chunk.strip(),
                    url=source_url,
                    module=module,
                    section=section,
                    token_count=current_tokens
                )
                chunks.append(chunk)

                # Start a new chunk with overlap if possible
                if self.overlap > 0 and i > 0:
                    # Add overlap by including some previous sentences
                    overlap_text = self.get_overlap_text(sentences, i)
                    current_chunk = overlap_text + " " + sentence
                    current_tokens = count_tokens_cohere(current_chunk)
                else:
                    current_chunk = sentence
                    current_tokens = sentence_tokens
            else:
                # Add sentence to current chunk
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence
                current_tokens += sentence_tokens

        # Add the last chunk if it has content
        if current_chunk.strip():
            chunk_id = f"chunk_{hashlib.md5((source_url + current_chunk[:50]).encode()).hexdigest()[:12]}_{int(time.time())}"
            chunk = DocumentChunk(
                chunk_id=chunk_id,
                content=current_chunk.strip(),
                url=source_url,
                module=module,
                section=section,
                token_count=current_tokens
            )
            chunks.append(chunk)

        return chunks

    def get_overlap_text(self, sentences: List[str], current_idx: int) -> str:
        """
        Get text for overlap from previous sentences
        """
        overlap_sentences = []
        tokens_count = 0

        # Go backwards through sentences until we reach overlap token count
        for i in range(current_idx - 1, max(-1, current_idx - 10), -1):  # Limit to 10 previous sentences
            sentence_tokens = count_tokens_cohere(sentences[i])
            if tokens_count + sentence_tokens > self.overlap:
                break
            overlap_sentences.insert(0, sentences[i])
            tokens_count += sentence_tokens

        return " ".join(overlap_sentences)

    def split_large_sentence(self, sentence: str) -> List[str]:
        """
        Split a sentence that is too large into smaller chunks
        """
        if count_tokens_cohere(sentence) <= self.max_chunk_size:
            return [sentence]

        # Split by paragraphs first
        paragraphs = sentence.split('\n\n')
        if len(paragraphs) > 1:
            chunks = []
            for para in paragraphs:
                if count_tokens_cohere(para) <= self.max_chunk_size:
                    chunks.append(para)
                else:
                    # Further split if still too large
                    sub_chunks = self.split_by_length(para)
                    chunks.extend(sub_chunks)
            return chunks

        # If no paragraphs, split by length
        return self.split_by_length(sentence)

    def split_by_length(self, text: str) -> List[str]:
        """
        Split text by length when semantic boundaries aren't sufficient
        """
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.max_chunk_size * 4  # Approximate character count (4 chars per token)

            # If we're near the end, take the rest
            if end >= len(text):
                chunks.append(text[start:])
                break

            # Find a good breaking point (try to break at sentence or word boundary)
            break_point = self.find_break_point(text, start, end)

            chunk = text[start:break_point].strip()
            if chunk and count_tokens_cohere(chunk) > 0:
                chunks.append(chunk)

            start = break_point

        return chunks

    def find_break_point(self, text: str, start: int, suggested_end: int) -> int:
        """
        Find a good break point for splitting text
        """
        end = min(suggested_end, len(text))

        # Try to break at sentence boundary
        for i in range(end, start, -1):
            if text[i:i+2] in ['. ', '! ', '? ']:
                return i + 2

        # Try to break at word boundary
        for i in range(end, start, -1):
            if text[i] == ' ':
                return i

        # If no good break point found, break at suggested end
        return end

    def chunk_page(self, crawled_page: CrawledPage) -> List[DocumentChunk]:
        """
        Chunk a single crawled page into DocumentChunk objects
        """
        if not crawled_page.content:
            logger.warning(f"No content to chunk for page: {crawled_page.url}")
            return []

        logger.info(f"Chunking page: {crawled_page.url} ({len(crawled_page.content)} chars)")

        # Split the content into sentences
        sentences = self.split_by_sentence(crawled_page.content)

        # Create chunks from sentences
        chunks = self.create_chunks_from_sentences(
            sentences,
            crawled_page.url,
            crawled_page.module,
            crawled_page.section
        )

        logger.info(f"Created {len(chunks)} chunks from page: {crawled_page.url}")

        # Validate chunk sizes
        valid_chunks = []
        for chunk in chunks:
            if chunk.token_count >= self.min_chunk_size or len(chunks) == 1:
                # Accept the chunk if it meets minimum size OR it's the only chunk from the page
                valid_chunks.append(chunk)
            else:
                logger.warning(f"Chunk too small ({chunk.token_count} tokens), skipping: {chunk.chunk_id}")

        return valid_chunks

    def chunk_pages(self, crawled_pages: List[CrawledPage]) -> List[DocumentChunk]:
        """
        Chunk multiple crawled pages
        """
        all_chunks = []
        for page in crawled_pages:
            chunks = self.chunk_page(page)
            all_chunks.extend(chunks)

        logger.info(f"Total chunks created from {len(crawled_pages)} pages: {len(all_chunks)}")
        return all_chunks