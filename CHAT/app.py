# file re-runs on every change, so make sure stuff is not re-initted
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from time import sleep
import html

from chat import (
    prepare_context_from_search_results,
    validate_query, 
    rewrite_query, 
    generate_answer,
    validate_answer,
    improve_answer
)
from create_weaviate_collection import create_weaviate_client
from utils.search import get_document_sources, hybrid_search

# Constants
MAX_RESULTS = 3
QUALITY_THRESHOLD = 0.7

def create_collapsible_box(summary, content, add_styling=True):
    """Create a collapsible HTML box that works inside st.status blocks.
    
    Args:
        summary: Text to show in the clickable header
        content: Content to display when expanded (can be text, HTML, or any string)
        add_styling: Whether to include CSS styling (set to False if styling added elsewhere)
    
    Returns:
        HTML string ready to be displayed with st.markdown
    """
    html = ""
    
    # Add styling only if requested (to avoid duplicate styles)
    if add_styling:
        html += """
            <style>
            .details-box {
                margin: 10px 0;
                padding: 10px;
                border-radius: 4px;
                background-color: #f0f2f6;
            }
            .details-box summary {
                cursor: pointer;
                color: #0f52ba;
                font-weight: 500;
            }
            .details-box summary:hover {
                color: #1e90ff;
            }
            </style>
        """
    
    # Add the actual collapsible element - removed <pre> tags to allow HTML rendering
    html += f"""
        <div class="details-box">
            <details>
                <summary>{summary}</summary>
                <div>{content}</div>
            </details>
        </div>
    """
    
    return html

def create_thinking_message(message):
    """Create a styled message to indicate the LLM is thinking.
    
    Args:
        message: Text content to display
    
    Returns:
        HTML string with styled thinking message
    """
    html = f"""
        <style>
        .thinking-message {{
            padding: 8px 12px;
            border-left: 3px solid #2e6fdb;
            background-color: #f8f9fa;
            margin: 8px 0;
            font-style: italic;
            color: #555;
        }}
        </style>
        <div class="thinking-message">💭 {message}</div>
    """
    
    return html

st.title("📚 Knowledge Hub Search")

