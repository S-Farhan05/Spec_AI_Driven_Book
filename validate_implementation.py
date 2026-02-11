"""
Validation script to check if all RAG Chatbot API Integration tasks have been completed and chnaged validation
"""
import os
import sys
from pathlib import Path

def validate_implementation():
    """Validate that all required files and functionality have been implemented"""

    print("Validating RAG Chatbot API Integration Implementation...")
    print("="*60)

    validation_results = []

    # Phase 1: Setup validation
    print("\nPhase 1: Setup Validation")
    print("-" * 30)

    # T001: backend directory exists
    backend_exists = os.path.exists("backend")
    validation_results.append(("T001: Create backend directory structure", backend_exists))
    print(f"  {'[OK]' if backend_exists else '[KO]'} Backend directory exists: {backend_exists}")

    # T002: Chatbot component directory exists
    chatbot_dir_exists = os.path.exists("book_frontend/src/components/Chatbot")
    validation_results.append(("T002: Create Chatbot component directory", chatbot_dir_exists))
    print(f"  {'[OK]' if chatbot_dir_exists else '[KO]'} Chatbot component directory exists: {chatbot_dir_exists}")

    # T003/T005: requirements.txt with FastAPI dependencies
    req_file = Path("backend/requirements.txt")
    has_fastapi_req = req_file.exists() and "fastapi" in req_file.read_text().lower()
    validation_results.append(("T003/T005: FastAPI dependencies in requirements.txt", has_fastapi_req))
    print(f"  {'[OK]' if has_fastapi_req else '[KO]'} FastAPI in requirements.txt: {has_fastapi_req}")

    # T004: api.py with FastAPI app
    api_file = Path("backend/api.py")
    has_fastapi_app = api_file.exists() and "fastapi" in api_file.read_text().lower()
    validation_results.append(("T004: Create api.py with FastAPI app", has_fastapi_app))
    print(f"  {'[OK]' if has_fastapi_app else '[KO]'} api.py with FastAPI app: {has_fastapi_app}")

    # Phase 2: Foundational validation
    print("\nPhase 2: Foundational Validation")
    print("-" * 35)

    # T006: agent.py exists (already existed)
    agent_exists = os.path.exists("backend/agent.py")
    validation_results.append(("T006: RAG agent interface exists", agent_exists))
    print(f"  {'[OK]' if agent_exists else '[KO]'} agent.py exists: {agent_exists}")

    # T007: Error handling in api.py
    api_content = api_file.read_text() if api_file.exists() else ""
    has_error_handling = "exception_handler" in api_content.lower() or "try:" in api_content
    validation_results.append(("T007: Error handling middleware", has_error_handling))
    print(f"  {'[OK]' if has_error_handling else '[KO]'} Error handling in API: {has_error_handling}")

    # T008/T009: Models directory and files
    models_dir = os.path.exists("backend/models")
    chat_model = os.path.exists("backend/models/chat.py")
    validation_results.append(("T008/T009: API response models", models_dir and chat_model))
    print(f"  {'[OK]' if (models_dir and chat_model) else '[KO]'} Models directory and chat models: {models_dir and chat_model}")

    # T010: Health endpoint
    has_health = "health" in api_content.lower() and "get" in api_content.lower()
    validation_results.append(("T010: Health check endpoint", has_health))
    print(f"  {'[OK]' if has_health else '[KO]'} Health check endpoint: {has_health}")

    # T011: CORS configuration
    has_cors = "cors" in api_content.lower() or "CORSMiddleware" in api_content
    validation_results.append(("T011: CORS configuration", has_cors))
    print(f"  {'[OK]' if has_cors else '[KO]'} CORS configuration: {has_cors}")

    # Phase 3: User Story 1 validation
    print("\nPhase 3: User Story 1 Validation")
    print("-" * 35)

    # T012-T018: Chat endpoint and frontend component
    has_chat_endpoint = "post" in api_content.lower() and "/chat" in api_content
    validation_results.append(("T012-T014: Chat endpoint with RAG agent", has_chat_endpoint))
    print(f"  {'[OK]' if has_chat_endpoint else '[KO]'} Chat endpoint with RAG agent: {has_chat_endpoint}")

    chatbot_jsx = os.path.exists("book_frontend/src/components/Chatbot/Chatbot.jsx")
    validation_results.append(("T015: Frontend Chatbot component", chatbot_jsx))
    print(f"  {'[OK]' if chatbot_jsx else '[KO]'} Chatbot.jsx component: {chatbot_jsx}")

    chatbot_css = os.path.exists("book_frontend/src/components/Chatbot/Chatbot.css")
    validation_results.append(("T018: Chatbot styling", chatbot_css))
    print(f"  {'[OK]' if chatbot_css else '[KO]'} Chatbot CSS: {chatbot_css}")

    api_service = os.path.exists("book_frontend/src/services/api.js")
    validation_results.append(("T016: API communication service", api_service))
    print(f"  {'[OK]' if api_service else '[KO]'} API service: {api_service}")

    # Phase 4: User Story 2 validation
    print("\nPhase 4: User Story 2 Validation")
    print("-" * 35)

    # Check for source references and confidence in responses
    has_sources = "sources" in api_content or "sources" in api_file.read_text()
    has_confidence = "confidence" in api_content or "confidence" in api_file.read_text()
    validation_results.append(("T019-T024: Source references and confidence", has_sources and has_confidence))
    print(f"  {'[OK]' if (has_sources and has_confidence) else '[KO]'} Source references and confidence: {has_sources and has_confidence}")

    # Phase 5: User Story 3 validation
    print("\nPhase 5: User Story 3 Validation")
    print("-" * 35)

    # Check for timeout handling
    has_timeout = "timeout" in api_content or "TimeoutError" in api_content
    validation_results.append(("T025: Timeout handling", has_timeout))
    print(f"  {'[OK]' if has_timeout else '[KO]'} Timeout handling: {has_timeout}")

    # Check for retry logic in frontend
    chatbot_content = Path("book_frontend/src/components/Chatbot/Chatbot.jsx").read_text() if chatbot_jsx else ""
    has_retry = "retry" in chatbot_content.lower() or "fetchwithretry" in chatbot_content.lower()
    validation_results.append(("T028-T030: Retry logic and error handling", has_retry))
    print(f"  {'[OK]' if has_retry else '[KO]'} Retry logic in frontend: {has_retry}")

    # Phase 6: Polish validation
    print("\nPhase 6: Polish Validation")
    print("-" * 25)

    # T031: Docusaurus integration
    docusaurus_config = Path("book_frontend/docusaurus.config.ts")
    has_chatbot_plugin = docusaurus_config.exists() and ("chatbot" in docusaurus_config.read_text().lower() or
                                                        "LayoutWrapper" in os.listdir("book_frontend/src/theme/")) if os.path.exists("book_frontend/src/theme/") else False
    validation_results.append(("T031: Docusaurus integration", has_chatbot_plugin))
    print(f"  {'[OK]' if has_chatbot_plugin else '[KO]'} Docusaurus integration: {has_chatbot_plugin}")

    # T032: Documentation
    has_docs = os.path.exists("backend/API_DOCUMENTATION.md") or os.path.exists("backend/README.md")
    validation_results.append(("T032: API documentation", has_docs))
    print(f"  {'[OK]' if has_docs else '[KO]'} API documentation: {has_docs}")

    # T034: Loading indicators
    has_loading = "loading" in chatbot_content.lower() and "spinner" in chatbot_content.lower()
    validation_results.append(("T034: Loading indicators", has_loading))
    print(f"  {'[OK]' if has_loading else '[KO]'} Loading indicators: {has_loading}")

    # T035: Session management
    has_session = "session" in chatbot_content.lower() and "localStorage" in chatbot_content.lower()
    validation_results.append(("T035: Session management", has_session))
    print(f"  {'[OK]' if has_session else '[KO]'} Session management: {has_session}")

    # Summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)

    total_tasks = len(validation_results)
    completed_tasks = sum(1 for _, result in validation_results if result)

    print(f"\nTotal tasks validated: {total_tasks}")
    print(f"Completed tasks: {completed_tasks}")
    print(f"Completion rate: {completed_tasks/total_tasks*100:.1f}%")

    print(f"\n{'[OK] SUCCESS' if completed_tasks == total_tasks else '[WARN] PARTIAL'}: Implementation {'fully' if completed_tasks == total_tasks else 'partially'} validated")

    if completed_tasks < total_tasks:
        print("\nIncomplete tasks:")
        for task, result in validation_results:
            if not result:
                print(f"  - {task}")

    return completed_tasks == total_tasks

if __name__ == "__main__":
    success = validate_implementation()
    if success:
        print("\n🎉 All implementation validation checks passed!")
        sys.exit(0)
    else:
        print("\n[WARN] Some validation checks failed!")
        sys.exit(1)