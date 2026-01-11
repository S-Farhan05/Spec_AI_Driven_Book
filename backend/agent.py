"""
RAG Agent with OpenAI Agent SDK and Qdrant Integration

This module implements a Retrieval-Augmented Generation (RAG) agent that:
- Connects to Qdrant vector database for content retrieval
- Uses OpenAI Agent SDK for intelligent response generation
- Grounds responses in retrieved book content
- Provides source attribution for all responses
"""

import os
import json
import time
import logging
import argparse
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import requests
from pydantic import BaseModel
from dotenv import load_dotenv
import hashlib
import statistics
import re
import asyncio
import random
from functools import wraps
from decouple import config

# Import OpenAI Agents SDK
from agents import Agent, Runner, function_tool ,OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import cohere

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


Key=config("OPEN_ROUTER_API_KEY")
base_url= config("OPEN_ROUTER_BASE_URL")
Client =AsyncOpenAI(api_key=Key,base_url=base_url)
Third_party_Model = OpenAIChatCompletionsModel(model="mistralai/devstral-2512:free",openai_client=Client)



class Config:
    """
    Configuration class to handle API credentials from environment
    """
    OPEN_ROUTER_API_KEY = os.getenv('OPEN_ROUTER_API_KEY')
    QDRANT_URL = os.getenv('QDRANT_URL')
    QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
    COHERE_API_KEY = os.getenv('COHERE_API_KEY')

    # Configuration defaults
    COLLECTION_NAME = os.getenv('QDRANT_COLLECTION_NAME', 'docs_embeddings')
    VALIDATION_TOP_K = int(os.getenv('VALIDATION_TOP_K', '5'))

    @classmethod
    def validate(cls) -> bool:
        """Validate that all required configuration variables are set"""
        required_vars = [
            'OPEN_ROUTER_API_KEY',
            'QDRANT_URL',
            'QDRANT_API_KEY',
            'COHERE_API_KEY'
        ]

        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)

        return len(missing_vars) == 0

    @classmethod
    def get_missing_vars(cls) -> List[str]:
        """Get list of missing required configuration variables"""
        required_vars = [
            'OPENAI_API_KEY',
            'QDRANT_URL',
            'QDRANT_API_KEY',
            'COHERE_API_KEY'
        ]

        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)

        return missing_vars


class RetrievedChunk(BaseModel):
    """
    Data model for a retrieved content chunk
    """
    chunk_id: str
    content: str
    url: str
    module: str
    section: str
    source_path: Optional[str] = None
    relevance_score: float
    token_count: int


class QueryResult(BaseModel):
    """
    Data model for query results
    """
    query_id: str
    original_query: str
    retrieved_chunks: List[RetrievedChunk]
    agent_response: Optional[str] = None
    confidence_score: Optional[float] = None
    query_time_ms: float
    retrieval_timestamp: datetime
    total_chunks_found: int = 0
    semantic_relevance_score: Optional[float] = None


class RetrievalTest(BaseModel):
    """
    Data model for validation test queries
    """
    test_id: str
    query: str
    expected_keywords: List[str]
    expected_module: str
    min_relevance_threshold: float
    test_category: str = "factual"


