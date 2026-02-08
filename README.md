# Agilebot MCP Server

Agilebot MCP Server 是一个基于 MCP (Model Context Protocol) 的捷勃特机器人控制中间件，旨在让 AI 大模型能够通过自然语言更方便地与 Agilebot 机器人交互，实现智能机器人控制。

## 功能特点

- **自然语言控制**：通过 MCP 协议，支持 AI 大模型以自然语言方式控制机器人
- **完整的机器人控制接口**：机器人连接与断开、状态查询、关节空间运动、笛卡尔空间运动、位置查询、机器人信息查询
- **寄存器操作**：R寄存器、MR寄存器、PR寄存器、MODBUS寄存器的读写操作
- **锁轴功能**：获取和修改锁轴状态、启用/禁用拖动示教
- **坐标系管理**：获取、添加、删除、更新用户/工具坐标系
- **负载管理**：创建、删除、激活、获取负载信息、检查3轴是否水平、负载测定等所有操作
- **日志记录**：详细记录服务器运行状态和操作历史
- **错误处理**：完善的错误处理机制，提供友好的错误提示

## 功能分类表格

| 工具ID | 功能分类 | 功能描述 | 关键参数 |
|--------|----------|----------|----------|
| connect_robot_tool | 连接管理 | 连接捷勃特机器人 | ip:机器人IP |
| disconnect_robot_tool | 连接管理 | 断开捷勃特机器人连接 | ip:机器人IP |
| get_status_tool | 状态监控 | 获取机器人运行状态 | ip:机器人IP |
| get_controller_info_tool | 状态监控 | 获取控制器运行状态 | ip:机器人IP |
| get_current_joint_positions_tool | 状态监控 | 获取机器人当前关节位置 | ip:机器人IP |
| get_current_cartesian_position_tool | 状态监控 | 获取机器人当前笛卡尔位置 | ip:机器人IP |
| get_robot_info_tool | 状态监控 | 获取机器人型号信息 | ip:机器人IP |
| get_servo_status_tool | 状态监控 | 获取伺服控制器状态 | ip:机器人IP |
| move_robot_joint | 运动控制 | 关节空间运动 | ip:机器人IP, joint_positions:关节位置JSON, speed:速度, accel:加速度 |
| move_robot_cartesian | 运动控制 | 笛卡尔空间运动 | ip:机器人IP, position:笛卡尔位置JSON, posture:形态JSON, speed:速度, accel:加速度 |
| power_on_robot_tool | 电源控制 | 机器人上电 | ip:机器人IP |
| power_off_robot_tool | 电源控制 | 机器人断电 | ip:机器人IP |
| servo_reset_tool | 电源控制 | 伺服复位 | ip:机器人IP |
| acquire_access_tool | 权限管理 | 上位机获取操作权限 | ip:机器人IP |
| release_access_tool | 权限管理 | 上位机返还操作权限 | ip:机器人IP |
| read_R | 寄存器操作 | 读取R寄存器（数值寄存器） | ip:机器人IP, index:寄存器编号 |
| write_R | 寄存器操作 | 写入R寄存器（数值寄存器） | ip:机器人IP, index:寄存器编号, value:数值 |
| delete_R | 寄存器操作 | 删除R寄存器（数值寄存器） | ip:机器人IP, index:寄存器编号 |
| read_MR | 寄存器操作 | 读取MR寄存器（运动寄存器） | ip:机器人IP, index:寄存器编号 |
| write_MR | 寄存器操作 | 写入MR寄存器（运动寄存器） | ip:机器人IP, index:寄存器编号, value:整数值 |
| delete_MR | 寄存器操作 | 删除MR寄存器（运动寄存器） | ip:机器人IP, index:寄存器编号 |
| read_PR | 寄存器操作 | 读取PR寄存器（位姿寄存器） | ip:机器人IP, index:寄存器编号 |
| write_PR | 寄存器操作 | 写入PR寄存器（位姿寄存器） | ip:机器人IP, index:寄存器编号, pose_data:位姿数据JSON |
| delete_PR | 寄存器操作 | 删除PR寄存器（位姿寄存器） | ip:机器人IP, index:寄存器编号 |
| read_modbus_coils_tool | Modbus通信 | 读取Modbus线圈寄存器 | ip:机器人IP, channel:通道, slave_id:从机ID, address:地址, number:数量 |
| write_modbus_coils_tool | Modbus通信 | 写入Modbus线圈寄存器 | ip:机器人IP, channel:通道, slave_id:从机ID, address:地址, values:值列表JSON |
| read_modbus_holding_regs_tool | Modbus通信 | 读取Modbus保持寄存器 | ip:机器人IP, channel:通道, slave_id:从机ID, address:地址, number:数量 |
| write_modbus_holding_regs_tool | Modbus通信 | 写入Modbus保持寄存器 | ip:机器人IP, channel:通道, slave_id:从机ID, address:地址, values:值列表JSON |
| read_modbus_discrete_inputs_tool | Modbus通信 | 读取Modbus离散寄存器 | ip:机器人IP, channel:通道, slave_id:从机ID, address:地址, number:数量 |
| read_modbus_input_regs_tool | Modbus通信 | 读取Modbus输入寄存器 | ip:机器人IP, channel:通道, slave_id:从机ID, address:地址, number:数量 |
| get_drag_status_tool | 锁轴功能 | 获取当前机器人轴锁定状态 | ip:机器人IP |
| set_drag_status_tool | 锁轴功能 | 设定当前机器人轴锁定状态 | ip:机器人IP, cart_x/y/z/a/b/c:笛卡尔轴状态, joint_j1/j2/j3/j4/j5/j6:关节轴状态 |
| enable_drag_tool | 锁轴功能 | 启用或禁用拖动示教模式 | ip:机器人IP, enable:启用/禁用 |
| get_coordinate_list_tool | 坐标系管理 | 获取用户/工具坐标系列表 | ip:机器人IP, sys_type:坐标系类型(0=用户,1=工具) |
| add_coordinate_tool | 坐标系管理 | 添加用户/工具坐标系 | ip:机器人IP, sys_type:坐标系类型(0=用户,1=工具) |
| delete_coordinate_tool | 坐标系管理 | 删除用户/工具坐标系 | ip:机器人IP, sys_type:坐标系类型, coordinate_id:坐标系编号 |
| update_coordinate_tool | 坐标系管理 | 更新用户/工具坐标系 | ip:机器人IP, sys_type:坐标系类型, coordinate_data:坐标系数据JSON |
| get_coordinate_tool | 坐标系管理 | 获取指定的用户/工具坐标系 | ip:机器人IP, sys_type:坐标系类型, coordinate_id:坐标系编号 |
| get_current_payload_tool | 负载管理 | 获取当前激活的负载编号 | ip:机器人IP |
| get_payload_by_id_tool | 负载管理 | 根据指定编号获取负载信息 | ip:机器人IP, payload_id:负载ID编号 |
| set_current_payload_tool | 负载管理 | 根据指定编号激活负载 | ip:机器人IP, payload_id:负载ID编号 |
| add_payload_tool | 负载管理 | 添加用户自定义负载信息 | ip:机器人IP, payload_info:负载信息JSON |
| delete_payload_tool | 负载管理 | 删除指定编号的负载信息 | ip:机器人IP, payload_id:负载ID编号 |
| update_payload_tool | 负载管理 | 更新已存在的负载信息 | ip:机器人IP, payload_info:负载信息JSON |
| get_all_payload_tool | 负载管理 | 获取所有负载信息 | ip:机器人IP |
| check_axis_three_horizontal_tool | 负载管理 | 检测3轴是否水平 | ip:机器人IP |
| get_payload_identify_state_tool | 负载管理 | 获取负载测定状态 | ip:机器人IP |
| start_payload_identify_tool | 负载管理 | 开始负载测定 | ip:机器人IP, weight:负载重量, angle:转动角度 |
| get_payload_identify_result_tool | 负载管理 | 获取负载测定结果 | ip:机器人IP |
| interference_check_for_payload_identify_tool | 负载管理 | 负载测定干涉检查 | ip:机器人IP, weight:负载重量, angle:转动角度 |
| payload_identify_start_tool | 负载管理 | 进入负载测定状态 | ip:机器人IP |
| payload_identify_done_tool | 负载管理 | 结束负载测定状态 | ip:机器人IP |
| payload_identify_tool | 负载管理 | 负载测定全流程 | ip:机器人IP, weight:负载重量, angle:转动角度 |

