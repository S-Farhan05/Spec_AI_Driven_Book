---
title: Executing Plans with ROS 2
description: Mapping action plans to ROS 2 services and actions for robot execution
tags: [ros2, navigation, robotics, action-execution, services, actions]
---

# Executing Plans with ROS 2

## Learning Objectives

After completing this chapter, students will be able to:
- Map structured action plans to ROS 2 services and action interfaces
- Implement action execution and monitoring systems for robotics applications
- Configure ROS 2 navigation and manipulation services for plan execution
- Design feedback mechanisms for plan monitoring and error handling
- Integrate perception systems with plan execution for adaptive behavior
- Implement recovery behaviors for plan execution failures
- Validate action execution against plan specifications
- Troubleshoot common plan execution issues in ROS 2

## Prerequisites

Before starting this chapter, students should:
- Have completed Chapter 1: Vision-Language-Action Overview
- Have completed Chapter 2: Voice-to-Text Interfaces
- Have completed Chapter 3: Language-Based Task Understanding
- Have completed Chapter 4: Cognitive Planning with LLMs
- Understand ROS 2 concepts including topics, services, and actions
- Be familiar with ROS 2 navigation and manipulation frameworks

## Estimated Duration

This chapter should take approximately **45 minutes** to complete.

## Introduction to Plan Execution in ROS 2

Plan execution in ROS 2 involves transforming high-level action plans into concrete robot behaviors through the ROS 2 communication infrastructure. This process bridges the gap between cognitive planning (where tasks are conceived) and physical robot action (where tasks are executed).

### The Plan Execution Pipeline

The complete plan execution pipeline follows this sequence:

```
High-Level Plan → Action Mapping → ROS 2 Interface → Robot Execution → Feedback → Plan Monitoring
```

### Key ROS 2 Components for Execution

#### Actions vs Services vs Topics

Understanding the differences between ROS 2 communication patterns is crucial for effective plan execution:

| Pattern | Use Case | Characteristics | Examples |
|---------|----------|----------------|----------|
| **Topics** | Continuous data streams | Publish-subscribe, fire-and-forget | Sensor data, robot state |
| **Services** | Request-response | Synchronous, single request-response | Map queries, simple commands |
| **Actions** | Long-running tasks | Asynchronous with feedback | Navigation, manipulation |

### Plan Execution Architecture

The plan execution system consists of several interconnected components:

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Plan Input    │───▶│  Action Mapper   │───▶│  ROS 2 Clients   │
│ (from Chapter 4)│    │  (Behavior Tree) │    │  (Navigation,    │
└─────────────────┘    └──────────────────┘    │   Manipulation)  │
                                              └──────────────────┘
                                                       │
┌─────────────────┐    ┌──────────────────┐           ▼
│  Plan Monitor   │◀───│  Plan Executor   │─────▶┌─────────────┐
│ (Feedback Loop) │    │ (State Machine)  │      │   Robot     │
└─────────────────┘    └──────────────────┘      │  Hardware   │
                                                └─────────────┘
```

## ROS 2 Actions for Robotics

### Understanding ROS 2 Actions

ROS 2 actions are designed for long-running robot behaviors that require:
- **Goal requests**: What to do
- **Feedback**: Progress updates during execution
- **Result responses**: Final outcome of the action

#### Action Structure
```yaml
# Example action structure
Goal:
  target_pose: PoseStamped
  behavior_tree: string
Feedback:
  current_pose: PoseStamped
  distance_remaining: float64
  velocity: Twist
Result:
  completed: bool
  error_code: int32
  error_message: string
```

### Navigation Actions

#### NavigateToPose Action
```python
# navigate_to_pose_example.py
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose

