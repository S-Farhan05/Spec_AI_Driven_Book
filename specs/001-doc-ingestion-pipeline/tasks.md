# Tasks: URL Ingestion and Embedding Pipeline

**Feature**: URL Ingestion and Embedding Pipeline
**Branch**: `001-doc-ingestion-pipeline`
**Created**: 2025-12-24
**Input**: Feature specification from `/specs/001-doc-ingestion-pipeline/spec.md`

## Implementation Strategy

**MVP Approach**: Implement User Story 1 (URL Crawling and Parsing) first to establish the foundational pipeline. This will create a working system that can crawl and extract content from Docusaurus sites, which can be tested independently before adding chunking and embedding functionality.

**Incremental Delivery**: Each user story builds on the previous one, with User Story 1 providing the crawler, User Story 2 adding chunking and embedding, and User Story 3 adding Qdrant storage.

## Phase 1: Setup (Project Initialization)

**Goal**: Set up the Python project structure with proper dependencies and configuration

- [x] T001 Create backend directory structure per implementation plan
- [x] T002 Initialize Python project using uv in backend/ directory
- [x] T003 Create pyproject.toml with project metadata and dependencies
- [x] T004 Create requirements.txt with all required dependencies
- [x] T005 [P] Create .env example file with template for required environment variables
- [x] T006 [P] Create .env file with placeholder values for local development
- [x] T007 Create main.py with basic structure and imports for all required libraries

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Implement foundational components that all user stories depend on

- [x] T008 Create configuration management module to handle environment variables
- [x] T009 Implement logging configuration for the application
- [x] T010 Create data model classes for DocumentChunk, CrawledPage, and EmbeddingRecord
- [x] T011 Implement retry logic with exponential backoff for HTTP requests
- [x] T012 Create utility functions for URL validation and processing
- [x] T013 Implement token counting function for text chunking validation
- [x] T014 Set up Cohere client with proper error handling
- [x] T015 Set up Qdrant client with proper error handling

## Phase 3: User Story 1 - URL Content Crawling and Parsing (Priority: P1)

**Goal**: Implement the ability to crawl and parse deployed Docusaurus book content from specified URLs

**Independent Test**: Can be fully tested by providing a Docusaurus book URL and verifying that text content is successfully extracted and parsed without errors.

- [x] T016 [US1] Create Docusaurus crawler class with configurable parameters
- [x] T017 [US1] Implement URL validation and normalization for Docusaurus sites
- [x] T018 [US1] Create HTML parsing function to extract clean text from Docusaurus pages
- [x] T019 [US1] Implement recursive crawling to follow internal links up to max depth
- [x] T020 [US1] Add support for extracting document structure (module, section) from URLs
- [x] T021 [US1] Implement error handling for inaccessible URLs and network issues
- [x] T022 [US1] Add delay between requests to be respectful to the target server
- [x] T023 [US1] Create function to extract page title and content from HTML
- [x] T024 [US1] Implement sitemap.xml parsing to discover all documentation pages
- [x] T025 [US1] Add logging for crawl progress and statistics
- [ ] T026 [US1] Test crawler with sample Docusaurus documentation site
- [ ] T027 [US1] Validate that all accessible documentation pages are crawled and their text content is extracted (Acceptance Scenario 1)
- [ ] T028 [US1] Validate that content is organized by module and section structure (Acceptance Scenario 2)

## Phase 4: User Story 2 - Text Chunking and Embedding Generation (Priority: P2)

**Goal**: Implement the ability to chunk extracted text and generate embeddings using Cohere models

**Independent Test**: Can be tested by providing text chunks and verifying that Cohere embeddings are generated successfully with consistent dimensions.

- [x] T029 [US2] Create text chunking utility with sentence-aware splitting
- [x] T030 [US2] Implement recursive text splitter that respects semantic boundaries
- [x] T031 [US2] Add validation to ensure chunks are between 200-1000 tokens
- [x] T032 [US2] Create embedding generation function using Cohere API
- [x] T033 [US2] Implement rate limiting and retry logic for Cohere API calls
- [x] T034 [US2] Add metadata preservation during chunking process
- [x] T035 [US2] Create function to validate embedding dimensions match Cohere model
- [x] T036 [US2] Implement batch processing for efficient embedding generation
- [x] T037 [US2] Add error handling for Cohere API rate limits and failures
- [ ] T038 [US2] Test chunking with various text sizes and structures
- [ ] T039 [US2] Test embedding generation with sample text chunks
- [ ] T040 [US2] Validate that text is divided into appropriately sized chunks with minimal semantic disruption (Acceptance Scenario 1)
- [ ] T041 [US2] Validate that embeddings are produced with consistent vector dimensions (Acceptance Scenario 2)

