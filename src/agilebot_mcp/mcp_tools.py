# -*- coding: utf-8 -*-
import json
import logging
from mcp.server.fastmcp import FastMCP

from .robot_core import (
    connect_robot, disconnect_robot, get_status, get_controller_info,
    get_current_joint_positions, get_current_cartesian_position,
    move_joint, move_cartesian, power_off_robot, power_on_robot,
    get_servo_status, get_robot_info, servo_reset,
    acquire_access, release_access, check_robot_ready
)
from .registers import (
    read_R_register, write_R_register, delete_R_register,
    read_MR_register, write_MR_register, delete_MR_register,
    read_PR_register, write_PR_register, delete_PR_register
)
from .modbus import (
    read_modbus_coils, write_modbus_coils,
    read_modbus_holding_regs, write_modbus_holding_regs,
    read_modbus_discrete_inputs, read_modbus_input_regs
)
from .drag_control import (
    get_drag_status, set_drag_status, enable_drag
)
from .coordinate_system import (
    get_coordinate_list, add_coordinate, delete_coordinate,
    update_coordinate, get_coordinate
)
from .payload import (
    get_current_payload, get_payload_by_id, set_current_payload,
    add_payload, delete_payload, update_payload, get_all_payload,
    check_axis_three_horizontal, get_payload_identify_state,
    start_payload_identify, get_payload_identify_result,
    interference_check_for_payload_identify, payload_identify_start,
    payload_identify_done, payload_identify
)

logger = logging.getLogger(__name__)

mcp = FastMCP(
    "agilebot_mcp_server",
    description="Control Agilebot robots through Model Context Protocol"
)


@mcp.tool()
def connect_robot_tool(ip: str):
    """连接捷勃特机器人
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 连接结果
    """
    return connect_robot(ip)


@mcp.tool()
def disconnect_robot_tool(ip: str):
    """断开与捷勃特机器人的连接
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 断开结果
    """
    return disconnect_robot(ip)


@mcp.tool()
def get_status_tool(ip: str):
    """获取机器人运行状态
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 机器人状态信息
    """
    return get_status(ip)


@mcp.tool()
def get_controller_info_tool(ip: str):
    """获取控制器运行状态
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 控制器状态信息
    """
    return get_controller_info(ip)


@mcp.tool()
def get_current_joint_positions_tool(ip: str):
    """获取机器人当前关节位置
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 关节位置信息
    """
    return get_current_joint_positions(ip)


@mcp.tool()
def get_current_cartesian_position_tool(ip: str):
    """获取机器人当前笛卡尔位置
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 笛卡尔位置信息
    """
    return get_current_cartesian_position(ip)


