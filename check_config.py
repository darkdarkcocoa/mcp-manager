#!/usr/bin/env python3
import os
import platform
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('check_config')

# OS별 기본 설정 파일 경로 확인
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

print(f"시스템: {system}")
print(f"홈 디렉토리: {home_dir}")
print(f"설정 디렉토리: {config_dir}")
print(f"설정 파일 경로: {config_path}")
print(f"설정 디렉토리 존재 여부: {os.path.exists(config_dir)}")
print(f"설정 파일 존재 여부: {os.path.exists(config_path)}")

# 설정 파일이 존재하면 내용 확인
if os.path.exists(config_path):
    try:
        import json
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"설정 파일 내용: {json.dumps(config, indent=2, ensure_ascii=False)}")
        print(f"MCP 서버 수: {len(config.get('mcp_servers', []))}")
    except Exception as e:
        print(f"설정 파일 로드 오류: {e}")