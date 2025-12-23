---
title: Chapter 5 - Python Agents with rclpy
sidebar_position: 5
description: Connecting AI agents to ROS 2 controllers using Python
tags: [ros2, python, rclpy, ai, agents]
---

# Python Agents with rclpy

## Learning Objectives

- Understand the rclpy client library for Python
- Create ROS 2 nodes in Python that connect AI agents to robotic systems
- Implement publishers, subscribers, services, and actions in Python
- Apply Python best practices for ROS 2 development
- Connect AI algorithms to ROS 2 control systems

## Content

### Introduction to rclpy

rclpy is the Python client library for ROS 2, providing a Pythonic interface to the ROS 2 middleware. It allows Python developers to create nodes, publish and subscribe to topics, provide and call services, and work with actions. This makes Python an excellent choice for AI agents that need to interface with robotic systems, as Python has rich support for machine learning, computer vision, and AI libraries.

The rclpy library follows Python conventions and idioms while providing access to all ROS 2 functionality. It handles the underlying communication with the ROS 2 middleware, allowing developers to focus on application logic rather than communication details.

### Setting up rclpy

To use rclpy in your Python projects, you need to install the ROS 2 Python packages. These are typically installed as part of a ROS 2 distribution. The basic import pattern is:

```python
import rclpy
from rclpy.node import Node
```

Before creating nodes, you must initialize the rclpy library:

```python
rclpy.init()
```

This initializes the underlying ROS 2 client library and prepares it for creating nodes. The initialization should happen once per process, typically at the beginning of your main function.

### Creating Nodes with rclpy

A ROS 2 node in Python is typically implemented as a class that inherits from `rclpy.node.Node`. This provides access to all the ROS 2 functionality needed for communication:

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node_name')
        # Node initialization code here