class NavigationActionClient(Node):
    def __init__(self):
        super().__init__('navigation_action_client')
        self._action_client = ActionClient(
            self, NavigateToPose, 'navigate_to_pose')

    def send_goal(self, target_pose):
        """Send navigation goal to Nav2"""
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = target_pose

        self.get_logger().info(f'Sending navigation goal to {target_pose.pose.position.x:.2f}, {target_pose.pose.position.y:.2f}')

        # Wait for action server
        self._action_client.wait_for_server()

        # Send goal and get future
        send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """Handle goal response"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected by server')
            return

        self.get_logger().info('Goal accepted by server, waiting for result')

        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        """Handle action feedback"""
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Current position: ({feedback.current_pose.pose.position.x:.2f}, {feedback.current_pose.pose.position.y:.2f})')

    def get_result_callback(self, future):
        """Handle action result"""
        result = future.result().result
        self.get_logger().info(f'Navigation result: {result.completed}')
```

#### FollowPath Action
```python
from nav2_msgs.action import FollowPath

class PathFollowingClient(Node):
    def __init__(self):
        super().__init__('path_following_client')
        self._action_client = ActionClient(
            self, FollowPath, 'follow_path')

    def follow_path(self, path):
        """Send path following goal"""
        goal_msg = FollowPath.Goal()
        goal_msg.path = path

        self._action_client.wait_for_server()
        send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.path_feedback_callback
        )

        send_goal_future.add_done_callback(self.path_goal_response_callback)
```

### Manipulation Actions

#### Manipulation Actions in ROS 2
```python
# Example manipulation action clients
from control_msgs.action import FollowJointTrajectory
from moveit_msgs.action import MoveGroup
from geometry_msgs.msg import Pose

class ManipulationActionClient(Node):
    def __init__(self):
        super().__init__('manipulation_action_client')

        # Joint trajectory controller
        self._trajectory_client = ActionClient(
            self, FollowJointTrajectory, 'joint_trajectory_controller/follow_joint_trajectory')

        # MoveIt! planning and execution
        self._move_group_client = ActionClient(
            self, MoveGroup, 'move_group')

    def execute_trajectory(self, joint_trajectory):
        """Execute joint trajectory"""
        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.trajectory = joint_trajectory

        self._trajectory_client.wait_for_server()
        future = self._trajectory_client.send_goal_async(goal_msg)
        return future

    def plan_and_move(self, target_pose):
        """Plan and execute movement to target pose"""
        goal_msg = MoveGroup.Goal()
        # Configure goal with target pose
        goal_msg.request.workspace_parameters.header.frame_id = 'base_link'
        goal_msg.request.workspace_parameters.header.stamp = self.get_clock().now().to_msg()

        self._move_group_client.wait_for_server()
        future = self._move_group_client.send_goal_async(goal_msg)
        return future
```

## Mapping Plans to ROS 2 Interfaces

### Plan-to-Action Mapping

#### Action Mapping Configuration
```python
class PlanActionMapper:
    def __init__(self):
        # Define mapping from high-level actions to ROS 2 actions/services
        self.action_mappings = {
            'navigation': {
                'navigate_to': {
                    'action_type': 'NavigateToPose',
                    'action_name': 'navigate_to_pose',
                    'parameter_mapping': {
                        'location': 'pose',
                        'target': 'pose',
                        'destination': 'pose'
                    }
                },
                'follow_path': {
                    'action_type': 'FollowPath',
                    'action_name': 'follow_path',
                    'parameter_mapping': {
                        'path': 'path',
                        'waypoints': 'path'
                    }
                }
            },
            'manipulation': {
                'pick_up': {
                    'action_type': 'Pick',
                    'action_name': 'pickup_object',
                    'parameter_mapping': {
                        'object': 'object_id',
                        'target': 'object_id'
                    }
                },
                'place': {
                    'action_type': 'Place',
                    'action_name': 'place_object',
                    'parameter_mapping': {
                        'object': 'object_id',
                        'location': 'target_pose',
                        'target': 'target_pose'
                    }
                },
                'grasp': {
                    'action_type': 'Grasp',
                    'action_name': 'grasp_object',
                    'parameter_mapping': {
                        'object': 'object_id',
                        'position': 'grasp_pose'
                    }
                }
            },
            'perception': {
                'look_at': {
                    'action_type': 'PanTilt',
                    'action_name': 'pan_tilt_camera',
                    'parameter_mapping': {
                        'target': 'target_pose',
                        'object': 'target_pose'
                    }
                },
                'inspect': {
                    'action_type': 'Inspect',
                    'action_name': 'inspect_area',
                    'parameter_mapping': {
                        'area': 'inspection_area',
                        'target': 'inspection_target'
                    }
                }
            }
        }

    def map_plan_to_ros_actions(self, plan):
        """Map high-level plan to ROS 2 action calls"""
        ros_action_sequence = []

        for step in plan.get('plan', []):
            action_type = step.get('action', '')
            parameters = step.get('parameters', {})

            # Find appropriate ROS 2 action
            ros_action = self.find_ros_action(action_type, parameters)

            if ros_action:
                # Convert parameters to ROS 2 format
                ros_params = self.convert_parameters(parameters, ros_action['parameter_mapping'])

                ros_action_call = {
                    'action_name': ros_action['action_name'],
                    'action_type': ros_action['action_type'],
                    'parameters': ros_params,
                    'timeout': step.get('timeout', 60.0),  # Default 60 second timeout
                    'retries': step.get('retries', 3)      # Default 3 retries
                }

                ros_action_sequence.append(ros_action_call)

        return ros_action_sequence

    def find_ros_action(self, action_name, parameters):
        """Find appropriate ROS 2 action for high-level action"""
        for category, actions in self.action_mappings.items():
            if action_name in actions:
                return actions[action_name]

        # If exact match not found, try partial matches
        for category, actions in self.action_mappings.items():
            for action_key, action_def in actions.items():
                if action_name in action_key or action_key in action_name:
                    return action_def

        return None

    def convert_parameters(self, high_level_params, mapping):
        """Convert high-level parameters to ROS 2 parameter format"""
        ros_params = {}

        for hl_param, ros_param in mapping.items():
            if hl_param in high_level_params:
                ros_params[ros_param] = high_level_params[hl_param]

        return ros_params
```

### Service Calls for Immediate Actions

Some actions are better suited for services rather than actions:

```python
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_srvs.srv import SetBool, Trigger
from geometry_msgs.msg import Twist

class ServiceActionExecutor(Node):
    def __init__(self):
        super().__init__('service_action_executor')

        # Service clients
        self.emergency_stop_client = self.create_client(
            SetBool, 'emergency_stop')
        self.reset_system_client = self.create_client(
            Trigger, 'reset_system')
        self.toggle_power_client = self.create_client(
            SetBool, 'toggle_power')

    def execute_immediate_action(self, action_name, parameters):
        """Execute immediate actions via services"""
        if action_name == 'emergency_stop':
            return self.call_emergency_stop(parameters.get('enabled', True))
        elif action_name == 'reset_system':
            return self.call_reset_system()
        elif action_name == 'toggle_power':
            return self.call_toggle_power(parameters.get('enabled', True))
        else:
            self.get_logger().warn(f'Unknown immediate action: {action_name}')
            return False

    def call_emergency_stop(self, enabled):
        """Call emergency stop service"""
        if not self.emergency_stop_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().error('Emergency stop service not available')
            return False

        request = SetBool.Request()
        request.data = enabled

        future = self.emergency_stop_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        return future.result().success if future.result() else False

    def call_reset_system(self):
        """Call system reset service"""
        if not self.reset_system_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().error('Reset system service not available')
            return False

        request = Trigger.Request()
        future = self.reset_system_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        return future.result().success if future.result() else False

    def call_toggle_power(self, enabled):
        """Call power toggle service"""
        if not self.toggle_power_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().error('Toggle power service not available')
            return False

        request = SetBool.Request()
        request.data = enabled

        future = self.toggle_power_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        return future.result().success if future.result() else False
```

## Plan Execution and Monitoring

### Plan Execution Manager

```python
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import String
from action_msgs.msg import GoalStatus

class PlanExecutionManager(Node):
    def __init__(self):
        super().__init__('plan_execution_manager')

        # Initialize action clients
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.manip_client = ActionClient(self, MoveGroup, 'move_group')

        # Publishers and subscribers
        self.status_pub = self.create_publisher(String, 'plan_execution_status', 10)
        self.plan_sub = self.create_subscription(
            String, 'generated_plan', self.plan_callback, 10)

        # Plan execution state
        self.current_plan = None
        self.execution_state = 'IDLE'  # IDLE, EXECUTING, PAUSED, FAILED, COMPLETED
        self.current_step = 0
        self.action_results = []

        # Callback group for multithreading
        self.callback_group = ReentrantCallbackGroup()

        # Timer for monitoring execution
        self.monitor_timer = self.create_timer(0.1, self.monitor_execution, callback_group=self.callback_group)

    def plan_callback(self, msg):
        """Receive and execute new plan"""
        try:
            import json
            plan_data = json.loads(msg.data)

            if self.execution_state == 'EXECUTING':
                self.get_logger().warn('Previous plan still executing, cannot start new plan')
                return

            self.current_plan = plan_data
            self.current_step = 0
            self.action_results = []
            self.execution_state = 'EXECUTING'

            self.get_logger().info(f'Received plan with {len(plan_data.get("plan", []))} steps')

            # Start plan execution
            self.execute_next_step()

        except json.JSONDecodeError:
            self.get_logger().error('Invalid plan format received')
        except Exception as e:
            self.get_logger().error(f'Error processing plan: {str(e)}')

    def execute_next_step(self):
        """Execute the next step in the plan"""
        if not self.current_plan or self.current_step >= len(self.current_plan.get('plan', [])):
            # Plan completed
            self.execution_state = 'COMPLETED'
            self.publish_status('PLAN_COMPLETED')
            return

        step = self.current_plan['plan'][self.current_step]
        action_name = step.get('action', '')
        parameters = step.get('parameters', {})

        self.get_logger().info(f'Executing step {self.current_step + 1}: {action_name}')

        # Map action to appropriate executor
        if action_name in ['navigate_to', 'move_to', 'go_to']:
            self.execute_navigation_step(parameters)
        elif action_name in ['pick_up', 'place', 'grasp']:
            self.execute_manipulation_step(parameters)
        elif action_name in ['look_at', 'inspect', 'examine']:
            self.execute_perception_step(parameters)
        else:
            # For unmapped actions, try immediate service execution
            self.execute_immediate_action(action_name, parameters)

    def execute_navigation_step(self, parameters):
        """Execute navigation action"""
        if not self.nav_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().error('Navigation server not available')
            self.handle_action_failure()
            return

        # Create navigation goal
        goal_msg = NavigateToPose.Goal()

        # Convert parameters to navigation format
        target_pose = self.convert_to_pose(parameters)
        goal_msg.pose = target_pose

        # Send goal with feedback callback
        send_goal_future = self.nav_client.send_goal_async(
            goal_msg,
            feedback_callback=self.navigation_feedback_callback
        )

        send_goal_future.add_done_callback(self.navigation_goal_response_callback)

    def convert_to_pose(self, parameters):
        """Convert parameters to PoseStamped format"""
        from geometry_msgs.msg import PoseStamped

        pose = PoseStamped()
        pose.header.frame_id = parameters.get('frame_id', 'map')
        pose.header.stamp = self.get_clock().now().to_msg()

        # Extract position and orientation from parameters
        pos = parameters.get('position', {'x': 0.0, 'y': 0.0, 'z': 0.0})
        orient = parameters.get('orientation', {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 1.0})

        pose.pose.position.x = pos.get('x', 0.0)
        pose.pose.position.y = pos.get('y', 0.0)
        pose.pose.position.z = pos.get('z', 0.0)

        pose.pose.orientation.x = orient.get('x', 0.0)
        pose.pose.orientation.y = orient.get('y', 0.0)
        pose.pose.orientation.z = orient.get('z', 0.0)
        pose.pose.orientation.w = orient.get('w', 1.0)

        return pose

    def navigation_feedback_callback(self, feedback_msg):
        """Handle navigation feedback"""
        feedback = feedback_msg.feedback
        current_pos = feedback.current_pose.pose.position
        self.get_logger().debug(f'Navigating: current position ({current_pos.x:.2f}, {current_pos.y:.2f})')

    def navigation_goal_response_callback(self, future):
        """Handle navigation goal response"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Navigation goal rejected')
            self.handle_action_failure()
            return

        # Get result
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.navigation_result_callback)

    def navigation_result_callback(self, future):
        """Handle navigation result"""
        result_msg = future.result()
        result = result_msg.result

        if result.completed:
            self.get_logger().info('Navigation completed successfully')
            self.action_results.append({
                'step': self.current_step,
                'action': 'navigation',
                'success': True,
                'result': result
            })
            self.current_step += 1
            self.execute_next_step()
        else:
            self.get_logger().error(f'Navigation failed: {result.error_message}')
            self.handle_action_failure()

    def handle_action_failure(self):
        """Handle action execution failure"""
        self.execution_state = 'FAILED'
        self.publish_status('ACTION_FAILED')

        # Trigger recovery behavior
        self.trigger_recovery_behavior()

    def trigger_recovery_behavior(self):
        """Trigger appropriate recovery behavior"""
        self.get_logger().info('Attempting recovery behavior...')

        # Example recovery: stop robot and assess situation
        cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        stop_cmd = Twist()
        cmd_vel_pub.publish(stop_cmd)

        # After recovery, either retry or abort
        # In a real implementation, you would have more sophisticated recovery logic

    def monitor_execution(self):
        """Monitor plan execution status"""
        if self.execution_state == 'EXECUTING':
            # Check for timeout
            if self.current_plan and self.current_step < len(self.current_plan.get('plan', [])):
                current_step_data = self.current_plan['plan'][self.current_step]
                timeout = current_step_data.get('timeout', 60.0)  # Default 60 seconds

                # In a real implementation, you would track start time and compare
                # This is a simplified version

    def publish_status(self, status_message):
        """Publish plan execution status"""
        status_msg = String()
        status_msg.data = status_message
        self.status_pub.publish(status_msg)

    def pause_execution(self):
        """Pause current plan execution"""
        self.execution_state = 'PAUSED'
        self.publish_status('EXECUTION_PAUSED')

    def resume_execution(self):
        """Resume paused plan execution"""
        if self.execution_state == 'PAUSED':
            self.execution_state = 'EXECUTING'
            self.publish_status('EXECUTION_RESUMED')
            self.execute_next_step()

    def cancel_execution(self):
        """Cancel current plan execution"""
        self.execution_state = 'IDLE'
        self.publish_status('EXECUTION_CANCELLED')
        # In a real implementation, you would cancel the current action goal