def setup_logging():
    """Set up logging configuration for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger.info("Logging configured successfully")


from agents import function_tool

@function_tool
def retrieve_content_from_qdrant(query: str, top_k: int = 5) -> List[RetrievedChunk]:
    """
    Retrieve relevant content from Qdrant based on the query
    """
    try:
        import requests
        import cohere

        # Initialize Cohere client for embedding generation
        co = cohere.Client(Config.COHERE_API_KEY)

        # Generate embedding for the query
        response = co.embed(
            texts=[query],
            model="embed-multilingual-v3.0",
            input_type="search_query"
        )
        query_embedding = response.embeddings[0]

        # Query Qdrant for similar content
        headers = {
            'Api-Key': Config.QDRANT_API_KEY,
            'Content-Type': 'application/json'
        }

        search_payload = {
            "vector": query_embedding,
            "limit": top_k,
            "with_payload": True,
            "with_vectors": False
        }

        response = requests.post(
            f"{Config.QDRANT_URL}/collections/{Config.COLLECTION_NAME}/points/query",
            headers=headers,
            json=search_payload
        )

        if response.status_code != 200:
            logger.error(f"Qdrant search failed: {response.status_code} - {response.text}")
            return []

        results = response.json()
        points = results.get('result', {}).get('points', [])

        # Format results
        retrieved_chunks = []
        for point in points:
            payload = point.get('payload', {})
            chunk = RetrievedChunk(
                chunk_id=str(point.get('id', '')),
                content=payload.get('content', ''),
                url=payload.get('url', ''),
                module=payload.get('module', ''),
                section=payload.get('section', ''),
                source_path=payload.get('source_path', ''),
                relevance_score=point.get('score', 0.0),
                token_count=len(payload.get('content', '').split())
            )
            retrieved_chunks.append(chunk)

        logger.info(f"Retrieved {len(retrieved_chunks)} chunks from Qdrant for query: {query[:50]}...")
        return retrieved_chunks

    except Exception as e:
        logger.error(f"Error retrieving content from Qdrant: {str(e)}")
        return []


@function_tool
def validate_content_relevance(query: str, retrieved_chunks: List[RetrievedChunk], expected_keywords: List[str]) -> float:
    """
    Validate the relevance of retrieved content to the query
    """
    try:
        relevance_score = 0.0
        if not retrieved_chunks:
            return 0.0

        # Calculate relevance based on keyword matching and average score
        total_score = 0.0
        valid_chunks = 0

        for chunk in retrieved_chunks:
            content = chunk.content.lower()
            chunk_relevance = 0.0

            # Check for expected keywords in content
            for keyword in expected_keywords:
                if keyword.lower() in content:
                    chunk_relevance += 1.0 / len(expected_keywords)

            # Combine with Qdrant relevance score
            combined_score = (chunk_relevance + chunk.relevance_score) / 2
            total_score += combined_score
            valid_chunks += 1

        if valid_chunks > 0:
            relevance_score = total_score / valid_chunks
        else:
            relevance_score = 0.0

        logger.info(f"Content relevance score calculated: {relevance_score:.3f} for query: {query[:50]}...")
        return relevance_score

    except Exception as e:
        logger.error(f"Error validating content relevance: {str(e)}")
        return 0.0


@function_tool
def generate_response_with_context(query: str, retrieved_chunks: List[RetrievedChunk]) -> str:
    """
    Generate a response based on the query and retrieved context
    """
    try:
        # Format context from retrieved chunks (internal use only)
        context_str = "\\n\\n".join([
            f"Source: {chunk.url or 'Unknown'}\\nModule: {chunk.module or 'Unknown'}\\nSection: {chunk.section or 'Unknown'}\\nContent: {chunk.content[:500]}"
            for chunk in retrieved_chunks
        ])

        # Create a system prompt that emphasizes using only the provided context
        system_prompt = "You are a helpful assistant that answers questions based only on the provided content from the humanoid robotics book. Do not use any external knowledge or make up information. If the answer is not available in the provided content, say so clearly and suggest the user ask about the humanoid robotics book content specifically. Do not mention technical terms like 'chunks', 'relevance', 'retrieval', 'sources', etc. to the user. Keep responses natural and user-friendly."

        # Create the full prompt
        full_prompt = f"{system_prompt}\\n\\nContext:\\n{context_str}\\n\\nQuestion: {query}\\n\\nAnswer:"

        # Use OpenAI to generate response (using a mock response since we can't call OpenAI directly from here)
        # In a real implementation, this would call the OpenAI API
        if len(retrieved_chunks) > 0:
            # Check if the retrieved content is actually relevant (average relevance score > 0.3)
            avg_relevance = sum(chunk.relevance_score for chunk in retrieved_chunks) / len(retrieved_chunks)

            if avg_relevance > 0.3:
                # Create a response based on the relevant context, without mentioning technical details
                response = f"Here's the answer to your question about '{query[:30]}...':\\n\\n"
                for i, chunk in enumerate(retrieved_chunks[:3]):  # Show top 3 pieces of information
                    response += f"- {chunk.content[:200]}...\\n"
            else:
                # Content retrieved but not very relevant
                response = f"I found some information related to '{query[:30]}...', but it may not fully address your specific question about humanoid robotics:\\n\\n"
                for i, chunk in enumerate(retrieved_chunks[:2]):  # Show top 2 pieces of information
                    response += f"- {chunk.content[:150]}...\\n\\n"
                response += "If you have a more specific question about the humanoid robotics book content, please try rephrasing."
        else:
            # No content retrieved
            response = f"I couldn't find any relevant information in the humanoid robotics book to answer your question about '{query}'. Please make sure your question is related to the book content about digital twins, ROS2, navigation, VLA models, or other humanoid robotics topics."

        logger.info(f"Generated response for query: {query[:50]}...")
        return response

    except Exception as e:
        logger.error(f"Error generating response with context: {str(e)}")
        return "An error occurred while generating the response."


def count_tokens_cohere(text: str) -> int:
    """
    Count tokens using Cohere's approach
    """
    if not text:
        return 0

    # Simple approach - in practice, use Cohere's tokenizer
    words = text.split()
    # Approximation: 1.3 tokens per word on average
    return int(len(words) * 1.3)


def validate_url(url: str) -> bool:
    """
    Validate URL format
    """
    if not url:
        return False

    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None


# Create the main RAG Agent
rag_agent = Agent(
    name="Humanoid Robotics Book Assistant",
    instructions="You are an assistant that answers questions based on content from the humanoid robotics book. Use the provided information to generate accurate responses. Do not mention technical terms like 'chunks', 'retrieval', 'database', 'tools', 'validation', 'relevance', etc. Keep responses natural and user-friendly. Focus on providing helpful answers about humanoid robotics topics.",
    tools=[retrieve_content_from_qdrant, validate_content_relevance, generate_response_with_context],
    model=Third_party_Model,
)


def query_agent(user_query: str, top_k: int = 5, expected_keywords: List[str] = None) -> QueryResult:
    """
    Main function to query the RAG agent
    """
    if expected_keywords is None:
        expected_keywords = []

    start_time = time.time()

    try:
        # Use the OpenAI Agent SDK to run the agent with the query
        result = Runner.run_sync(
            rag_agent,
            f"Retrieve and analyze information about: {user_query}",
            context={
                "top_k": top_k,
                "expected_keywords": expected_keywords
            }
        )

        # Process the result to create a QueryResult object
        # This is a simplified version - in practice, you'd parse the agent's structured response
        retrieved_chunks = []  # Would be extracted from agent response
        agent_response = result.final_output
        confidence_score = 0.8  # Placeholder - would come from validation

        query_result = QueryResult(
            query_id=f"query_{int(time.time())}_{hashlib.md5(user_query.encode()).hexdigest()[:8]}",
            original_query=user_query,
            retrieved_chunks=[],  # Would populate from agent response
            agent_response=agent_response,
            confidence_score=confidence_score,
            query_time_ms=(time.time() - start_time) * 1000,
            retrieval_timestamp=datetime.now(),
            total_chunks_found=len(retrieved_chunks),
            semantic_relevance_score=confidence_score
        )

        logger.info(f"Query processed in {(time.time() - start_time)*1000:.2f}ms")
        return query_result

    except Exception as e:
        logger.error(f"Error querying RAG agent: {str(e)}")
        # Return an empty result in case of error
        query_result = QueryResult(
            query_id=f"error_{int(time.time())}",
            original_query=user_query,
            retrieved_chunks=[],
            agent_response="An error occurred while processing your request.",
            confidence_score=0.0,
            query_time_ms=(time.time() - start_time) * 1000,
            retrieval_timestamp=datetime.now(),
            total_chunks_found=0,
            semantic_relevance_score=0.0
        )
        return query_result


def validate_qdrant_connection() -> Dict[str, Any]:
    """
    Validate connection to Qdrant
    """
    try:
        import requests

        headers = {
            'Api-Key': Config.QDRANT_API_KEY,
            'Content-Type': 'application/json'
        }

        response = requests.get(
            f"{Config.QDRANT_URL}/collections/{Config.COLLECTION_NAME}",
            headers=headers
        )

        if response.status_code == 200:
            collection_info = response.json()
            points_count = collection_info.get('result', {}).get('points_count', 0)

            result = {
                "validation_passed": True,
                "collection_exists": True,
                "points_count": points_count,
                "message": f"Successfully connected to Qdrant collection '{Config.COLLECTION_NAME}' with {points_count} vectors"
            }
            logger.info(result["message"])
            return result
        else:
            result = {
                "validation_passed": False,
                "collection_exists": False,
                "points_count": 0,
                "message": f"Failed to connect to Qdrant: {response.status_code}"
            }
            logger.error(result["message"])
            return result

    except Exception as e:
        result = {
            "validation_passed": False,
            "collection_exists": False,
            "points_count": 0,
            "message": f"Error connecting to Qdrant: {str(e)}"
        }
        logger.error(result["message"])
        return result


def run_comprehensive_validation() -> Dict[str, Any]:
    """
    Run comprehensive validation of the RAG system
    """
    logger.info("Starting comprehensive RAG validation...")

    start_time = time.time()

    # Test connectivity
    connectivity_result = validate_qdrant_connection()

    # Test retrieval with sample queries
    sample_queries = [
        {"query": "What is digital twin simulation?", "keywords": ["digital twin", "simulation"]},
        {"query": "How does ROS2 navigation work?", "keywords": ["ROS2", "navigation"]},
        {"query": "What are VLA models?", "keywords": ["VLA", "models"]}
    ]

    total_queries = len(sample_queries)
    successful_queries = 0

    for test_query in sample_queries:
        try:
            result = query_agent(test_query["query"], expected_keywords=test_query["keywords"])
            if result.agent_response and "error" not in result.agent_response.lower():
                successful_queries += 1
        except:
            pass  # Query failed

    success_rate = (successful_queries / total_queries) * 100 if total_queries > 0 else 0
    retrieval_success = success_rate >= 60  # Require 60% success rate

    validation_result = {
        "validation_suite_passed": connectivity_result["validation_passed"] and retrieval_success,
        "connectivity_validation": connectivity_result,
        "retrieval_validation": {
            "total_queries": total_queries,
            "successful_queries": successful_queries,
            "success_rate": success_rate,
            "validation_passed": retrieval_success
        },
        "total_duration_ms": (time.time() - start_time) * 1000,
        "timestamp": datetime.now().isoformat()
    }

    if validation_result["validation_suite_passed"]:
        logger.info("✓ Comprehensive RAG validation PASSED")
    else:
        logger.warning("✗ Comprehensive RAG validation FAILED")

    return validation_result


def interactive_query_mode():
    """
    Interactive mode for querying the RAG agent
    """
    logger.info("Starting interactive query mode...")
    print("\\nRAG Agent Interactive Mode")
    print("===========================")
    print("Ask questions about your book content!")
    print("Type 'quit' or 'exit' to end the session\\n")

    while True:
        try:
            user_query = input("[Q] Enter your question: ").strip()

            if user_query.lower() in ['quit', 'exit', 'q']:
                print("[Goodbye!]")
                break

            if not user_query:
                print("[Please enter a valid question.]")
                continue

            print(f"\\n[Processing: '{user_query}']")

            # Query the agent
            result = query_agent(user_query)

            print(f"\\n[Answer: {result.agent_response}]")
            print(f"[Confidence: {result.confidence_score:.3f}]")
            print(f"[Retrieved {result.total_chunks_found} chunks]")

            if result.retrieved_chunks:
                print("\\n[Top Sources:]")
                for i, chunk in enumerate(result.retrieved_chunks[:3]):  # Show top 3
                    print(f"- {chunk.module}: {chunk.section} (Score: {chunk.relevance_score:.3f})")

        except KeyboardInterrupt:
            print("\\n\\n[Session interrupted. Goodbye!]")
            break
        except Exception as e:
            logger.error(f"Error in interactive mode: {str(e)}")
            print(f"[An error occurred: {str(e)}]")


def create_command_line_interface():
    """
    Create command-line interface for the RAG agent
    """
    logger.info("Setting up command-line interface...")

    parser = argparse.ArgumentParser(
        description="RAG Agent with OpenAI Agent SDK and Qdrant Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python agent.py --query "What is digital twin simulation?"  # Ask a question
  python agent.py --validate                                # Run validation tests
  python agent.py --interactive                             # Interactive mode
        """
    )

    parser.add_argument(
        '--query',
        type=str,
        help='Ask a specific question to the RAG agent'
    )

    parser.add_argument(
        '--validate',
        action='store_true',
        help='Run comprehensive validation tests'
    )

    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode to ask questions'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    return parser


