---
title: Chapter 4 - Services, Actions, and Robot Control
sidebar_position: 4
description: Mechanisms for synchronous and asynchronous robot commands
tags: [ros2, services, actions, robot-control, communication]
---

# Services, Actions, and Robot Control

## Learning Objectives

- Understand the differences between topics, services, and actions
- Implement services for synchronous robot control
- Create actions for complex, long-running robot tasks
- Apply appropriate communication patterns for different control scenarios
- Design effective robot control architectures using ROS 2 primitives

## Content

### Introduction to Robot Control Communication Patterns

Robot control in ROS 2 utilizes three primary communication patterns, each designed for specific types of interactions:

**Topics** provide asynchronous, decoupled communication ideal for continuous data streams like sensor readings and velocity commands.

**Services** offer synchronous request-response communication suitable for discrete operations with clear input and output.

**Actions** enable goal-oriented communication with feedback for long-running tasks that require monitoring and potential interruption.

Understanding when to use each pattern is crucial for effective robot control system design.

### Services for Synchronous Robot Control

Services in ROS 2 implement a synchronous request-response pattern where a client sends a request to a server and waits for a response. This pattern is ideal for operations that:

- Have a clear beginning and end
- Require confirmation of completion
- Need to return specific results
- Should block the client until completion

Service communication involves three components (ROS 2 Documentation, 2023):
1. **Service Definition**: Defines the request and response message types
2. **Service Server**: Implements the service functionality
3. **Service Client**: Calls the service and receives the response

#### Service Definition

Service definitions use the `.srv` file format, which specifies both request and response message structures:

```
# Request (input parameters)
string goal_name
float64 target_value
---
# Response (output parameters)
bool success
string message
float64 actual_value
```

#### Service Server Implementation

A service server in Python using rclpy:

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import SetBool  # Example service type

class RobotControlService(Node):
    def __init__(self):
        super().__init__('robot_control_service')
        self.srv = self.create_service(
            SetBool,
            'robot_enable',
            self.enable_robot_callback)

    def enable_robot_callback(self, request, response):
        if request.data:  # Enable command
            success = self.enable_robot_system()
            response.success = success
            response.message = "Robot enabled" if success else "Failed to enable robot"
        else:  # Disable command
            success = self.disable_robot_system()
            response.success = success
            response.message = "Robot disabled" if success else "Failed to disable robot"

        self.get_logger().info(f'Service called: {response.message}')
        return response

def main(args=None):
    rclpy.init(args=args)
    service_node = RobotControlService()
    rclpy.spin(service_node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

#### Service Client Implementation

A service client that calls the service:

```python
import rclpy
from rclpy.node import Node
from example_interfaces.srv import SetBool

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        self.cli = self.create_client(SetBool, 'robot_enable')

        # Wait for service to be available
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')

        self.request = SetBool.Request()

    def enable_robot(self, enable=True):
        self.request.data = enable
        future = self.cli.call_async(self.request)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            response = future.result()
            self.get_logger().info(f'Response: {response.message}')
            return response.success
        else:
            self.get_logger().error('Exception while calling service: %r' % future.exception())
            return False

def main(args=None):
    rclpy.init(args=args)
    controller = RobotController()

    # Enable the robot
    success = controller.enable_robot(True)
    if success:
        controller.get_logger().info('Robot enabled successfully')
    else:
        controller.get_logger().error('Failed to enable robot')

    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Actions for Asynchronous Robot Control

Actions are designed for long-running tasks that require feedback, goal management, and the ability to cancel operations. They are ideal for:

- Navigation to waypoints
- Manipulation tasks
- Calibration procedures
- Any task that takes significant time and needs monitoring

Action communication involves (ROS 2 Documentation, 2023):
1. **Action Definition**: Defines goal, feedback, and result message types
2. **Action Server**: Executes goals and provides feedback
3. **Action Client**: Sends goals and monitors progress

#### Action Definition

Action definitions use the `.action` file format:

```
# Goal: What the action should do
float64 target_position
float64 max_time

---
# Result: What was achieved
bool success
float64 final_position
string message

---
# Feedback: Current status during execution
float64 current_position
float64 elapsed_time
string status_message
```

#### Action Server Implementation

An action server implementation:

```python
import time
import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from example_interfaces.action import Fibonacci  # Example action type

class RobotMotionActionServer(Node):
    def __init__(self):
        super().__init__('robot_motion_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,  # Replace with your action type
            'robot_motion',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback)

    def goal_callback(self, goal_request):
        """Accept or reject a client request to begin an action."""
        self.get_logger().info('Received goal request')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        """Accept or reject a client request to cancel an action."""
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        """Execute the goal."""
        self.get_logger().info('Executing goal...')

        # Get the goal request
        order = goal_handle.request.order

        # Create feedback and result messages
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]

        # Execute the action with feedback
        for i in range(1, order):
            # Check if there's a cancel request
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()

            # Update the sequence
            feedback_msg.sequence.append(
                feedback_msg.sequence[i] + feedback_msg.sequence[i-1])

            # Publish feedback
            goal_handle.publish_feedback(feedback_msg)

            # Sleep to simulate work
            time.sleep(0.1)

        # Check if goal was canceled
        if goal_handle.is_cancel_requested:
            goal_handle.canceled()
            self.get_logger().info('Goal canceled during execution')
            return Fibonacci.Result()

        # Succeed the goal
        goal_handle.succeed()

        # Return the result
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        self.get_logger().info(f'Goal succeeded with result: {result.sequence}')
        return result