@mcp.tool()
def move_robot_joint(ip: str, joint_positions: str, speed: int = 50, accel: float = 0.5):
    """关节空间运动
    
    参数:
        ip: 机器人控制柜IP地址
        joint_positions: JSON字符串格式的关节位置 [j1, j2, j3, j4, j5, j6]
        speed: 运动速度 (0-100)，默认50
        accel: 运动加速度 (0-1)，默认0.5
        
    返回:
        str: 运动结果
    """
    try:
        positions = json.loads(joint_positions)
        if not isinstance(positions, list) or len(positions) != 6:
            return json.dumps({"status": "error", "message": "关节位置格式错误，应为长度为6的数组"}, ensure_ascii=False)
        if not all(isinstance(pos, (int, float)) for pos in positions):
            return json.dumps({"status": "error", "message": "关节位置格式错误，所有元素应为数字"}, ensure_ascii=False)
        
        check_robot_ready(ip)
        return move_joint(ip, positions, speed, accel)
        
    except json.JSONDecodeError:
        return json.dumps({"status": "error", "message": "关节位置格式错误，应为JSON字符串"}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"关节运动时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"关节运动时发生异常: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
def move_robot_cartesian(ip: str, position: str, posture: str = None, speed: int = 50, accel: float = 0.5):
    """笛卡尔空间运动
    
    参数:
        ip: 机器人控制柜IP地址
        position: JSON字符串格式的笛卡尔位置 [x, y, z, a, b, c]
        posture: JSON字符串格式的机器人形态参数（可选）
        speed: 运动速度 (0-100)，默认50
        accel: 运动加速度 (0-1)，默认0.5
        
    返回:
        str: 运动结果
    """
    try:
        positions = json.loads(position)
        if not isinstance(positions, list) or len(positions) != 6:
            return json.dumps({"status": "error", "message": "笛卡尔位置格式错误，应为长度为6的数组"}, ensure_ascii=False)
        
        posture_dict = json.loads(posture) if posture else None
        check_robot_ready(ip)
        return move_cartesian(ip, positions, posture_dict, speed, accel)
        
    except json.JSONDecodeError:
        return json.dumps({"status": "error", "message": "位置格式错误，应为JSON字符串"}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"笛卡尔运动时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"笛卡尔运动时发生异常: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
def power_off_robot_tool(ip: str):
    """机器人断电
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 断电结果
    """
    return power_off_robot(ip)


@mcp.tool()
def power_on_robot_tool(ip: str):
    """机器人上电
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 上电结果
    """
    return power_on_robot(ip)


@mcp.tool()
def get_servo_status_tool(ip: str):
    """获取伺服控制器状态
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 伺服状态信息
    """
    return get_servo_status(ip)


@mcp.tool()
def get_robot_info_tool(ip: str):
    """获取机器人型号信息
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 机器人型号信息
    """
    return get_robot_info(ip)


@mcp.tool()
def servo_reset_tool(ip: str):
    """复位伺服状态
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 复位结果
    """
    return servo_reset(ip)


@mcp.tool()
def acquire_access_tool(ip: str):
    """上位机获取操作权限
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 获取权限结果
    """
    return acquire_access(ip)


@mcp.tool()
def release_access_tool(ip: str):
    """上位机返还操作权限
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 返还权限结果
    """
    return release_access(ip)


@mcp.tool()
def read_R(ip: str, index: int):
    """读取R寄存器（数值寄存器）的值
    
    参数:
        ip: 机器人控制柜IP地址
        index: R寄存器的编号
        
    返回:
        str: R寄存器的值
    """
    return read_R_register(ip, index)


@mcp.tool()
def write_R(ip: str, index: int, value: float):
    """写入R寄存器（数值寄存器）的值
    
    参数:
        ip: 机器人控制柜IP地址
        index: R寄存器的编号
        value: 需要写入的值
        
    返回:
        str: 写入结果
    """
    return write_R_register(ip, index, value)


@mcp.tool()
def delete_R(ip: str, index: int):
    """删除R寄存器（数值寄存器）
    
    参数:
        ip: 机器人控制柜IP地址
        index: R寄存器的编号
        
    返回:
        str: 删除结果
    """
    return delete_R_register(ip, index)


@mcp.tool()
def read_MR(ip: str, index: int):
    """读取MR寄存器（运动寄存器）的值
    
    参数:
        ip: 机器人控制柜IP地址
        index: MR寄存器的编号
        
    返回:
        str: MR寄存器的值
    """
    return read_MR_register(ip, index)


@mcp.tool()
def write_MR(ip: str, index: int, value: int):
    """写入MR寄存器（运动寄存器）的值
    
    参数:
        ip: 机器人控制柜IP地址
        index: MR寄存器的编号
        value: 需要写入的值
        
    返回:
        str: 写入结果
    """
    return write_MR_register(ip, index, value)


@mcp.tool()
def delete_MR(ip: str, index: int):
    """删除MR寄存器（运动寄存器）
    
    参数:
        ip: 机器人控制柜IP地址
        index: MR寄存器的编号
        
    返回:
        str: 删除结果
    """
    return delete_MR_register(ip, index)


@mcp.tool()
def read_PR(ip: str, index: int):
    """读取PR寄存器（位姿寄存器）的值
    
    参数:
        ip: 机器人控制柜IP地址
        index: PR寄存器的编号
        
    返回:
        str: PR寄存器的位姿数据
    """
    return read_PR_register(ip, index)


@mcp.tool()
def write_PR(ip: str, index: int, pose_data: str):
    """写入PR寄存器（位姿寄存器）的值
    
    参数:
        ip: 机器人控制柜IP地址
        index: PR寄存器的编号
        pose_data: JSON字符串格式的位姿数据
        
    返回:
        str: 写入结果
    """
    return write_PR_register(ip, index, pose_data)


@mcp.tool()
def delete_PR(ip: str, index: int):
    """删除PR寄存器（位姿寄存器）
    
    参数:
        ip: 机器人控制柜IP地址
        index: PR寄存器的编号
        
    返回:
        str: 删除结果
    """
    return delete_PR_register(ip, index)


@mcp.tool()
def read_modbus_coils_tool(ip: str, channel: int, slave_id: int, address: int, number: int, master_id: int = 0):
    """读取Modbus线圈寄存器
    
    参数:
        ip: 机器人控制柜IP地址
        channel: Modbus通道
        slave_id: 从机ID
        address: 寄存器地址
        number: 寄存器数量 (最大120)
        master_id: 主机ID (默认0)
        
    返回:
        str: 寄存器值
    """
    return read_modbus_coils(ip, channel, slave_id, address, number, master_id)


@mcp.tool()
def write_modbus_coils_tool(ip: str, channel: int, slave_id: int, address: int, values: str, master_id: int = 0):
    """写入Modbus线圈寄存器
    
    参数:
        ip: 机器人控制柜IP地址
        channel: Modbus通道
        slave_id: 从机ID
        address: 寄存器地址
        values: JSON字符串格式的寄存器值列表
        master_id: 主机ID (默认0)
        
    返回:
        str: 写入结果
    """
    try:
        values_list = json.loads(values)
        return write_modbus_coils(ip, channel, slave_id, address, values_list, master_id)
    except json.JSONDecodeError:
        return json.dumps({"status": "error", "message": "寄存器值格式错误，应为JSON字符串"}, ensure_ascii=False)


@mcp.tool()
def read_modbus_holding_regs_tool(ip: str, channel: int, slave_id: int, address: int, number: int, master_id: int = 0):
    """读取Modbus保持寄存器
    
    参数:
        ip: 机器人控制柜IP地址
        channel: Modbus通道
        slave_id: 从机ID
        address: 寄存器地址
        number: 寄存器数量 (最大120)
        master_id: 主机ID (默认0)
        
    返回:
        str: 寄存器值
    """
    return read_modbus_holding_regs(ip, channel, slave_id, address, number, master_id)


@mcp.tool()
def write_modbus_holding_regs_tool(ip: str, channel: int, slave_id: int, address: int, values: str, master_id: int = 0):
    """写入Modbus保持寄存器
    
    参数:
        ip: 机器人控制柜IP地址
        channel: Modbus通道
        slave_id: 从机ID
        address: 寄存器地址
        values: JSON字符串格式的寄存器值列表
        master_id: 主机ID (默认0)
        
    返回:
        str: 写入结果
    """
    try:
        values_list = json.loads(values)
        return write_modbus_holding_regs(ip, channel, slave_id, address, values_list, master_id)
    except json.JSONDecodeError:
        return json.dumps({"status": "error", "message": "寄存器值格式错误，应为JSON字符串"}, ensure_ascii=False)


@mcp.tool()
def read_modbus_discrete_inputs_tool(ip: str, channel: int, slave_id: int, address: int, number: int, master_id: int = 0):
    """读取Modbus离散寄存器
    
    参数:
        ip: 机器人控制柜IP地址
        channel: Modbus通道
        slave_id: 从机ID
        address: 寄存器地址
        number: 寄存器数量 (最大120)
        master_id: 主机ID (默认0)
        
    返回:
        str: 寄存器值
    """
    return read_modbus_discrete_inputs(ip, channel, slave_id, address, number, master_id)


@mcp.tool()
def read_modbus_input_regs_tool(ip: str, channel: int, slave_id: int, address: int, number: int, master_id: int = 0):
    """读取Modbus输入寄存器
    
    参数:
        ip: 机器人控制柜IP地址
        channel: Modbus通道
        slave_id: 从机ID
        address: 寄存器地址
        number: 寄存器数量 (最大120)
        master_id: 主机ID (默认0)
        
    返回:
        str: 寄存器值
    """
    return read_modbus_input_regs(ip, channel, slave_id, address, number, master_id)


@mcp.tool()
def get_drag_status_tool(ip: str):
    """获取当前机器人轴锁定状态
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 轴锁定状态
    """
    return get_drag_status(ip)


@mcp.tool()
def set_drag_status_tool(ip: str, cart_x: bool = None, cart_y: bool = None, cart_z: bool = None,
                       cart_a: bool = None, cart_b: bool = None, cart_c: bool = None,
                       joint_j1: bool = None, joint_j2: bool = None, joint_j3: bool = None, 
                       joint_j4: bool = None, joint_j5: bool = None, joint_j6: bool = None, 
                       is_continuous_drag: bool = None):
    """设定当前机器人轴锁定状态
    
    参数:
        ip: 机器人控制柜IP地址
        cart_x: X轴锁定状态 (True=解锁, False=锁定)
        cart_y: Y轴锁定状态 (True=解锁, False=锁定)
        cart_z: Z轴锁定状态 (True=解锁, False=锁定)
        cart_a: A轴锁定状态 (True=解锁, False=锁定)
        cart_b: B轴锁定状态 (True=解锁, False=锁定)
        cart_c: C轴轴锁定状态 (True=解锁, False=锁定)
        joint_j1: J1轴锁定状态 (True=解锁, False=锁定)
        joint_j2: J2轴锁定状态 (True=解锁, False=锁定)
        joint_j3: J3轴锁定状态 (True=解锁, False=锁定)
        joint_j4: J4轴锁定状态 (True=解锁, False=锁定)
        joint_j5: J5轴锁定状态 (True=解锁, False=锁定)
        joint_j6: J6轴锁定状态 (True=解锁, False=锁定)
        is_continuous_drag: 连续拖动开关
        
    返回:
        str: 设置结果
    """
    return set_drag_status(ip, cart_x, cart_y, cart_z, cart_a, cart_b, cart_c, joint_j1, joint_j2, joint_j3, joint_j4, joint_j5, joint_j6, is_continuous_drag)


@mcp.tool()
def enable_drag_tool(ip: str, enable: bool):
    """启用或禁用拖动示教模式
    
    参数:
        ip: 机器人控制柜IP地址
        enable: True=启用拖动, False=禁用拖动
        
    返回:
        str: 设置结果
    """
    return enable_drag(ip, enable)


@mcp.tool()
def get_coordinate_list_tool(ip: str, sys_type: int):
    """获取用户坐标系或工具坐标系列表
    
    参数:
        ip: 机器人控制柜IP地址
        sys_type: 坐标系类型 (0=用户坐标系, 1=工具坐标系)
        
    返回:
        str: 坐标系列表
    """
    return get_coordinate_list(ip, sys_type)


@mcp.tool()
def add_coordinate_tool(ip: str, sys_type: int):
    """添加用户/工具坐标系
    
    参数:
        ip: 机器人控制柜IP地址
        sys_type: 坐标系类型 (0=用户坐标系, 1=工具坐标系)
        
    返回:
        str: 新建坐标系信息
    """
    return add_coordinate(ip, sys_type)


@mcp.tool()
def delete_coordinate_tool(ip: str, sys_type: int, coordinate_id: int):
    """删除用户/工具坐标系
    
    参数:
        ip: 机器人控制柜IP地址
        sys_type: 坐标系类型 (0=用户坐标系, 1=工具坐标系)
        coordinate_id: 坐标系编号
        
    返回:
        str: 删除结果
    """
    return delete_coordinate(ip, sys_type, coordinate_id)


@mcp.tool()
def update_coordinate_tool(ip: str, sys_type: int, coordinate_data: str):
    """更新用户/工具坐标系
    
    参数:
        ip: 机器人控制柜IP地址
        sys_type: 坐标系类型 (0=用户坐标系, 1=工具坐标系)
        coordinate_data: JSON字符串格式的坐标系数据
        
    返回:
        str: 更新结果
    """
    return update_coordinate(ip, sys_type, coordinate_data)


@mcp.tool()
def get_coordinate_tool(ip: str, sys_type: int, coordinate_id: int):
    """获取指定的用户/工具坐标系
    
    参数:
        ip: 机器人控制柜IP地址
        sys_type: 坐标系类型 (0=用户坐标系, 1=工具坐标系)
        coordinate_id: 坐标系编号
        
    返回:
        str: 坐标系信息
    """
    return get_coordinate(ip, sys_type, coordinate_id)


@mcp.tool()
def get_current_payload_tool(ip: str):
    """获取当前激活的负载编号
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 负载编号信息
    """
    return get_current_payload(ip)


@mcp.tool()
def get_payload_by_id_tool(ip: str, payload_id: int):
    """根据指定编号获取负载信息
    
    参数:
        ip: 机器人控制柜IP地址
        payload_id: 负载ID编号
        
    返回:
        str: 负载信息
    """
    return get_payload_by_id(ip, payload_id)


@mcp.tool()
def set_current_payload_tool(ip: str, payload_id: int):
    """根据指定编号激活负载
    
    参数:
        ip: 机器人控制柜IP地址
        payload_id: 负载ID编号
        
    返回:
        str: 操作结果
    """
    return set_current_payload(ip, payload_id)


@mcp.tool()
def add_payload_tool(ip: str, payload_info: str):
    """向机器人控制柜添加一个用户自定义负载信息
    
    参数:
        ip: 机器人控制柜IP地址
        payload_info: JSON字符串格式的负载信息
        
    返回:
        str: 操作结果
    """
    try:
        payload_data = json.loads(payload_info)
        return add_payload(ip, payload_data)
    except json.JSONDecodeError:
        return json.dumps({"status": "error", "message": "负载信息格式错误，应为JSON字符串"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"status": "error", "message": f"添加负载时发生异常: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
def delete_payload_tool(ip: str, payload_id: int):
    """根据指定编号删除对应的负载信息
    
    参数:
        ip: 机器人控制柜IP地址
        payload_id: 负载ID编号
        
    返回:
        str: 操作结果
    """
    return delete_payload(ip, payload_id)


@mcp.tool()
def update_payload_tool(ip: str, payload_info: str):
    """更新一个已存在负载信息
    
    参数:
        ip: 机器人控制柜IP地址
        payload_info: JSON字符串格式的负载信息
        
    返回:
        str: 操作结果
    """
    try:
        payload_data = json.loads(payload_info)
        return update_payload(ip, payload_data)
    except json.JSONDecodeError:
        return json.dumps({"status": "error", "message": "负载信息格式错误，应为JSON字符串"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"status": "error", "message": f"更新负载时发生异常: {str(e)}"}, ensure_ascii=False)


@mcp.tool()
def get_all_payload_tool(ip: str):
    """获取所有负载信息
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 所有负载信息
    """
    return get_all_payload(ip)


@mcp.tool()
def check_axis_three_horizontal_tool(ip: str):
    """检测3轴是否水平
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 3轴水平角度信息
    """
    return check_axis_three_horizontal(ip)


@mcp.tool()
def get_payload_identify_state_tool(ip: str):
    """获取负载测定状态
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 负载测定状态信息
    """
    return get_payload_identify_state(ip)


@mcp.tool()
def start_payload_identify_tool(ip: str, weight: float, angle: float):
    """开始负载测定
    
    参数:
        ip: 机器人控制柜IP地址
        weight: 负载重量（未知重量填-1）
        angle: 6轴允许转动的角度（30-90度）
        
    返回:
        str: 操作结果
    """
    return start_payload_identify(ip, weight, angle)


@mcp.tool()
def get_payload_identify_result_tool(ip: str):
    """获取负载测定结果
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 负载测定结果
    """
    return get_payload_identify_result(ip)


@mcp.tool()
def interference_check_for_payload_identify_tool(ip: str, weight: float, angle: float):
    """开始负载测定的干涉检查
    
    参数:
        ip: 机器人控制柜IP地址
        weight: 负载重量
        angle: 6轴转动角度（30-90度）
        
    返回:
        str: 操作结果
    """
    return interference_check_for_payload_identify(ip, weight, angle)


@mcp.tool()
def payload_identify_start_tool(ip: str):
    """进入负载测定状态
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 操作结果
    """
    return payload_identify_start(ip)


@mcp.tool()
def payload_identify_done_tool(ip: str):
    """结束负载测定状态
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: 操作结果
    """
    return payload_identify_done(ip)


@mcp.tool()
def payload_identify_tool(ip: str, weight: float, angle: float):
    """负载测定全流程
    
    参数:
        ip: 机器人控制柜IP地址
        weight: 负载重量（未知重量填-1）
        angle: 6轴转动角度（30-90度）
        
    返回:
        str: 负载测定结果
    """
    return payload_identify(ip, weight, angle)


@mcp.tool()
def update_payload_from_identify_tool(ip: str, payload_id: int, identify_result: str):
    """将负载测定结果更新到指定负载
    
    参数:
        ip: 机器人控制柜IP地址
        payload_id: 要更新的负载ID
        identify_result: 负载测定结果JSON字符串
        
    返回:
        str: 操作结果
    """
    return update_payload_from_identify(ip, payload_id, json.loads(identify_result))
