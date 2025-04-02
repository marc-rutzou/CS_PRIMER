"""
1. load environment variables using load_dotenv() from dotenv
2. Create Weaviate client using function create_weaviate_client() src/create_weaviate_database.py
3. Extract titles from Weaviate database using function get_document_sources(client: weaviate.Client, limit: int = 1000) from src/utils/search.py
4. Create Pydantic model QueryValidation with fields boolean is_knowledge_hub_query and float confidence_score
5. Create function that queries openai llm using the context from step 3 to validate if the user prompt can be answered with data from the knowledge hub, otherwise If you're unsure or the context
    doesn't contain the relevant information, say so.
6. if not, stop process
7. if yes, another function that lets the LLM call the function hybrid_search(client: weaviate.Client, query_text: str, limit: int = 3, alpha: float = 0.5) from src/utils/search.py to gather context from the knowledge hub about the prompt using keyword and vector search
8. function that creates answer to initial prompt using the context gathered in previous step.
9. LLM-as-a-judge that checks compares the final output of the previous step with the text from the chunks that were given as context and answers the question: is the answer solely based on the following information?
"""

# TODO: need a short summary about documents instead of just titles

from dotenv import load_dotenv
import logging
from pydantic import BaseModel, Field
from typing import List
from openai import OpenAI

from create_weaviate_collection import create_weaviate_client
from utils.search import get_document_sources
from utils.search import hybrid_search

logging.getLogger().setLevel(logging.WARNING)  # Set root logger to WARNING to suppress other loggers
logging.basicConfig(
    format='%(message)s'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set your logger to INFO


def prepare_context_from_search_results(search_results) -> str:
    """
    Prepares formatted context string from search results.
    
    Args:
        search_results: Results from hybrid search with text chunks and relevance scores
        
    Returns:
        formatted_context: String formatted for prompt use
    """
    context_chunks = []
    
    for i, obj in enumerate(search_results.objects):
        score = obj.metadata.score
        text = obj.properties.get('text', '')
        title = obj.properties.get('title', 'No title')
        source = obj.properties.get('filename', 'Unknown')
        
        context_chunks.append({
            "index": i+1,
            "score": score,
            "title": title,
            "text": text,
            "source": source
        })
    
    # Format context for the prompt
    formatted_context = ""
    for chunk in context_chunks:
        formatted_context += f"\nCHUNK {chunk['index']} (Relevance Score: {chunk['score']:.2f}):\n"
        formatted_context += f"Title: {chunk['title']}\n"
        formatted_context += f"Source: {chunk['source']}\n"
        formatted_context += f"Text: {chunk['text']}\n"
    
    return formatted_context


class QueryValidation(BaseModel):
    explanation: str = Field(
        description="Detailed reasoning about whether the query can be answered using the knowledge hub, "
                    "explaining the thought process before making a decision"
    )
    is_knowledge_hub_query: bool = Field(
        description="Whether the query can be answered using the knowledge hub"
    )
    confidence_score: float = Field(
        description="Confidence in the decision (0-1). 1.0 means completely certain about the yes/no decision, "
                   "0.0 means completely uncertain. This score reflects certainty regardless of whether "
                   "the answer is yes or no."
    )

def validate_query(client: OpenAI, query: str, document_titles: List[str]) -> QueryValidation:
    """
    Validates if a query can be answered using the knowledge hub content.
    
    Args:
        client: OpenAI client instance
        query: The user's question
        document_titles: List of available document titles in the knowledge hub
    
    Returns:
        QueryValidation object containing validation results
    """
    prompt = f"""Given the following user query and list of available document titles, 
    determine if the query can be answered using information from these documents.

    Note: These are just document titles and can be quite vague. The actual documents may be large and contain more information than their titles suggest. 
    If you think there's a reasonable chance that any of these documents might contain information about the query, err on the side of checking the documents (is_knowledge_hub_query = true).

    User Query: {query}

    Available Documents:
    {chr(10).join(f'- {title}' for title in document_titles)}

    Instructions:
    1. First, provide a detailed explanation of your reasoning, analyzing whether the query relates to the available documents
    2. Analyze if the query's topic appears related to the available documents
    3. Consider if the type of information requested would likely be found in these documents
    4. After your explanation, provide your assessment with:
    - explanation: your detailed reasoning about whether the query can be answered using the knowledge hub
    - is_knowledge_hub_query: true if the query can likely be answered, false if it cannot
    - confidence_score: your confidence in your decision between 0-1
        (1.0 = absolutely certain about your yes/no decision, 0.0 = completely uncertain)
        
        For example:
        - "What is 2+2?" -> {{
            "explanation": "This is a basic arithmetic question that doesn't require specialized knowledge from the documents. None of the document titles suggest they contain basic math information.",
            "is_knowledge_hub_query": false, 
            "confidence_score": 1.0
        }} (Certain it's not in docs)
        
        - "What is the MLOps lifecycle?" -> {{
            "explanation": "Several documents appear to cover MLOps topics, including potentially 'Introduction to MLOps' and 'MLOps Best Practices'. These documents would likely explain the MLOps lifecycle.",
            "is_knowledge_hub_query": true, 
            "confidence_score": 0.9
        }} (Very confident it's in docs)"""

    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that validates if queries can be answered using a knowledge hub."},
            {"role": "user", "content": prompt}
        ],
        response_format=QueryValidation,
    )
    
    return completion.choices[0].message.parsed


