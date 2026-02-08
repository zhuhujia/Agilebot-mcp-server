# -*- coding: utf-8 -*-
import json
import logging
from Agilebot.IR.A.status_code import StatusCodeEnum
from Agilebot.IR.A.sdk_types import CoordinateSystemType
from Agilebot.IR.A.sdk_classes import GeometryPose, CoordinateInfo, Translation, Rotation

from .robot_core import robot_list

logger = logging.getLogger(__name__)


def get_coordinate_list(ip: str, sys_type: int):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        if sys_type == 0:
            coord_type = CoordinateSystemType.UserFrame
        elif sys_type == 1:
            coord_type = CoordinateSystemType.ToolFrame
        else:
            return json.dumps({"status": "error", "message": "无效的坐标系类型，0=用户坐标系，1=工具坐标系"}, ensure_ascii=False)
        
        coord_list, ret = robot_list[ip].coordinate_system.get_coordinate_list(coord_type)
        
        if ret == StatusCodeEnum.OK:
            result = []
            fields = coord_list.ListFields()
            if fields:
                coord_container = fields[0][1]
                for coord in coord_container:
                    result.append({
                        "id": coord.id,
                        "name": coord.name,
                        "comment": coord.comment,
                        "group_id": coord.group_id
                    })
            logger.info(f"获取坐标系列表成功: {ip}, 类型: {sys_type}")
            return json.dumps({"status": "success", "data": result}, ensure_ascii=False)
        else:
            logger.error(f"获取坐标系列表失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "获取坐标系列表失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"获取坐标系列表时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"获取坐标系列表时发生异常: {str(e)}"}, ensure_ascii=False)


def add_coordinate(ip: str, sys_type: int):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        if sys_type == 0:
            coord_type = CoordinateSystemType.UserFrame
        elif sys_type == 1:
            coord_type = CoordinateSystemType.ToolFrame
        else:
            return json.dumps({"status": "error", "message": "无效的坐标系类型，0=用户坐标系，1=工具坐标系"}, ensure_ascii=False)
        
        coord, ret = robot_list[ip].coordinate_system.add(coord_type)
        
        if ret == StatusCodeEnum.OK:
            result = {
                "id": coord.coordinate_info.coordinate_id,
                "name": coord.coordinate_info.name,
                "comment": coord.coordinate_info.comment,
                "group_id": coord.coordinate_info.group_id,
                "position": {
                    "x": coord.position.x,
                    "y": coord.position.y,
                    "z": coord.position.z
                },
                "orientation": {
                    "r": coord.orientation.r,
                    "p": coord.orientation.p,
                    "y": coord.orientation.y
                }
            }
            logger.info(f"添加坐标系成功: {ip}, 类型: {sys_type}, ID: {coord.coordinate_info.coordinate_id}")
            return json.dumps({"status": "success", "data": result}, ensure_ascii=False)
        else:
            logger.error(f"添加坐标系失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "添加坐标系失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"添加坐标系时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"添加坐标系时发生异常: {str(e)}"}, ensure_ascii=False)


def delete_coordinate(ip: str, sys_type: int, coordinate_id: int):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人器"}, ensure_ascii=False)
        
        if sys_type == 0:
            coord_type = CoordinateSystemType.UserFrame
        elif sys_type == 1:
            coord_type = CoordinateSystemType.ToolFrame
        else:
            return json.dumps({"status": "error", "message": "无效的坐标系类型，0=用户坐标系，1=工具坐标系"}, ensure_ascii=False)
        
        ret = robot_list[ip].coordinate_system.delete(coord_type, coordinate_id)
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"删除坐标系成功: {ip}, 类型: {sys_type}, ID: {coordinate_id}")
            return json.dumps({"status": "success", "message": "删除坐标系成功"}, ensure_ascii=False)
        else:
            logger.error(f"删除坐标系失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "删除坐标系失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"删除坐标系时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"删除坐标系时发生异常: {str(e)}"}, ensure_ascii=False)


def update_coordinate(ip: str, sys_type: int, coordinate_data: str):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        if sys_type == 0:
            coord_type = CoordinateSystemType.UserFrame
        elif sys_type == 1:
            coord_type = CoordinateSystemType.ToolFrame
        else:
            return json.dumps({"status": "error", "message": "无效的坐标系类型，0=用户坐标系，1=工具坐标系"}, ensure_ascii=False)
        
        data = json.loads(coordinate_data)
        
        coord_info = CoordinateInfo()
        coord_info.coordinate_id = data.get("id", 0)
        coord_info.name = data.get("name", "")
        coord_info.comment = data.get("comment", "")
        coord_info.group_id = data.get("group_id", 0)
        
        position = Translation()
        position.x = data["position"]["x"]
        position.y = data["position"]["y"]
        position.z = data["position"]["z"]
        
        orientation = Rotation()
        orientation.r = data["orientation"]["r"]
        orientation.p = data["orientation"]["p"]
        orientation.y = data["orientation"]["y"]
        
        coord = GeometryPose(coord_info, position, orientation)
        
        ret = robot_list[ip].coordinate_system.update(coord_type, coord)
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"更新坐标系成功: {ip}, 类型: {sys_type}, ID: {coord_info.coordinate_id}")
            return json.dumps({"status": "success", "message": "更新坐标系成功"}, ensure_ascii=False)
        else:
            logger.error(f"更新坐标系失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "更新坐标系失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"更新坐标系时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"更新坐标系时发生异常: {str(e)}"}, ensure_ascii=False)


def get_coordinate(ip: str, sys_type: int, coordinate_id: int):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        if sys_type == 0:
            coord_type = CoordinateSystemType.UserFrame
        elif sys_type == 1:
            coord_type = CoordinateSystemType.ToolFrame
        else:
            return json.dumps({"status": "error", "message": "无效的坐标系类型，0=用户坐标系，1=工具坐标系"}, ensure_ascii=False)
        
        coord, ret = robot_list[ip].coordinate_system.get(coord_type, coordinate_id)
        
        if ret == StatusCodeEnum.OK:
            result = {
                "id": coord.coordinate_info.coordinate_id,
                "name": coord.coordinate_info.name,
                "comment": coord.coordinate_info.comment,
                "group_id": coord.coordinate_info.group_id,
                "position": {
                    "x": coord.position.x,
                    "y": coord.position.y,
                    "z": coord.position.z
                },
                "orientation": {
                    "r": coord.orientation.r,
                    "p": coord.orientation.p,
                    "y": coord.orientation.y
                }
            }
            logger.info(f"获取坐标系成功: {ip}, 类型: {sys_type}, ID: {coordinate_id}")
            return json.dumps({"status": "success", "data": result}, ensure_ascii=False)
        else:
            logger.error(f"获取坐标系失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "获取坐标系失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"获取坐标系时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"获取坐标系时发生异常: {str(e)}"}, ensure_ascii=False)