```

### Isaac ROS Integration for Execution

#### Isaac ROS Action Bridge
```python
# isaac_ros_action_bridge.py
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class IsaacROSActionBridge(Node):
    def __init__(self):
        super().__init__('isaac_ros_action_bridge')

        # Isaac-specific action clients
        self.joint_trajectory_client = ActionClient(
            self, FollowJointTrajectory, 'isaac_joint_trajectory_controller/follow_joint_trajectory')

        # Isaac perception publishers
        self.perception_pub = self.create_publisher(
            String, 'isaac_perception_output', 10)

        # Isaac state subscribers
        self.joint_state_sub = self.create_subscription(
            JointState, 'isaac_joint_states', self.joint_state_callback, 10)
        self.odom_sub = self.create_subscription(
            Odometry, 'isaac_odom', self.odom_callback, 10)

        # Isaac-specific services
        self.reset_simulation_cli = self.create_client(Trigger, 'isaac_reset_simulation')
        self.capture_image_cli = self.create_client(CaptureImage, 'isaac_capture_image')

        # Isaac state tracking
        self.current_joint_states = None
        self.current_odom = None

    def execute_manipulation_in_isaac(self, target_pose, object_id):
        """Execute manipulation action in Isaac simulation"""
        # Plan trajectory using Isaac's manipulation capabilities
        trajectory = self.plan_manipulation_trajectory(target_pose, object_id)

        if trajectory:
            return self.execute_trajectory_in_isaac(trajectory)
        else:
            return False

    def plan_manipulation_trajectory(self, target_pose, object_id):
        """Plan manipulation trajectory using Isaac's capabilities"""
        # In a real Isaac implementation, this would use Isaac's planning capabilities
        # This is a simplified example
        trajectory = JointTrajectory()
        trajectory.joint_names = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6", "joint7"]

        # Create trajectory points
        point = JointTrajectoryPoint()
        point.positions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # Home position
        point.velocities = [0.0] * 7
        point.accelerations = [0.0] * 7
        point.time_from_start.sec = 1
        point.time_from_start.nanosec = 0

        trajectory.points.append(point)

        # Add target position
        target_point = JointTrajectoryPoint()
        target_point.positions = [1.0, 0.5, -0.5, 0.0, 0.0, 0.0, 0.0]  # Example target
        target_point.velocities = [0.0] * 7
        target_point.accelerations = [0.0] * 7
        target_point.time_from_start.sec = 2
        target_point.time_from_start.nanosec = 0

        trajectory.points.append(target_point)

        return trajectory

    def execute_trajectory_in_isaac(self, trajectory):
        """Execute joint trajectory in Isaac"""
        if not self.joint_trajectory_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().error('Isaac joint trajectory server not available')
            return False

        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.trajectory = trajectory

        send_goal_future = self.joint_trajectory_client.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(self.trajectory_result_callback)

        return True

    def trajectory_result_callback(self, future):
        """Handle trajectory execution result"""
        goal_handle = future.result()
        if goal_handle.accepted:
            get_result_future = goal_handle.get_result_async()
            get_result_future.add_done_callback(self.final_trajectory_callback)

    def final_trajectory_callback(self, future):
        """Handle final trajectory result"""
        result = future.result().result
        self.get_logger().info(f'Trajectory execution result: {result.error_code}')
