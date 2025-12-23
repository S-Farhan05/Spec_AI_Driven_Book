---
title: Navigation with Nav2
description: Path planning and movement for humanoid robots using Navigation2
tags: [navigation, nav2, robotics, path-planning, humanoid, ros2]
---

# Navigation with Nav2

## Learning Objectives

After completing this chapter, students will be able to:
- Configure Navigation2 (Nav2) for humanoid robot navigation
- Implement path planning and obstacle avoidance algorithms
- Integrate sensor data for safe robot navigation
- Configure costmaps for humanoid robot-specific navigation
- Tune navigation parameters for optimal performance
- Implement recovery behaviors for navigation failures
- Evaluate navigation performance and success metrics
- Integrate navigation with perception and SLAM systems

## Prerequisites

Before starting this chapter, students should:
- Have completed Chapter 1: The AI-Robot Brain
- Have completed Chapter 2: NVIDIA Isaac Ecosystem
- Have completed Chapter 3: Photorealistic Simulation & Synthetic Data
- Have completed Chapter 4: Visual SLAM with Isaac ROS
- Understand basic concepts of path planning and robot kinematics
- Be familiar with ROS 2 navigation concepts

## Estimated Duration

This chapter should take approximately **50 minutes** to complete.

## Introduction to Navigation2 (Nav2)

Navigation2 (Nav2) is the next-generation navigation framework for ROS 2, designed to provide advanced navigation capabilities for mobile robots. Nav2 builds upon the lessons learned from ROS 1's navigation stack while introducing modern software architecture, improved performance, and enhanced capabilities.

### What is Navigation2?

Navigation2 is a comprehensive navigation framework that provides:
- **Path Planning**: Algorithms to find optimal routes from start to goal
- **Path Execution**: Controllers to follow planned paths
- **Obstacle Avoidance**: Local planners to avoid dynamic obstacles
- **Localization**: Integration with AMCL for robot pose estimation
- **Costmap Management**: Dynamic obstacle mapping and inflation
- **Recovery Behaviors**: Strategies to recover from navigation failures

### Why Nav2 for Humanoid Robots?

Humanoid robots present unique navigation challenges that Nav2 addresses:

#### Humanoid-Specific Requirements
- **Stability**: Maintain balance during navigation
- **Step Planning**: Navigate stairs and uneven terrain
- **Social Navigation**: Respect human comfort zones
- **Dynamic Obstacles**: Handle moving humans and objects
- **Multi-Modal Navigation**: Handle different gaits and movement patterns

### Nav2 Architecture

The Nav2 system consists of several interconnected components:

```
Navigation Stack Components:
├── Global Planner
│   ├── A* / Dijkstra / Theta*
│   ├── Grid-based planning
│   └── Topological planning
├── Local Planner
│   ├── DWA (Dynamic Window Approach)
│   ├── MPC (Model Predictive Control)
│   └── TEB (Timed Elastic Band)
├── Costmap 2D
│   ├── Static Layer
│   ├── Obstacle Layer
│   ├── Inflation Layer
│   └── Voxel Layer
├── Controller Server
│   ├── Path smoothing
│   ├── Velocity limiting
│   └── Feedback control
├── Behavior Tree Executor
│   ├── Task sequencing
│   ├── Conditional execution
│   └── Recovery management
└── Recovery Server
    ├── Spin recovery
    ├── Backup recovery
    └── Wait recovery
```

## Nav2 Core Components

### Global Planner

The global planner computes a path from the robot's current location to the goal location. It operates on the static map and considers known obstacles.

#### Available Global Planners
- **NavFn**: Legacy Dijkstra-based planner
- **GlobalPlanner**: A* implementation with visualization
- **CarrotPlanner**: Simple point-reachable planner
- **Theta*: Visibility graph-based planner
- **SBPL**: Lattice-based planning for complex robots

#### Humanoid-Specific Considerations
For humanoid robots, global planners must consider:
- **Kinematic constraints**: Leg limitations and balance requirements
- **Footstep planning**: Sequence of foot placements
- **Center of Mass**: Balance during movement
- **Terrain traversability**: Step height and surface stability

### Local Planner

The local planner executes the global path while avoiding dynamic obstacles. It operates in real-time and reacts to sensor data.

#### Available Local Planners
- **DWB (Dynamic Window Based)**: Velocity-based local planning
- **TEB (Timed Elastic Band)**: Trajectory optimization approach
- **MPC (Model Predictive Control)**: Predictive control approach

#### Humanoid-Specific Considerations
For humanoid robots, local planners must consider:
- **Balance constraints**: Maintaining center of mass
- **Step timing**: Coordinated leg movements
- **Stability margins**: Safety during dynamic movement
- **Human-like behavior**: Natural walking patterns

### Costmap 2D

