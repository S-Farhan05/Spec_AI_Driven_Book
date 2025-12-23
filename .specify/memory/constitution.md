<!--
Sync Impact Report:
Version change: N/A -> 1.0.0
Added sections: All principles and sections specific to Physical AI & Humanoid Robotics Book
Removed sections: Template placeholder tokens
Modified principles: None (new constitution)
Templates requiring updates:
- .specify/templates/plan-template.md ✅ will automatically adapt to new constitution in Constitution Check section
Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics Book Constitution

## Core Principles

### Spec-Driven Development
All content creation follows Spec-Kit Plus methodology with formal specifications before implementation; Every chapter/section must have clear acceptance criteria and verification steps before publication

### Docusaurus-Only Markdown Standard
All content must be written in Docusaurus-compatible Markdown format; No proprietary formats allowed; Content must build cleanly with Docusaurus static site generator

### Source-Backed Claims (NON-NEGOTIABLE)
Every factual claim must be backed by verifiable sources in APA format; At least 40% of sources must be peer-reviewed academic publications; Zero tolerance for plagiarism or hallucinated content

### Grounded RAG Implementation
RAG chatbot responses must be strictly grounded in indexed book content; Responses must cite specific chapters/pages; No hallucination of information outside the book

### Technical Standards Compliance
Content must cover specified technologies: ROS 2, Gazebo, Unity, NVIDIA Isaac stack, Vision-Language-Action pipelines; Autonomous humanoid capstone project must be included

### Content Scope and Quality
Book must be 8,000-12,000 words with minimum 20 real sources; Content must address Physical AI & Embodied Intelligence concepts comprehensively

## Technical Implementation Requirements

RAG system using OpenAI Agents/ChatKit + FastAPI, Neon Postgres + Qdrant backend; Deployed to GitHub Pages; Embedded in Docusaurus frontend

## Quality Assurance and Validation

Clean Docusaurus build required; Verifiable content through citations; Citation-aware RAG responses that reference specific sources

## Governance

Constitution supersedes all other practices; All content must comply with source-backing requirements; Book structure must follow formal specifications; RAG implementation must pass grounding validation tests

**Version**: 1.0.0 | **Ratified**: 2025-12-22 | **Last Amended**: 2025-12-22
