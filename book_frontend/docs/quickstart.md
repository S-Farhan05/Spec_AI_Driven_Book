---
title: Quickstart Guide
sidebar_position: 1
description: Get started with the Physical AI & Humanoid Robotics book project
---

# Quickstart Guide

## Prerequisites

- Node.js v18+ installed
- npm or yarn package manager
- Git for version control
- Basic knowledge of Markdown syntax
- Understanding of ROS 2 concepts (for content accuracy)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/S-Farhan05/Spec_AI_Driven_Book.git
cd Spec_AI_Driven_Book
```

### 2. Install Docusaurus Dependencies
```bash
npm install
# OR
yarn install
```

### 3. Verify Docusaurus Installation
```bash
npm run start
# OR
yarn start
```
This should start the development server and open the documentation site in your browser at http://localhost:3000.

### 4. Explore the ROS 2 Module Content
The ROS 2 module content is located in `docs/modules/ros2/` and includes:

- Chapter 1: Physical AI and the Robotic Nervous System
- Chapter 2: ROS 2 Architecture and Core Concepts
- Chapter 3: Nodes, Topics, and Message Flow
- Chapter 4: Services, Actions, and Robot Control
- Chapter 5: Python Agents with rclpy
- Chapter 6: Humanoid Modeling with URDF
- Practice Section: Exercises and workflows

## Content Development

### Running the Development Server
To work on the content with live preview:

```bash
npm run start
# OR
yarn start
```

The documentation will be available at http://localhost:3000

### Building the Site
To build the static site:

```bash
npm run build
# OR
yarn build
```

### Quality Checks
1. Run the build process to ensure all content renders correctly
2. Verify all links are functional
3. Check that all citations follow APA format
4. Ensure content meets word count requirements

## Project Structure

```
Spec_AI_Driven_Book/
├── docs/
│   ├── modules/
│   │   └── ros2/
│   │       ├── chapter-1-physical-ai.md
│   │       ├── chapter-2-architecture.md
│   │       ├── chapter-3-nodes-topics.md
│   │       ├── chapter-4-services-actions.md
│   │       ├── chapter-5-python-agents.md
│   │       ├── chapter-6-urdf-modeling.md
│   │       └── practice-section.md
│   ├── quickstart.md (this file)
│   └── intro.md
├── src/
├── static/
├── package.json
└── docusaurus.config.js
```

## Contributing

1. Make changes to the documentation files in the `docs/` directory
2. Test your changes using the development server
3. Commit your changes with descriptive commit messages
4. Push changes to the repository

## Deployment

When ready to deploy:

```bash
GIT_USER=<Your GitHub username> CURRENT_BRANCH=main npm run deploy
```

This will build the site and push it to the GitHub Pages branch.