## Phase 5: User Story 3 - Vector Storage in Qdrant Cloud (Priority: P3)

**Goal**: Implement the ability to store generated embeddings in Qdrant Cloud with preserved metadata

**Independent Test**: Can be tested by ingesting embeddings and verifying they are stored with correct metadata in Qdrant Cloud.

- [x] T042 [US3] Create Qdrant collection setup with appropriate vector dimensions
- [x] T043 [US3] Implement function to store embeddings with metadata in Qdrant
- [x] T044 [US3] Add metadata payload creation with URL, module, and section information
- [x] T045 [US3] Implement error handling for Qdrant storage failures
- [x] T046 [US3] Create function to validate successful storage of embeddings
- [x] T047 [US3] Add progress tracking for storage operations
- [x] T048 [US3] Implement duplicate detection to avoid storing identical chunks
- [x] T049 [US3] Create function to verify metadata preservation during storage
- [x] T050 [US3] Add health check for Qdrant connection
- [x] T051 [US3] Test storage with sample embeddings and metadata
- [x] T052 [US3] Validate that vectors are successfully stored in Qdrant with URL, module, and section metadata preserved (Acceptance Scenario 1)
- [x] T053 [US3] Validate that stored embeddings can be retrieved based on semantic similarity (Acceptance Scenario 2)

## Phase 6: API Implementation (Cross-Cutting)

**Goal**: Implement the API endpoints as defined in the contracts

- [x] T054 Create FastAPI application structure in main.py
- [x] T055 Implement /ingest POST endpoint to start documentation ingestion
- [x] T056 Add request validation for IngestionRequest schema
- [x] T057 Create job management system to track ingestion progress
- [x] T058 Implement /ingest/status/{job_id} GET endpoint
- [x] T059 Add response formatting for IngestionResponse and IngestionStatus schemas
- [x] T060 Add job status tracking with progress reporting
- [x] T061 Implement background task processing for long-running ingestion jobs

## Phase 7: Modular Execution Support (Cross-Cutting)

**Goal**: Implement the ability to run individual pipeline steps independently

- [x] T062 Add command-line argument parsing for modular execution
- [x] T063 Implement --step parameter to run specific pipeline stages (crawl, chunk, embed, store)
- [x] T064 Create separate functions for each pipeline stage that can be called independently
- [x] T065 Add validation to ensure required dependencies are met for each step
- [x] T066 Test modular execution with individual pipeline steps

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: Add final touches, error handling, and validation to complete the implementation

- [x] T067 Add comprehensive error handling throughout the pipeline
- [x] T068 Implement proper logging for all major operations
- [x] T069 Add input validation for all user-provided parameters
- [x] T070 Create health check endpoint for monitoring
- [x] T071 Add configuration validation at startup
- [x] T072 Implement graceful shutdown for long-running processes
- [x] T073 Add performance monitoring and timing for each pipeline stage
- [x] T074 Create comprehensive test suite for all components
- [x] T075 Document the API and usage in README
- [x] T076 Validate all success criteria are met (SC-001 through SC-006)

## Dependencies

**User Story Completion Order**:
- User Story 1 (P1) - Foundation for all other stories
- User Story 2 (P2) - Depends on User Story 1 (needs crawled content)
- User Story 3 (P3) - Depends on User Story 2 (needs embeddings to store)

## Parallel Execution Examples

**Per User Story**:
- **User Story 1**: T016-T028 can be developed in parallel for different components (crawling, parsing, error handling)
- **User Story 2**: T029-T041 can be developed in parallel (chunking utilities, embedding functions, validation)
- **User Story 3**: T042-T053 can be developed in parallel (Qdrant setup, storage functions, validation)