The costmap system maintains a representation of the environment with cost values indicating the desirability of different locations.

#### Costmap Layers
- **Static Layer**: Pre-built map of permanent obstacles
- **Obstacle Layer**: Dynamic obstacles from sensors
- **Inflation Layer**: Safety buffer around obstacles
- **Voxel Layer**: 3D obstacle representation
- **Range Layer**: Sonar/laser range sensor data

#### Humanoid-Specific Costmap Considerations
- **Height-based filtering**: Ignore obstacles above head level
- **Step height constraints**: Mark terrain as impassable if steps too high
- **Surface stability**: Consider ground conditions for walking
- **Social zones**: Maintain distance from humans

### Behavior Trees

Nav2 uses behavior trees to orchestrate navigation tasks, providing a flexible and maintainable architecture.

#### Behavior Tree Components
- **Actions**: Atomic navigation tasks
- **Conditions**: Boolean checks
- **Decorators**: Modify child behavior
- **Controls**: Manage child execution

#### Common Behavior Trees
- **NavigateWithReplanning**: Global plan → local plan → execute
- **FollowPath**: Execute precomputed path
- **ComputePathToPose**: Plan path to goal
- **SmoothPath**: Smooth path for better execution

## Isaac Nav2 Integration

### Isaac-Specific Navigation Features

Isaac Navigation extends Nav2 with NVIDIA-specific optimizations:

#### GPU-Accelerated Path Planning
- **CUDA-optimized algorithms**: Faster path computation
- **Parallel processing**: Multiple path evaluations
- **Deep learning integration**: ML-enhanced navigation
- **Semantic navigation**: Object-aware path planning

#### Isaac Navigation Server
The Isaac Navigation Server provides:
- **GPU-accelerated planning**: Optimized for NVIDIA hardware
- **Deep learning integration**: Neural networks for perception
- **Semantic mapping**: Object-aware navigation
- **3D navigation**: Path planning in 3D environments

### Configuration Parameters