class QueryRewrite(BaseModel):
    reasoning: str = Field(
        description="Detailed explanation of the thought process: analyze the query's intent, "
                   "identify key concepts, and explain how the rewrite will improve retrieval"
    )
    original_query: str = Field(description="The original user query")
    rewritten_query: str = Field(description="The rewritten query optimized for knowledge retrieval")

def rewrite_query(client: OpenAI, query: str, document_titles: List[str]) -> QueryRewrite:
    """
    Rewrites a user query to optimize it for knowledge retrieval.
    
    Args:
        client: OpenAI client instance
        query: The original user query
        document_titles: List of available document titles to provide context
    
    Returns:
        QueryRewrite object containing the original and rewritten queries
    """
    prompt = f"""Given the following user query and available document titles, 
    rewrite the query to optimize it for retrieving relevant information from these documents.
    Think through this step-by-step:

    Original Query: {query}

    Available Documents:
    {chr(10).join(f'- {title}' for title in document_titles)}

    Instructions:
    1. First, analyze the query's intent and core information need
    2. Identify key concepts and terminology that might appear in technical documentation
    3. Consider which document titles suggest relevant content
    4. Then, rewrite the query by:
        - Removing conversational elements or irrelevant details
        - Using terminology aligned with the documents
        - Expanding ambiguous terms or acronyms
        - Keeping it concise and focused
    
    Provide your response as:
    - reasoning: detailed explanation of your analysis and rewrite process
    - original_query: the exact query provided
    - rewritten_query: your optimized version for retrieval
    """

    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that rewrites queries to optimize retrieval from knowledge bases."},
            {"role": "user", "content": prompt}
        ],
        response_format=QueryRewrite,
    )
    
    return completion.choices[0].message.parsed


class GeneratedAnswer(BaseModel):
    reasoning: str = Field(
        description="Detailed explanation of the reasoning process, including how different sources were weighed based on relevance"
    )
    final_answer: str = Field(
        description="The final answer to the user's query based on the knowledge hub content"
    )
    sources_used: List[str] = Field(
        description="List of sources used to generate the answer",
        default_factory=list
    )

def generate_answer(client: OpenAI, original_query: str, formatted_context: str) -> GeneratedAnswer:
    """
    Generates an answer to the user's query based on retrieved context.
    
    Args:
        client: OpenAI client instance
        original_query: The user's original question
        formatted_context: String formatted for prompt use
        
    Returns:
        GeneratedAnswer object containing the reasoning and final answer
    """
    prompt = f"""Answer the following query based solely on the provided information chunks from the knowledge hub.

    User Query: {original_query}

    Context Information (sorted by relevance score):
    {formatted_context}

    Instructions:
    1. Base your answer ONLY on the information provided in these chunks
    2. Consider the relevance scores when weighing the importance of different chunks
    3. If the provided chunks don't contain sufficient information to answer the query, state that clearly
    4. Don't introduce external knowledge that isn't present in the context
    5. Format your answer in a clear, structured way
    6. Cite relevant chunks by their numbers when explaining your reasoning

    Provide your response as:
    - reasoning: detailed explanation of how you arrived at the answer, including which chunks were most relevant
    - final_answer: concise, well-structured answer to the original query
    - sources_used: list of sources you referenced (e.g. ["document1.pdf", "document2.md"])
    """

    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions based strictly on provided context information."},
            {"role": "user", "content": prompt}
        ],
        response_format=GeneratedAnswer,
    )
    
    return completion.choices[0].message.parsed


