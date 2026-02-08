# -*- coding: utf-8 -*-
import json
import logging
from Agilebot.IR.A.arm import Arm
from Agilebot.IR.A.status_code import StatusCodeEnum
from .robot_core import robot_list

logger = logging.getLogger(__name__)


def get_current_payload(ip):
    """获取当前激活的负载编号
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: JSON格式的负载编号信息
    """
    try:
        robot = robot_list.get(ip)
        if not robot:
            return json.dumps({"status": "error", "message": "机器人未连接"}, ensure_ascii=False)
        
        payload_id, ret = robot.motion.payload.get_current_payload()
        if ret != StatusCodeEnum.OK:
            return json.dumps({"status": "error", "message": f"获取当前负载失败: {ret.errmsg}"}, ensure_ascii=False)
        
        return json.dumps({"status": "success", "data": {"payload_id": payload_id}}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取当前负载时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"获取当前负载时发生异常: {str(e)}"}, ensure_ascii=False)


def get_payload_by_id(ip, payload_id):
    """根据指定编号获取负载信息
    
    参数:
        ip: 机器人控制柜IP地址
        payload_id: 负载ID编号
        
    返回:
        str: JSON格式的负载信息
    """
    try:
        robot = robot_list.get(ip)
        if not robot:
            return json.dumps({"status": "error", "message": "机器人未连接"}, ensure_ascii=False)
        
        payload_info, ret = robot.motion.payload.get_payload_by_id(payload_id)
        if ret != StatusCodeEnum.OK:
            return json.dumps({"status": "error", "message": f"获取负载信息失败: {ret.errmsg}"}, ensure_ascii=False)
        
        payload_data = {
            "id": payload_info.id,
            "m_load": payload_info.m_load,
            "lcx_load": payload_info.lcx_load,
            "lcy_load": payload_info.lcy_load,
            "lcz_load": payload_info.lcz_load,
            "Ixx_load": payload_info.Ixx_load,
            "Iyy_load": payload_info.Iyy_load,
            "Izz_load": payload_info.Izz_load,
            "comment": payload_info.comment.decode('utf-8') if payload_info.comment else ""
        }
        
        return json.dumps({"status": "success", "data": payload_data}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取负载信息时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"获取负载信息时发生异常: {str(e)}"}, ensure_ascii=False)