#### Main Configuration File Structure
```yaml
# navigation_params.yaml
amcl:
  ros__parameters:
    use_sim_time: True
    alpha1: 0.2
    alpha2: 0.2
    alpha3: 0.2
    alpha4: 0.2
    alpha5: 0.2
    base_frame_id: "base_footprint"
    beam_skip_distance: 0.5
    beam_skip_error_threshold: 0.9
    beam_skip_threshold: 0.3
    do_beamskip: False
    global_frame_id: "map"
    lambda_short: 0.1
    likelihood_max_dist: 2.0
    max_beams: 60
    max_particles: 2000
    min_particles: 500
    odom_frame_id: "odom"
    pf_err: 0.05
    pf_z: 0.99
    recovery_alpha_fast: 0.0
    recovery_alpha_slow: 0.0
    resample_interval: 1
    robot_model_type: "differential"
    save_pose_rate: 0.5
    set_initial_pose: True
    sigma_hit: 0.2
    tf_broadcast: True
    transform_tolerance: 1.0
    update_min_a: 0.2
    update_min_d: 0.2
    z_hit: 0.5
    z_max: 0.05
    z_rand: 0.5
    z_short: 0.05

bt_navigator:
  ros__parameters:
    use_sim_time: True
    global_frame: "map"
    robot_base_frame: "base_link"
    odom_topic: "odom"
    bt_loop_duration: 10
    default_server_timeout: 20
    enable_groot_monitoring: True
    groot_zmq_publisher_port: 1666
    groot_zmq_server_port: 1667
    plugin_lib_names:
      - nav2_compute_path_to_pose_action_bt_node
      - nav2_follow_path_action_bt_node
      - nav2_back_up_action_bt_node
      - nav2_spin_action_bt_node
      - nav2_wait_action_bt_node
      - nav2_clear_costmap_service_bt_node
      - nav2_is_stuck_condition_bt_node
      - nav2_goal_reached_condition_bt_node
      - nav2_goal_updated_condition_bt_node
      - nav2_initial_pose_received_condition_bt_node
      - nav2_reinitialize_global_localization_service_bt_node
      - nav2_rate_controller_bt_node
      - nav2_distance_controller_bt_node
      - nav2_speed_controller_bt_node
      - nav2_truncate_path_action_bt_node
      - nav2_goal_updater_node_bt_node
      - nav2_recovery_node_bt_node
      - nav2_pipeline_sequence_bt_node
      - nav2_round_robin_node_bt_node
      - nav2_transform_available_condition_bt_node
      - nav2_time_expired_condition_bt_node
      - nav2_path_expiring_timer_condition
      - nav2_distance_traveled_condition_bt_node
      - nav2_single_trigger_bt_node
      - nav2_is_battery_low_condition_bt_node
      - nav2_navigate_to_pose_action_bt_node
      - nav2_remove_passed_goals_action_bt_node
      - nav2_planner_selector_bt_node
      - nav2_controller_selector_bt_node
      - nav2_goal_checker_selector_bt_node

controller_server:
  ros__parameters:
    use_sim_time: True
    controller_frequency: 20.0
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.5
    min_theta_velocity_threshold: 0.001
    progress_checker_plugin: "progress_checker"
    goal_checker_plugin: "goal_checker"
    controller_plugins: ["FollowPath"]

    # Progress checker parameters
    progress_checker:
      plugin: "nav2_controller::SimpleProgressChecker"
      required_movement_radius: 0.5
      movement_time_allowance: 10.0

    # Goal checker parameters
    goal_checker:
      plugin: "nav2_controller::SimpleGoalChecker"
      xy_goal_tolerance: 0.25
      yaw_goal_tolerance: 0.25
      stateful: True

    # DWB parameters
    FollowPath:
      plugin: "nav2_navfn_planner/NavfnPlanner"
      debug_cost_spaces: False
      desired_linear_vel: 0.5
      max_vel_x: 0.5
      min_vel_x: 0.1
      max_vel_y: 0.0
      min_vel_y: 0.0
      max_vel_theta: 1.0
      min_vel_theta: 0.4
      acc_lim_x: 2.5
      acc_lim_y: 0.0
      acc_lim_theta: 3.2
      decel_lim_x: -2.5
      decel_lim_y: 0.0
      decel_lim_theta: -3.2
      vx_samples: 20
      vy_samples: 5
      vtheta_samples: 20
      sim_time: 1.7
      linear_granularity: 0.05
      angular_granularity: 0.1
      transform_tolerance: 0.2
      xy_goal_tolerance: 0.25
      trans_stopped_velocity: 0.25
      short_circuit_trajectory_evaluation: True
      stateful: True
      critics: ["RotateToGoal", "Oscillation", "BaseObstacle", "GoalAlign", "PathAlign", "PathDist", "GoalDist"]
      BaseObstacle.scale: 0.02
      PathAlign.scale: 0.1
      PathAlign.forward_point_distance: 0.1
      GoalAlign.scale: 0.5
      GoalAlign.forward_point_distance: 0.1
      PathDist.scale: 0.1
      GoalDist.scale: 0.8
      RotateToGoal.scale: 0.5
      RotateToGoal.slowing_factor: 5.0
      RotateToGoal.lookahead_time: -1.0

global_costmap:
  global_costmap:
    ros__parameters:
      update_frequency: 1.0
      publish_frequency: 1.0
      global_frame: "map"
      robot_base_frame: "base_link"
      use_sim_time: True
      rolling_window: False
      width: 100
      height: 100
      resolution: 0.05
      origin_x: -50.0
      origin_y: -50.0
      plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
      obstacle_layer:
        plugin: "nav2_costmap_2d::ObstacleLayer"
        enabled: True
        observation_sources: scan
        scan:
          topic: "/scan"
          max_obstacle_height: 2.0
          clearing: True
          marking: True
          data_type: "LaserScan"
          raytrace_max_range: 3.0
          raytrace_min_range: 0.0
          obstacle_max_range: 2.5
          obstacle_min_range: 0.0
      static_layer:
        plugin: "nav2_costmap_2d::StaticLayer"
        map_subscribe_transient_local: True
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        cost_scaling_factor: 3.0
        inflation_radius: 0.55
      always_send_full_costmap: True

local_costmap:
  local_costmap:
    ros__parameters:
      update_frequency: 5.0
      publish_frequency: 2.0
      global_frame: "odom"
      robot_base_frame: "base_link"
      use_sim_time: True
      rolling_window: True
      width: 3
      height: 3
      resolution: 0.05
      plugins: ["voxel_layer", "inflation_layer"]
      voxel_layer:
        plugin: "nav2_costmap_2d::VoxelLayer"
        enabled: True
        publish_voxel_map: True
        origin_z: 0.0
        z_resolution: 0.2
        z_voxels: 10
        max_obstacle_height: 2.0
        mark_threshold: 0
        observation_sources: scan
        scan:
          topic: "/scan"
          max_obstacle_height: 2.0
          clearing: True
          marking: True
          data_type: "LaserScan"
          raytrace_max_range: 3.0
          raytrace_min_range: 0.0
          obstacle_max_range: 2.5
          obstacle_min_range: 0.0
      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        cost_scaling_factor: 3.0
        inflation_radius: 0.55
      always_send_full_costmap: True

planner_server:
  ros__parameters:
    expected_planner_frequency: 20.0
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner/NavfnPlanner"
      tolerance: 0.5
      use_astar: false
      allow_unknown: true

smoother_server:
  ros__parameters:
    smoother_plugins: ["simple_smoother"]
    simple_smoother:
      plugin: "nav2_smoother::SimpleSmoother"
      tolerance: 1.0e-10
      max_its: 1000
      w_smooth: 0.9
      w_data: 0.1

behavior_server:
  ros__parameters:
    costmap_topic: "local_costmap/costmap_raw"
    footprint_topic: "local_costmap/published_footprint"
    cycle_frequency: 10.0
    behavior_plugins: ["spin", "backup", "wait"]
    spin:
      plugin: "nav2_behaviors/Spin"
      spin_dist: 1.57
    backup:
      plugin: "nav2_behaviors/BackUp"
      backup_dist: 0.15
      backup_speed: 0.025
    wait:
      plugin: "nav2_behaviors/Wait"
      wait_duration: 1.0
```

