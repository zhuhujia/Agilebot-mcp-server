# -*- coding: utf-8 -*-
import json
import logging
import time
from Agilebot.IR.A.arm import Arm
from Agilebot.IR.A.status_code import StatusCodeEnum
from Agilebot.IR.A.sdk_types import PoseType
from Agilebot.IR.A.sdk_classes import MotionPose, Posture

logger = logging.getLogger(__name__)

robot_list = dict()
global_speed = 50
global_accel = 0.5


def cleanup_robot_connections():
    global robot_list
    if robot_list:
        logger.info(f"正在断开所有机器人连接，共 {len(robot_list)} 个机器人")
        for ip in list(robot_list.keys()):
            try:
                robot_list[ip].disconnect()
                logger.info(f"成功断开机器人连接: {ip}")
            except Exception as e:
                logger.error(f"断开机器人连接时发生异常: {ip}, 异常信息: {str(e)}")
        robot_list.clear()
        logger.info("所有机器人连接已断开")


def check_robot_ready(ip):
    if ip not in robot_list:
        return json.dumps({"status": "error", "message": "机器人未连接"}, ensure_ascii=False)
    
    robot = robot_list[ip]
    
    ctrl_status, ret = robot.get_ctrl_status()
    ctrl_status_str = str(ctrl_status)
    
    if 'CTRL_ESTOP' in ctrl_status_str:
        logger.info(f"机器人处于急停状态，尝试复位: {ip}")
        reset_ret = robot.servo_reset()
        logger.info(f"复位结果: {reset_ret}")
        time.sleep(1)
    
    servo_status, ret = robot.get_servo_status()
    servo_status_str = str(servo_status)
    
    if 'SERVO_DISABLE' in servo_status_str or 'SERVO_IDLE' in servo_status_str:
        logger.info(f"伺服未上电，尝试上电: {ip}")
        power_ret = robot.servo_on()
        logger.info(f"上电结果: {power_ret}")
        
        if power_ret != StatusCodeEnum.OK:
            logger.warning(f"上电失败，尝试清除错误状态: {ip}")
            clear_ret = robot.servo_reset()
            logger.info(f"清除错误结果: {clear_ret}")
            time.sleep(0.5)
            
            power_ret = robot.servo_on()
            logger.info(f"重新上电结果: {power_ret}")
        
        time.sleep(1)
    
    return json.dumps({"status": "success", "message": "机器人准备就绪"}, ensure_ascii=False)


def connect_robot(ip: str):
    try:
        if ip in robot_list:
            return json.dumps({"status": "success", "message": "机器人已连接"}, ensure_ascii=False)
        
        try:
            arm = Arm()
        except Exception as e:
            logger.error(f"初始化机器人实例时发生异常: {ip}, 异常信息: {str(e)}")
            return json.dumps({"status": "error", "message": "初始化机器人实例失败"}, ensure_ascii=False)
        
        try:
            ret = arm.connect(ip)
        except Exception as e:
            logger.error(f"连接机器人时发生异常: {ip}, 异常信息: {str(e)}")
            return json.dumps({"status": "error", "message": "连接机器人失败: 网络错误"}, ensure_ascii=False)
        
        if ret == StatusCodeEnum.OK:
            robot_list[ip] = arm
            logger.info(f"成功连接机器人: {ip}")
            return json.dumps({"status": "success", "message": "机器人连接成功"}, ensure_ascii=False)
        else:
            logger.error(f"连接机器人失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "机器人连接失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"连接机器人时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": "连接机器人时发生异常: 网络或编码错误"}, ensure_ascii=False)


def disconnect_robot(ip: str):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "机器人未连接"}, ensure_ascii=False)
        
        ret = robot_list[ip].disconnect()
        del robot_list[ip]
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"成功断开机器人连接: {ip}")
            return json.dumps({"status": "success", "message": "机器人断开连接成功"}, ensure_ascii=False)
        else:
            logger.error(f"断开机器人连接失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "机器人断开连接失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"断开机器人连接时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": "断开机器人连接时发生异常: 编码错误"}, ensure_ascii=False)


