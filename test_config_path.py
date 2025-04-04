#!/usr/bin/env python3
"""
설정 파일 경로 테스트 스크립트

선택된 설정 파일을 읽어서 MCP 서버 목록을 출력합니다.
"""

import os
import sys
import json
import logging
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox

# 로깅 설정
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('test_config_path')

def select_config_file():
    """설정 파일 선택"""
    app = QApplication(sys.argv)
    
    # 파일 대화상자로 설정 파일 선택
    file_path, _ = QFileDialog.getOpenFileName(
        None, 
        "Claude 설정 파일 선택", 
        "", 
        "JSON 파일 (*.json);;모든 파일 (*)"
    )
    
    if not file_path:
        logger.warning("파일이 선택되지 않았습니다.")
        return None
    
    logger.info(f"선택된 파일: {file_path}")
    
    try:
        # 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            logger.info(f"파일 내용: {content}")
            
            # JSON 파싱
            config = json.loads(content)
            
            # MCP 서버 목록 확인
            mcp_servers = config.get('mcp_servers', [])
            logger.info(f"MCP 서버 수: {len(mcp_servers)}")
            
            for i, server in enumerate(mcp_servers):
                logger.info(f"MCP 서버 {i+1}: {server.get('name', '이름 없음')}")
            
            # 메시지 박스로 결과 표시
            if mcp_servers:
                server_names = "\n".join([f"{i+1}. {server.get('name', '이름 없음')}" for i, server in enumerate(mcp_servers)])
                QMessageBox.information(
                    None,
                    "설정 파일 분석 결과",
                    f"총 {len(mcp_servers)}개의 MCP 서버를 찾았습니다:\n\n{server_names}"
                )
            else:
                QMessageBox.warning(
                    None,
                    "설정 파일 분석 결과",
                    "MCP 서버 목록이 비어있습니다."
                )
            
            # MCP 설정 관리자 설정 파일 저장
            save_mcp_manager_config(file_path)
            
            return config
    except Exception as e:
        logger.error(f"파일 읽기 오류: {e}")
        logger.exception("상세 오류 정보:")
        QMessageBox.critical(
            None,
            "오류",
            f"설정 파일 읽기 중 오류가 발생했습니다: {e}"
        )
        return None
    finally:
        app.quit()

def save_mcp_manager_config(file_path):
    """MCP 설정 관리자 설정 파일 저장"""
    try:
        # MCP 설정 관리자 설정 파일 경로
        config_dir = os.path.join(os.path.expanduser("~"), ".config", "mcp_manager")
        os.makedirs(config_dir, exist_ok=True)
        
        config_path = os.path.join(config_dir, "config.json")
        
        # 설정 저장 (파일 경로 직접 저장)
        config = {"claude_config_path": os.path.dirname(file_path), "claude_config_file": file_path}
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        logger.info(f"MCP 설정 관리자 설정 파일 저장: {config_path}")
        QMessageBox.information(
            None,
            "설정 저장 완료",
            f"MCP 설정 관리자 설정 파일이 저장되었습니다:\n{config_path}"
        )
    except Exception as e:
        logger.error(f"설정 저장 오류: {e}")
        logger.exception("상세 오류 정보:")
        QMessageBox.critical(
            None,
            "오류",
            f"설정 저장 중 오류가 발생했습니다: {e}"
        )

if __name__ == "__main__":
    select_config_file()