```

## Plan Monitoring and Validation

### Execution Monitoring System

```python
class PlanMonitor:
    def __init__(self, node):
        self.node = node
        self.execution_log = []
        self.metrics = {
            'successful_actions': 0,
            'failed_actions': 0,
            'total_time': 0.0,
            'average_completion_rate': 0.0
        }

    def log_execution_event(self, event_type, action_name, details=None):
        """Log execution events for analysis"""
        log_entry = {
            'timestamp': self.node.get_clock().now().seconds_nanoseconds(),
            'event_type': event_type,
            'action_name': action_name,
            'details': details or {},
            'status': 'in_progress'
        }

        self.execution_log.append(log_entry)
        self.node.get_logger().debug(f'{event_type}: {action_name} - {details}')

    def validate_action_result(self, action_name, result, expected_outcome):
        """Validate action result against expected outcome"""
        validation_result = {
            'action': action_name,
            'expected': expected_outcome,
            'actual': result,
            'success': False,
            'confidence': 0.0
        }

        # Simple validation based on action type
        if action_name in ['navigate_to', 'move_to']:
            # Check if robot reached target position
            target_pos = expected_outcome.get('target_position', {})
            actual_pos = result.get('final_position', {})

            if 'x' in target_pos and 'x' in actual_pos:
                distance = self.calculate_2d_distance(target_pos, actual_pos)
                tolerance = expected_outcome.get('tolerance', 0.2)  # 20cm tolerance
                validation_result['success'] = distance <= tolerance
                validation_result['confidence'] = max(0.0, 1.0 - (distance / tolerance))

        elif action_name in ['pick_up', 'grasp']:
            # Check if object was successfully grasped
            validation_result['success'] = result.get('grasped', False)
            validation_result['confidence'] = 1.0 if result.get('grasped', False) else 0.0

        elif action_name in ['place', 'release']:
            # Check if object was successfully placed
            validation_result['success'] = result.get('released', False)
            validation_result['confidence'] = 1.0 if result.get('released', False) else 0.0

        # Update metrics
        if validation_result['success']:
            self.metrics['successful_actions'] += 1
        else:
            self.metrics['failed_actions'] += 1

        return validation_result

    def calculate_2d_distance(self, pos1, pos2):
        """Calculate 2D Euclidean distance between positions"""
        dx = pos1.get('x', 0) - pos2.get('x', 0)
        dy = pos1.get('y', 0) - pos2.get('y', 0)
        return (dx**2 + dy**2)**0.5

    def calculate_completion_rate(self):
        """Calculate plan completion rate"""
        total_actions = self.metrics['successful_actions'] + self.metrics['failed_actions']
        if total_actions == 0:
            return 0.0

        return self.metrics['successful_actions'] / total_actions

    def get_execution_summary(self):
        """Get execution summary for reporting"""
        completion_rate = self.calculate_completion_rate()

        return {
            'total_actions': self.metrics['successful_actions'] + self.metrics['failed_actions'],
            'successful_actions': self.metrics['successful_actions'],
            'failed_actions': self.metrics['failed_actions'],
            'completion_rate': completion_rate,
            'average_confidence': sum([entry.get('confidence', 0) for entry in self.execution_log]) / len(self.execution_log) if self.execution_log else 0.0,
            'execution_log': self.execution_log
        }