```

The node name passed to the parent constructor should be unique within your system. The Node class provides methods for creating publishers, subscribers, services, and actions.

### Publishers in Python

Publishers allow nodes to send messages to topics. To create a publisher, use the `create_publisher` method:

```python
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.publisher = self.create_publisher(String, 'topic_name', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1
```

The third parameter to `create_publisher` is the QoS (Quality of Service) profile, which specifies how messages should be handled. The value 10 indicates the size of the message queue.

### Subscribers in Python

Subscribers receive messages from topics. To create a subscriber, use the `create_subscription` method:

```python
from std_msgs.msg import String

class Listener(Node):
    def __init__(self):
        super().__init__('listener')
        self.subscription = self.create_subscription(
            String,
            'topic_name',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')
```

The second parameter is the topic name, the third is the callback function to handle incoming messages, and the fourth is the QoS profile.

### Services in Python

Services allow for request-response communication. To create a service server:

```python
from example_interfaces.srv import AddTwoInts

class ServiceServer(Node):
    def __init__(self):
        super().__init__('service_server')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Returning: {response.sum}')
        return response
```

To call a service from a client:

```python
from example_interfaces.srv import AddTwoInts

class ServiceClient(Node):
    def __init__(self):
        super().__init__('service_client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
```

### Actions in Python

Actions are used for long-running tasks that provide feedback. To create an action server:

```python
from rclpy.action import ActionServer
from example_interfaces.action import Fibonacci

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()

            feedback_msg.sequence.append(
                feedback_msg.sequence[i] + feedback_msg.sequence[i-1])

            goal_handle.publish_feedback(feedback_msg)

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        return result
```

### Connecting AI Agents to ROS 2

Python's rich ecosystem of AI libraries makes it ideal for connecting AI agents to ROS 2 systems. Common integration patterns include:

1. **Perception Pipeline**: Using libraries like OpenCV, scikit-image, or PyTorch to process sensor data received via ROS 2 topics and publish results.

2. **Decision Making**: Implementing AI algorithms that consume data from multiple ROS 2 topics and make decisions that are published as commands.

3. **Learning Systems**: Creating nodes that collect data from ROS 2 topics for training ML models or that apply trained models to sensor data.

### Practical Example: AI Agent with ROS 2

Here's a complete example of an AI agent that subscribes to sensor data and publishes commands:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class NavigationAI(Node):
    def __init__(self):
        super().__init__('navigation_ai')

        # Subscribe to laser scan data
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.laser_callback,
            10)

        # Publish velocity commands
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        # Timer for AI processing
        self.timer = self.create_timer(0.1, self.ai_callback)

        # Store latest sensor data
        self.latest_scan = None

    def laser_callback(self, msg):
        self.latest_scan = msg

    def ai_callback(self):
        if self.latest_scan is None:
            return

        # Simple AI: move forward if clear path, turn otherwise
        cmd = Twist()

        # Check if path is clear (simplified)
        if min(self.latest_scan.ranges) > 1.0:  # 1 meter threshold
            cmd.linear.x = 0.5  # Move forward
            cmd.angular.z = 0.0
        else:
            cmd.linear.x = 0.0
            cmd.angular.z = 1.0  # Turn in place

        self.publisher.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    navigation_ai = NavigationAI()
    rclpy.spin(navigation_ai)
    navigation_ai.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Best Practices for Python ROS 2 Development

1. **Use Type Hints**: Leverage Python's type hinting to improve code clarity and catch errors early.

```python
from typing import Optional
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class NavigationAI(Node):
    def __init__(self, node_name: str = 'navigation_ai') -> None:
        super().__init__(node_name)
        self.latest_scan: Optional[LaserScan] = None
        # Additional initialization code
```

2. **Handle Exceptions**: ROS 2 communication can fail, so wrap calls in try-catch blocks where appropriate.

```python
try:
    rclpy.spin(self)
except KeyboardInterrupt:
    self.get_logger().info('Node interrupted by user')
except Exception as e:
    self.get_logger().error(f'Error during execution: {e}')
finally:
    self.destroy_node()
    rclpy.shutdown()
```

3. **Resource Management**: Always properly shut down nodes and clean up resources.

```python
def destroy_node(self):
    # Clean up any resources before destroying the node
    if hasattr(self, 'publisher'):
        self.publisher.destroy()
    if hasattr(self, 'subscription'):
        self.subscription.destroy()
    if hasattr(self, 'timer'):
        self.timer.destroy()
    super().destroy_node()
```

4. **Logging**: Use the built-in logging system rather than print statements.

```python
# Good: Use ROS 2 logging
self.get_logger().info(f'Processing scan with {len(msg.ranges)} readings')

# Avoid: Plain print statements
# print(f'Processing scan with {len(msg.ranges)} readings')
```

5. **Parameter Handling**: Use ROS 2 parameters for configuration rather than hardcoded values.

```python
class ConfigurableNode(Node):
    def __init__(self):
        super().__init__('configurable_node')

        # Declare parameters with defaults
        self.declare_parameter('linear_velocity', 0.5)
        self.declare_parameter('angular_velocity', 1.0)
        self.declare_parameter('safety_distance', 1.0)

        # Access parameters
        self.linear_vel = self.get_parameter('linear_velocity').value
        self.angular_vel = self.get_parameter('angular_velocity').value
        self.safety_dist = self.get_parameter('safety_distance').value
```

6. **Testing**: Write unit tests for your AI logic separate from ROS 2 communication.

```python
# Example test for AI logic
def test_navigation_logic():
    # Test the core logic without ROS 2 infrastructure
    sensor_data = [2.0, 2.0, 2.0, 0.5, 2.0]  # Simulated laser scan
    command = calculate_navigation_command(sensor_data, safety_threshold=1.0)

    assert command.linear.x == 0.0  # Should stop due to obstacle
    assert command.angular.z > 0.0  # Should turn to avoid obstacle
```

### Advanced rclpy Features

rclpy provides several advanced features that can enhance your AI agents:

**Timers**: Execute callbacks at regular intervals, useful for control loops.

```python
def __init__(self):
    super().__init__('control_node')
    # Create a timer that triggers every 100ms
    self.timer = self.create_timer(0.1, self.control_loop)
```

**Multi-threading**: Handle multiple ROS 2 contexts in different threads.

```python
from rclpy.executors import MultiThreadedExecutor
import threading

def run_node_in_thread(node):
    rclpy.spin(node)

# Create nodes
node1 = MyNode('node1')
node2 = MyNode('node2')

# Create executor
executor = MultiThreadedExecutor(num_threads=2)
executor.add_node(node1)
executor.add_node(node2)

# Run in separate thread
executor_thread = threading.Thread(target=executor.spin)
executor_thread.start()
```

**Custom Message Types**: Create and use custom message types specific to your AI application.

```python
# Assuming you have a custom message MyCustomMessage
from my_package_msgs.msg import MyCustomMessage

class CustomMessageNode(Node):
    def __init__(self):
        super().__init__('custom_msg_node')
        self.publisher = self.create_publisher(MyCustomMessage, 'custom_topic', 10)
        self.subscription = self.create_subscription(
            MyCustomMessage,
            'custom_topic',
            self.custom_callback,
            10)
```

### Error Handling and Debugging

ROS 2 nodes should handle various error conditions gracefully:

- Communication timeouts
- Missing message dependencies
- Invalid data from sensors
- Resource exhaustion

The rclpy library provides logging capabilities to help with debugging:

```python
self.get_logger().debug('Debug message')
self.get_logger().info('Informational message')
self.get_logger().warn('Warning message')
self.get_logger().error('Error message')
self.get_logger().fatal('Fatal error message')
```

## Acceptance Scenarios

1. **Given** a Python development environment with ROS 2, **When** student follows the rclpy chapter, **Then** they can create a working ROS 2 node
2. **Given** a simple robotic task, **When** student implements it using Python and rclpy, **Then** they can successfully control a simulated or real robot

## Summary

This chapter covered the rclpy Python client library for ROS 2, including how to create nodes, publishers, subscribers, services, and actions. Python's integration with AI libraries makes it an excellent choice for connecting AI agents to robotic systems through ROS 2.

## Further Reading

- ROS 2 Documentation. (2023). Python Client Library (rclpy) Concepts. Retrieved from https://docs.ros.org/en/rolling/Concepts/About-Clients-and-Servers.html
- Open Source Robotics Foundation. (2023). rclpy API Documentation. ROS 2 Documentation.
- Choset, H., et al. (2005). Principles of Robot Motion: Theory, Algorithms, and Implementations. MIT Press.