---
title: Chapter 2 - ROS 2 Architecture and Core Concepts
sidebar_position: 2
description: Understanding the core architecture of ROS 2, including nodes, topics, and communication patterns
tags: [ros2, architecture, nodes, topics, communication]
---

# ROS 2 Architecture and Core Concepts

## Learning Objectives

- Understand the fundamental architectural components of ROS 2
- Identify and distinguish between nodes, topics, services, and actions
- Recognize the publish-subscribe communication pattern
- Comprehend how different components interact in a ROS 2 system
- Appreciate the distributed nature of ROS 2 architecture

## Content

### Introduction to ROS 2 Architecture

ROS 2 follows a distributed computing architecture based on the Data Distribution Service (DDS) standard. This architecture enables multiple processes, potentially running on different machines, to communicate with each other through a publish-subscribe model. The core architectural elements include:

- **Nodes**: Independent processes that perform computation
- **Topics**: Named buses over which nodes exchange messages
- **Services**: Request-response communication between nodes
- **Actions**: Goal-oriented communication with feedback and status
- **Messages**: Data structures exchanged between nodes
- **Parameters**: Configuration values shared across nodes

This architecture is designed to be both flexible and robust, supporting everything from simple single-robot applications to complex multi-robot systems.

### Nodes: The Building Blocks of ROS 2

A node is the fundamental unit of computation in ROS 2. Each node typically performs a specific function or set of related functions. Examples include:

- Sensor driver nodes that interface with hardware
- Perception nodes that process sensor data
- Planning nodes that generate robot trajectories
- Control nodes that send commands to actuators
- Visualization nodes that display robot state

Nodes are designed to be modular and reusable. A well-designed node should have a single, well-defined purpose and communicate with other nodes through standardized interfaces. This modularity allows developers to:

1. Develop and test components independently
2. Reuse nodes across different robotic applications
3. Replace nodes with alternative implementations without affecting other parts of the system
4. Scale applications by adding more nodes as needed

In ROS 2, nodes are implemented as objects that inherit from the `rclcpp::Node` class (in C++) or `rclpy.node.Node` class (in Python). This provides nodes with access to ROS 2 communication primitives, parameter management, logging capabilities, and lifecycle management.

### Topics and Publish-Subscribe Communication

Topics form the backbone of ROS 2 communication, implementing a publish-subscribe pattern. In this pattern:

- **Publishers** send messages to a topic
- **Subscribers** receive messages from a topic
- Multiple publishers and subscribers can exist for the same topic
- Communication is asynchronous and decoupled

The publish-subscribe pattern offers several advantages for robotic systems:

1. **Loose coupling**: Publishers and subscribers don't need to know about each other
2. **Scalability**: Multiple subscribers can receive the same data stream
3. **Flexibility**: New publishers or subscribers can be added without modifying existing code
4. **Robustness**: The failure of one node doesn't necessarily affect others

Messages published to a topic must conform to a specific message type. ROS 2 provides standard message types for common robotics concepts (poses, velocities, sensor data) and allows users to define custom message types. Message types are defined using the `.msg` file format and compiled into language-specific implementations.

### Quality of Service (QoS) in Topic Communication

ROS 2 introduces Quality of Service (QoS) policies that allow fine-tuning of communication behavior. QoS settings control aspects such as:

- **Reliability**: Whether messages must be delivered reliably or best-effort delivery is sufficient
- **Durability**: Whether late-joining subscribers should receive previous messages
- **History**: How many messages to store for delivery
- **Deadline**: Maximum time between consecutive messages
- **Liveliness**: How to detect if a publisher is still active

These QoS policies are crucial for robotic systems that handle both safety-critical and non-critical data (DDS Specification, 2015). For example, sensor data for obstacle avoidance might require reliable delivery with bounded latency, while diagnostic information might tolerate occasional loss (ROS 2 Documentation, 2023).

### Services: Request-Response Communication

While topics provide asynchronous, decoupled communication, services implement synchronous request-response patterns. A service has:

- A **service server** that provides functionality
- One or more **service clients** that request functionality
- A defined **service interface** that specifies the request and response message types

Service communication is synchronous from the client's perspective: the client sends a request and waits for a response. This pattern is appropriate for operations that have a clear beginning and end, such as:

- Saving robot configuration
- Triggering calibration procedures
- Requesting system status
- Activating specific behaviors

### Actions: Goal-Oriented Communication

Actions provide a more sophisticated communication pattern for long-running tasks. An action involves:

- An **action server** that executes goals
- One or more **action clients** that send goals
- A defined **action interface** with goal, feedback, and result message types

