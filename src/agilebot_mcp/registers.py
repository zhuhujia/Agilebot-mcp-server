# -*- coding: utf-8 -*-
import json
import logging
from Agilebot.IR.A.status_code import StatusCodeEnum
from Agilebot.IR.A.sdk_types import PoseType
from Agilebot.IR.A.sdk_classes import PoseRegister

from .robot_core import robot_list

logger = logging.getLogger(__name__)


def read_R_register(ip: str, index: int):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        value, ret = robot_list[ip].register.read_R(index)
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"读取R寄存器成功: {ip}, 索引: {index}, 值: {value}")
            return json.dumps({"status": "success", "index": index, "value": value}, ensure_ascii=False)
        else:
            logger.error(f"读取R寄存器失败: {ip}, 索引: {index}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "读取R寄存器失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"读取R寄存器时发生异常: {ip}, 索引: {index}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"读取R寄存器时发生异常: {str(e)}"}, ensure_ascii=False)


def write_R_register(ip: str, index: int, value: float):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        ret = robot_list[ip].register.write_R(index, value)
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"写入R寄存器成功: {ip}, 索引: {index}, 值: {value}")
            return json.dumps({"status": "success", "message": "写入R寄存器成功"}, ensure_ascii=False)
        else:
            logger.error(f"写入R寄存器失败: {ip}, 索引: {index}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "写入R寄存器失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"写入R寄存器时发生异常: {ip}, 索引: {index}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"写入R寄存器时发生异常: {str(e)}"}, ensure_ascii=False)


def delete_R_register(ip: str, index: int):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        ret = robot_list[ip].register.delete_R(index)
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"删除R寄存器成功: {ip}, 索引: {index}")
            return json.dumps({"status": "success", "message": "删除R寄存器成功"}, ensure_ascii=False)
        else:
            logger.error(f"删除R寄存器失败: {ip}, 索引: {index}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "删除R寄存器失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"删除R寄存器时发生异常: {ip}, 索引: {index}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"删除R寄存器时发生异常: {str(e)}"}, ensure_ascii=False)


def read_MR_register(ip: str, index: int):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        value, ret = robot_list[ip].register.read_MR(index)
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"读取MR寄存器成功: {ip}, 索引: {index}, 值: {value}")
            return json.dumps({"status": "success", "index": index, "value": value}, ensure_ascii=False)
        else:
            logger.error(f"读取MR寄存器失败: {ip}, 索引: {index}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "读取MR寄存器失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"读取MR寄存器时发生异常: {ip}, 索引: {index}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"读取MR寄存器时发生异常: {str(e)}"}, ensure_ascii=False)


def write_MR_register(ip: str, index: int, value: int):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        ret = robot_list[ip].register.write_MR(index, value)
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"写入MR寄存器成功: {ip}, 索引: {index}, 值: {value}")
            return json.dumps({"status": "success", "message": "写入MR寄存器成功"}, ensure_ascii=False)
        else:
            logger.error(f"写入MR寄存器失败: {ip}, 索引: {index}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "写入MR寄存器失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"写入MR寄存器时发生异常: {ip}, 索引: {index}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"写入MR寄存器时发生异常: {str(e)}"}, ensure_ascii=False)


def delete_MR_register(ip: str, index: int):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        ret = robot_list[ip].register.delete_MR(index)
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"删除MR寄存器成功: {ip}, 索引: {index}")
            return json.dumps({"status": "success", "message": "删除MR寄存器成功"}, ensure_ascii=False)
        else:
            logger.error(f"删除MR寄存器失败: {ip}, 索引: {index}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "删除MR寄存器失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"删除MR寄存器时发生异常: {ip}, 索引: {index}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"删除MR寄存器时发生异常: {str(e)}"}, ensure_ascii=False)


def read_PR_register(ip: str, index: int):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        pose_register, ret = robot_list[ip].register.read_PR(index)
        
        if ret == StatusCodeEnum.OK:
            pose_data = pose_register.poseRegisterData
            result = {
                "index": index,
                "id": pose_register.id,
                "name": pose_register.name,
                "comment": pose_register.comment,
                "pose_type": str(pose_data.pt)
            }
            
            if pose_data.pt == PoseType.JOINT:
                result["joint"] = {
                    "j1": pose_data.joint.j1,
                    "j2": pose_data.joint.j2,
                    "j3": pose_data.joint.j3,
                    "j4": pose_data.joint.j4,
                    "j5": pose_data.joint.j5,
                    "j6": pose_data.joint.j6
                }
            elif pose_data.pt == PoseType.CART:
                result["cartesian"] = {
                    "x": pose_data.cartData.position.x,
                    "y": pose_data.cartData.position.y,
                    "z": pose_data.cartData.position.z,
                    "a": pose_data.cartData.position.a,
                    "b": pose_data.cartData.position.b,
                    "c": pose_data.cartData.position.c
                }
                result["posture"] = {
                    "arm_back_front": pose_data.cartData.posture.arm_back_front,
                    "arm_left_right": pose_data.cartData.posture.arm_left_right,
                    "arm_up_down": pose_data.cartData.posture.arm_up_down,
                    "wrist_flip": pose_data.cartData.posture.wrist_flip
                }
            
            logger.info(f"读取PR寄存器成功: {ip}, 索引: {index}")
            return json.dumps({"status": "success", "data": result}, ensure_ascii=False)
        else:
            logger.error(f"读取PR寄存器失败: {ip}, 索引: {index}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "读取PR寄存器失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"读取PR寄存器时发生异常: {ip}, 索引: {index}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"读取PR寄存器时发生异常: {str(e)}"}, ensure_ascii=False)


def write_PR_register(ip: str, index: int, pose_data: str):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        data = json.loads(pose_data)
        pose_register = PoseRegister()
        pose_register.id = index
        pose_register.name = data.get("name", "")
        pose_register.comment = data.get("comment", "")
        
        if "pose_type" in data:
            pose_type_str = data["pose_type"].upper()
            if "JOINT" in pose_type_str:
                pose_register.poseRegisterData.pt = PoseType.JOINT
                if "joint" in data:
                    joint = data["joint"]
                    pose_register.poseRegisterData.joint.j1 = joint.get("j1", 0)
                    pose_register.poseRegisterData.joint.j2 = joint.get("j2", 0)
                    pose_register.poseRegisterData.joint.j3 = joint.get("j3", 0)
                    pose_register.poseRegisterData.joint.j4 = joint.get("j4", 0)
                    pose_register.poseRegisterData.joint.j5 = joint.get("j5", 0)
                    pose_register.poseRegisterData.joint.j6 = joint.get("j6", 0)
            elif "CART" in pose_type_str:
                pose_register.poseRegisterData.pt = PoseType.CART
                if "cartesian" in data:
                    cartesian = data["cartesian"]
                    pose_register.poseRegisterData.cartData.position.x = cartesian.get("x", 0)
                    pose_register.poseRegisterData.cartData.position.y = cartesian.get("y", 0)
                    pose_register.poseRegisterData.cartData.position.z = cartesian.get("z", 0)
                    pose_register.poseRegisterData.cartData.position.a = cartesian.get("a", 0)
                    pose_register.poseRegisterData.cartData.position.b = cartesian.get("b", 0)
                    pose_register.poseRegisterData.cartData.position.c = cartesian.get("c", 0)
                if "posture" in data:
                    posture = data["posture"]
                    pose_register.poseRegisterData.cartData.posture.arm_back_front = posture.get("arm_back_front", 0)
                    pose_register.poseRegisterData.cartData.posture.arm_left_right = posture.get("arm_left_right", 0)
                    pose_register.poseRegisterData.cartData.posture.arm_up_down = posture.get("arm_up_down", 0)
                    pose_register.poseRegisterData.cartData.posture.wrist_flip = posture.get("wrist_flip", 0)
        
        ret = robot_list[ip].register.write_PR(pose_register)
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"写入PR寄存器成功: {ip}, 索引: {index}")
            return json.dumps({"status": "success", "message": "写入PR寄存器成功"}, ensure_ascii=False)
        else:
            logger.error(f"写入PR寄存器失败: {ip}, 索引: {index}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "写入PR寄存器失败"}, ensure_ascii=False)
            
    except json.JSONDecodeError:
        return json.dumps({"status": "error", "message": "位姿数据格式错误，应为JSON字符串"}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"写入PR寄存器时发生异常: {ip}, 索引: {index}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"写入PR寄存器时发生异常: {str(e)}"}, ensure_ascii=False)


def delete_PR_register(ip: str, index: int):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        ret = robot_list[ip].register.delete_PR(index)
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"删除PR寄存器成功: {ip}, 索引: {index}")
            return json.dumps({"status": "success", "message": "删除PR寄存器成功"}, ensure_ascii=False)
        else:
            logger.error(f"删除PR寄存器失败: {ip}, 索引: {index}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "删除PR寄存器失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"删除PR寄存器时发生异常: {ip}, 索引: {index}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"删除PR寄存器时发生异常: {str(e)}"}, ensure_ascii=False)