```

### Error Handling and Recovery

```python
class PlanRecoverySystem:
    def __init__(self, node):
        self.node = node
        self.recovery_strategies = {
            'navigation_failure': [
                self.retry_with_different_path,
                self.use_alternative_navigation_method,
                self.request_human_assistance
            ],
            'manipulation_failure': [
                self.adjust_grasp_approach,
                self.retry_with_different_orientation,
                self.use_tool_assisted_manipulation
            ],
            'perception_failure': [
                self.change_sensor_configuration,
                self.move_to_better_viewpoint,
                self.use_alternative_sensor_modality
            ]
        }

    def handle_execution_error(self, error_type, context):
        """Handle execution error with appropriate recovery strategy"""
        self.node.get_logger().error(f'Execution error: {error_type} in context {context}')

        if error_type in self.recovery_strategies:
            strategies = self.recovery_strategies[error_type]

            for i, strategy in enumerate(strategies):
                self.node.get_logger().info(f'Attempting recovery strategy {i+1}: {strategy.__name__}')

                try:
                    success = strategy(context)
                    if success:
                        self.node.get_logger().info(f'Recovery successful with strategy {i+1}')
                        return True
                except Exception as e:
                    self.node.get_logger().error(f'Recovery strategy {i+1} failed: {str(e)}')
                    continue

        # If all strategies fail, escalate to human operator
        self.escalate_to_human(context)
        return False

    def retry_with_different_path(self, context):
        """Retry navigation with alternative path"""
        # In real implementation, this would call path planner with different parameters
        target_pose = context.get('target_pose')
        current_pose = context.get('current_pose')

        # Try a different path planning approach
        # This is a simplified example
        self.node.get_logger().info('Retrying navigation with alternative path')
        return True  # Simplified - in reality would attempt alternative path

    def adjust_grasp_approach(self, context):
        """Adjust grasp approach for manipulation failure"""
        # Adjust grasp pose or approach direction
        object_info = context.get('object_info')
        grasp_params = context.get('grasp_params', {})

        # Modify grasp parameters
        grasp_params['approach_angle'] = (grasp_params.get('approach_angle', 0) + 45) % 360
        self.node.get_logger().info(f'Adjusted grasp approach angle to {grasp_params["approach_angle"]} degrees')

        return True  # Simplified

    def change_sensor_configuration(self, context):
        """Change sensor configuration for perception failure"""
        # Change sensor parameters like exposure, gain, or viewpoint
        sensor_config = context.get('sensor_config', {})
        new_config = sensor_config.copy()

        # Adjust parameters
        new_config['exposure'] = min(10000, new_config.get('exposure', 5000) * 1.2)
        new_config['gain'] = min(2.0, new_config.get('gain', 1.0) * 1.1)

        self.node.get_logger().info('Adjusted sensor configuration for better perception')
        return True  # Simplified

    def escalate_to_human(self, context):
        """Escalate to human operator when recovery fails"""
        self.node.get_logger().warn('All recovery strategies failed, escalating to human operator')
        # In a real system, this would trigger a human-in-the-loop interface
        # For example, publish to a topic that alerts a human operator
        human_alert_pub = self.node.create_publisher(String, 'human_operator_alert', 10)
        alert_msg = String()
        alert_msg.data = f"Manual intervention required for {context.get('failed_action', 'unknown action')}"
        human_alert_pub.publish(alert_msg)
