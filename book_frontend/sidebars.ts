import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    'preface',
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
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'modules/digital-twin/chapter-1-introduction',
        'modules/digital-twin/chapter-2-gazebo-physics',
        'modules/digital-twin/chapter-3-gazebo-environment',
        'modules/digital-twin/chapter-4-unity-rendering',
        'modules/digital-twin/chapter-5-sensor-simulation',
        'modules/digital-twin/chapter-6-integration-workflows',
        'modules/digital-twin/practice-section'
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac)',
      items: [
        'modules/isaac/chapter-1-ai-brain',
        'modules/isaac/chapter-2-isaac-ecosystem',
        'modules/isaac/chapter-3-simulation-synthetic-data',
        'modules/isaac/chapter-4-visual-slam',
        'modules/isaac/chapter-5-navigation-nav2',
        'modules/isaac/chapter-6-perception-action',
        'modules/isaac/practice-section'
      ],
    },
    {
      type: 'category',
      label: 'Module 4: The Vision-Language-Action Pipeline (NVIDIA Isaac)',
      items: [
        'modules/vla/chapter-1-overview',
        'modules/vla/chapter-2-voice-to-text',
        'modules/vla/chapter-3-language-understanding',
        'modules/vla/chapter-4-cognitive-planning',
        'modules/vla/chapter-5-ros-execution',
        'modules/vla/chapter-6-integration-workflows',
        'modules/vla/practice-section'
      ],
    },
  ],

  // But you can create a sidebar manually
  /*
  tutorialSidebar: [
    'intro',
    'hello',
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial-basics/create-a-document'],
    },
  ],
   */
};

export default sidebars;