### Isaac-Specific Configuration

#### GPU-Accelerated Planning Configuration
```yaml
# Isaac-specific navigation parameters
isaac_nav2:
  ros__parameters:
    # Enable GPU acceleration
    gpu_planning_enabled: True
    cuda_device_id: 0

    # Semantic navigation
    semantic_navigation_enabled: True
    object_detection_topic: "/isaac_ros/detections"

    # 3D navigation
    enable_3d_navigation: True
    height_map_topic: "/isaac_ros/height_map"

    # Deep learning integration
    ml_planning_enabled: True
    neural_network_model_path: "/models/nav_model.pt"
```

## Practical Implementation

### Setting Up Navigation

#### 1. Launch Configuration
```python
# launch/navigation.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from nav2_common.launch import RewrittenYaml


def generate_launch_description():
    # Launch arguments
    namespace = LaunchConfiguration('namespace')
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    params_file = LaunchConfiguration('params_file')
    default_bt_xml_filename = LaunchConfiguration('default_bt_xml_filename')
    map_subscribe_transient_local = LaunchConfiguration('map_subscribe_transient_local')

    # Launch configuration variables
    lifecycle_nodes = ['controller_server',
                       'planner_server',
                       'recoveries_server',
                       'bt_navigator',
                       'waypoint_follower']

    # Launch navigation nodes
    navigation_cmd = Node(
        package='nav2_controller',
        executable='controller_server',
        output='screen',
        parameters=[configured_params],
        remappings=remappings,
    )

    planner_cmd = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[configured_params],
        remappings=remappings)

    recoveries_cmd = Node(
        package='nav2_recoveries',
        executable='recoveries_server',
        name='recoveries_server',
        output='screen',
        parameters=[configured_params],
        remappings=remappings)

    bt_navigator_cmd = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[configured_params],
        remappings=remappings)

    waypoint_follower_cmd = Node(
        package='nav2_waypoint_follower',
        executable='waypoint_follower',
        name='waypoint_follower',
        output='screen',
        parameters=[configured_params],
        remappings=remappings)

    lifecycle_manager_cmd = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time},
                    {'autostart': autostart},
                    {'node_names': lifecycle_nodes}])

    # Create launch description
    ld = LaunchDescription()

    # Declare launch arguments
    ld.add_action(declare_namespace_cmd)
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_autostart_cmd)
    ld.add_action(declare_params_file_cmd)
    ld.add_action(declare_bt_xml_cmd)
    ld.add_action(declare_map_subscribe_transient_local_cmd)

    # Add nodes to launch description
    ld.add_action(lifecycle_manager_cmd)
    ld.add_action(navigation_cmd)
    ld.add_action(planner_cmd)
    ld.add_action(recoveries_cmd)
    ld.add_action(bt_navigator_cmd)
    ld.add_action(waypoint_follower_cmd)

    return ld
```