```

## Performance Optimization

### Execution Performance Considerations

#### Real-time Execution Requirements
```python
class RealTimeExecutionOptimizer:
    def __init__(self):
        self.action_queue = []
        self.timing_constraints = {}
        self.resource_allocations = {}

    def schedule_action_with_timing_constraints(self, action, deadline):
        """Schedule action with real-time timing constraints"""
        import heapq
        # Add action to priority queue based on deadline
        heapq.heappush(self.action_queue, (deadline, action))

    def optimize_concurrent_execution(self, plan):
        """Optimize plan for concurrent execution where possible"""
        # Identify actions that can be executed in parallel
        # Actions that use different robot resources can often run concurrently
        parallelizable_actions = []
        sequential_actions = []

        for action in plan:
            if self.can_execute_concurrently(action):
                parallelizable_actions.append(action)
            else:
                sequential_actions.append(action)

        # Return optimized execution order
        return {
            'parallel_actions': parallelizable_actions,
            'sequential_actions': sequential_actions
        }

    def can_execute_concurrently(self, action):
        """Check if action can be executed concurrently with others"""
        # Actions that don't share resources can run concurrently
        resource_requirements = {
            'navigation': ['base_motion'],
            'manipulation': ['arm_joints', 'gripper'],
            'perception': ['camera', 'processing_units'],
            'communication': ['network_bandwidth']
        }

        action_resources = resource_requirements.get(action.get('action', ''), [])
        # In a real implementation, you would check against currently allocated resources
        return len(action_resources) <= 1  # Simplified
```

#### Resource Management
```python
class ResourceManager:
    def __init__(self, node):
        self.node = node
        self.resource_status = {
            'navigation': {'available': True, 'busy_until': 0.0},
            'manipulation': {'available': True, 'busy_until': 0.0},
            'perception': {'available': True, 'busy_until': 0.0},
            'computation': {'available': True, 'load': 0.0}
        }

    def acquire_resource(self, resource_type, duration_estimate):
        """Acquire resource for planned action"""
        import time
        current_time = self.node.get_clock().now().nanoseconds / 1e9

        if self.resource_status[resource_type]['available']:
            if current_time >= self.resource_status[resource_type]['busy_until']:
                # Resource is available
                self.resource_status[resource_type]['busy_until'] = current_time + duration_estimate
                self.resource_status[resource_type]['available'] = False
                return True

        # Resource is busy, wait or schedule for later
        return False

    def release_resource(self, resource_type):
        """Release resource after action completion"""
        self.resource_status[resource_type]['available'] = True
        self.resource_status[resource_type]['busy_until'] = 0.0
