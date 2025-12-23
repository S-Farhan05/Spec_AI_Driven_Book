---
title: Chapter 6 - Humanoid Modeling with URDF
sidebar_position: 6
description: Defining robot structure, joints, and sensors using URDF
tags: [ros2, urdf, humanoid, modeling, robotics]
---

# Humanoid Modeling with URDF

## Learning Objectives

- Understand the Unified Robot Description Format (URDF) for robot modeling
- Create URDF files that define humanoid robot structure
- Define joints, links, and sensors in URDF
- Apply best practices for humanoid robot modeling
- Validate and visualize URDF models

## Content

### Introduction to URDF

The Unified Robot Description Format (URDF) is an XML-based format used in ROS to describe robot models. URDF defines the physical and visual properties of a robot, including its links (rigid parts), joints (connections between links), and other components like sensors and actuators. For humanoid robots, URDF is particularly important as it allows for precise definition of the complex kinematic structure with multiple degrees of freedom.

URDF serves as the foundation for robot simulation, visualization, motion planning, and control. A well-defined URDF model enables:
- Accurate physics simulation in environments like Gazebo
- Proper visualization in tools like RViz
- Kinematic analysis and inverse kinematics calculations
- Collision detection and avoidance algorithms

### URDF Structure and Components

A URDF file consists of several key components:

**Links**: Represent rigid parts of the robot. Each link has:
- Visual properties (shape, color, mesh) for visualization
- Collision properties for physics simulation
- Inertial properties (mass, center of mass, inertia tensor) for dynamics

**Joints**: Define how links connect and move relative to each other. Joint types include:
- **Fixed**: No movement between links
- **Revolute**: Rotational movement around a single axis
- **Continuous**: Unlimited rotational movement (like a wheel)
- **Prismatic**: Linear sliding movement along an axis
- **Floating**: 6 degrees of freedom movement
- **Planar**: Movement in a plane

**Materials**: Define visual appearance properties like color and texture.

### Basic URDF Structure

A basic URDF file follows this structure:

```xml
<?xml version="1.0"?>
<robot name="my_robot">
  <!-- Define materials -->
  <material name="blue">
    <color rgba="0.0 0.0 1.0 1.0"/>
  </material>

  <!-- Define links -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
      <material name="blue"/>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10.0"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
  </link>

  <!-- Define joints -->
  <joint name="base_to_wheel" type="continuous">
    <parent link="base_link"/>
    <child link="wheel_link"/>
    <origin xyz="0 0.2 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
  </joint>

  <link name="wheel_link">
    <visual>
      <geometry>
        <cylinder length="0.1" radius="0.1"/>
      </geometry>
    </visual>
  </link>
</robot>
```

### URDF for Humanoid Robots

Humanoid robots have complex kinematic structures that require careful modeling. A typical humanoid URDF includes:

**Torso**: The main body with head, arms, and legs connected
**Head**: Usually with sensors like cameras
**Arms**: Shoulders, elbows, wrists, and hands/fingers
**Legs**: Hips, knees, ankles, and feet

The kinematic chain typically starts from the world frame or a fixed base (often the pelvis or torso for humanoids) and branches out to the limbs.

### Defining Links in URDF

Links represent rigid bodies in the robot. For each link, you typically define:

**Visual elements**: How the link appears in visualization:
```xml
<visual>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <geometry>
    <box size="0.1 0.1 0.1"/>
    <!-- Other options: <cylinder>, <sphere>, <mesh> -->
  </geometry>
  <material name="my_material"/>
</visual>
```

**Collision elements**: Used for physics simulation:
```xml
<collision>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <geometry>
    <box size="0.1 0.1 0.1"/>
  </geometry>
</collision>
```

**Inertial elements**: Physical properties for dynamics:
```xml
<inertial>
  <mass value="1.0"/>
  <origin xyz="0 0 0" rpy="0 0 0"/>
  <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
</inertial>
```

