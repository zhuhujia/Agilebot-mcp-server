# -*- coding: utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONUTF8'] = '1'
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

log_dir = Path("logs")
log_dir.mkdir(parents=True, exist_ok=True)
handler = RotatingFileHandler(
    str(log_dir / "agilebot_mcp_server.log"),
    maxBytes=1024 * 1024,
    backupCount=3,
    encoding="utf-8"
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

from .robot_core import cleanup_robot_connections
from .mcp_tools import mcp

def main():
    logger.info("Agilebot MCP Server 启动")
    logger.info("MCP服务器启动中...")
    try:
        mcp.run()
    except KeyboardInterrupt:
        logger.info("用户中断，MCP服务器停止")
    except Exception as e:
        logger.error(f"MCP服务器运行时发生异常: {str(e)}")
    finally:
        cleanup_robot_connections()
        logger.info("MCP服务器已停止")


if __name__ == "__main__":
    main()