def get_status(ip: str):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        robot_status, ret = robot_list[ip].get_robot_status()
        
        if ret == StatusCodeEnum.OK:
            try:
                status_msg = str(robot_status)
            except Exception as e:
                status_msg = "未知状态"
            logger.info(f"获取机器人状态成功: {ip}, 状态: {status_msg}")
            return json.dumps({"status": "success", "message": status_msg}, ensure_ascii=False)
        else:
            logger.error(f"获取机器人状态失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "获取机器人状态失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"获取机器人状态时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": "获取机器人状态时发生异常: 编码错误"}, ensure_ascii=False)


def get_controller_info(ip: str):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        ctrl_status, ret = robot_list[ip].get_ctrl_status()
        
        if ret == StatusCodeEnum.OK:
            try:
                status_msg = str(ctrl_status)
            except Exception as e:
                status_msg = "未知状态"
            logger.info(f"获取控制器状态成功: {ip}, 状态: {status_msg}")
            return json.dumps({"status": "success", "message": status_msg}, ensure_ascii=False)
        else:
            logger.error(f"获取控制器状态失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "获取控制器状态失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"获取控制器状态时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": "获取控制器状态时发生异常: 编码错误"}, ensure_ascii=False)


def get_current_joint_positions(ip: str):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        pose, ret = robot_list[ip].motion.get_current_pose(PoseType.JOINT)
        
        if ret == StatusCodeEnum.OK:
            positions = {
                "j1": pose.joint.j1,
                "j2": pose.joint.j2,
                "j3": pose.joint.j3,
                "j4": pose.joint.j4,
                "j5": pose.joint.j5,
                "j6": pose.joint.j6
            }
            logger.info(f"获取关节位置成功: {ip}, 位置: {positions}")
            return json.dumps({"status": "success", "positions": positions}, ensure_ascii=False)
        else:
            logger.error(f"获取关节位置失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "获取关节位置失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"获取关节位置时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": "获取关节位置时发生异常: 编码错误"}, ensure_ascii=False)


def get_current_cartesian_position(ip: str):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        pose, ret = robot_list[ip].motion.get_current_pose(PoseType.CART)
        
        if ret == StatusCodeEnum.OK:
            position = {
                "x": pose.cartData.position.x,
                "y": pose.cartData.position.y,
                "z": pose.cartData.position.z,
                "a": pose.cartData.position.a,
                "b": pose.cartData.position.b,
                "c": pose.cartData.position.c
            }
            posture = {
                "arm_back_front": pose.cartData.posture.arm_back_front,
                "arm_left_right": pose.cartData.posture.arm_left_right,
                "arm_up_down": pose.cartData.posture.arm_up_down,
                "wrist_flip": pose.cartData.posture.wrist_flip
            }
            logger.info(f"获取笛卡尔位置成功: {ip}, 位置: {position}")
            return json.dumps({"status": "success", "position": position, "posture": posture}, ensure_ascii=False)
        else:
            logger.error(f"获取笛卡尔位置失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "获取笛卡尔位置失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"获取笛卡尔位置时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": "获取笛卡尔位置时发生异常: 编码错误"}, ensure_ascii=False)


