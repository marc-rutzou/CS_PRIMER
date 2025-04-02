import weaviate
from weaviate.classes.query import MetadataQuery
from weaviate.collections.classes.internal import QueryReturn
from typing import Optional, List
import os
from dotenv import load_dotenv

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

def hybrid_search(client: weaviate.Client, query_text: str, limit: int = 3, alpha: float = 0.5) -> Optional[QueryReturn]:
    """
    Perform hybrid search combining vector and keyword search capabilities.
    
    This function balances semantic understanding (vector search) with keyword matching (BM25),
    providing results that may be conceptually related and/or contain specific keywords.
    The alpha parameter controls the balance between these two search methods.
    
    Args:
        client: An initialized Weaviate client
        query_text: The search query text
        limit: Maximum number of results to return (default: 3)
        alpha: Balance between keyword and vector search (0.0-1.0)
               - 0.0: Pure keyword search
               - 1.0: Pure vector search
               - 0.5 (default): Equal weight to both methods
        
    Returns:
        Optional[QueryReturn]: Weaviate search results or None if error occurs
            - If successful, contains:
                - objects: List of matched document chunks
                - Each object has properties (text, title, filename) and metadata
                - metadata.score: Combined relevance score
                - metadata.explain_score: Shows vector and keyword contributions
    
    Example:
        # Balanced search (default)
        results = hybrid_search(client, "data security compliance")
        
        # More emphasis on semantic meaning
        results = hybrid_search(client, "data security compliance", alpha=0.7)
        
        # More emphasis on exact keyword matches
        results = hybrid_search(client, "data security compliance", alpha=0.3)
    """
    try:
        collection = client.collections.get("Chunk")
        results = collection.query.hybrid(
            query=query_text,
            limit=limit,
            alpha=alpha,
            return_metadata=MetadataQuery(score=True, explain_score=True)
        )
        return results
    except Exception as e:
        print(f"Error performing hybrid search: {e}")
        return None

def get_document_sources(client: weaviate.Client, limit: int = 1000) -> List[str]:
    """
    Extract unique document sources (filenames) to understand knowledge base scope.
    
    Args:
        client: An initialized Weaviate client
        
    Returns:
        List[str]: A list of unique document sources in the collection
    """
    try:
        collection = client.collections.get("Chunk")
        response = collection.query.fetch_objects(
            return_properties=["filename"],
            limit=limit  # Set a high limit to get all objects
        )
        
        # Extract unique filenames and clean them up
        unique_sources = set()
        for i, obj in enumerate(response.objects):
            filename = obj.properties.get("filename")
            if filename:
                # Remove file extension and ID numbers, replace separators with spaces
                clean_name = filename.split(".")[0]  # Remove extension
                if "_" in clean_name:
                    # Remove ID number if present (assumes ID is after last underscore)
                    clean_name = "_".join(clean_name.split("_")[:-1])
                clean_name = clean_name.replace("-", " ").replace("_", " ")
                unique_sources.add(clean_name)
        
        return sorted(list(unique_sources))
    except Exception as e:
        print(f"Error retrieving document sources: {e}")
        return []


if __name__ == "__main__":
    """
    Demonstrate the hybrid search and document source retrieval functionality.
    """
    # Set up the query and result limit
    prompt = "centralized ML team"
    max_results = 3
    
    # Load environment variables first
    load_dotenv()
    
    # Create Weaviate client
    client = create_weaviate_client()
    
    try:
        # Perform hybrid search with default balanced settings
        print(f"\nPerforming hybrid search (balanced) for: '{prompt}'")
        results = hybrid_search(client, prompt, max_results)
        if results:
            for i, obj in enumerate(results.objects):
                print(f"\nResult {i+1}:")
                print(f"Score: {obj.metadata.score}; Explanation: {obj.metadata.explain_score}")
                print(f"Source file: {obj.properties.get('filename', 'Unknown')}\n")
                print(f"Title: {obj.properties.get('title', 'No title')}\n")
                print(f"Text: {obj.properties.get('text', '')}\n")
        
        # Demonstrate retrieving all document sources from the collection
        print("\nRetrieving all document sources:")
        sources = get_document_sources(client)
        print(f"Found {len(sources)} unique document sources:")
        # Print all sources as they should be a reasonable number
        for i, source in enumerate(sources):
            print(f"  {i+1}. {source}")
        
    finally:
        # Ensure client is closed properly
        client.close()
