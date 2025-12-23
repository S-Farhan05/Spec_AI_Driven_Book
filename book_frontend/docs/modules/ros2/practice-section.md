---
title: "Practice: ROS 2 Concepts"
sidebar_position: 7
description: "Practical exercises for ROS 2 concepts"
tags: ["practice", "exercises", "ros2"]
---

# Practice: ROS 2 Concepts

## Exercises

### Exercise 1: Node Communication Analysis
**Objective**: Understand how nodes communicate through topics in a simple scenario.

**Description**: Given a basic mobile robot system with a laser scanner, IMU, and motor controller, analyze the node-topic architecture and identify potential communication patterns.

**Difficulty**: Beginner

**Instructions**:
1. Draw a node-topic diagram showing publishers and subscribers
2. Identify the message types for each topic
3. Determine appropriate QoS settings for safety-critical sensor data
4. Explain how the system would handle a node failure

**Expected Outcome**: Students should be able to create a complete node-topic architecture diagram and justify their design choices.

**Solution Approach**: The laser scanner node publishes sensor_msgs/LaserScan messages to the /scan topic. The navigation node subscribes to /scan and /imu/data topics, and publishes geometry_msgs/Twist messages to /cmd_vel. For safety-critical data like laser scans, reliable QoS with durability is recommended.

### Exercise 2: Service Implementation for Robot Control
**Objective**: Implement a simple service to control a robot's operational state.

**Description**: Create a service that allows clients to enable or disable robot operations with appropriate safety checks.

**Difficulty**: Intermediate

**Instructions**:
1. Define a service interface for enabling/disabling the robot
2. Implement a service server that validates safety conditions
3. Create a client that calls the service
4. Test the service with different safety scenarios

**Expected Outcome**: Working service that safely controls robot operations with proper error handling.

**Solution Approach**: Define a service with boolean enable/disable request and status response. The server should check safety conditions (e.g., emergency stop state, calibration status) before changing the robot state.

### Exercise 3: Action-Based Navigation
**Objective**: Implement an action server for robot navigation with feedback.

**Description**: Create an action server that simulates navigating to waypoints with progress feedback and cancellation capability.

**Difficulty**: Advanced

**Instructions**:
1. Define an action interface for navigation goals
2. Implement an action server that simulates navigation
3. Provide feedback on progress to goal
4. Implement cancellation handling
5. Create a client to test the action

**Expected Outcome**: Working action server that simulates navigation with proper feedback and cancellation.

**Solution Approach**: Use geometry_msgs/PoseStamped for goals, include progress percentage in feedback, and handle preemption requests properly.

### Exercise 4: URDF Modeling Challenge
**Objective**: Create a URDF model for a simple robot arm.

**Description**: Design and implement a URDF file for a 3-DOF robot arm with proper joints and visual elements.

**Difficulty**: Intermediate

**Instructions**:
1. Define the kinematic structure with appropriate joints
2. Add visual and collision elements
3. Set realistic mass and inertia properties
4. Validate the URDF model

**Expected Outcome**: Valid URDF file that represents a functional robot arm model.

**Solution Approach**: Use revolute joints for rotational degrees of freedom, create links with appropriate dimensions, and ensure proper parent-child relationships.

### Exercise 5: System Integration Challenge
**Objective**: Integrate multiple ROS 2 concepts in a complete system.

**Description**: Design a complete system that uses topics, services, and actions together to control a robot performing a complex task.

**Difficulty**: Advanced

**Instructions**:
1. Design the overall system architecture
2. Identify which communication patterns to use for different functions
3. Implement at least one service, one action, and multiple topics
4. Test the integrated system behavior

**Expected Outcome**: A well-designed system architecture with appropriate use of ROS 2 communication patterns.

**Solution Approach**: Use topics for continuous sensor data and commands, services for discrete operations like calibration, and actions for complex tasks like navigation or manipulation.

## Small ROS 2 Workflows

1. **Simple Publisher-Subscriber**: Create a publisher that sends "Hello World" messages and a subscriber that prints them.

2. **Parameter Configuration**: Create a node that uses parameters for configuration and can be reconfigured at runtime.

3. **Service Call Chain**: Create multiple services where one service calls another, demonstrating service composition.

4. **Action Feedback Loop**: Implement an action that provides continuous feedback and demonstrate how clients can monitor progress.

5. **Multi-Node Coordination**: Create multiple nodes that coordinate to achieve a common goal using topics and services.

6. **Simulation Integration**: Create nodes that interface with a Gazebo simulation to control a virtual robot.

7. **Sensor Data Processing**: Build a pipeline that processes sensor data through multiple nodes using topics.

8. **Emergency Handling**: Implement a system that can detect and respond to emergency conditions using services for immediate actions.

## Learning Goals and Expected Outcomes

By completing the exercises and workflows in this practice section, students will:

- Gain hands-on experience with all major ROS 2 communication patterns
- Develop skills in system architecture design for robotic applications
- Learn best practices for implementing ROS 2 nodes, services, and actions
- Understand how to integrate different components into a cohesive system
- Practice debugging and validating ROS 2 systems
- Apply safety considerations in robot control implementations
- Gain confidence in building real-world robotic applications

The exercises progress from basic concepts to complex system integration, allowing students to build their skills incrementally while reinforcing theoretical knowledge with practical implementation.