#### 2. Navigation Server Implementation
```python
# navigation_server.py
import rclpy
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
from action_msgs.msg import GoalStatus
import math

class IsaacNavigationServer(Node):
    def __init__(self):
        super().__init__('isaac_navigation_server')

        # Action server for navigation
        self.navigation_action_server = self.create_action_server(
            NavigateToPose,
            'navigate_to_pose',
            self.execute_navigate_to_pose_callback,
            cancel_callback=self.cancel_navigate_to_pose_callback
        )

        # Publishers and subscribers
        self.goal_pub = self.create_publisher(PoseStamped, 'goal_pose', 10)
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        # Navigation state
        self.current_pose = None
        self.target_pose = None
        self.is_navigating = False

        # Navigation parameters
        self.linear_speed = 0.5  # m/s
        self.angular_speed = 0.5  # rad/s
        self.linear_tolerance = 0.2  # m
        self.angular_tolerance = 0.1  # rad

    def execute_navigate_to_pose_callback(self, goal_handle):
        """Execute navigation to pose action"""
        self.get_logger().info('Executing navigation goal...')

        target_pose = goal_handle.request.pose

        # Plan path using Isaac Nav2
        path = self.plan_path(target_pose)

        if not path:
            self.get_logger().error('Failed to plan path to goal')
            goal_handle.abort()
            return NavigateToPose.Result()

        # Execute path following
        success = self.follow_path(path, goal_handle)

        if success:
            goal_handle.succeed()
            result = NavigateToPose.Result()
            result.result = True
            self.get_logger().info('Navigation succeeded!')
            return result
        else:
            goal_handle.abort()
            result = NavigateToPose.Result()
            result.result = False
            self.get_logger().info('Navigation failed!')
            return result

    def plan_path(self, target_pose):
        """Plan path using Isaac Nav2 with GPU acceleration"""
        # In a real implementation, this would interface with Isaac Nav2
        # For this example, we'll use a simple straight-line approach
        if self.current_pose is None:
            return None

        # Calculate path waypoints
        start_x = self.current_pose.pose.position.x
        start_y = self.current_pose.pose.position.y
        goal_x = target_pose.pose.position.x
        goal_y = target_pose.pose.position.y

        # Simple straight-line path
        path = []
        steps = max(int(abs(goal_x - start_x) / 0.1), int(abs(goal_y - start_y) / 0.1))
        steps = max(steps, 10)  # Ensure at least 10 steps

        for i in range(steps + 1):
            t = i / float(steps)
            x = start_x + t * (goal_x - start_x)
            y = start_y + t * (goal_y - start_y)

            pose = PoseStamped()
            pose.header.frame_id = 'map'
            pose.pose.position.x = x
            pose.pose.position.y = y
            path.append(pose)

        return path

    def follow_path(self, path, goal_handle):
        """Follow planned path with obstacle avoidance"""
        for i, waypoint in enumerate(path):
            # Check if navigation is canceled
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return False

            # Move to waypoint
            success = self.move_to_pose(waypoint.pose)

            if not success:
                # Try recovery behavior
                recovery_success = self.execute_recovery_behavior()
                if not recovery_success:
                    return False

            # Update progress
            progress = float(i) / len(path)
            feedback = NavigateToPose.Feedback()
            feedback.current_pose = self.current_pose
            feedback.distance_remaining = self.calculate_distance_to_goal(path[-1].pose)
            goal_handle.publish_feedback(feedback)

        return True

    def move_to_pose(self, target_pose):
        """Move robot to target pose with obstacle avoidance"""
        # Calculate distance and angle to target
        current_pos = self.current_pose.pose.position
        target_pos = target_pose.position

        dx = target_pos.x - current_pos.x
        dy = target_pos.y - current_pos.y
        distance = math.sqrt(dx*dx + dy*dy)

        # Calculate target orientation
        target_yaw = math.atan2(dy, dx)

        # Simple proportional controller
        linear_vel = min(self.linear_speed, distance * 1.0)
        angular_vel = (target_yaw - self.get_current_yaw()) * 1.0

        # Limit angular velocity
        angular_vel = max(-self.angular_speed, min(self.angular_speed, angular_vel))

        # Publish velocity command
        twist = Twist()
        twist.linear.x = linear_vel
        twist.angular.z = angular_vel
        self.cmd_vel_pub.publish(twist)

        # Wait for robot to reach position
        timeout = self.get_clock().now() + rclpy.duration.Duration(seconds=10.0)
        while self.get_clock().now() < timeout:
            current_pos = self.current_pose.pose.position
            current_yaw = self.get_current_yaw()

            # Check if reached
            curr_dx = target_pos.x - current_pos.x
            curr_dy = target_pos.y - current_pos.y
            curr_distance = math.sqrt(curr_dx*curr_dx + curr_dy*curr_dy)

            if curr_distance < self.linear_tolerance:
                break

            rclpy.spin_once(self, timeout_sec=0.1)

        # Stop robot
        stop_twist = Twist()
        self.cmd_vel_pub.publish(stop_twist)

        return True  # Simplified - in real implementation check for success

    def calculate_distance_to_goal(self, goal_pose):
        """Calculate remaining distance to goal"""
        if self.current_pose is None:
            return float('inf')

        current_pos = self.current_pose.pose.position
        goal_pos = goal_pose.position

        dx = goal_pos.x - current_pos.x
        dy = goal_pos.y - current_pos.y

        return math.sqrt(dx*dx + dy*dy)

    def get_current_yaw(self):
        """Get current robot orientation from current_pose"""
        if self.current_pose is None:
            return 0.0

        q = self.current_pose.pose.orientation
        # Convert quaternion to yaw
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        return math.atan2(siny_cosp, cosy_cosp)

    def execute_recovery_behavior(self):
        """Execute recovery behavior when navigation fails"""
        # In a real implementation, this would execute specific recovery behaviors
        # like spinning, backing up, or waiting
        self.get_logger().info('Executing recovery behavior...')

        # Example: Spin in place
        for i in range(20):  # 2 seconds of spinning
            twist = Twist()
            twist.angular.z = 0.5  # Spin at 0.5 rad/s
            self.cmd_vel_pub.publish(twist)
            rclpy.spin_once(self, timeout_sec=0.1)

        # Stop
        stop_twist = Twist()
        self.cmd_vel_pub.publish(stop_twist)

        return True  # Assume recovery successful for this example

def main(args=None):
    rclpy.init(args=args)
    node = IsaacNavigationServer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Costmap Configuration for Humanoid Robots

#### Humanoid-Specific Costmap Parameters
```yaml
# humanoid_costmap_params.yaml
global_costmap:
  global_costmap:
    ros__parameters:
      # Humanoid-specific parameters
      robot_radius: 0.4  # Radius of humanoid robot
      max_obstacle_height: 1.8  # Height of humanoid robot
      min_obstacle_height: 0.0  # Minimum obstacle to consider
      lethal_cost_threshold: 99  # Threshold for lethal obstacles
      transform_tolerance: 0.5  # Increased tolerance for humanoid balance

      plugins: ["static_layer", "obstacle_layer", "inflation_layer", "voxel_layer"]

      obstacle_layer:
        plugin: "nav2_costmap_2d::ObstacleLayer"
        enabled: True
        observation_sources: laser_scan_sensor depth_camera_sensor
        laser_scan_sensor:
          topic: "/scan"
          max_obstacle_height: 1.8
          clearing: True
          marking: True
          data_type: "LaserScan"
          raytrace_max_range: 5.0
          raytrace_min_range: 0.0
          obstacle_max_range: 4.0
          obstacle_min_range: 0.0
        depth_camera_sensor:
          topic: "/camera/depth/image_raw"
          max_obstacle_height: 1.8
          clearing: True
          marking: True
          data_type: "PointCloud2"
          expected_update_rate: 0.0
          observation_persistence: 0.0
          inf_is_valid: False
          clearing: True
          marking: True
          min_obstacle_height: 0.0
          max_obstacle_height: 1.8

