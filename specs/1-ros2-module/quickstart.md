# Quickstart: ROS 2 Module Development

## Prerequisites

- Node.js v18+ installed
- npm or yarn package manager
- Git for version control
- Basic knowledge of Markdown syntax
- Understanding of ROS 2 concepts (for content accuracy)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
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
This should start the development server and open the documentation site in your browser.

### 4. Create Module Directory Structure
```bash
mkdir -p docs/modules/ros2
```

## Creating Module Content

### 1. Create Chapter Files
Create each chapter as a separate Markdown file in `docs/modules/ros2/`:

```bash
touch docs/modules/ros2/chapter-1-physical-ai.md
touch docs/modules/ros2/chapter-2-architecture.md
touch docs/modules/ros2/chapter-3-nodes-topics.md
touch docs/modules/ros2/chapter-4-services-actions.md
touch docs/modules/ros2/chapter-5-python-agents.md
touch docs/modules/ros2/chapter-6-urdf-modeling.md
touch docs/modules/ros2/practice-section.md
```

### 2. Add Content to Each Chapter
Follow the Docusaurus Markdown format with frontmatter:

```markdown
---
title: Chapter Title
sidebar_position: 1
description: Brief description of the chapter
---

# Chapter Title

Content goes here...

## Section Header

More content...
```

### 3. Configure Sidebar Navigation
Update `sidebar.js` to include the new module:

```javascript
module.exports = {
  docs: [
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System',
      items: [
        'modules/ros2/chapter-1-physical-ai',
        'modules/ros2/chapter-2-architecture',
        'modules/ros2/chapter-3-nodes-topics',
        'modules/ros2/chapter-4-services-actions',
        'modules/ros2/chapter-5-python-agents',
        'modules/ros2/chapter-6-urdf-modeling',
        'modules/ros2/practice-section'
      ],
    },
  ],
};
```

## Content Development Guidelines

### Source Verification
- All technical claims must be verified against official ROS 2 documentation
- Academic sources should be peer-reviewed publications
- Include APA citations for all sources
- Mark any unverified information with [NEEDS VERIFICATION]

### Writing Standards
- Write for CS/AI students new to robotics
- Use clear, accessible language
- Include practical examples and diagrams where helpful
- Follow the learning objectives defined in the specification

### Quality Checks
1. Run the build process to ensure all content renders correctly:
   ```bash
   npm run build
   # OR
   yarn build
   ```

2. Verify all links are functional
3. Check that all citations follow APA format
4. Ensure content meets word count requirements

## Running the Development Server

To work on the content with live preview:

```bash
npm run start
# OR
yarn start
```

The documentation will be available at http://localhost:3000

## Deployment

When ready to deploy:

```bash
GIT_USER=<Your GitHub username> CURRENT_BRANCH=main npm run deploy
```

This will build the site and push it to the GitHub Pages branch.