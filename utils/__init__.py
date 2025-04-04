"""
MCP 설정 관리자의 유틸리티 패키지

유틸리티 함수를 제공합니다.
"""

import os
import sys
import logging
import platform
import subprocess

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('utils')

def restart_claude_desktop():
    """
    Claude Desktop 애플리케이션을 재시작합니다.
    
    Returns:
        bool: 재시작 성공 여부
    """
    try:
        system = platform.system()
        
        if system == "Windows":
            # Windows에서 Claude Desktop 프로세스 종료 및 재시작
            subprocess.run(["taskkill", "/F", "/IM", "Claude.exe"], check=False)
            subprocess.Popen(["start", "", "Claude.exe"], shell=True)
        elif system == "Darwin":  # macOS
            # macOS에서 Claude Desktop 프로세스 종료 및 재시작
            subprocess.run(["pkill", "-x", "Claude"], check=False)
            subprocess.Popen(["open", "-a", "Claude"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:  # Linux
            # Linux에서 Claude Desktop 프로세스 종료 및 재시작
            subprocess.run(["pkill", "-x", "Claude"], check=False)
            subprocess.Popen(["Claude"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        logger.info("Claude Desktop 애플리케이션을 재시작했습니다.")
        return True
    except Exception as e:
        logger.error(f"Claude Desktop 재시작 오류: {e}")
        return False

def get_app_version():
    """
    애플리케이션 버전을 반환합니다.
    
    Returns:
        str: 애플리케이션 버전
    """
    return "1.0.0"