def main(args=None):
    rclpy.init(args=args)
    action_server = RobotMotionActionServer()
    rclpy.spin(action_server)
    action_server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

#### Action Client Implementation

An action client that sends goals and monitors progress:

```python
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class RobotMotionClient(Node):
    def __init__(self):
        super().__init__('robot_motion_client')
        self._action_client = ActionClient(
            self,
            Fibonacci,
            'robot_motion')

    def send_goal(self, order=10):
        # Wait for the action server to be available
        self._action_client.wait_for_server()

        # Create a goal message
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        # Send the goal and get a future
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        # Add a callback for when the goal is accepted
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        # Add a callback for when the result is ready
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Received feedback: {feedback.sequence}')

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    action_client = RobotMotionClient()

    # Send a goal
    action_client.send_goal(10)

    # Spin to process callbacks
    rclpy.spin(action_client)

if __name__ == '__main__':
    main()
```

### Choosing Between Services and Actions

The choice between services and actions depends on the specific requirements of the robot control task:

**Use Services When**:
- The operation is quick (less than a few seconds)
- There's no need for feedback during execution
- The operation has a clear, discrete outcome
- Synchronous behavior is acceptable
- The client needs to wait for completion

**Use Actions When**:
- The operation takes a long time to complete
- Feedback during execution is needed
- The operation might be canceled
- The client needs to do other work while the operation runs
- The operation has intermediate states to monitor

### Robot Control Architecture Patterns

Effective robot control systems often combine multiple communication patterns:

**Command and Control Pattern**: Uses topics for continuous commands (e.g., velocity) and services for discrete operations (e.g., enable/disable).

**Goal-Oriented Pattern**: Uses actions for complex tasks (e.g., navigation) with topics for status updates.

**Hierarchical Control Pattern**: Combines all three patterns at different levels of the control hierarchy.

### Practical Robot Control Examples

#### Emergency Stop System

An emergency stop system might use a service for immediate stop commands:

```python
from example_interfaces.srv import Trigger

class EmergencyStop(Node):
    def __init__(self):
        super().__init__('emergency_stop')
        self.srv = self.create_service(Trigger, 'emergency_stop', self.emergency_stop_callback)

    def emergency_stop_callback(self, request, response):
        # Immediately stop all robot motion
        self.stop_all_motors()
        self.disable_actuators()

        response.success = True
        response.message = "Emergency stop activated"
        return response
```

#### Navigation System

A navigation system would use actions for path following:

```python
from nav2_msgs.action import NavigateToPose

class NavigationClient(Node):
    def __init__(self):
        super().__init__('navigation_client')
        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    def navigate_to_position(self, x, y, theta):
        # Create goal for navigation
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.orientation.z = theta

        # Send goal and monitor progress
        self._action_client.send_goal_async(goal_msg)
```

### Best Practices for Robot Control

1. **Use Appropriate Communication Patterns**: Match the communication pattern to the task requirements.

2. **Implement Proper Error Handling**: Handle service and action failures gracefully.

3. **Provide Clear Feedback**: For actions, provide meaningful feedback messages.

4. **Design for Safety**: Implement safety checks in all control services and actions.

5. **Consider Timing Requirements**: Ensure communication patterns meet real-time constraints where necessary.

6. **Validate Inputs**: Check all service and action parameters for validity.

7. **Log Important Events**: Maintain logs of control actions for debugging and safety analysis.

### Integration with Control Systems

Services and actions integrate with traditional control systems through:

- **State Machines**: Using services to transition between states
- **Control Loops**: Using actions for high-level goals while maintaining low-level control loops
- **Safety Systems**: Implementing safety services that can interrupt ongoing actions
- **Monitoring**: Using services to query system status and actions for long-term monitoring

## Acceptance Scenarios

1. **Given** a communication problem in a robotic system, **When** student applies ROS 2 architecture concepts, **Then** they can design an appropriate node-topic structure
2. **Given** a simple robotic task, **When** student implements it using services or actions, **Then** they can successfully control a simulated or real robot with appropriate feedback

## Summary

This chapter covered services and actions in ROS 2, focusing on their application to robot control. Services provide synchronous request-response communication for discrete operations, while actions enable goal-oriented communication with feedback for long-running tasks. The choice between these patterns significantly impacts system design and user experience.

## Further Reading

- ROS 2 Documentation. (2023). Services and Actions. Retrieved from https://docs.ros.org/en/rolling/Concepts/About-Services.html
- Navigation2. (2023). Action-based Navigation System. ROS 2 Navigation Documentation.
- Cousins, S. (2014). ActionLib: A framework for managing asynchronous tasks. IEEE Robotics & Automation Magazine.