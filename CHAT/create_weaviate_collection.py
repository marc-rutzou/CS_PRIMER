import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from typing import List, Dict, Tuple, Union

from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker

import weaviate
from weaviate.classes.config import Configure, Property, DataType

from utils.tokenizer import OpenAITokenizerWrapper


logging.getLogger().setLevel(logging.WARNING)  # Set root logger to WARNING to suppress other loggers
logging.basicConfig(
    format='%(message)s'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set your logger to INFO


def get_kb_files(folder_path: Path, file_extension: str) -> List[Path]:
    """
    Retrieve all files with specified extension from the given folder path.
    
    Args:
        folder_path (Path): Absolute or relative path to the target folder
        file_extension (str): File extension to search for (without dot). Defaults to "html"
    
    Returns:
        List[Path]: List of Path objects for all matching files
        
    Raises:
        FileNotFoundError: If the target directory doesn't exist
    """
    if not folder_path.exists():
        raise FileNotFoundError(f"Directory '{folder_path}' not found")
    
    # Find all files with specified extension
    files = list(folder_path.glob(f"**/*.{file_extension}"))
    logger.info(f"Found {len(files)} .{file_extension} files in {folder_path} directory\n")
    
    return files


def convert_files_to_documents(converter: DocumentConverter, file_paths: List[Union[Path, str]]) -> Tuple[List, Dict[str, str]]:
    """
    Convert a list of files to documents using the provided converter.
    
    Args:
        file_paths (List[Union[Path, str]]): List of Path objects or strings representing file paths
        converter (DocumentConverter): An initialized docling DocumentConverter instance
        log_progress (bool, optional): Whether to log progress. Defaults to True.
        
    Returns:
        Tuple[List, Dict[str, str]]: (
            list: Successfully converted documents,
            dict: Failed conversions with file paths as keys and error messages as values
        )
    """
    documents = []
    failed_conversions: Dict[str, str] = {}
    total_files = len(file_paths)
    
    logger.info(f"Starting conversion of {total_files} files")
    
    for i, file_path in enumerate(file_paths):
        try:
            # Convert single file
            result = converter.convert(file_path)
            documents.append(result.document)
            
            # Log progress at intervals for large batches
            if (i + 1) % 10 == 0:
                logger.info(f"Converted {i + 1}/{total_files} files")
                
        except Exception as e:
            error_msg = str(e)
            failed_conversions[str(file_path)] = error_msg
            logger.warning(f"Failed to convert {file_path}: {error_msg}")
    
    # Log summary
    success_count = len(documents)
    failed_count = len(failed_conversions)
    logger.info(f"Successfully converted {success_count}/{total_files} documents")
    if failed_count > 0:
        logger.warning(f"Failed to convert {failed_count} documents")
    
    return documents, failed_conversions


def chunk_documents(chunker: HybridChunker, documents: List) -> Tuple[List, Dict[int, str]]:
    """
    Process documents through the chunker and create text chunks.
    
    Args:
        chunker (HybridChunker): An initialized docling HybridChunker instance
        documents (List): List of documents to chunk
        
    Returns:
        Tuple[List, Dict[int, str]]: (
            list: Successfully created chunks from all documents,
            dict: Failed chunking operations with document indices as keys and error messages as values
        )
    """
    all_chunks = []
    failed_chunks: Dict[int, str] = {}
    total_docs = len(documents)
    
    logger.info(f"\nStarting chunking of {total_docs} documents")
    
    for i, doc in enumerate(documents):
        try:
            # Chunk single document
            doc_chunks = list(chunker.chunk(dl_doc=doc))
            all_chunks.extend(doc_chunks)
        except Exception as e:
            error_msg = str(e)
            failed_chunks[i] = error_msg
            logger.warning(f"Failed to chunk document at index {i}: {error_msg}")
    
    # Log summary
    success_count = total_docs - len(failed_chunks)
    failed_count = len(failed_chunks)
    logger.info(f"Successfully chunked {success_count}/{total_docs} documents")
    logger.info(f"Created {len(all_chunks)} chunks total")
    if failed_count > 0:
        logger.warning(f"Failed to chunk {failed_count} documents")
    
    return all_chunks, failed_chunks


def create_weaviate_client() -> weaviate.Client:
    """
    Create and return a connection to the local Weaviate database.
    
    Establishes a connection to the Weaviate vector database running locally,
    configuring it with the OpenAI API key from environment variables.
    
    Returns:
        weaviate.Client: Initialized Weaviate client that can be used for queries
        
    Raises:
        ValueError: If OPENAI_API_KEY environment variable is not set
        
    Note:
        Assumes environment variables are already loaded into memory
        The connection assumes Weaviate is running on the default port (8080)
    """
    # Check for required environment variable
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")
    
    # Connection to local weaviate database (looks at port 8080)
    client = weaviate.connect_to_local(
        headers={
            "X-OpenAI-Api-Key": openai_api_key
        }
    )
    return client


def recreate_chunk_collection(client: weaviate.WeaviateClient, embedding_model: str) -> weaviate.collections.Collection:
    """
    Recreate the Chunk collection in Weaviate with predefined properties.
    
    This function will delete the existing Chunk collection if it exists
    and create a new one with text, filename, and title properties.
    
    Args:
        client: The Weaviate client instance
        
    Returns:
        The newly created Chunk collection object
    """
    collection_name = "Chunk"
    
    # Delete existing collection if it exists
    if client.collections.exists(collection_name):
        client.collections.delete(collection_name)
        logger.info(f"Deleted existing {collection_name} collection")
    
    # Create new collection with fixed properties
    collection = client.collections.create(
        name=collection_name,
        properties=[
            Property(name="text", data_type=DataType.TEXT),
            Property(name="filename", data_type=DataType.TEXT),
            Property(name="title", data_type=DataType.TEXT),
        ],
        vectorizer_config=Configure.Vectorizer.text2vec_openai(model=embedding_model)
    )
    logger.info(f"Created {collection_name} collection in Weaviate with OpenAI vectorizer")
    
    return collection


def populate_chunk_collection(collection: weaviate.collections.Collection, chunks: List) -> Tuple[int, int, int]:
    """
    Populate the Weaviate collection with the provided chunks.
    
    Args:
        collection: The Weaviate collection to populate
        chunks: List of chunks to add to the collection
        
    Returns:
        Tuple[int, int, int]: (
            total_chunks: Total number of chunks added,
            chunks_with_filename: Number of chunks with filename metadata,
            chunks_with_title: Number of chunks with title metadata
        )
    """
    total_chunks = len(chunks)
    chunks_with_filename = 0
    chunks_with_title = 0
    
    logger.info(f"\nStarting to populate collection with {total_chunks} chunks")
    
    with collection.batch.dynamic() as batch:
        for i, chunk in enumerate(chunks):
            # Extract filename
            filename = None
            if hasattr(chunk.meta, 'origin') and hasattr(chunk.meta.origin, 'filename'):
                filename = chunk.meta.origin.filename
                chunks_with_filename += 1
            
            # Extract title (first heading)
            title = None
            if hasattr(chunk.meta, 'headings') and chunk.meta.headings:
                title = chunk.meta.headings[0]
                chunks_with_title += 1
            
            # Add to batch (Weaviate handles vectorization automatically)
            batch.add_object(
                properties={
                    "text": chunk.text,                # Original text without enrichment
                    "filename": filename,              # Source file
                    "title": title,                    # Title from first heading
                }
            )
    
    # Log detailed metadata statistics
    logger.info(f"Added {total_chunks} chunks to Weaviate")
    logger.info(f"Metadata statistics:")
    logger.info(f"  - Chunks with filenames: {chunks_with_filename}/{total_chunks} ({chunks_with_filename/total_chunks*100:.1f}%)")
    logger.info(f"  - Chunks with titles: {chunks_with_title}/{total_chunks} ({chunks_with_title/total_chunks*100:.1f}%)")
    
    return total_chunks, chunks_with_filename, chunks_with_title



if __name__ == "__main__":
    # Create Docling converter
    converter = DocumentConverter()    

    # Get all html files from our data folder
    kb_path = Path(__file__).parent.parent / "kb"
    html_files = get_kb_files(kb_path, "html")

    # Convert files to Docling Document Objects
    docs, failed_files = convert_files_to_documents(converter, html_files)
    if failed_files:
        logger.warning(f"The following files failed conversion: {list(failed_files.keys())}")

    # Set context length for OpenAI's embedding model
    MAX_TOKENS = 8191  # https://platform.openai.com/docs/guides/embeddings#embedding-models
    
    # Initialize OpenAI's tokenizer
    tokenizer = OpenAITokenizerWrapper(model_name="cl100k_base", max_length=MAX_TOKENS)

    # Create Docling Hybrid Chunker
    chunker = HybridChunker(
        tokenizer=tokenizer,
        max_tokens=MAX_TOKENS,
        merge_peers=True,
    )

    # Chunk all documents into chunks
    all_chunks, failed_chunks = chunk_documents(chunker, docs)
    if failed_chunks:
        logger.warning(f"The following document indices failed chunking: {list(failed_chunks.keys())}")

    # load .env variables
    load_dotenv()

    # Create Weaviate Client
    weaviate_client = create_weaviate_client()
    meta_info = weaviate_client.get_meta()
    logger.info(f"\nMetadata about the Weaviate instance: {meta_info}\n")

    # Replace the collection creation code with simplified function call
    chunks_collection = recreate_chunk_collection(weaviate_client, "text-embedding-3-large")

    # Replace the direct batch operation with the function call
    populate_chunk_collection(chunks_collection, all_chunks)

    weaviate_client.close()