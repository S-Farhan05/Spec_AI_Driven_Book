# Quickstart Guide: Digital Twin Module - The Digital Twin (Gazebo & Unity)

**Feature**: Digital Twin Module | **Date**: 2025-12-22 | **Spec**: [specs/2-digital-twin-module/spec.md](../specs/2-digital-twin-module/spec.md)

## Overview

This quickstart guide provides the essential steps to set up and begin working with the Digital Twin Module covering Gazebo and Unity for physics simulation and human-robot interaction.

## Prerequisites

Before starting with the Digital Twin Module, ensure you have:

### System Requirements
- **Operating System**: Ubuntu 20.04/22.04 LTS or Windows 10/11 (64-bit)
- **CPU**: Multi-core processor (Intel i5 or equivalent)
- **RAM**: 8GB minimum, 16GB recommended
- **GPU**: Dedicated graphics card with OpenGL 3.3+ support
- **Storage**: 20GB free disk space
- **Network**: Internet connection for package downloads

### Software Dependencies
1. **Node.js**: v18+ with npm
2. **ROS 2**: Humble Hawksbill or later
3. **Gazebo**: Garden or Harmonic version
4. **Unity**: 2022.3 LTS
5. **Git**: Version control system
6. **Python**: 3.8+ with pip

## Setup Steps

### 1. Clone and Initialize Repository
```bash
git clone [repository-url]
cd [repository-name]
npm install
```

### 2. Install ROS 2 and Gazebo
Follow the official ROS 2 installation guide for your OS:
- Ubuntu: https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html
- Windows: https://docs.ros.org/en/humble/Installation/Windows-Install-Binary.html

Install Gazebo Garden:
```bash
sudo apt install ros-humble-gazebo-*
```

### 3. Set Up Docusaurus Documentation
```bash
cd [repository-root]
npm run start
```
This will start the local documentation server.

### 4. Verify Setup
Run the following command to ensure all dependencies are properly installed:
```bash
# Check ROS 2
ros2 --version

# Check Gazebo
gz --version

# Check Node.js
node --version

# Check npm
npm --version
```

## Module Structure

The Digital Twin Module consists of 6 chapters and a practice section:

1. **Chapter 1**: Introduction to Digital Twins
2. **Chapter 2**: Gazebo Physics Simulation
3. **Chapter 3**: Environment Modeling in Gazebo
4. **Chapter 4**: Unity High-Fidelity Rendering
5. **Chapter 5**: Sensor Simulation
6. **Chapter 6**: Integrating Digital Twin Workflows
7. **Practice Section**: Hands-on exercises with Gazebo and Unity

## Getting Started with Content Creation

### 1. Create Chapter Files
Chapter files will be created in the `docs/modules/digital-twin/` directory:
```bash
# Example for Chapter 1
docs/modules/digital-twin/chapter-1-introduction.md
```

### 2. Configure Navigation
Update `sidebar.js` and `docusaurus.config.js` to include the new module:
```javascript
// In sidebar.js
module.exports = {
  digitalTwin: [
    'modules/digital-twin/chapter-1-introduction',
    'modules/digital-twin/chapter-2-gazebo-physics',
    // ... other chapters
    'modules/digital-twin/practice-section'
  ]
};
```

### 3. Content Guidelines
- All content must follow Docusaurus-compatible Markdown format
- Include APA-formatted citations for all technical claims
- At least 40% of sources must be peer-reviewed
- Use consistent heading structure (H1 for chapter title, H2 for sections, etc.)

## Common Commands

```bash
# Start local documentation server
npm run start

# Build documentation
npm run build

# Serve built documentation locally
npm run serve

# Run documentation validation
npm run lint
```

## Troubleshooting

### Common Issues
1. **Gazebo won't start**: Ensure NVIDIA drivers are properly installed if using GPU acceleration
2. **Unity import errors**: Check that Unity 2022.3 LTS is installed and properly licensed
3. **Docusaurus build fails**: Verify all chapter files follow proper Markdown syntax

### Verification Steps
1. Test Gazebo simulation: `gz sim`
2. Test Unity: Open Unity Hub and verify installation
3. Test Docusaurus: `npm run start` and navigate to http://localhost:3000

## Next Steps

After completing the setup:
1. Review the module specification in `specs/2-digital-twin-module/spec.md`
2. Examine the implementation plan in `specs/2-digital-twin-module/plan.md`
3. Begin creating content following the structure defined in the data model