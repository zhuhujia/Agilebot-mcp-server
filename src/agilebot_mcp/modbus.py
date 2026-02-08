# -*- coding: utf-8 -*-
import json
import logging
from Agilebot.IR.A.status_code import StatusCodeEnum
from Agilebot.IR.A.sdk_types import ModbusChannel

from .robot_core import robot_list

logger = logging.getLogger(__name__)


def read_modbus_coils(ip: str, channel: int, slave_id: int, address: int, number: int, master_id: int = 0):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        if number > 120:
            return json.dumps({"status": "error", "message": "寄存器数量不能超过120个"}, ensure_ascii=False)
        
        slave = robot_list[ip].modbus.get_slave(ModbusChannel(channel), slave_id, master_id)
        values, ret = slave.read_coils(address, number)
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"读取Modbus线圈寄存器成功: {ip}, 通道: {channel}, 从机ID: {slave_id}, 地址: {address}, 数量: {number}")
            return json.dumps({"status": "success", "channel": channel, "slave_id": slave_id, "address": address, "values": values}, ensure_ascii=False)
        else:
            logger.error(f"读取Modbus线圈寄存器失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "读取Modbus线圈寄存器失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"读取Modbus线圈寄存器时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"读取Modbus线圈寄存器时发生异常: {str(e)}"}, ensure_ascii=False)


def write_modbus_coils(ip: str, channel: int, slave_id: int, address: int, values: list, master_id: int = 0):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        slave = robot_list[ip].modbus.get_slave(ModbusChannel(channel), slave_id, master_id)
        ret = slave.write_coils(address, values)
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"写入Modbus线圈寄存器成功: {ip}, 通道: {channel}, 从机ID: {slave_id}, 地址: {address}, 值: {values}")
            return json.dumps({"status": "success", "message": "写入Modbus线圈寄存器成功"}, ensure_ascii=False)
        else:
            logger.error(f"写入Modbus线圈寄存器失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "写入Modbus线圈寄存器失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"写入Modbus线圈寄存器时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"写入Modbus线圈寄存器时发生异常: {str(e)}"}, ensure_ascii=False)


def read_modbus_holding_regs(ip: str, channel: int, slave_id: int, address: int, number: int, master_id: int = 0):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        if number > 120:
            return json.dumps({"status": "error", "message": "寄存器数量不能超过120个"}, ensure_ascii=False)
        
        slave = robot_list[ip].modbus.get_slave(ModbusChannel(channel), slave_id, master_id)
        values, ret = slave.read_holding_regs(address, number)
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"读取Modbus保持寄存器成功: {ip}, 通道: {channel}, 从机ID: {slave_id}, 地址: {address}, 数量: {number}")
            return json.dumps({"status": "success", "channel": channel, "slave_id": slave_id, "address": address, "values": values}, ensure_ascii=False)
        else:
            logger.error(f"读取Modbus保持寄存器失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "读取Modbus保持寄存器失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"读取Modbus保持寄存器时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"读取Modbus保持寄存器时发生异常: {str(e)}"}, ensure_ascii=False)


def write_modbus_holding_regs(ip: str, channel: int, slave_id: int, address: int, values: list, master_id: int = 0):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        slave = robot_list[ip].modbus.get_slave(ModbusChannel(channel), slave_id, master_id)
        ret = slave.write_holding_regs(address, values)
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"写入Modbus保持寄存器成功: {ip}, 通道: {channel}, 从机ID: {slave_id}, 地址: {address}, 值: {values}")
            return json.dumps({"status": "success", "message": "写入Modbus保持寄存器成功"}, ensure_ascii=False)
        else:
            logger.error(f"写入Modbus保持寄存器失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "写入Modbus保持寄存器失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"写入Modbus保持寄存器时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"写入Modbus保持寄存器时发生异常: {str(e)}"}, ensure_ascii=False)


def read_modbus_discrete_inputs(ip: str, channel: int, slave_id: int, address: int, number: int, master_id: int = 0):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        if number > 120:
            return json.dumps({"status": "error", "message": "寄存器数量不能超过120个"}, ensure_ascii=False)
        
        slave = robot_list[ip].modbus.get_slave(ModbusChannel(channel), slave_id, master_id)
        values, ret = slave.read_discrete_inputs(address, number)
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"读取Modbus离散寄存器成功: {ip}, 通道: {channel}, 从机ID: {slave_id}, 地址: {address}, 数量: {number}")
            return json.dumps({"status": "success", "channel": channel, "slave_id": slave_id, "address": address, "values": values}, ensure_ascii=False)
        else:
            logger.error(f"读取Modbus离散寄存器失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "读取Modbus离散寄存器失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"读取Modbus离散寄存器时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"读取Modbus离散寄存器时发生异常: {str(e)}"}, ensure_ascii=False)


def read_modbus_input_regs(ip: str, channel: int, slave_id: int, address: int, number: int, master_id: int = 0):
    try:
        if ip not in robot_list:
            return json.dumps({"status": "error", "message": "请先连接机器人"}, ensure_ascii=False)
        
        if number > 120:
            return json.dumps({"status": "error", "message": "寄存器数量不能超过120个"}, ensure_ascii=False)
        
        slave = robot_list[ip].modbus.get_slave(ModbusChannel(channel), slave_id, master_id)
        values, ret = slave.read_input_regs(address, number)
        
        if ret == StatusCodeEnum.OK:
            logger.info(f"读取Modbus输入寄存器成功: {ip}, 通道: {channel}, 从机ID: {slave_id}, 地址: {address}, 数量: {number}")
            return json.dumps({"status": "success", "channel": channel, "slave_id": slave_id, "address": address, "values": values}, ensure_ascii=False)
        else:
            logger.error(f"读取Modbus输入寄存器失败: {ip}, 错误代码: {ret}")
            return json.dumps({"status": "error", "message": "读取Modbus输入寄存器失败"}, ensure_ascii=False)
            
    except Exception as e:
        logger.error(f"读取Modbus输入寄存器时发生异常: {ip}, 异常信息: {str(e)}")
        return json.dumps({"status": "error", "message": f"读取Modbus输入寄存器时发生异常: {str(e)}"}, ensure_ascii=False)
