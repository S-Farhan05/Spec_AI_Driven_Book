---
title: Chapter 3 - Nodes, Topics, and Message Flow
sidebar_position: 3
description: How ROS 2 nodes communicate and exchange messages
tags: [ros2, nodes, topics, communication, message-flow]
---

# Nodes, Topics, and Message Flow

## Learning Objectives

- Understand the relationship between nodes and topics in ROS 2
- Analyze message flow patterns in robotic systems
- Design effective node-topic architectures
- Implement proper message handling and routing
- Apply best practices for message flow management

## Content

### Understanding the Node-Topic Relationship

In ROS 2, nodes and topics form the fundamental communication infrastructure. Nodes are the active computational elements that perform specific functions, while topics serve as the communication channels that enable nodes to exchange information. This publish-subscribe pattern creates a decoupled architecture where nodes can interact without direct dependencies.

The relationship between nodes and topics can be understood as follows:

**Nodes as Publishers**: Nodes that produce data publish messages to specific topics. Each publisher is associated with one or more topics and sends messages at a rate determined by the application requirements and system capabilities.

**Nodes as Subscribers**: Nodes that consume data subscribe to specific topics to receive messages. Subscribers register their interest in particular topics and receive messages that are published to those topics.

**Topics as Communication Channels**: Topics serve as named buses that carry messages between publishers and subscribers. Multiple nodes can publish to the same topic, and multiple nodes can subscribe to the same topic, enabling complex communication patterns.

### Message Flow Fundamentals

Message flow in ROS 2 follows a well-defined pattern that ensures reliable communication between distributed components (DDS Specification, 2015):

1. **Message Creation**: A publisher node creates a message instance, populates it with data, and sends it to a specific topic.

2. **Message Distribution**: The ROS 2 middleware (DDS implementation) receives the message and distributes it to all active subscribers of that topic.

3. **Message Reception**: Subscribers receive the message and process it according to their application logic.

4. **Message Lifecycle**: Messages are handled according to Quality of Service (QoS) policies, which determine how they are stored, delivered, and managed in the system (ROS 2 Documentation, 2023).

### Types of Message Flow Patterns

ROS 2 systems commonly exhibit several message flow patterns:

**Unidirectional Flow**: Data flows in one direction from publishers to subscribers, such as sensor data flowing from sensor nodes to processing nodes.

**Bidirectional Flow**: Nodes exchange information in both directions, such as a navigation system sending goals to a controller and receiving status updates in return.

**Broadcast Flow**: A single publisher sends messages to multiple subscribers simultaneously, such as a clock node broadcasting time information.

**Fan-in Flow**: Multiple publishers send messages to a single subscriber, such as multiple sensors feeding data to a fusion algorithm.

**Fan-out Flow**: A single publisher sends messages to multiple subscribers, such as processed sensor data being used by multiple decision-making nodes.

### Node Implementation Patterns

Effective node design in ROS 2 follows several established patterns:

**Producer Nodes**: Focus on generating and publishing data. These nodes typically interface with hardware sensors or generate synthetic data. They should handle hardware errors gracefully and provide consistent message timing.

**Consumer Nodes**: Focus on receiving and processing data. These nodes implement the core application logic and should be designed to handle variable message rates and potential data gaps.

**Transformer Nodes**: Receive data from one or more topics, process it, and publish results to other topics. These nodes implement the core business logic of the system.

**Coordinator Nodes**: Manage the interaction between multiple other nodes, often implementing complex state machines or decision logic.

### Topic Naming Conventions and Best Practices

Proper topic naming is crucial for maintainable ROS 2 systems:

**Descriptive Names**: Use names that clearly indicate the content and purpose of the topic (e.g., `/robot1/sensors/laser_scan` rather than `/topic1`).

**Hierarchical Organization**: Use forward slashes to create a logical hierarchy (e.g., `/robot1/control/cmd_vel`, `/robot1/sensors/imu`).

**Consistent Schemas**: Use consistent naming patterns across similar topics (e.g., all velocity commands follow the pattern `/robotX/cmd_vel`).

**Avoid Special Characters**: Use only alphanumeric characters, underscores, and forward slashes in topic names.

