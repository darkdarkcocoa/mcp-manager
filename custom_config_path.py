#!/usr/bin/env python3
import os
import sys
import json
import logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QLabel, QWidget

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('custom_config_path')

class ConfigPathSelector(QMainWindow):
    """클로드 설정 파일 경로 선택 창"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Claude 설정 파일 경로 선택")
        self.setGeometry(100, 100, 500, 200)
        
        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 안내 텍스트
        info_label = QLabel("Claude Desktop이 설치된 폴더를 선택해주세요.")
        layout.addWidget(info_label)
        
        # 현재 설정 경로
        self.path_label = QLabel("선택된 경로: 없음")
        layout.addWidget(self.path_label)
        
        # 버튼
        self.select_button = QPushButton("클로드 설치 폴더 선택")
        self.select_button.clicked.connect(self.select_folder)
        layout.addWidget(self.select_button)
        
        self.save_button = QPushButton("저장")
        self.save_button.clicked.connect(self.save_config_path)
        self.save_button.setEnabled(False)
        layout.addWidget(self.save_button)
        
        # 결과 텍스트
        self.result_label = QLabel("")
        layout.addWidget(self.result_label)
        
        # 선택된 경로
        self.selected_path = None
    
    def select_folder(self):
        """클로드 설치 폴더 선택"""
        folder = QFileDialog.getExistingDirectory(self, "클로드 설치 폴더 선택")
        if folder:
            self.selected_path = folder
            self.path_label.setText(f"선택된 경로: {folder}")
            self.save_button.setEnabled(True)
            
            # 설정 파일 존재 여부 확인
            config_path = os.path.join(folder, "claude_desktop_config.json")
            if os.path.exists(config_path):
                self.result_label.setText(f"기존 설정 파일을 발견했습니다: {config_path}")
            else:
                self.result_label.setText("선택한 폴더에 설정 파일이 없습니다. 새로 생성됩니다.")
    
    def save_config_path(self):
        """설정 파일 경로 저장"""
        if not self.selected_path:
            return
            
        try:
            # MCP 설정 관리자 설정 파일 경로
            config_dir = os.path.join(os.path.expanduser("~"), ".config", "mcp_manager")
            os.makedirs(config_dir, exist_ok=True)
            
            config_path = os.path.join(config_dir, "config.json")
            
            # 설정 저장
            config = {"claude_config_path": self.selected_path}
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            self.result_label.setText(f"설정이 저장되었습니다: {config_path}\n이제 MCP 설정 관리자를 다시 실행해주세요.")
            logger.info(f"클로드 설정 파일 경로 저장: {self.selected_path}")
        except Exception as e:
            self.result_label.setText(f"오류 발생: {e}")
            logger.error(f"설정 저장 오류: {e}")

def main():
    app = QApplication(sys.argv)
    window = ConfigPathSelector()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()