Actions are appropriate for operations that take time to complete and may provide ongoing feedback, such as:

- Navigation to a specific location
- Manipulation tasks that require multiple steps
- Calibration procedures that report progress
- Trajectory execution with continuous monitoring

Action communication includes:

1. **Goal**: The desired outcome
2. **Feedback**: Ongoing status updates during execution
3. **Result**: The final outcome when the goal is completed (or canceled/aborted)

### Parameters: Configuration Management

Parameters provide a way to share configuration values across nodes. Each node can declare parameters that can be:

- Set at launch time
- Modified during runtime
- Read by other nodes
- Saved and loaded from configuration files

Parameters are useful for values that control node behavior but don't need the full communication overhead of topics or services, such as:

- Sensor calibration values
- Algorithm tuning parameters
- Operational modes
- Safety limits

### Communication Patterns and When to Use Each

Understanding when to use each communication pattern is crucial for effective ROS 2 design:

- **Topics** for continuous data streams (sensor data, robot state, commands)
- **Services** for discrete operations with clear input/output (calibration, configuration)
- **Actions** for long-running tasks with feedback (navigation, manipulation)
- **Parameters** for configuration values (thresholds, modes, settings)

The choice of communication pattern affects system performance, reliability, and maintainability. For example, using topics for high-frequency sensor data allows multiple nodes to consume the same data stream, while using services for configuration changes ensures that the operation completes before continuing.

### Practical Architecture Considerations

When designing ROS 2 systems, several architectural considerations impact the effectiveness of the implementation:

**Node Design Principles**:
1. **Single Responsibility**: Each node should have one primary purpose to maintain modularity
2. **Clear Interfaces**: Nodes should have well-defined inputs and outputs
3. **Error Handling**: Nodes should handle errors gracefully and report status appropriately
4. **Resource Management**: Nodes should properly manage memory, file handles, and other resources

**Topic Design Guidelines**:
1. **Naming Conventions**: Use consistent, descriptive names that reflect the data being published
2. **Message Frequency**: Consider the computational load and network bandwidth implications of message frequency
3. **Message Size**: Balance information content with transmission efficiency
4. **QoS Configuration**: Match QoS settings to the requirements of the data being transmitted

**System Architecture Patterns**:
1. **Layered Architecture**: Organize nodes into layers (sensing, processing, actuation) to manage complexity
2. **Component-Based Design**: Group related functionality into reusable components
3. **Event-Driven Architecture**: Use topics to trigger reactions to system events
4. **Service-Oriented Approach**: Use services for operations that don't fit the publish-subscribe model

### Lifecycle Management

ROS 2 provides a lifecycle management system that allows nodes to transition through different states:

- **Unconfigured**: Node is loaded but not yet configured
- **Inactive**: Node is configured but not yet activated
- **Active**: Node is fully operational
- **Finalized**: Node is shutting down

This lifecycle system is particularly important for safety-critical applications where the order of node startup and shutdown must be carefully controlled (ROS 2 Design Paper, 2023). It allows for coordinated system initialization and graceful degradation in case of failures.

### Tooling and Visualization

ROS 2 provides extensive tooling to understand and debug architectural designs:

- **ros2 topic**: Inspect topic data and monitor communication
- **ros2 node**: List active nodes and their connections
- **ros2 service**: Interact with services for testing and debugging
- **rqt**: Graphical tools for visualization and debugging
- **ros2 bag**: Record and replay system data for analysis
- **rviz2**: Visualization tool for sensor data and robot state

These tools are essential for understanding the runtime behavior of complex ROS 2 systems and for validating that the architectural design is working as intended.

## Acceptance Scenarios

1. **Given** a student who read the architecture chapter, **When** presented with a robotic system description, **Then** they can identify the appropriate ROS 2 architectural patterns to implement it
2. **Given** a communication problem in a robotic system, **When** student applies ROS 2 architecture concepts, **Then** they can design an appropriate node-topic structure

## Summary

This chapter covered the fundamental architectural concepts of ROS 2, including nodes, topics, services, actions, and parameters. Understanding these concepts is essential for designing effective robotic systems using ROS 2. The choice of communication pattern significantly impacts system performance, reliability, and maintainability.

## Further Reading

- ROS 2 Documentation. (2023). ROS 2 Concepts. Retrieved from https://docs.ros.org/en/rolling/Concepts.html
- DDS Specification. (2015). Data Distribution Service for Real-Time Systems. OMG Standard.
- Gerkey, B., et al. (2016). Refactoring Robot Operating System code: approaches, challenges, and solutions. Journal of Software Engineering for Robotics.