### Quality of Service (QoS) and Message Flow

QoS settings significantly impact message flow behavior:

**Reliability Policy**: Determines whether messages must be delivered reliably or if best-effort delivery is sufficient. Reliable delivery ensures all messages are received but may introduce latency.

**Durability Policy**: Determines whether late-joining subscribers receive previous messages. Transient-local durability stores messages for new subscribers, while volatile discards them.

**History Policy**: Controls how many messages are stored for delivery. Keep-all stores all messages (subject to resource limits), while keep-last stores only the most recent messages.

**Deadline Policy**: Sets the maximum time between consecutive messages, allowing detection of publisher failures.

### Message Flow Analysis and Optimization

Analyzing message flow helps optimize system performance:

**Message Rate Analysis**: Monitor the frequency of messages on each topic to identify potential bottlenecks or excessive communication.

**Message Size Analysis**: Track the size of messages to optimize network usage and processing time.

**Latency Measurement**: Measure the time from message publication to reception to ensure timing requirements are met.

**Resource Utilization**: Monitor CPU and memory usage of nodes to identify resource constraints.

### Advanced Message Flow Concepts

**Message Filters**: Implement filtering mechanisms to process only relevant messages based on content, timing, or other criteria.

**Message Synchronization**: Coordinate messages from multiple topics to ensure temporal consistency, particularly important for sensor fusion applications.

**Message Transformation**: Convert messages between different coordinate frames or data representations as needed by different system components.

**Message Aggregation**: Combine multiple messages into single messages to reduce communication overhead for high-frequency data.

### Practical Example: Navigation Message Flow

Consider a navigation system with the following message flow:

1. **Sensor Nodes**: Publish laser scan data (`/scan`), IMU data (`/imu/data`), and odometry (`/odom`).

2. **Localization Node**: Subscribes to sensor data and publishes the robot's pose (`/amcl_pose`).

3. **Path Planning Node**: Subscribes to the robot's pose and goal poses, publishes planned paths (`/plan`).

4. **Control Node**: Subscribes to planned paths and publishes velocity commands (`/cmd_vel`).

5. **Robot Driver**: Subscribes to velocity commands and controls the physical robot.

This flow demonstrates how different types of nodes work together through topics to achieve complex behavior.

### Error Handling and Robustness

Robust message flow systems include error handling:

**Publisher Failures**: Implement timeouts and fallback behaviors when publishers become unavailable.

**Message Loss**: Design systems to handle occasional message loss gracefully, particularly for non-critical data streams.

**Data Validation**: Validate incoming messages to prevent errors from propagating through the system.

**Node Restart**: Implement proper reconnection and state recovery when nodes restart.

### Tools for Message Flow Analysis

ROS 2 provides several tools to analyze and debug message flow:

- `ros2 topic list`: Shows all active topics in the system
- `ros2 topic echo <topic>`: Displays messages published to a topic
- `ros2 topic info <topic>`: Shows information about publishers and subscribers for a topic
- `ros2 node info <node>`: Shows topic connections for a specific node
- `rqt_graph`: Visualizes the node-topic network
- `ros2 bag`: Records and replays message sequences for analysis

These tools are essential for understanding and debugging message flow in complex ROS 2 systems.

## Acceptance Scenarios

1. **Given** a robotic system description, **When** student analyzes the communication requirements, **Then** they can design an appropriate node-topic architecture
2. **Given** a communication problem in a robotic system, **When** student applies message flow concepts, **Then** they can identify the appropriate node-topic structure to solve it

## Summary

This chapter explored the relationship between nodes and topics in ROS 2, covering message flow patterns, implementation best practices, and analysis techniques. Understanding these concepts is crucial for designing effective and efficient robotic systems that communicate reliably.

## Further Reading

- ROS 2 Documentation. (2023). Topics and Services. Retrieved from https://docs.ros.org/en/rolling/Concepts/About-Topics.html
- DDS Consortium. (2020). Data Distribution Service (DDS) for Real-Time Systems. Version 1.4 Specification.
- Quigley, M., et al. (2009). ROS: an open-source Robot Operating System. ICRA Workshop on Open Source Software.