local_costmap:
  local_costmap:
    ros__parameters:
      # Humanoid-specific local costmap parameters
      robot_radius: 0.3  # Smaller radius for local planning
      max_obstacle_height: 1.8
      update_frequency: 10.0  # Higher frequency for humanoid stability
      publish_frequency: 5.0

      plugins: ["obstacle_layer", "voxel_layer", "inflation_layer"]

      obstacle_layer:
        plugin: "nav2_costmap_2d::ObstacleLayer"
        enabled: True
        observation_sources: laser_scan_sensor
        laser_scan_sensor:
          topic: "/scan"
          max_obstacle_height: 1.8
          clearing: True
          marking: True
          data_type: "LaserScan"
          raytrace_max_range: 3.0
          raytrace_min_range: 0.0
          obstacle_max_range: 2.5
          obstacle_min_range: 0.0
```

## Navigation Performance Optimization

### Tuning Parameters

#### Path Planning Optimization
```yaml
# Path planning optimization parameters
planner_server:
  ros__parameters:
    GridBased:
      # Optimize for humanoid robot
      allow_unknown: false  # Don't plan through unknown areas
      use_astar: true       # A* for better path quality
      visualize_potential: false  # Disable visualization for performance

      # Costmap considerations
      costmap_weight: 2.0   # Weight of costmap vs distance
      neutral_cost: 50      # Neutral cost value
      lethal_cost: 254      # Lethal cost value
```

#### Controller Tuning
```yaml
# Controller tuning for humanoid robot
controller_server:
  ros__parameters:
    FollowPath:
      # Humanoid-specific velocity limits
      max_vel_x: 0.3        # Slower for stability
      min_vel_x: 0.1
      max_vel_theta: 0.5    # Slower turning for balance
      min_vel_theta: 0.2

      # Acceleration limits for humanoid stability
      acc_lim_x: 0.5        # Lower acceleration for balance
      acc_lim_theta: 1.0
      decel_lim_x: -0.5     # Lower deceleration for balance
      decel_lim_theta: -1.0

      # Sampling parameters
      vx_samples: 10        # Fewer samples for faster computation
      vtheta_samples: 10
```

### GPU Acceleration Settings

#### CUDA Optimization Parameters
```yaml
# GPU acceleration parameters
isaac_nav2:
  ros__parameters:
    # GPU settings
    cuda_device_id: 0
    gpu_memory_fraction: 0.8  # Use 80% of GPU memory
    enable_tensor_cores: true  # Enable tensor cores if available

    # Parallel processing settings
    num_parallel_planners: 2  # Number of parallel planners
    batch_size: 32            # Batch size for neural networks
    inference_precision: "FP16"  # Precision for inference
