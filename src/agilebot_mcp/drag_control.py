# -*- coding: utf-8 -*-
import json
import logging
from Agilebot.IR.A.status_code import StatusCodeEnum

from .robot_core import robot_list, check_robot_ready

logger = logging.getLogger(__name__)


def get_drag_status(ip: str):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        drag_status, ret = robot_list[ip].motion.get_drag_set()
        
        if ret == StatusCodeEnum.OK:
            result = {
                "cart_status": {
                    "x": drag_status.cart_status.x,
                    "y": drag_status.cart_status.y,
                    "z": drag_status.cart_status.z,
                    "a": drag_status.cart_status.a,
                    "b": drag_status.cart_status.b,
                    "c": drag_status.cart_status.c
                },
                "joint_status": {
                    "j1": drag_status.joint_status.j1,
                    "j2": drag_status.joint_status.j2,
                    "j3": drag_status.joint_status.j3,
                    "j4": drag_status.joint_status.j4,
                    "j5": drag_status.joint_status.j5,
                    "j6": drag_status.joint_status.j6
                },
                "is_continuous_drag": drag_status.is_continuous_drag
            }
            logger.info(f"获取锁轴状态成功: {ip}")
            return json.dumps({"status": "success", "data": result}, ensure_ascii=False)
        else:
            logger.error(f"获取锁轴状态失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "获取锁轴状态失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"获取锁轴状态时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"获取锁轴状态时发生异常: {str(e)}"}, ensure_ascii=False)


def set_drag_status(ip: str, cart_x: bool = None, cart_y: bool = None, cart_z: bool = None,
                   cart_a: bool = None, cart_b: bool = None, cart_c: bool = None,
                   joint_j1: bool = None, joint_j2: bool = None, joint_j3: bool = None, 
                   joint_j4: bool = None, joint_j5: bool = None, joint_j6: bool = None, 
                   is_continuous_drag: bool = None):
    """
    设置轴锁定状态（支持自由解锁和锁住某个或某些轴）
    
    参数说明:
        ip: 机器人控制柜IP地址
        cart_x: X轴锁定状态 (True=锁定/不可移动, False=解锁/可移动, None=不修改)
        cart_y: Y轴锁定状态 (True=锁定/不可移动, False=解锁/可移动, None=不修改)
        cart_z: Z轴锁定状态 (True=锁定/不可移动, False=解锁/可移动, None=不修改)
        cart_a: A轴锁定状态 (True=锁定/不可移动, False=解锁/可移动, None=不修改)
        cart_b: B轴锁定状态 (True=锁定/不可移动(旋转), False=解锁/可移动, None=不修改)
        cart_c: C轴锁定状态 (True=锁定/不可移动(旋转), False=解锁/可移动, None=不修改)
        joint_j1: J1轴锁定状态 (True=锁定/不可移动, False=解锁/可移动, None=不修改)
        joint_j2: J2轴锁定状态 (True=锁定/不可移动, False=解锁/可移动, None=不修改)
        joint_j3: J3轴锁定状态 (True=锁定/不可移动, False=解锁/可移动, None=不修改)
        joint_j4: J4轴锁定状态 (True=锁定/不可移动(旋转), False=解锁/可移动, None=不修改)
        joint_j5: J5轴锁定状态 (True=锁定/不可移动(旋转), False=解锁/可移动, None=不修改)
        joint_j6: J6轴锁定状态 (True=锁定/不可移动(旋转), False=解锁/可移动, None=不修改)
        is_continuous_drag: 连续拖动模式 (True=启用, False=禁用, None=不修改)
    
    返回:
        str: JSON格式的操作结果
    """
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        check_robot_ready(ip)
        
        drag_status, ret = robot_list[ip].motion.get_drag_set()
        if ret != StatusCodeEnum.OK:
            logger.error(f"获取当前锁轴状态失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "获取当前锁轴状态失败"}, ensure_ascii=False)
        
        if cart_x is not None:
            drag_status.cart_status.x = not cart_x
        if cart_y is not None:
            drag_status.cart_status.y = not cart_y
        if cart_z is not None:
            drag_status.cart_status.z = not cart_z
        if cart_a is not None:
            drag_status.cart_status.a = not cart_a
        if cart_b is not None:
            drag_status.cart_status.b = not cart_b
        if cart_c is not None:
            drag_status.cart_status.c = not cart_c
            
        if joint_j1 is not None:
            drag_status.joint_status.j1 = not joint_j1
        if joint_j2 is not None:
            drag_status.joint_status.j2 = not joint_j2
        if joint_j3 is not None:
            drag_status.joint_status.j3 = not joint_j3
        if joint_j4 is not None:
            drag_status.joint_status.j4 = not joint_j4
        if joint_j5 is not None:
            drag_status.joint_status.j5 = not joint_j5
        if joint_j6 is not None:
            drag_status.joint_status.j6 = not joint_j6
            
        if is_continuous_drag is not None:
            drag_status.is_continuous_drag = is_continuous_drag
        
        ret = robot_list[ip].motion.set_drag_set(drag_status)
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"设置锁轴状态成功: {ip}")
            
            enable_ret = robot_list[ip].motion.enable_drag(True)
            if enable_ret == StatusCodeEnum.OK:
                logger.info(f"自动启用拖动示教成功: {ip}")
                return json.dumps({"status": "success", "message": "设置锁轴状态成功并自动启用拖动示教"}, ensure_ascii=False)
            else:
                logger.warning(f"设置锁轴状态成功但启用拖动示教失败: {ip}, 错误代码: {enable_ret}")
                return json.dumps({"status": "success", "message": "设置锁轴状态成功（拖动示教启用失败）"}, ensure_ascii=False)
        else:
            logger.error(f"设置锁轴状态失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "设置锁轴状态失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"设置锁轴状态时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"设置锁轴状态时发生异常: {str(e)}"}, ensure_ascii=False)


def enable_drag(ip: str, enable: bool):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        ret = robot_list[ip].motion.enable_drag(enable)
        
        if ret == StatusCodeEnum.OK:
            action = "启用" if enable else "禁用"
            logger.info(f"{action}拖动示教成功: {ip}")
            return json.dumps({"status": "success", "message": f"{action}拖动示教成功"}, ensure_ascii=False)
        else:
            logger.error(f"设置拖动示教失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "设置拖动示教失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"设置拖动示教时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"设置拖动示教时发生异常: {str(e)}"}, ensure_ascii=False)