def set_current_payload(ip, payload_id):
    """根据指定编号激活负载
    
    参数:
        ip: 机器人控制柜IP地址
        payload_id: 负载ID编号
        
    返回:
        str: JSON格式的操作结果
    """
    try:
        robot = robot_list.get(ip)
        if not robot:
            return json.dumps({"status": "error", "message": "机器人未连接"}, ensure_ascii=False)
        
        ret = robot.motion.payload.set_current_payload(payload_id)
        if ret != StatusCodeEnum.OK:
            return json.dumps({"status": "error", "message": f"激活负载失败: {ret.errmsg}"}, ensure_ascii=False)
        
        return json.dumps({"status": "success", "message": f"成功激活负载 {payload_id}"}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"激活负载时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"激活负载时发生异常: {str(e)}"}, ensure_ascii=False)


def add_payload(ip, payload_info):
    """向机器人控制柜添加一个用户自定义负载信息
    
    参数:
        ip: 机器人控制柜IP地址
        payload_info: 负载信息字典
        
    返回:
        str: JSON格式的操作结果
    """
    try:
        from Agilebot.IR.A.flyshot import Payload
        
        robot = robot_list.get(ip)
        if not robot:
            return json.dumps({"status": "error", "message": "机器人未连接"}, ensure_ascii=False)
        
        new_payload = Payload()
        new_payload.id = payload_info.get("id", 0)
        new_payload.m_load = payload_info.get("m_load", 0.0)
        new_payload.lcx_load = payload_info.get("lcx_load", 0.0)
        new_payload.lcy_load = payload_info.get("lcy_load", 0.0)
        new_payload.lcz_load = payload_info.get("lcz_load", 0.0)
        new_payload.Ixx_load = payload_info.get("Ixx_load", 0.0)
        new_payload.Iyy_load = payload_info.get("Iyy_load", 0.0)
        new_payload.Izz_load = payload_info.get("Izz_load", 0.0)
        
        comment = payload_info.get("comment", "")
        if comment:
            new_payload.comment = comment.encode('utf-8')
        
        ret = robot.motion.payload.add_payload(new_payload)
        if ret != StatusCodeEnum.OK:
            return json.dumps({"status": "error", "message": f"添加负载失败: {ret.errmsg}"}, ensure_ascii=False)
        
        return json.dumps({"status": "success", "message": f"成功添加负载 {new_payload.id}"}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"添加负载时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"添加负载时发生异常: {str(e)}"}, ensure_ascii=False)


def delete_payload(ip, payload_id):
    """根据指定编号删除对应的负载信息
    
    参数:
        ip: 机器人控制柜IP地址
        payload_id: 负载ID编号
        
    返回:
        str: JSON格式的操作结果
    """
    try:
        robot = robot_list.get(ip)
        if not robot:
            return json.dumps({"status": "error", "message": "机器人未连接"}, ensure_ascii=False)
        
        ret = robot.motion.payload.delete_payload(payload_id)
        if ret != StatusCodeEnum.OK:
            return json.dumps({"status": "error", "message": f"删除负载失败: {ret.errmsg}"}, ensure_ascii=False)
        
        return json.dumps({"status": "success", "message": f"成功删除负载 {payload_id}"}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"删除负载时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"删除负载时发生异常: {str(e)}"}, ensure_ascii=False)


def update_payload(ip, payload_info):
    """更新一个已存在负载信息
    
    参数:
        ip: 机器人控制柜IP地址
        payload_info: 负载信息字典
        
    返回:
        str: JSON格式的操作结果
    """
    try:
        from Agilebot.IR.A.flyshot import Payload
        
        robot = robot_list.get(ip)
        if not robot:
            return json.dumps({"status": "error", "message": "机器人未连接"}, ensure_ascii=False)
        
        payload_id = payload_info.get("id")
        if not payload_id:
            return json.dumps({"status": "error", "message": "负载ID不能为空"}, ensure_ascii=False)
        
        existing_payload, ret = robot.motion.payload.get_payload_by_id(payload_id)
        if ret != StatusCodeEnum.OK:
            return json.dumps({"status": "error", "message": f"获取负载信息失败: {ret.errmsg}"}, ensure_ascii=False)
        
        if "m_load" in payload_info:
            existing_payload.m_load = payload_info["m_load"]
        if "lcx_load" in payload_info:
            existing_payload.lcx_load = payload_info["lcx_load"]
        if "lcy_load" in payload_info:
            existing_payload.lcy_load = payload_info["lcy_load"]
        if "lcz_load" in payload_info:
            existing_payload.lcz_load = payload_info["lcz_load"]
        if "Ixx_load" in payload_info:
            existing_payload.Ixx_load = payload_info["Ixx_load"]
        if "Iyy_load" in payload_info:
            existing_payload.Iyy_load = payload_info["Iyy_load"]
        if "Izz_load" in payload_info:
            existing_payload.Izz_load = payload_info["Izz_load"]
        if "comment" in payload_info:
            existing_payload.comment = payload_info["comment"].encode('utf-8')
        
        ret = robot.motion.payload.update_payload(existing_payload)
        if ret != StatusCodeEnum.OK:
            return json.dumps({"status": "error", "message": f"更新负载失败: {ret.errmsg}"}, ensure_ascii=False)
        
        return json.dumps({"status": "success", "message": f"成功更新负载 {payload_id}"}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"更新负载时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"更新负载时发生异常: {str(e)}"}, ensure_ascii=False)


def get_all_payload(ip):
    """获取所有负载信息
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: JSON格式的所有负载信息
    """
    try:
        robot = robot_list.get(ip)
        if not robot:
            return json.dumps({"status": "error", "message": "机器人未连接"}, ensure_ascii=False)
        
        payloads, ret = robot.motion.payload.get_all_payload()
        if ret != StatusCodeEnum.OK:
            return json.dumps({"status": "error", "message": f"获取所有负载失败: {ret.errmsg}"}, ensure_ascii=False)
        
        payload_list = []
        for payload in payloads:
            payload_list.append({
                "id": payload[0],
                "comment": payload[1].decode('utf-8') if payload[1] else ""
            })
        
        return json.dumps({"status": "success", "data": {"payloads": payload_list}}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取所有负载时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"获取所有负载时发生异常: {str(e)}"}, ensure_ascii=False)


def check_axis_three_horizontal(ip):
    """检测3轴是否水平
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: JSON格式的3轴水平角度信息
    """
    try:
        robot = robot_list.get(ip)
        if not robot:
            return json.dumps({"status": "error", "message": "机器人未连接"}, ensure_ascii=False)
        
        angle, ret = robot.motion.payload.check_axis_three_horizontal()
        if ret != StatusCodeEnum.OK:
            return json.dumps({"status": "error", "message": f"检测3轴水平失败: {ret.errmsg}"}, ensure_ascii=False)
        
        is_horizontal = -1 <= angle <= 1
        return json.dumps({
            "status": "success",
            "data": {
                "angle": angle,
                "is_horizontal": is_horizontal,
                "message": "3轴水平" if is_horizontal else "3轴不水平"
            }
        }, ensure_ascii=False)
    except Exception as e:
        logger.error(f"检测3轴水平时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"检测3轴水平时发生异常: {str(e)}"}, ensure_ascii=False)


def get_payload_identify_state(ip):
    """获取负载测定状态
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: JSON格式的负载测定状态信息
    """
    try:
        robot = robot_list.get(ip)
        if not robot:
            return json.dumps({"status": "error", "message": "机器人未连接"}, ensure_ascii=False)
        
        state, ret = robot.motion.payload.get_payload_identify_state()
        if ret != StatusCodeEnum.OK:
            return json.dumps({"status": "error", "message": f"获取负载测定状态失败: {ret.errmsg}"}, ensure_ascii=False)
        
        return json.dumps({
            "status": "success",
            "data": {
                "state": str(state)
            }
        }, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取负载测定状态时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"获取负载测定状态时发生异常: {str(e)}"}, ensure_ascii=False)


def start_payload_identify(ip, weight, angle):
    """开始负载测定
    
    参数:
        ip: 机器人控制柜IP地址
        weight: 负载重量（未知重量填-1）
        angle: 6轴允许转动的角度（30-90度）
        
    返回:
        str: JSON格式的操作结果
    """
    try:
        robot = robot_list.get(ip)
        if not robot:
            return json.dumps({"status": "error", "message": "机器人未连接"}, ensure_ascii=False)
        
        if not (30 <= angle <= 90):
            return json.dumps({"status": "error", "message": "角度必须在30-90度之间"}, ensure_ascii=False)
        
        ret = robot.motion.payload.start_payload_identify(weight, angle)
        if ret != StatusCodeEnum.OK:
            return json.dumps({"status": "error", "message": f"开始负载测定失败: {ret.errmsg}"}, ensure_ascii=False)
        
        return json.dumps({"status": "success", "message": "开始负载测定成功"}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"开始负载测定时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"开始负载测定时发生异常: {str(e)}"}, ensure_ascii=False)


def get_payload_identify_result(ip):
    """获取负载测定结果
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: JSON格式的负载测定结果
    """
    try:
        robot = robot_list.get(ip)
        if not robot:
            return json.dumps({"status": "error", "message": "机器人未连接"}, ensure_ascii=False)
        
        payload_info, ret = robot.motion.payload.payload_identify_result()
        if ret != StatusCodeEnum.OK:
            return json.dumps({"status": "error", "message": f"获取负载测定结果失败: {ret.errmsg}"}, ensure_ascii=False)
        
        payload_data = {
            "m_load": payload_info.m_load,
            "lcx_load": payload_info.lcx_load,
            "lcy_load": payload_info.lcy_load,
            "lcz_load": payload_info.lcz_load,
            "Ixx_load": payload_info.Ixx_load,
            "Iyy_load": payload_info.Iyy_load,
            "Izz_load": payload_info.Izz_load
        }
        
        return json.dumps({"status": "success", "data": payload_data}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"获取负载测定结果时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"获取负载测定结果时发生异常: {str(e)}"}, ensure_ascii=False)


def interference_check_for_payload_identify(ip, weight, angle):
    """开始负载测定的干涉检查
    
    参数:
        ip: 机器人控制柜IP地址
        weight: 负载重量
        angle: 6轴转动角度（30-90度）
        
    返回:
        str: JSON格式的操作结果
    """
    try:
        robot = robot_list.get(ip)
        if not robot:
            return json.dumps({"status": "error", "message": "机器人未连接"}, ensure_ascii=False)
        
        if not (30 <= angle <= 90):
            return json.dumps({"status": "error", "message": "角度必须在30-90度之间"}, ensure_ascii=False)
        
        ret = robot.motion.payload.interference_check_for_payload_identify(weight, angle)
        if ret != StatusCodeEnum.OK:
            return json.dumps({"status": "error", "message": f"干涉检查失败: {ret.errmsg}"}, ensure_ascii=False)
        
        return json.dumps({"status": "success", "message": "干涉检查成功"}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"干涉检查时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"干涉检查时发生异常: {str(e)}"}, ensure_ascii=False)


def payload_identify_start(ip):
    """进入负载测定状态
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: JSON格式的操作结果
    """
    try:
        robot = robot_list.get(ip)
        if not robot:
            return json.dumps({"status": "error", "message": "机器人未连接"}, ensure_ascii=False)
        
        ret = robot.motion.payload.payload_identify_start()
        if ret != StatusCodeEnum.OK:
            return json.dumps({"status": "error", "message": f"进入负载测定状态失败: {ret.errmsg}"}, ensure_ascii=False)
        
        return json.dumps({"status": "success", "message": "成功进入负载测定状态"}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"进入负载测定状态时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"进入负载测定状态时发生异常: {str(e)}"}, ensure_ascii=False)


def payload_identify_done(ip):
    """结束负载测定状态
    
    参数:
        ip: 机器人控制柜IP地址
        
    返回:
        str: JSON格式的操作结果
    """
    try:
        robot = robot_list.get(ip)
        if not robot:
            return json.dumps({"status": "error", "message": "机器人未连接"}, ensure_ascii=False)
        
        ret = robot.motion.payload.payload_identify_done()
        if ret != StatusCodeEnum.OK:
            return json.dumps({"status": "error", "message": f"结束负载测定状态失败: {ret.errmsg}"}, ensure_ascii=False)
        
        return json.dumps({"status": "success", "message": "成功结束负载测定状态"}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"结束负载测定状态时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"结束负载测定状态时发生异常: {str(e)}"}, ensure_ascii=False)


def payload_identify(ip, weight, angle):
    """负载测定全流程
    
    参数:
        ip: 机器人控制柜IP地址
        weight: 负载重量（未知重量填-1）
        angle: 6轴转动角度（30-90度）
        
    返回:
        str: JSON格式的负载测定结果
    """
    try:
        robot = robot_list.get(ip)
        if not robot:
            return json.dumps({"status": "error", "message": "机器人未连接"}, ensure_ascii=False)
        
        if not (30 <= angle <= 90):
            return json.dumps({"status": "error", "message": "角度必须在30-90度之间"}, ensure_ascii=False)
        
        payload_info, ret = robot.motion.payload.payload_identify(weight, angle)
        if ret != StatusCodeEnum.OK:
            return json.dumps({"status": "error", "message": f"负载测定失败: {ret.errmsg}"}, ensure_ascii=False)
        
        payload_data = {
            "m_load": payload_info.m_load,
            "lcx_load": payload_info.lcx_load,
            "lcy_load": payload_info.lcy_load,
            "lcz_load": payload_info.lcz_load,
            "Ixx_load": payload_info.Ixx_load,
            "Iyy_load": payload_info.Iyy_load,
            "Izz_load": payload_info.Izz_load
        }
        
        return json.dumps({"status": "success", "data": payload_data, "message": "负载测定成功"}, ensure_ascii=False)
    except Exception as e:
        logger.error(f"负载测定时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"负载测定时发生异常: {str(e)}"}, ensure_ascii=False)


def update_payload_from_identify(ip, payload_id, identify_result):
    """将负载测定结果更新到指定负载
    
    参数:
        ip: 机器人控制柜IP地址
        payload_id: 要更新的负载ID
        identify_result: 负载测定结果字典（来自payload_identify函数的返回）
        
    返回:
        str: JSON格式的操作结果
    """
    try:
        if identify_result.get("status") != "success":
            return json.dumps({"status": "error", "message": "负载测定结果无效"}, ensure_ascii=False)
        
        payload_data = identify_result.get("data", {})
        payload_data["id"] = payload_id
        
        if "m_load" in payload_data:
            payload_data["m_load"] = round(payload_data["m_load"], 3)
        
        return update_payload(ip, payload_data)
    except Exception as e:
        logger.error(f"从测定结果更新负载时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"从测定结果更新负载时发生异常: {str(e)}"}, ensure_ascii=False)