def move_joint(ip, joint_positions, speed=None, accel=None):
    if speed is None:
        speed = global_speed
    if accel is None:
        accel = global_accel
    
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        pose = MotionPose()
        pose.pt = PoseType.JOINT
        pose.joint.j1, pose.joint.j2, pose.joint.j3 = joint_positions[0], joint_positions[1], joint_positions[2]
        pose.joint.j4, pose.joint.j5, pose.joint.j6 = joint_positions[3], joint_positions[4], joint_positions[5]
        
        ret = robot_list[ip].motion.move_line(pose, speed, accel)
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"关节运动指令发送成功: {ip}, 目标位置: {joint_positions}")
            return json.dumps({"status": "success", "message": "关节运动指令发送成功"}, ensure_ascii=False)
        else:
            logger.error(f"关节运动指令发送失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "关节运动指令发送失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"关节运动时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"关节运动时发生异常: {str(e)}"}, ensure_ascii=False)


def move_cartesian(ip, position, posture=None, speed=None, accel=None):
    if speed is None:
        speed = global_speed
    if accel is None:
        accel = global_accel
    
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        pose = MotionPose()
        pose.pt = PoseType.CART
        pose.cartData.position.x, pose.cartData.position.y, pose.cartData.position.z = position[0], position[1], position[2]
        pose.cartData.position.a, pose.cartData.position.b, pose.cartData.position.c = position[3], position[4], position[5]
        
        if posture:
            new_posture = Posture()
            new_posture.arm_back_front = posture.get("arm_back_front", 0)
            new_posture.arm_left_right = posture.get("arm_left_right", 0)
            new_posture.arm_up_down = posture.get("arm_up_down", 0)
            new_posture.wrist_flip = posture.get("wrist_flip", 0)
            pose.cartData.posture = new_posture
        
        ret = robot_list[ip].motion.move_line(pose, speed, accel)
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"笛卡尔运动指令发送成功: {ip}, 目标位置: {position}")
            return json.dumps({"status": "success", "message": "笛卡尔运动指令发送成功"}, ensure_ascii=False)
        else:
            logger.error(f"笛卡尔运动指令发送失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "笛卡尔运动指令发送失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"笛卡尔运动时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"笛卡尔运动时发生异常: {str(e)}"}, ensure_ascii=False)


def power_off_robot(ip: str):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        ret = robot_list[ip].servo_off()
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"机器人断电成功: {ip}")
            return json.dumps({"status": "success", "message": "机器人断电成功"}, ensure_ascii=False)
        else:
            logger.error(f"机器人断电失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "机器人断电失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"机器人断电时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": "机器人断电时发生异常: 编码错误"}, ensure_ascii=False)


def power_on_robot(ip: str):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        ret = robot_list[ip].servo_on()
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"机器人上电成功: {ip}")
            return json.dumps({"status": "success", "message": "机器人上电成功"}, ensure_ascii=False)
        else:
            logger.error(f"机器人上电失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "机器人上电失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"机器人上电时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": "机器人上电时发生异常: 编码错误"}, ensure_ascii=False)


def get_servo_status(ip: str):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        servo_status, ret = robot_list[ip].get_servo_status()
        
        if ret == StatusCodeEnum.OK:
            try:
                status_msg = str(servo_status)
            except Exception as e:
                status_msg = "未知状态"
            logger.info(f"获取伺服控制器状态成功: {ip}, 状态: {status_msg}")
            return json.dumps({"status": "success", "message": status_msg}, ensure_ascii=False)
        else:
            logger.error(f"获取伺服控制器状态失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "获取伺服控制器状态失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"获取伺服控制器状态时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": "获取伺服控制器状态时发生异常: 编码错误"}, ensure_ascii=False)


def get_robot_info(ip: str):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        model_info, ret = robot_list[ip].get_arm_model_info()
        
        if ret == StatusCodeEnum.OK:
            try:
                model_str = str(model_info)
            except Exception as e:
                model_str = "未知型号"
            logger.info(f"获取机器人型号成功: {ip}, 型号: {model_str}")
            return json.dumps({"status": "success", "model": model_str}, ensure_ascii=False)
        else:
            logger.error(f"获取机器人型号失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "获取机器人型号失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"获取机器人型号时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": "获取机器人型号时发生异常: 编码错误"}, ensure_ascii=False)


def servo_reset(ip: str):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        ret = robot_list[ip].servo_reset()
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"伺服复位成功: {ip}")
            return json.dumps({"status": "success", "message": "伺服复位成功"}, ensure_ascii=False)
        else:
            logger.error(f"伺服复位失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "伺服复位失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"伺服复位时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": "伺服复位时发生异常: 编码错误"}, ensure_ascii=False)


def acquire_access(ip: str):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        ret = robot_list[ip].acquire_access()
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"获取操作权限成功: {ip}")
            return json.dumps({"status": "success", "message": "获取操作权限成功"}, ensure_ascii=False)
        else:
            logger.error(f"获取操作权限失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "获取操作权限失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"获取操作权限时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": "获取操作权限时发生异常: 编码错误"}, ensure_ascii=False)


def release_access(ip: str):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        ret = robot_list[ip].release_access()
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"返还操作权限成功: {ip}")
            return json.dumps({"status": "success", "message": "返还操作权限成功"}, ensure_ascii=False)
        else:
            logger.error(f"返还操作权限失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "返还操作权限失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"返还操作权限时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": "返还操作权限时发生异常: 编码错误"}, ensure_ascii=False)