### Defining Joints in URDF

Joints connect links and define their relative motion. A joint definition includes:

- **Parent and child links**: Which links the joint connects
- **Joint type**: The type of motion allowed
- **Origin**: Position and orientation of the joint relative to the parent link
- **Axis**: Motion axis for revolute and prismatic joints
- **Limits**: For revolute joints (min/max angle, effort, velocity)

Example of a revolute joint for an elbow:
```xml
<joint name="elbow_joint" type="revolute">
  <parent link="upper_arm"/>
  <child link="forearm"/>
  <origin xyz="0.3 0 0" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-2.0" upper="1.0" effort="100" velocity="3.0"/>
  <dynamics damping="0.1" friction="0.0"/>
</joint>
```

### URDF for Humanoid Kinematics

Humanoid robots require special attention to kinematic chains. A common approach is to use a tree structure starting from the torso:

```
torso
├── head
├── left_upper_arm
│   └── left_forearm
│       └── left_hand
├── right_upper_arm
│   └── right_forearm
│       └── right_hand
├── left_thigh
│   └── left_shin
│       └── left_foot
└── right_thigh
    └── right_shin
        └── right_foot
```

Each chain represents a kinematic branch that can be controlled independently.

### Gazebo-Specific Elements

For simulation in Gazebo, URDF can include Gazebo-specific elements:

```xml
<gazebo reference="my_link">
  <material>Gazebo/Blue</material>
  <mu1>0.9</mu1>
  <mu2>0.9</mu2>
</gazebo>
```

### Xacro: URDF's Macro System

For complex humanoid models, Xacro (XML Macros) is essential. Xacro allows:
- Variable definitions
- Macros and properties
- Mathematical expressions
- Inclusion of other Xacro files

Example Xacro usage:
```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="humanoid">

  <xacro:property name="M_PI" value="3.1415926535897931" />
  <xacro:property name="arm_length" value="0.3" />

  <xacro:macro name="simple_arm" params="prefix parent_link">
    <joint name="${prefix}_shoulder_joint" type="revolute">
      <parent link="${parent_link}"/>
      <child link="${prefix}_upper_arm"/>
      <origin xyz="0.2 0 0" rpy="0 0 0"/>
      <axis xyz="0 1 0"/>
      <limit lower="${-M_PI/2}" upper="${M_PI/2}" effort="100" velocity="3.0"/>
    </joint>

    <link name="${prefix}_upper_arm">
      <visual>
        <geometry>
          <cylinder length="0.3" radius="0.05"/>
        </geometry>
      </visual>
    </link>
  </xacro:macro>

  <xacro:simple_arm prefix="left" parent_link="torso"/>
  <xacro:simple_arm prefix="right" parent_link="torso"/>

</robot>
```

### Sensors in URDF

Sensors can be attached to links in URDF, though the specific sensor plugin configuration is often done in Gazebo:

```xml
<link name="camera_link">
  <visual>
    <geometry>
      <box size="0.02 0.05 0.02"/>
    </geometry>
  </visual>
</link>

<joint name="head_camera_joint" type="fixed">
  <parent link="head"/>
  <child link="camera_link"/>
  <origin xyz="0.05 0 0.05" rpy="0 0 0"/>
</joint>

<gazebo reference="camera_link">
  <sensor type="camera" name="head_camera">
    <visualize>true</visualize>
    <update_rate>30.0</update_rate>
    <camera name="head_camera">
      <horizontal_fov>1.3962634</horizontal_fov>
      <image>
        <width>800</width>
        <height>600</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.02</near>
        <far>300</far>
      </clip>
    </camera>
  </sensor>
</gazebo>
```

### Validation and Visualization

URDF models should be validated before use:

1. **Syntax validation**: Check XML syntax
2. **Kinematic validation**: Ensure the model has a proper kinematic tree
3. **Collision checking**: Verify no links intersect in default pose
4. **Dynamics validation**: Check inertial properties make sense