## 安装

### 环境要求

- Python 3.10+（推荐 Python 3.10）
- Windows 10+ 或 Linux (Ubuntu 18.04+)

### 安装步骤

1. **克隆或下载项目**

2. **安装依赖**

   ```bash
   cd Agilebot-mcp
   pip install -r requirements.txt
   ```

3. **安装 Agilebot SDK**

   请参考捷勃特机器人提供的 SDK 说明文档，安装对应的 Python SDK：

   ```bash
   pip install Agilebot.SDK.A-x.x.x-py3-none-any.whl
   ```

4. **安装 MCP Server**

   ```bash
   pip install -e .
   ```

## 使用

### 启动 MCP Server

```bash
python -m agilebot_mcp
```

### 在 AI 客户端中使用

启动服务器后，您可以在支持 MCP 协议的 AI 客户端中连接该服务器，并通过自然语言控制 Agilebot 机器人。

例如：

- 请帮我连接 IP 为 192.168.1.100 的捷勃特机器人
- 请让机器人移动到关节位置 [0, -90, 90, 0, 0, 0]
- 请让机器人移动到笛卡尔位置 [300, 0, 300, 0, 180, 0]
- 创建一个名称为料盘1的用户坐标
- 创建一个名称为Gripper的工具坐标
- 锁定X轴
- 获取PR1的关节及笛卡尔坐标

