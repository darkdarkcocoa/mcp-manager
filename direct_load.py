#!/usr/bin/env python3
"""
설정 파일에서 MCP 서버를 직접 로드하는 도구

설정 파일에서 모든 MCP 서버를 읽어와서 표시합니다.
"""

import os
import sys
import json
import logging
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, 
                            QListWidget, QListWidgetItem, QMessageBox, 
                            QWidget, QTextEdit, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# 로깅 설정
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('direct_load')

class DirectLoadWindow(QMainWindow):
    """설정 파일 직접 로드 창"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Claude 설정 파일 직접 로드")
        self.setGeometry(100, 100, 800, 600)
        
        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 파일 선택 영역
        file_layout = QHBoxLayout()
        
        self.file_path_label = QLabel("설정 파일을 선택하세요")
        file_layout.addWidget(self.file_path_label)
        
        select_file_button = QPushButton("파일 선택")
        select_file_button.clicked.connect(self.select_file)
        file_layout.addWidget(select_file_button)
        
        layout.addLayout(file_layout)
        
        # 설정 파일 내용 표시
        content_label = QLabel("설정 파일 내용:")
        content_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(content_label)
        
        self.content_text = QTextEdit()
        self.content_text.setReadOnly(True)
        layout.addWidget(self.content_text)
        
        # MCP 서버 목록 영역
        servers_label = QLabel("MCP 서버 목록:")
        servers_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(servers_label)
        
        self.servers_list = QListWidget()
        layout.addWidget(self.servers_list)
        
        # 상태 표시줄 설정
        self.statusBar().showMessage("준비")
        
        # 설정 파일 경로
        self.config_path = None
    
    def select_file(self):
        """설정 파일 선택"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Claude 설정 파일 선택", 
            "", 
            "JSON 파일 (*.json);;모든 파일 (*)"
        )
        
        if file_path:
            self.config_path = file_path
            self.file_path_label.setText(f"선택된 파일: {file_path}")
            self.load_config()
    
    def load_config(self):
        """설정 파일 로드"""
        if not self.config_path:
            return
            
        try:
            # 설정 파일 읽기
            with open(self.config_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.content_text.setText(content)
                
                # JSON 파싱
                config = json.loads(content)
                
                # MCP 서버 목록 추출
                servers = self.extract_servers(config)
                
                # 목록 표시
                self.display_servers(servers)
                
                # 상태 표시줄 업데이트
                self.statusBar().showMessage(f"총 {len(servers)}개의 MCP 서버를 로드했습니다.")
                
        except Exception as e:
            logger.error(f"설정 파일 로드 오류: {e}")
            logger.exception("상세 오류 정보:")
            QMessageBox.critical(
                self,
                "오류",
                f"설정 파일 로드 중 오류가 발생했습니다: {e}"
            )
    
    def extract_servers(self, config):
        """설정에서 MCP 서버 목록 추출"""
        servers = []
        
        # 1. mcp_servers 키가 있는 경우
        if "mcp_servers" in config and isinstance(config["mcp_servers"], list):
            servers = config["mcp_servers"]
            logger.info(f"mcp_servers 키에서 {len(servers)}개의 서버를 찾았습니다.")
        
        # 2. 키가 없는 경우, 모든 최상위 항목을 서버로 처리
        elif isinstance(config, dict):
            for key, value in config.items():
                if isinstance(value, dict):
                    # name 키가 있으면 그대로 사용
                    if "name" in value:
                        servers.append(value)
                    # 없으면 키를 name으로 사용
                    else:
                        server = value.copy()
                        server["name"] = key
                        servers.append(server)
            
            logger.info(f"최상위 항목에서 {len(servers)}개의 서버를 찾았습니다.")
        
        # 3. 설정이 서버 목록인 경우
        elif isinstance(config, list):
            for item in config:
                if isinstance(item, dict):
                    # name 키가 있는지 확인
                    if "name" in item:
                        servers.append(item)
                    else:
                        # 기본 이름 추가
                        server = item.copy()
                        server["name"] = f"서버 {len(servers) + 1}"
                        servers.append(server)
            
            logger.info(f"목록에서 {len(servers)}개의 서버를 찾았습니다.")
        
        # 필수 필드 없는 항목 처리
        for server in servers:
            if "name" not in server:
                server["name"] = "이름 없는 MCP 서버"
            
            if "description" not in server:
                server["description"] = "설명 없음"
            
            if "installation_options" not in server:
                server["installation_options"] = []
            
            if "env_vars" not in server:
                server["env_vars"] = []
            
            if "args" not in server:
                server["args"] = []
            
            if "category" not in server:
                server["category"] = "일반"
        
        return servers
    
    def display_servers(self, servers):
        """MCP 서버 목록 표시"""
        # 목록 초기화
        self.servers_list.clear()
        
        # 서버 목록 채우기
        for i, server in enumerate(servers):
            name = server.get("name", f"서버 {i+1}")
            desc = server.get("description", "설명 없음")
            item = QListWidgetItem(f"{name} - {desc}")
            item.setData(Qt.ItemDataRole.UserRole, server)
            self.servers_list.addItem(item)
        
        # MCP 서버 목록을 저장 옵션 제공
        if servers:
            # MCP 설정 관리자 설정 파일 경로
            config_dir = os.path.join(os.path.expanduser("~"), ".config", "mcp_manager")
            os.makedirs(config_dir, exist_ok=True)
            
            config_path = os.path.join(config_dir, "config.json")
            
            # 설정 저장
            if QMessageBox.question(
                self,
                "설정 저장",
                f"이 설정 파일({self.config_path})을 MCP 설정 관리자의 기본 설정 파일로 지정하시겠습니까?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            ) == QMessageBox.StandardButton.Yes:
                try:
                    # 설정 저장
                    config = {"claude_config_path": os.path.dirname(self.config_path), "claude_config_file": self.config_path}
                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump(config, f, ensure_ascii=False, indent=2)
                    
                    QMessageBox.information(
                        self,
                        "설정 저장 완료",
                        f"MCP 설정 관리자 설정 파일이 저장되었습니다:\n{config_path}\n\n이제 MCP 설정 관리자를 실행하면 이 설정 파일이 사용됩니다."
                    )
                except Exception as e:
                    logger.error(f"설정 저장 오류: {e}")
                    QMessageBox.critical(
                        self,
                        "오류",
                        f"설정 저장 중 오류가 발생했습니다: {e}"
                    )

def main():
    app = QApplication(sys.argv)
    window = DirectLoadWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()