Tools for validation:
- `check_urdf` command: Basic URDF syntax and structure check
- RViz: Visualize the robot model
- Gazebo: Test physics simulation
- Robot State Publisher: Publish joint states for visualization

### Best Practices for Humanoid URDF

1. **Start Simple**: Begin with a basic skeleton and add complexity gradually
2. **Use Xacro**: For complex humanoid models, Xacro is essential for maintainability
3. **Realistic Inertials**: Use proper mass properties based on real robot specifications
4. **Consistent Naming**: Use a consistent naming convention for joints and links
5. **Documentation**: Comment complex URDF files to explain the structure
6. **Validation**: Always validate URDF files before simulation
7. **Simplified Collision Models**: Use simple geometric shapes for collision detection to improve performance

### Practical Example: Simple Humanoid

Here's a basic humanoid model structure:

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Constants -->
  <xacro:property name="torso_height" value="0.5"/>
  <xacro:property name="torso_radius" value="0.15"/>
  <xacro:property name="arm_length" value="0.4"/>
  <xacro:property name="leg_length" value="0.6"/>

  <!-- Base link -->
  <link name="base_link"/>

  <!-- Torso -->
  <joint name="torso_joint" type="fixed">
    <parent link="base_link"/>
    <child link="torso"/>
    <origin xyz="0 0 ${torso_height/2}" rpy="0 0 0"/>
  </joint>

  <link name="torso">
    <visual>
      <geometry>
        <cylinder length="${torso_height}" radius="${torso_radius}"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <cylinder length="${torso_height}" radius="${torso_radius}"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10.0"/>
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
  </link>

  <!-- Head -->
  <joint name="neck_joint" type="revolute">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0 0 ${torso_height/2 + 0.1}" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-0.5" upper="0.5" effort="10" velocity="1.0"/>
  </joint>

  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
    </visual>
  </link>

  <!-- Left Arm -->
  <joint name="left_shoulder_joint" type="revolute">
    <parent link="torso"/>
    <child link="left_upper_arm"/>
    <origin xyz="${torso_radius} 0 ${torso_height*0.3}" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="10" velocity="1.0"/>
  </joint>

  <link name="left_upper_arm">
    <visual>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
      <origin xyz="0 0 0.15" rpy="1.57 0 0"/>
    </visual>
  </link>

  <joint name="left_elbow_joint" type="revolute">
    <parent link="left_upper_arm"/>
    <child link="left_forearm"/>
    <origin xyz="0 0 0.3" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="10" velocity="1.0"/>
  </joint>

  <link name="left_forearm">
    <visual>
      <geometry>
        <cylinder length="0.3" radius="0.04"/>
      </geometry>
      <origin xyz="0 0 0.15" rpy="1.57 0 0"/>
    </visual>
  </link>

  <!-- Similar definitions for right arm, legs, etc. -->

</robot>
```

## Acceptance Scenarios

1. **Given** requirements for a humanoid robot, **When** student creates a URDF file, **Then** it correctly defines the robot's structure, joints, and sensors
2. **Given** a URDF file, **When** student loads it in a simulator, **Then** the robot model displays correctly with proper joint configurations

## Summary

This chapter covered the Unified Robot Description Format (URDF) for defining humanoid robot models. We explored the structure of URDF files, including links, joints, and sensors, with specific focus on humanoid robot modeling. The use of Xacro for complex models and best practices for validation were also discussed.

## Further Reading

- ROS Documentation. (2023). URDF Tutorials. Retrieved from http://wiki.ros.org/urdf/Tutorials
- Smith, T., & Mistry, M. (2019). Robot Modeling and Control with URDF. IEEE Robotics & Automation Magazine.
- Hornung, A., et al. (2013). Octomap: An Efficient Probabilistic 3D Mapping Framework Based on Octrees. Autonomous Robots Journal.