```

## Integration with Isaac Perception and Navigation

### Isaac-Specific Execution Optimizations

#### GPU-Accelerated Execution Monitoring
```python
class IsaacGPUExecutionMonitor:
    def __init__(self):
        # Initialize GPU resources for execution monitoring
        try:
            import cupy as cp
            self.gpu_available = True
            self.gpu_device = cp.cuda.Device(0)
        except ImportError:
            self.gpu_available = False

    def accelerate_perception_processing(self, sensor_data):
        """Use GPU to accelerate perception processing during execution"""
        if self.gpu_available:
            # Move data to GPU for accelerated processing
            import cupy as cp
            gpu_data = cp.asarray(sensor_data)
            # Process with GPU-accelerated kernels
            processed_data = self.gpu_perception_pipeline(gpu_data)
            # Return to CPU for ROS 2 interface
            return cp.asnumpy(processed_data)
        else:
            # Fall back to CPU processing
            return self.cpu_perception_pipeline(sensor_data)

    def gpu_perception_pipeline(self, data):
        """GPU-accelerated perception pipeline"""
        # This would contain actual GPU-accelerated perception code
        # For example: CUDA kernels for feature detection, matching, etc.
        return data  # Placeholder
```

### Isaac Navigation Integration

#### Isaac Navigation Execution
```python
class IsaacNavigationExecutor:
    def __init__(self, node):
        self.node = node

        # Isaac-specific navigation interfaces
        self.global_planner = self.node.create_client(NavSrv, 'isaac_global_plan')
        self.local_planner = self.node.create_client(NavSrv, 'isaac_local_plan')
        self.controller = ActionClient(node, FollowWaypoints, 'isaac_follow_waypoints')

    def execute_navigation_with_isaac(self, goal_pose, navigation_params=None):
        """Execute navigation using Isaac's optimized navigation stack"""
        if navigation_params is None:
            navigation_params = {
                'planner_type': 'global_then_local',
                'collision_checking': True,
                'dynamic_obstacles': True,
                'smooth_path': True
            }

        # Plan global path
        global_plan = self.plan_global_path(goal_pose, navigation_params)
        if not global_plan:
            return False

        # Plan local path adjustments
        local_plan = self.plan_local_adjustments(global_plan, navigation_params)

        # Execute path following
        success = self.execute_path_following(local_plan, navigation_params)

        return success

    def plan_global_path(self, goal_pose, params):
        """Plan global path using Isaac's optimized global planner"""
        if not self.global_planner.wait_for_service(timeout_sec=1.0):
            self.node.get_logger().error('Isaac global planner service not available')
            return None

        request = NavSrv.Request()
        request.goal = goal_pose
        request.planner_type = params.get('planner_type', 'global_then_local')

        future = self.global_planner.call_async(request)
        rclpy.spin_until_future_complete(self.node, future)

        if future.result() is not None:
            return future.result().path
        else:
            return None

    def execute_path_following(self, path, params):
        """Execute path following using Isaac's optimized controller"""
        if not self.controller.wait_for_server(timeout_sec=1.0):
            self.node.get_logger().error('Isaac path follower server not available')
            return False

        goal_msg = FollowWaypoints.Goal()
        goal_msg.poses = path.poses

        send_goal_future = self.controller.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(self.path_following_result_callback)

        return True
```

## Troubleshooting Plan Execution

### Common Execution Issues

#### Action Server Unavailability
- **Problem**: Action server not responding to requests
- **Diagnosis**: Check if action server is running and properly initialized
- **Solution**: Restart action server or verify network connectivity

#### Plan Timeout Issues
- **Problem**: Actions taking longer than expected
- **Diagnosis**: Check robot configuration, environment complexity, or hardware issues
- **Solution**: Adjust timeout parameters or investigate bottlenecks

#### State Synchronization Problems
- **Problem**: Robot state not synchronized with plan execution
- **Diagnosis**: Check TF tree, odometry, and sensor data streams
- **Solution**: Verify timing and coordinate frame relationships

#### Resource Conflicts
- **Problem**: Multiple actions trying to use same resources
- **Diagnosis**: Check resource allocation and action dependencies
- **Solution**: Implement proper resource locking or scheduling

### Debugging Strategies

#### Logging and Visualization
```python
def enable_detailed_logging(node, log_level='DEBUG'):
    """Enable detailed logging for debugging execution issues"""
    import logging

    # Set up detailed logging
    rclpy.logging.set_logger_level('plan_execution_manager', logging.DEBUG)
    rclpy.logging.set_logger_level('action_client', logging.DEBUG)
    rclpy.logging.set_logger_level('navigation', logging.DEBUG)

    # Add custom loggers for specific components
    node.get_logger().set_level(rclpy.logging.LoggingSeverity.DEBUG)

def visualize_plan_execution(plan, execution_log, robot_pose):
    """Visualize plan execution for debugging"""
    # This would create visualizations in RViz or other tools
    # showing planned vs executed paths, action timing, etc.
    pass
```

#### Step-by-step Execution Mode
```python
class StepByStepExecutor:
    def __init__(self, node):
        self.node = node
        self.paused = False
        self.step_mode = False

        # Service to control step-by-step execution
        self.pause_service = node.create_service(
            SetBool, 'execution_pause', self.pause_callback)
        self.step_service = node.create_service(
            Trigger, 'execution_step', self.step_callback)

    def pause_callback(self, request, response):
        """Handle pause/unpause requests"""
        self.paused = request.data
        response.success = True
        response.message = f"Execution {'paused' if self.paused else 'resumed'}"
        return response

    def step_callback(self, request, response):
        """Execute next step in plan"""
        if self.paused and self.step_mode:
            # Execute next action
            self.execute_next_step()
            response.success = True
            response.message = "Executed next step"
        else:
            response.success = False
            response.message = "Step mode not active"
        return response