```

## Integration with Perception and SLAM

### SLAM Integration

#### Navigation-SLAM Coordination
```python
# slam_navigation_coordinator.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool

class SLAMNavigationCoordinator(Node):
    def __init__(self):
        super().__init__('slam_navigation_coordinator')

        # Subscriptions
        self.localization_sub = self.create_subscription(
            PoseWithCovarianceStamped, 'amcl_pose', self.localization_callback, 10)
        self.map_sub = self.create_subscription(
            OccupancyGrid, 'map', self.map_callback, 10)
        self.scan_sub = self.create_subscription(
            LaserScan, 'scan', self.scan_callback, 10)

        # Publishers
        self.navigation_active_pub = self.create_publisher(Bool, 'navigation_active', 10)
        self.slam_active_pub = self.create_publisher(Bool, 'slam_active', 10)

        # State management
        self.navigation_active = False
        self.slam_active = True
        self.robot_pose = None

        # Timer for coordination
        self.coordination_timer = self.create_timer(0.1, self.coordination_callback)

    def localization_callback(self, msg):
        """Update robot pose from localization"""
        self.robot_pose = msg.pose.pose
        self.check_navigation_readiness()

    def map_callback(self, msg):
        """Handle map updates from SLAM"""
        self.current_map = msg
        self.get_logger().info(f'Received map update: {msg.info.width}x{msg.info.height}')

    def scan_callback(self, msg):
        """Handle laser scan for navigation"""
        if self.navigation_active:
            # Forward scan to navigation system
            self.forward_scan_for_navigation(msg)

    def coordination_callback(self):
        """Coordinate SLAM and navigation activities"""
        if self.navigation_active and self.slam_active:
            # Check if navigation is safe to proceed
            if self.is_navigation_safe():
                self.enable_navigation()
            else:
                self.pause_navigation()
        elif self.navigation_active and not self.slam_active:
            # Navigation requested but SLAM not active
            self.get_logger().warn('Navigation requested but SLAM is not active')

    def is_navigation_safe(self):
        """Check if navigation is safe given current SLAM state"""
        # Check if localization is reliable
        if not self.robot_pose:
            return False

        # Check if map is sufficiently built
        if hasattr(self, 'current_map'):
            # Check map quality metrics
            occupied_cells = sum(1 for cell in self.current_map.data if cell > 50)
            total_cells = len(self.current_map.data)
            occupancy_ratio = occupied_cells / total_cells if total_cells > 0 else 0

            # Require at least 10% occupancy for reliable navigation
            return occupancy_ratio > 0.1
        else:
            return False

    def enable_navigation(self):
        """Enable navigation system"""
        msg = Bool()
        msg.data = True
        self.navigation_active_pub.publish(msg)
        self.get_logger().info('Navigation enabled')

    def pause_navigation(self):
        """Pause navigation for safety"""
        msg = Bool()
        msg.data = False
        self.navigation_active_pub.publish(msg)
        self.get_logger().info('Navigation paused for safety')

    def forward_scan_for_navigation(self, scan_msg):
        """Forward scan data to navigation system"""
        # In a real implementation, this would forward the scan
        # to the navigation costmap and local planner
        pass

    def check_navigation_readiness(self):
        """Check if robot is ready for navigation"""
        if self.robot_pose and hasattr(self, 'current_map'):
            self.get_logger().info('Robot is ready for navigation')
```

## Performance Evaluation and Metrics

### Navigation Success Metrics

#### Quantitative Metrics
```python
# navigation_metrics.py
class NavigationMetrics:
    def __init__(self):
        self.total_attempts = 0
        self.successful_navigations = 0
        self.failed_navigations = 0
        self.total_distance = 0.0
        self.total_time = 0.0
        self.path_efficiency = 0.0
        self.obstacle_avoidance_count = 0

    def calculate_success_rate(self):
        """Calculate navigation success rate"""
        if self.total_attempts == 0:
            return 0.0
        return (self.successful_navigations / self.total_attempts) * 100.0

    def calculate_time_efficiency(self):
        """Calculate average navigation time per meter"""
        if self.total_distance == 0:
            return float('inf')
        return self.total_time / self.total_distance

    def calculate_path_efficiency(self):
        """Calculate ratio of optimal path to actual path"""
        # In real implementation, compare planned path to optimal path
        return self.path_efficiency

    def calculate_obstacle_avoidance_frequency(self):
        """Calculate how often obstacle avoidance is triggered"""
        if self.total_distance == 0:
            return 0.0
        return self.obstacle_avoidance_count / self.total_distance
