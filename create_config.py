#!/usr/bin/env python3
import os
import json
import platform
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('create_config')

# OS별 기본 설정 파일 경로 설정
system = platform.system()
home_dir = os.path.expanduser("~")

if system == "Windows":
    # Windows: %APPDATA%/Claude/claude_desktop_config.json
    config_dir = os.path.join(os.getenv('APPDATA') or "", "Claude")
elif system == "Darwin":  # macOS
    # macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
    config_dir = os.path.join(home_dir, "Library", "Application Support", "Claude")
else:  # Linux 및 기타
    # Linux: ~/.config/Claude/claude_desktop_config.json
    config_dir = os.path.join(home_dir, ".config", "Claude")

config_path = os.path.join(config_dir, "claude_desktop_config.json")

# 디렉토리가 없으면 생성
if not os.path.exists(config_dir):
    try:
        os.makedirs(config_dir)
        logger.info(f"설정 디렉토리 생성: {config_dir}")
    except Exception as e:
        logger.error(f"설정 디렉토리 생성 오류: {e}")
        exit(1)

# 기본 설정 파일 생성
if not os.path.exists(config_path):
    try:
        # 기본 설정 내용
        default_config = {
            "mcp_servers": [
                {
                    "name": "예제 MCP 서버",
                    "description": "예제 MCP 서버 설명",
                    "installation_options": ["npm", "docker"],
                    "env_vars": ["API_KEY", "SERVER_URL"],
                    "args": ["--port", "--verbose"],
                    "category": "search",
                    "enabled": True
                }
            ]
        }
        
        # 설정 파일 저장
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        
        logger.info(f"기본 설정 파일 생성: {config_path}")
    except Exception as e:
        logger.error(f"설정 파일 생성 오류: {e}")
        exit(1)

print(f"설정 파일이 생성되었습니다: {config_path}")
print(f"이제 프로그램을 다시 실행하면 MCP 목록이 로드될 것입니다.")