## 项目结构

```
Agilebot-mcp/
├── src/
│   └── agilebot_mcp/
│       ├── __init__.py           # 包初始化文件
│       ├── server.py             # MCP 服务器主文件
│       ├── robot_core.py         # 核心机器人控制模块
│       ├── registers.py          # 寄存器操作模块
│       ├── modbus.py             # Modbus通信模块
│       ├── drag_control.py       # 拖动示教和锁轴模块
│       ├── coordinate_system.py   # 坐标系管理模块
│       ├── payload.py            # 负载管理模块
│       └── mcp_tools.py         # MCP工具包装模块
├── logs/                     # 日志目录
├── .gitignore                # Git 忽略文件
├── LICENSE                   # 许可证
├── pyproject.toml            # 项目配置
├── requirements.txt          # 依赖列表
└── README.md                 # 项目说明
```

## 日志

服务器运行日志保存在项目根目录下的 `logs/agilebot_mcp_server.log` 文件中。

## 开发

### 代码结构

- **robot_core.py**: 核心机器人控制模块，包含机器人连接、状态查询、运动控制等功能
- **registers.py**: 寄存器操作模块，包含R、MR、PR寄存器的读写操作
- **modbus.py**: Modbus通信模块，包含各种Modbus寄存器的读写操作
- **drag_control.py**: 拖动示教和锁轴模块，包含拖动控制和轴锁定功能
- **coordinate_system.py**: 坐标系管理模块，包含用户/工具坐标系的增删改查功能
- **payload.py**: 负载管理模块，包含负载的创建、删除、激活、获取信息、3轴水平检查、负载测定等功能
- **mcp_tools.py**: MCP工具包装模块，将所有底层功能包装为MCP工具
- **server.py**: MCP服务器主文件，负责启动服务器和日志配置
- **__init__.py**: 包的初始化文件，定义了版本和导出接口

### 扩展开发

如果需要扩展功能，可以在相应的模块文件中添加新的函数，并在 `mcp_tools.py` 中使用 `@mcp.tool()` 装饰器注册为 MCP 工具。

## 注意事项

1. 确保机器人已正确连接到网络，并且 IP 地址配置正确
2. 使用前请确保机器人处于安全状态，避免发生碰撞
3. 运动参数（速度、加速度）请根据实际情况设置，避免过快的运动
4. 笛卡尔空间运动时，请注意姿态参数的正确性
5. 所有工具均需先建立机器人连接后才能使用

## 许可证

MIT License

## 联系方式

如有问题或建议，请联系：

- 邮箱：your.email@example.com