# init messages in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# display all messages in the state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask anything about our knowdledge hub"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        # prompt = "How should a ML team be structued?"
        st.markdown(prompt)

    final_answer = ""
    with st.status("Thinking", expanded=True) as status:
        st.markdown(create_thinking_message("Let me first check if the answer to your question can be found in the knowledge hub."), unsafe_allow_html=True)
        st.markdown(create_thinking_message("To do that I will gather some metadata about the KH from our database."), unsafe_allow_html=True)

        load_dotenv() 
        st.write("Connecting to Weaviate vector database...")
        weaviate_client = create_weaviate_client()
        meta_info = weaviate_client.get_meta()
        st.markdown(create_collapsible_box("Metadata about the Weaviate instance", str(meta_info)), unsafe_allow_html=True)
        st.write("Connection set up.")
        st.write("Get all page titles from the KH")
        sources = get_document_sources(weaviate_client)
        st.markdown(create_collapsible_box("Page titles from KH", html.escape(str(sources))), unsafe_allow_html=True)

        openai_client = OpenAI()
        response = validate_query(openai_client, prompt, sources)

        if response.is_knowledge_hub_query:
            st.markdown(create_thinking_message(f"I think we might indeed find the answer in the KH (confidence: {response.confidence_score:.2f})"), unsafe_allow_html=True)
            st.markdown(create_collapsible_box("Reasoning", html.escape(response.explanation).replace('\n', ' ')), unsafe_allow_html=True)

            st.markdown(create_thinking_message(f"But, let me first rewrite your question so I can use it to query the vector database, because you suck at writing good queries."), unsafe_allow_html=True)
            rewritten = rewrite_query(openai_client, prompt, sources)
            st.write(f"New query: {rewritten.rewritten_query}")

            st.markdown(create_thinking_message(f"Now I will search the Weaviate vector database using 50% keyword search and 50% vector similarity search."), unsafe_allow_html=True)
            search_results = hybrid_search(weaviate_client, rewritten.rewritten_query, limit=3, alpha=0.5)

            results_str = ""
            for i, obj in enumerate(search_results.objects):
                results_str += f"<div style='margin-bottom: 15px; padding: 10px; border-left: 3px solid #2e6fdb; background-color: #f8f9fa;'>"
                results_str += f"<strong>Result {i+1}</strong><br>"
                results_str += f"<strong>Score:</strong> {html.escape(str(obj.metadata.score))}<br>"
                results_str += f"<strong>Source:</strong> {html.escape(obj.properties.get('filename', 'Unknown'))}<br>"
                results_str += f"<strong>Title:</strong> {html.escape(obj.properties.get('title', 'No title'))}<br>"
                results_str += f"<strong>Text:</strong> {html.escape(obj.properties.get('text', '')).replace('\n', ' ')}<br>"
                results_str += "</div>"
            
            
            # Use unsafe_allow_html since we're using HTML formatting
            st.markdown(create_collapsible_box("Search Results", results_str, add_styling=True), unsafe_allow_html=True)

            if not search_results or search_results.objects[0].metadata.score < 0.5:
                st.markdown(create_thinking_message(f"I did not get a single good match when searching the vector database, so the answer was not in KH after all. Bye!"), unsafe_allow_html=True)
                exit()
            
            formatted_context = prepare_context_from_search_results(search_results)

            st.markdown(create_thinking_message(f"I'll now think of an answer your question based on the information I found:"), unsafe_allow_html=True)
            answer = generate_answer(openai_client, prompt, formatted_context)
            st.markdown(create_collapsible_box("Sources used", html.escape(str(answer.sources_used)).replace('\n', ' '), add_styling=True), unsafe_allow_html=True)
            st.markdown(create_collapsible_box("Reasoning", html.escape(answer.reasoning).replace('\n', ' '), add_styling=True), unsafe_allow_html=True)
            
            # Validate the answer using LLM-as-a-judge
            st.markdown(create_thinking_message(f"Before you see my answer I will let a independent judge verify if my answer is accurate and based solely on the knowledge hub information:"), unsafe_allow_html=True)
            validation = validate_answer(openai_client, prompt, answer.final_answer, formatted_context)
            ans_validation_str = f"Is factual (based solely on provided context): {'Yes' if validation.is_factual else 'No'}\nIs comprehensive: {'Yes' if validation.is_comprehensive else 'No'}\nQuality score: {validation.quality_score:.2f}/1.0\n"
            st.markdown(create_collapsible_box("Answer validation", html.escape(ans_validation_str).replace('\n', '<br>'), add_styling=True), unsafe_allow_html=True)
            st.markdown(create_collapsible_box("Detailed evaluation", html.escape(validation.explanation).replace('\n', '<br>'), add_styling=True), unsafe_allow_html=True)

            QUALITY_THRESHOLD = 0.7
            if (not validation.is_factual or 
                not validation.is_comprehensive or 
                validation.quality_score < QUALITY_THRESHOLD):

                st.markdown(create_thinking_message(f"The answer didn't meet quality standards. Let me improve it based on the feedback."), unsafe_allow_html=True)

                if validation.improvement_suggestions:
                    improvements_str = f""
                    for i, suggestion in enumerate(validation.improvement_suggestions, 1):
                        improvements_str = f"{i}. {suggestion}\n"

                st.markdown(create_collapsible_box("Suggested improvements", html.escape(improvements_str).replace('\n', '<br>'), add_styling=True), unsafe_allow_html=True)
                improved_answer = improve_answer(openai_client, prompt, answer.final_answer, validation, formatted_context)
                st.markdown(create_collapsible_box("Sources used", html.escape(str(improved_answer.sources_used)).replace('\n', ' '), add_styling=True), unsafe_allow_html=True)
                st.markdown(create_collapsible_box("Reasoning for improvements", html.escape(improved_answer.reasoning).replace('\n', ' '), add_styling=True), unsafe_allow_html=True)
                st.markdown(create_thinking_message(f"Here is my answer:"), unsafe_allow_html=True)
                final_answer = improved_answer.final_answer
            else:
                st.markdown(create_thinking_message(f"The answer meets quality standards."), unsafe_allow_html=True)
                st.markdown(create_thinking_message(f"Here is my answer:"), unsafe_allow_html=True)
                final_answer = answer.final_answer

        else:
            st.markdown(create_collapsible_box("Reasoning", html.escape(response.explanation).replace('\n', ' ')), unsafe_allow_html=True)
            final_answer = f"I think  we can NOT find the answer in the KH (confidence: {response.confidence_score:.2f})"

        weaviate_client.close() 

    with st.chat_message("assistant"):
        st.markdown(final_answer)