class AnswerValidation(BaseModel):
    explanation: str = Field(
        description="Detailed analysis of how well the answer is grounded in the provided context"
    )
    is_factual: bool = Field(
        description="Whether the answer is solely based on the information provided in the context chunks"
    )
    is_comprehensive: bool = Field(
        description="Whether the answer addresses all relevant aspects of the query found in the context"
    )
    quality_score: float = Field(
        description="Overall quality score of the answer (0-1), considering factuality, comprehensiveness, and clarity"
    )
    improvement_suggestions: List[str] = Field(
        description="Specific suggestions for improving the answer, if any",
        default_factory=list
    )

def validate_answer(client: OpenAI, query: str, answer: str, formatted_context: str) -> AnswerValidation:
    """
    Validates if the generated answer is solely based on the provided context and evaluates its quality.
    
    Args:
        client: OpenAI client instance
        query: The original user query
        answer: The generated answer to validate
        formatted_context: String formatted for prompt use
        
    Returns:
        AnswerValidation object containing the validation results
    """
    prompt = f"""Evaluate whether the following answer is solely based on the provided context chunks and assess its overall quality.

    Original Query: {query}

    Generated Answer:
    {answer}

    Context Information (sorted by relevance score):
    {formatted_context}

    Instructions:
    1. Carefully compare the answer with the context chunks
    2. Check if all claims and information in the answer are supported by the context
    3. Identify any information in the answer that is not present in the context
    4. Determine if the answer addresses all relevant aspects of the query that are covered in the context
    5. Assess the overall quality, clarity, and usefulness of the answer

    Provide your evaluation with:
    - explanation: detailed analysis of how well the answer is grounded in the provided context
    - is_factual: boolean indicating whether the answer is solely based on the provided context (true) or contains external information (false)
    - is_comprehensive: boolean indicating whether the answer addresses all relevant aspects from the context
    - quality_score: overall quality score from 0-1, considering factuality, comprehensiveness, and clarity
    - improvement_suggestions: list of specific ways the answer could be improved, if any
    """

    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a critical evaluator who assesses if answers are grounded in provided context and evaluates their quality."},
            {"role": "user", "content": prompt}
        ],
        response_format=AnswerValidation,
    )
    
    return completion.choices[0].message.parsed

def improve_answer(client: OpenAI, query: str, original_answer: str, validation: AnswerValidation, formatted_context: str) -> GeneratedAnswer:
    """
    Improves an answer based on validation feedback.
    
    Args:
        client: OpenAI client instance
        query: The original user query
        original_answer: The answer that needs improvement
        validation: The validation feedback from the judge
        formatted_context: String formatted for prompt use
        
    Returns:
        GeneratedAnswer object containing the improved answer
    """
    # Format improvement suggestions
    improvement_feedback = "\n".join([f"- {suggestion}" for suggestion in validation.improvement_suggestions])
    
    factuality_issue = "" if validation.is_factual else "- The previous answer contained information not found in the context. Stick strictly to the provided context."
    comprehensiveness_issue = "" if validation.is_comprehensive else "- The previous answer missed important information from the context. Be more comprehensive."
    
    issues = "\n".join(filter(None, [factuality_issue, comprehensiveness_issue]))
    if issues:
        issues = f"Key issues to address:\n{issues}"
    
    prompt = f"""Improve the following answer to the user's query based on specific feedback and the provided context.

    User Query: {query}
    
    Original Answer (needs improvement):
    {original_answer}
    
    Validation Feedback:
    {validation.explanation}
    
    Specific improvement suggestions:
    {improvement_feedback}
    
    {issues}
    
    Context Information (use ONLY this information):
    {formatted_context}
    
    Instructions:
    1. Base your answer SOLELY on the information provided in the context chunks above
    2. Address ALL issues mentioned in the feedback
    3. Do not introduce any information not found in the context
    4. Make the answer comprehensive by covering all relevant aspects in the context
    5. Structure the answer clearly and concisely
    6. Maintain the same level of detail and depth as the original answer, just improve the accuracy and completeness
    
    Provide your response as:
    - reasoning: detailed explanation of your approach to improving the answer and how you addressed the feedback
    - final_answer: your improved, well-structured answer to the original query
    - sources_used: list of sources you referenced (from the context chunks)
    """
    
    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates improved answers based on feedback and strictly adheres to provided context."},
            {"role": "user", "content": prompt}
        ],
        response_format=GeneratedAnswer,
    )
    
    return completion.choices[0].message.parsed

