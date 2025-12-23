# Data Model: Isaac Module - The AI-Robot Brain (NVIDIA Isaac)

**Feature**: Isaac Module | **Date**: 2025-12-23 | **Spec**: [specs/3-isaac-module/spec.md](../specs/3-isaac-module/spec.md)

## Overview

This document defines the data model for the Isaac Module content. Since this is a documentation module rather than a software application, the data model focuses on content structure and relationships.

## Content Entities

### 1. Chapter Entity

**Name**: Chapter
**Description**: A single chapter in the Isaac Module
**Fields**:
- id: string (unique identifier, e.g., "chapter-1-ai-brain")
- title: string (chapter title)
- content: string (Markdown content)
- order: integer (chapter sequence number)
- learningObjectives: array of strings (what students should learn)
- prerequisites: array of strings (what students need to know)
- duration: integer (estimated reading time in minutes)
- exercises: array of Exercise entities

**Validation Rules**:
- id must be unique across all chapters
- order must be sequential (1-6 for main chapters)
- title must be 10-100 characters
- content must follow Docusaurus-compatible Markdown format

### 2. Exercise Entity

**Name**: Exercise
**Description**: A practice exercise within a chapter or practice section
**Fields**:
- id: string (unique identifier)
- title: string (exercise title)
- description: string (detailed description)
- difficulty: enum (beginner, intermediate, advanced)
- estimatedTime: integer (time to complete in minutes)
- requirements: array of strings (software/hardware needed)
- steps: array of strings (step-by-step instructions)
- expectedOutcome: string (what the student should achieve)

**Validation Rules**:
- difficulty must be one of the specified enum values
- estimatedTime must be positive
- steps must have at least one element

### 3. Resource Entity

**Name**: Resource
**Description**: External resources referenced in chapters
**Fields**:
- id: string (unique identifier)
- title: string (resource title)
- url: string (URL to the resource)
- type: enum (documentation, tutorial, paper, video, code)
- description: string (brief description)
- citation: string (APA format citation)
- relevance: string (how it relates to the chapter content)

**Validation Rules**:
- url must be a valid URL
- type must be one of the specified enum values
- citation must follow APA format

### 4. IsaacComponent Entity

**Name**: IsaacComponent
**Description**: NVIDIA Isaac ecosystem components discussed in the module
**Fields**:
- id: string (unique identifier, e.g., "isaac-sim", "isaac-ros", "nav2")
- name: string (component name)
- description: string (what the component does)
- useCases: array of strings (scenarios where it's used)
- integrationPoints: array of strings (how it connects to other components)

**Validation Rules**:
- id must be unique
- name must be 2-50 characters
- useCases must have at least one element

### 5. PracticeSection Entity

**Name**: PracticeSection
**Description**: The practice section at the end of the module
**Fields**:
- id: string (unique identifier, e.g., "practice-section")
- title: string (practice section title)
- content: string (Markdown content)
- exercises: array of Exercise entities
- objectives: array of strings (what skills are practiced)
- prerequisites: array of strings (what knowledge is required)

**Validation Rules**:
- id must be unique
- exercises array must have at least one element
- content must follow Docusaurus-compatible Markdown format

## Relationships

### Chapter to Exercise
- One Chapter can have many Exercises
- Exercises belong to one Chapter (or PracticeSection)
- Relationship: One-to-Many

### Chapter to IsaacComponent
- One Chapter can reference many IsaacComponents
- IsaacComponents can be referenced by many Chapters
- Relationship: Many-to-Many (through references)

### Module to Chapter
- One Module has many Chapters
- One Chapter belongs to one Module
- Relationship: One-to-Many

## Content State Transitions

### Chapter States
1. **Draft** → Content is being written
2. **Review** → Content is under review
3. **Approved** → Content has been approved
4. **Published** → Content is live in documentation

### Exercise States
1. **Draft** → Exercise is being designed
2. **Tested** → Exercise has been tested
3. **Validated** → Exercise meets learning objectives
4. **Active** → Exercise is available to students

## Validation Rules Summary

- All content must follow Docusaurus-compatible Markdown format
- All citations must follow APA format
- At least 40% of resources must be peer-reviewed sources
- Content must be appropriate for CS/AI students advancing into perception and navigation
- All external links must be verified and active
- Learning objectives must be measurable and achievable
- Isaac-specific content must accurately represent the technology capabilities