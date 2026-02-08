---
name: "agilebot-robot-control"
description: "Controls Agilebot robots via MCP protocol. Invoke when user needs to connect, power on/off, move robot, or query robot status."
---

# Agilebot Robot Control

This skill provides comprehensive control for Agilebot robots through the MCP (Model Context Protocol) server. It enables AI assistants to interact with Agilebot robots using natural language commands.

## Available Functions

### Connection Management
- **connect_robot(ip)**: Connect to robot at specified IP address
- **disconnect_robot(ip)**: Disconnect from robot
- **test_connect(ip)**: Test network connectivity and robot connection

### Power Control
- **power_on_robot(ip)**: Power on the robot servos
- **power_off_robot(ip)**: Power off the robot servos
- **servo_reset(ip)**: Reset servo status

### Motion Control
- **move_robot_joint(ip, joint_positions, speed, accel)**: Move robot in joint space
  - joint_positions: JSON string format [j1, j2, j3, j4, j5, j6]
  - speed: 0-100, default 10
  - accel: 0-100, default 10

- **move_robot_cartesian(ip, position, posture, speed, accel)**: Move robot in Cartesian space
  - position: JSON string format [x, y, z, a, b, c]
  - posture: JSON string format (optional)
  - speed: 0-100, default 10
  - accel: 0-100, default 10

- **move_to_target_joint(ip)**: Move to predefined target joint position
- **move_robot_direct(ip, joint_positions)**: Direct joint movement with automatic state handling

### Status Query
- **get_status(ip)**: Get robot running status
- **get_controller_info(ip)**: Get controller status
- **get_servo_status(ip)**: Get servo controller status
- **get_current_joint_positions(ip)**: Get current joint positions
- **get_current_cartesian_position(ip)**: Get current Cartesian position
- **get_robot_info(ip)**: Get robot model information
- **get_robot_status(ip)**: Get comprehensive robot status

### Access Control
- **acquire_access(ip)**: Acquire operation permission
- **release_access(ip)**: Release operation permission

### Other Functions
- **reset_estop(ip)**: Reset emergency stop status
- **get_soft_mode(ip)**: Get current soft mode
- **set_soft_mode(ip, mode)**: Set soft mode
- **get_version(ip)**: Get controller version
- **switch_led_light(ip, mode)**: Control LED indicator

## Usage Examples

### Basic Connection and Power On
```python
# Connect to robot
connect_robot("10.27.1.2")

# Power on the robot
power_on_robot("10.27.1.2")
```

### Joint Space Movement
```python
# Move to joint position
move_robot_joint("10.27.1.2", "[0, -90, 90, 0, 0, 0]", speed=10, accel=10)

# Move to specific joint positions
move_robot_joint("10.27.1.2", "[17, 78, -62, 71, -89, 79]", speed=10, accel=10)
```

### Cartesian Space Movement
```python
# Move to Cartesian position
move_robot_cartesian("10.27.1.2", "[300, 0, 300, 0, 180, 0]", speed=10, accel=10)
```

### Status Query
```python
# Get current joint positions
get_current_joint_positions("10.27.1.2")

# Get robot status
get_robot_status("10.27.1.2")

# Get controller info
get_controller_info("10.27.1.2")
```

## Common Workflows

### Complete Movement Workflow
1. Connect to robot: `connect_robot(ip)`
2. Acquire access: `acquire_access(ip)`
3. Reset emergency stop if needed: `reset_estop(ip)`
4. Power on robot: `power_on_robot(ip)`
5. Execute movement: `move_robot_joint(ip, positions)`
6. Release access: `release_access(ip)`
7. Disconnect: `disconnect_robot(ip)`

### Troubleshooting
- If connection fails: Check network connectivity with `test_connect(ip)`
- If power on fails: Check controller status with `get_controller_info(ip)`
- If movement fails: Check servo status with `get_servo_status(ip)`
- If robot is in emergency stop: Use `reset_estop(ip)` first

## Error Handling

All functions return JSON-formatted responses:
```json
{
  "status": "success" | "error",
  "message": "Description of result or error",
  "data": {}  // Additional data if applicable
}
```

Common error messages:
- "请先连接机器人" - Robot not connected
- "机器人连接失败" - Connection failed
- "机器人上电失败" - Power on failed
- "关节运动指令发送失败" - Movement command failed

## Notes

- Ensure robot is properly connected before executing any operations
- Always check robot status before movement operations
- Use appropriate speed and acceleration values for safety
- Emergency stop must be reset before power on operations
- Release access permission when operations are complete