if __name__ == "__main__":
    load_dotenv()

    logger.info(f"Connecting to Weaviate vector database...\n")
    weaviate_client = create_weaviate_client()
    meta_info = weaviate_client.get_meta()
    # logger.info(f"\nMetadata about the Weaviate instance: {meta_info}\n")
    logger.info(f"Connection set up.\n")

    # retrieving all document sources from the collection
    sources = get_document_sources(weaviate_client)
 
    openai_client = OpenAI()

    # Example usage
    query = "How should a ML team be structured?"
    logger.info(f"{query}\n")
    
    logger.info(f"Let me first check if the answer to your question can be found in the knowledge hub.\n")
    response = validate_query(openai_client, query, sources)
    
    if response.is_knowledge_hub_query:
        logger.info(f"I think (confidence: {response.confidence_score:.2f}) we might indeed find the answer in the KH, because {response.explanation}\n")
        
        # Rewrite query for better retrieval
        logger.info(f"But, let me first rewrite your question so I can use it to query the vector database, because you suck at writing good queries.\n")
        rewritten = rewrite_query(openai_client, query, sources)
        logger.info(f"This is the new query: {rewritten.rewritten_query}\n")
        
        # Use the rewritten query to retrieve relevant chunks
        logger.info(f"Now I will search the Weaviate vector database using 50% keyword search and 50% vector similarity search.")
        search_results = hybrid_search(weaviate_client, rewritten.rewritten_query, limit=3, alpha=0.5)
        if not search_results or search_results.objects[0].metadata.score < 0.5:
            logger.info(f"I did not get a single good match match when searching the vector database, so the answer was not in KH after all. Bye!\n")
            exit()

        for i, obj in enumerate(search_results.objects):
            print(f"\nResult {i+1}:")
            print(f"Score: {obj.metadata.score}; Explanation: {obj.metadata.explain_score}")
            print(f"Source file: {obj.properties.get('filename', 'Unknown')}\n")
            print(f"Title: {obj.properties.get('title', 'No title')}\n")
        
        # Prepare context once
        formatted_context = prepare_context_from_search_results(search_results)
        
        # Generate answer based on retrieved context
        logger.info(f"Now I'll answer your question based on the information I found:\n")
        answer = generate_answer(openai_client, query, formatted_context)
        logger.info(f"Sources used: {', '.join(answer.sources_used)}\n")
        logger.info(f"Answer: {answer.final_answer}\n")
        logger.info(f"Reasoning: {answer.reasoning}\n")
        
        # Validate the answer using LLM-as-a-judge
        logger.info(f"Before you see my answer I will let a judge verify if my answer is accurate and based solely on the knowledge hub information:\n")
        validation = validate_answer(openai_client, query, answer.final_answer, formatted_context)
        
        logger.info(f"Answer validation:\n")
        logger.info(f"Is factual (based solely on provided context): {'Yes' if validation.is_factual else 'No'}\n")
        logger.info(f"Is comprehensive: {'Yes' if validation.is_comprehensive else 'No'}\n") 
        logger.info(f"Quality score: {validation.quality_score:.2f}/1.0\n")
        
        if validation.improvement_suggestions:
            logger.info(f"Suggestions for improvement:\n")
            for i, suggestion in enumerate(validation.improvement_suggestions, 1):
                logger.info(f"{i}. {suggestion}\n")
                
        logger.info(f"Detailed evaluation: {validation.explanation}\n")
        
        # Handle case where answer needs improvement - only call when there's actual feedback
        QUALITY_THRESHOLD = 0.7
        if (validation.improvement_suggestions or 
            not validation.is_factual or 
            not validation.is_comprehensive or 
            validation.quality_score < QUALITY_THRESHOLD):
            
            logger.info(f"The answer didn't meet quality standards. Let me improve it based on the feedback.\n")
            improved_answer = improve_answer(openai_client, query, answer.final_answer, validation, formatted_context)
            logger.info(f"Sources used: {', '.join(improved_answer.sources_used)}\n")
            logger.info(f"Improved answer:\n{improved_answer.final_answer}\n")
            logger.info(f"Reasoning for improvements: {improved_answer.reasoning}\n")
    else:
        logger.info(f"I think (confidence: {response.confidence_score:.2f}) we can NOT find the answer in the KH, because {response.explanation}\n")
        logger.info("Please don't bother me with these types of questions.\n")
        # Handle rejection...

    weaviate_client.close() 