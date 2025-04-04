"""
설정 파일 관리자 테스트 스크립트

설정 파일 관리 기능을 테스트합니다.
"""

import os
import sys
import json

# 상위 디렉토리를 모듈 검색 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config_manager import ConfigManager

def test_config_manager():
    """설정 파일 관리자 테스트 함수"""
    print("설정 파일 관리자 테스트를 시작합니다...")
    
    # 테스트용 설정 디렉토리 설정
    test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_config")
    os.makedirs(test_dir, exist_ok=True)
    test_config_path = os.path.join(test_dir, "test_claude_desktop_config.json")
    
    # ConfigManager 인스턴스 생성
    config_manager = ConfigManager(config_path=test_config_path)
    
    # 1. 기본 설정 로드 테스트
    print("\n1. 기본 설정 로드 테스트")
    config = config_manager.load_config()
    print(f"기본 설정: {json.dumps(config, ensure_ascii=False, indent=2)}")
    
    # 2. MCP 서버 추가 테스트
    print("\n2. MCP 서버 추가 테스트")
    test_server1 = {
        "name": "테스트 서버 1",
        "description": "테스트용 MCP 서버 1",
        "installation_options": ["npm", "docker"],
        "env_vars": ["API_KEY", "SERVER_URL"],
        "args": ["--port", "--verbose"],
        "category": "search",
        "enabled": True
    }
    
    test_server2 = {
        "name": "테스트 서버 2",
        "description": "테스트용 MCP 서버 2",
        "installation_options": ["uvx"],
        "env_vars": ["SECRET_KEY"],
        "args": ["--debug"],
        "category": "vision",
        "enabled": False
    }
    
    result = config_manager.add_mcp_server(test_server1)
    print(f"서버 1 추가 결과: {result}")
    
    result = config_manager.add_mcp_server(test_server2)
    print(f"서버 2 추가 결과: {result}")
    
    # 3. MCP 서버 목록 가져오기 테스트
    print("\n3. MCP 서버 목록 가져오기 테스트")
    mcp_servers = config_manager.get_mcp_servers()
    print(f"MCP 서버 목록 ({len(mcp_servers)}개):")
    for i, server in enumerate(mcp_servers):
        print(f"{i+1}. {server['name']} - {server['description']}")
        print(f"   활성화 상태: {server['enabled']}")
    
    # 4. MCP 서버 업데이트 테스트
    print("\n4. MCP 서버 업데이트 테스트")
    mcp_servers[0]["description"] = "업데이트된 설명"
    result = config_manager.update_mcp_server(0, mcp_servers[0])
    print(f"서버 업데이트 결과: {result}")
    
    # 5. MCP 서버 순서 변경 테스트
    print("\n5. MCP 서버 순서 변경 테스트")
    result = config_manager.move_mcp_server(0, 1)
    print(f"서버 순서 변경 결과: {result}")
    
    # 6. MCP 서버 활성화 상태 토글 테스트
    print("\n6. MCP 서버 활성화 상태 토글 테스트")
    result = config_manager.toggle_mcp_server(0)
    print(f"서버 활성화 상태 토글 결과: {result}")
    
    # 7. 설정 파일 백업 테스트
    print("\n7. 설정 파일 백업 테스트")
    backup_list = config_manager.get_backup_list()
    print(f"백업 파일 목록 ({len(backup_list)}개):")
    for i, backup in enumerate(backup_list):
        print(f"{i+1}. {backup['filename']} - {backup['date']} ({backup['size']})")
    
    # 8. MCP 서버 제거 테스트
    print("\n8. MCP 서버 제거 테스트")
    result = config_manager.remove_mcp_server(0)
    print(f"서버 제거 결과: {result}")
    
    # 9. 최종 설정 확인
    print("\n9. 최종 설정 확인")
    final_config = config_manager.load_config()
    print(f"최종 설정: {json.dumps(final_config, ensure_ascii=False, indent=2)}")
    
    print("\n설정 파일 관리자 테스트를 완료했습니다.")
    print(f"테스트 설정 파일 경로: {test_config_path}")

if __name__ == "__main__":
    test_config_manager()