def main_execution_function():
    """
    Main execution function with proper argument handling
    """
    logger.info("Starting RAG Agent with OpenAI Agent SDK and Qdrant Integration...")

    # Create argument parser
    parser = create_command_line_interface()
    args = parser.parse_args()

    # Set logging level based on verbose flag
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Validate configuration
    if not Config.validate():
        missing_vars = Config.get_missing_vars()
        logger.error(f"Missing required configuration variables: {missing_vars}")
        print(f"Error: Missing required configuration variables: {missing_vars}")
        return

    try:
        if args.validate:
            logger.info("Running comprehensive validation suite...")
            result = run_comprehensive_validation()

            print(f"\\nValidation Summary:")
            print(f"- Overall Status: {'PASSED' if result['validation_suite_passed'] else 'FAILED'}")
            print(f"- Connectivity: {'PASSED' if result['connectivity_validation']['validation_passed'] else 'FAILED'}")
            print(f"- Retrieval: {'PASSED' if result['retrieval_validation']['validation_passed'] else 'FAILED'}")
            print(f"- Success Rate: {result['retrieval_validation']['success_rate']:.1f}%")
            print(f"- Total Duration: {result['total_duration_ms']:.2f}ms")

            return result

        elif args.query:
            logger.info(f"Processing query: {args.query}")
            result = query_agent(args.query)

            print(f"\\nAnswer: {result.agent_response}")
            print(f"Confidence: {result.confidence_score:.3f}")
            print(f"Retrieved {result.total_chunks_found} chunks")

            if result.retrieved_chunks:
                print("\\nTop Sources:")
                for i, chunk in enumerate(result.retrieved_chunks[:3]):  # Show top 3
                    print(f"- {chunk.module}: {chunk.section} (Score: {chunk.relevance_score:.3f})")

            return result

        elif args.interactive:
            interactive_query_mode()

        else:
            # Default behavior - show help
            parser.print_help()

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main_execution_function()