```

## Best Practices for Plan Execution

### Design Principles

#### Modularity
- Keep action execution components separate
- Use clear interfaces between components
- Allow for easy substitution of components
- Implement proper error boundaries

#### Safety First
- Implement comprehensive safety checks
- Use conservative parameters by default
- Include emergency stop capabilities
- Monitor system health continuously

#### Performance Optimization
- Minimize communication overhead
- Use efficient data structures
- Implement caching where appropriate
- Optimize for real-time requirements

#### Robustness
- Handle all possible error conditions
- Implement proper timeouts
- Include fallback behaviors
- Design for graceful degradation

### Testing and Validation

#### Unit Testing
```python
import unittest
from unittest.mock import Mock, patch

class TestPlanExecution(unittest.TestCase):
    def setUp(self):
        # Set up test environment
        self.plan_executor = PlanExecutionManager(Mock())

    def test_navigation_action_mapping(self):
        """Test that navigation actions are properly mapped"""
        action_mapper = PlanActionMapper()

        # Test navigation action mapping
        result = action_mapper.find_ros_action('navigate_to', {})
        self.assertIsNotNone(result)
        self.assertEqual(result['action_name'], 'navigate_to_pose')

    def test_plan_validation(self):
        """Test plan validation functionality"""
        plan_monitor = PlanMonitor(Mock())

        # Test validation of successful navigation
        result = plan_monitor.validate_action_result(
            'navigate_to',
            {'final_position': {'x': 1.0, 'y': 1.0}},
            {'target_position': {'x': 1.0, 'y': 1.0}, 'tolerance': 0.2}
        )

        self.assertTrue(result['success'])

if __name__ == '__main__':
    unittest.main()
```

#### Integration Testing
- Test complete plan execution pipeline
- Verify data flow between components
- Validate error handling and recovery
- Test with realistic robot configurations

## Exercises

### Exercise 1: Basic Plan Execution Setup

**Difficulty**: Intermediate
**Estimated Time**: 20 minutes
**Requirements**: ROS 2 environment, robot simulation

Steps:
1. Set up a basic plan execution manager node
2. Connect to navigation and manipulation action servers
3. Create a simple 3-step plan (navigate, grasp, place)
4. Execute the plan and monitor its progress
5. Verify that each action completes successfully

**Expected Outcome**: Students will create a working plan execution system that can execute a simple multi-step plan.

### Exercise 2: Plan Monitoring and Validation

**Difficulty**: Advanced
**Estimated Time**: 25 minutes
**Requirements**: Plan execution system, simulation environment

Steps:
1. Implement plan monitoring functionality
2. Add validation checks for action results
3. Create metrics collection for execution performance
4. Test with both successful and failed execution scenarios
5. Evaluate the effectiveness of monitoring and validation

**Expected Outcome**: Students will implement comprehensive plan monitoring and validation capabilities.

### Exercise 3: Isaac Integration for Execution

**Difficulty**: Advanced
**Estimated Time**: 30 minutes
**Requirements**: Isaac ROS setup, robot simulation environment

Steps:
1. Integrate Isaac-specific action clients with the execution system
2. Implement GPU-accelerated monitoring capabilities
3. Test execution with Isaac's optimized navigation stack
4. Compare performance with standard ROS 2 navigation
5. Evaluate the benefits of Isaac integration

**Expected Outcome**: Students will create an integrated system that leverages Isaac's optimized execution capabilities.

## Resources

- ROS 2 Navigation: https://navigation.ros.org/. Comprehensive documentation for ROS 2 navigation stack and action interfaces.

- ROS 2 Actions Design: https://design.ros2.org/articles/actions.html. Detailed explanation of ROS 2 actions and their appropriate use cases.

- Fox, D., Burgard, W., & Thrun, S. (1997). The dynamic window approach to collision avoidance. *IEEE Robotics & Automation Magazine*, 4(1), 23-33. Original paper on the dynamic window approach used in many navigation systems.

- Quigley, M., et al. (2009). ROS: an open-source Robot Operating System. *ICRA Workshop on Open Source Software*. The foundational paper on ROS architecture and messaging.

- Isaac ROS Documentation: https://nvidia-isaac-ros.github.io/repositories_and_packages/index.html. Documentation for Isaac ROS packages including navigation and perception components.

## Summary

Plan execution in ROS 2 involves the critical integration of high-level planning with concrete robot action capabilities. Through proper use of ROS 2 actions, services, and topics, we can create robust systems that translate cognitive plans into physical robot behaviors.

The key to successful plan execution lies in proper mapping between high-level concepts and ROS 2 interfaces, comprehensive monitoring and validation of execution progress, and effective error handling and recovery mechanisms. Isaac ROS provides optimized components that can enhance execution performance through GPU acceleration and specialized robotics algorithms.

Understanding the differences between ROS 2 communication patterns (topics, services, actions) and using the appropriate one for each situation is essential for creating efficient and reliable systems. The integration of perception feedback with plan execution enables adaptive behaviors that respond to changing environmental conditions.

As with all robotics systems, proper testing, validation, and safety considerations are paramount. The next chapter will explore how to integrate all these components into a complete end-to-end pipeline that connects voice commands to physical robot execution.