```

### Quality Assessment

#### Path Quality Metrics
- **Path Length**: Compare planned path length to Euclidean distance
- **Smoothness**: Measure curvature and sharp turns
- **Safety Margin**: Average distance to obstacles along path
- **Computational Efficiency**: Planning time and resource usage

#### Execution Quality Metrics
- **Tracking Accuracy**: How well robot follows planned path
- **Velocity Profiles**: Smoothness of motion execution
- **Recovery Frequency**: How often recovery behaviors are triggered
- **Goal Achievement**: Success rate in reaching targets

## Troubleshooting Common Issues

### Navigation Failures

#### Path Planning Failures
- **Problem**: Planner cannot find valid path
- **Causes**:
  - Map not properly built
  - Goal pose invalid
  - Costmap not updated
- **Solutions**:
  - Verify SLAM is active and building map
  - Check goal pose is in free space
  - Restart costmap if stuck

#### Local Planning Issues
- **Problem**: Robot oscillates or gets stuck
- **Causes**:
  - Local minima in costmap
  - High obstacle density
  - Controller parameters too aggressive
- **Solutions**:
  - Tune local planner parameters
  - Increase inflation radius
  - Enable recovery behaviors

### Performance Issues

#### Slow Planning
- **Problem**: Long planning times
- **Solutions**:
  - Use GPU acceleration if available
  - Simplify costmap resolution
  - Use approximate planners
  - Limit planning horizon

#### Poor Tracking
- **Problem**: Robot deviates from path
- **Solutions**:
  - Tune controller parameters
  - Improve odometry quality
  - Increase local costmap size
  - Reduce navigation speed

### Integration Problems

#### SLAM-Navigation Conflicts
- **Problem**: SLAM and navigation interfere with each other
- **Solutions**:
  - Coordinate activity scheduling
  - Use separate costmap layers
  - Implement proper state management
  - Add safety timeouts

## Best Practices for Humanoid Navigation

### System Design Guidelines

#### Architecture Considerations
- Use layered navigation architecture
- Implement proper state machines
- Coordinate SLAM and navigation activities
- Plan for graceful degradation

#### Performance Optimization
- Use GPU acceleration where possible
- Optimize costmap resolution
- Implement efficient path smoothing
- Use predictive models for dynamic obstacles

### Safety and Reliability

#### Safety Measures
- Implement emergency stops
- Use conservative parameters
- Monitor navigation health
- Plan for sensor failures

#### Robustness
- Test in various environments
- Handle edge cases gracefully
- Implement fallback strategies
- Monitor system health continuously

## Exercises

### Exercise 1: Navigation Configuration

**Difficulty**: Intermediate
**Estimated Time**: 20 minutes
**Requirements**: Isaac Nav2 installation and robot simulation

Steps:
1. Configure Nav2 parameters for humanoid robot navigation
2. Set up costmap parameters appropriate for humanoid dimensions
3. Configure path planning and execution parameters
4. Launch navigation system in simulation
5. Verify all navigation components initialize correctly

**Expected Outcome**: Students will configure and launch a navigation system with proper humanoid-specific parameters.

### Exercise 2: Navigation Performance Evaluation

**Difficulty**: Advanced
**Estimated Time**: 30 minutes
**Requirements**: Navigation system with ground truth data

Steps:
1. Navigate robot to multiple goal positions
2. Record navigation metrics (success rate, path efficiency, etc.)
3. Analyze obstacle avoidance behavior
4. Evaluate recovery behavior effectiveness
5. Identify optimization opportunities

**Expected Outcome**: Students will evaluate navigation system performance and identify areas for improvement.

## Resources

- Navigation2 Documentation: https://navigation.ros.org/. Comprehensive documentation for Navigation2 framework and components.

- Isaac Navigation User Guide: https://docs.omniverse.nvidia.com/isaacsim/latest/isaac_navigation.html. Official guide for Isaac Navigation integration.

- Path Planning for Mobile Robots: A Comprehensive Review. Academic survey of path planning algorithms and techniques.

- Humanoid Robot Navigation: Challenges and Solutions. Research paper on humanoid-specific navigation challenges.

## Summary

Navigation with Nav2 provides a comprehensive framework for mobile robot navigation, with special considerations for humanoid robots. The system integrates path planning, obstacle avoidance, and execution control in a modular architecture that can be optimized for specific robot platforms.

Isaac Nav2 adds GPU acceleration and deep learning integration, enhancing performance and capabilities for complex navigation tasks. Proper configuration of costmaps, controllers, and planners is essential for successful navigation, especially for humanoid robots with unique kinematic and stability constraints.

The integration with SLAM systems enables autonomous navigation in unknown environments, while proper performance evaluation ensures the system meets operational requirements. Troubleshooting common issues and following best practices leads to robust and reliable navigation systems.

The next chapter will explore perception-to-action integration, connecting vision, SLAM, and navigation modules for complete autonomous robot operation.