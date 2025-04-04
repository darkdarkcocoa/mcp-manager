"""
메인 윈도우 모듈

MCP 설정 관리자의 메인 윈도우 클래스를 정의합니다.
"""

import os
import sys
from PyQt6.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QListWidget, QListWidgetItem, QComboBox, 
                            QCheckBox, QScrollArea, QSplitter, QDialog,
                            QMessageBox, QGroupBox, QFormLayout, QTextEdit,
                            QMenuBar)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QAction

class MainWindow(QMainWindow):
    """MCP 설정 관리자의 메인 윈도우 클래스"""
    # 언어 변경 시그널 정의
    language_changed = pyqtSignal(str)
    
    def __init__(self):
        """메인 윈도우 초기화"""
        super().__init__()
        
        # 윈도우 설정 (초기화 시에는 기본값 설정, retranslateUi에서 변경)
        self.setWindowTitle("MCP Config Manager") 
        self.setMinimumSize(800, 600)
        
        # 메뉴바 생성
        self._create_menu_bar()
        
        # 중앙 위젯 설정
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 메인 레이아웃 설정
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # 탭 위젯 생성
        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)
        
        # 탭 생성
        self.available_mcp_tab = QWidget()
        self.my_mcp_tab = QWidget()
        
        # 탭 추가 (초기화 시에는 기본값 설정, retranslateUi에서 변경)
        self.tab_widget.addTab(self.available_mcp_tab, "Available MCPs")
        self.tab_widget.addTab(self.my_mcp_tab, "My MCPs")
        
        # 각 탭 설정
        self._setup_available_mcp_tab()
        self._setup_my_mcp_tab()
        
        # UI 텍스트 초기 번역 적용
        self.retranslateUi()
        
        # 상태 표시줄 설정 (초기화 시에는 기본값 설정, retranslateUi에서 변경)
        # self.statusBar().showMessage("준비") # retranslateUi에서 처리

    def _create_menu_bar(self):
        """메뉴바 생성 및 언어 변경 메뉴 추가"""
        menu_bar = self.menuBar()
        
        # 언어 메뉴
        language_menu = menu_bar.addMenu(self.tr("&Language"))
        
        # 영어 액션
        english_action = QAction(self.tr("English"), self)
        english_action.triggered.connect(lambda: self._change_language('en'))
        language_menu.addAction(english_action)
        
        # 한국어 액션
        korean_action = QAction(self.tr("한국어"), self)
        korean_action.triggered.connect(lambda: self._change_language('ko'))
        language_menu.addAction(korean_action)

    def _change_language(self, lang_code):
        """언어 변경 시그널 발생"""
        self.language_changed.emit(lang_code)
    
    def _setup_available_mcp_tab(self):
        """사용 가능한 MCP 탭 설정"""
        # 레이아웃 설정
        layout = QVBoxLayout(self.available_mcp_tab)
        
        # 검색 및 필터링 영역
        search_layout = QHBoxLayout()
        
        # 검색 입력 필드
        self.search_label = QLabel() # 텍스트는 retranslateUi에서 설정
        self.search_input = QLineEdit()
        # self.search_input.setPlaceholderText("MCP 이름 또는 키워드 입력") # retranslateUi에서 설정
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_input)
        
        # 카테고리 필터
        self.category_label = QLabel() # 텍스트는 retranslateUi에서 설정
        self.category_filter = QComboBox()
        # self.category_filter.addItems(["전체", "검색", "비전", "오디오", "문서", "유틸리티", "일반"]) # retranslateUi에서 설정
        search_layout.addWidget(self.category_label)
        search_layout.addWidget(self.category_filter)
        
        # 설치 방법 필터
        self.install_label = QLabel() # 텍스트는 retranslateUi에서 설정
        self.install_filter = QComboBox()
        # self.install_filter.addItems(["전체", "npm", "uvx", "docker"]) # retranslateUi에서 설정
        search_layout.addWidget(self.install_label)
        search_layout.addWidget(self.install_filter)
        
        # 검색 버튼
        self.search_button = QPushButton() # 텍스트는 retranslateUi에서 설정
        search_layout.addWidget(self.search_button)
        
        layout.addLayout(search_layout)
        
        # 스플리터 생성 (목록과 상세 정보 분할)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # MCP 목록 영역
        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        
        # MCP 목록 레이블
        self.list_label = QLabel() # 텍스트는 retranslateUi에서 설정
        self.list_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        list_layout.addWidget(self.list_label)
        
        # MCP 목록 위젯
        self.mcp_list = QListWidget()
        self.mcp_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        list_layout.addWidget(self.mcp_list)
        
        # 선택 버튼 영역
        button_layout = QHBoxLayout()
        self.select_all_button = QPushButton() # 텍스트는 retranslateUi에서 설정
        self.deselect_all_button = QPushButton() # 텍스트는 retranslateUi에서 설정
        self.apply_button = QPushButton() # 텍스트는 retranslateUi에서 설정
        self.apply_button.setStyleSheet("background-color: #4CAF50; color: white;")
        
        button_layout.addWidget(self.select_all_button)
        button_layout.addWidget(self.deselect_all_button)
        button_layout.addStretch()
        button_layout.addWidget(self.apply_button)
        
        list_layout.addLayout(button_layout)
        
        # 상세 정보 영역
        detail_widget = QWidget()
        detail_layout = QVBoxLayout(detail_widget)
        
        # 상세 정보 레이블
        self.detail_label = QLabel() # 텍스트는 retranslateUi에서 설정
        self.detail_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        detail_layout.addWidget(self.detail_label)
        
        # 상세 정보 스크롤 영역
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        # 상세 정보 컨텐츠 위젯
        self.detail_content = QWidget()
        self.detail_layout = QVBoxLayout(self.detail_content)
        
        # 기본 상세 정보 표시
        self.detail_name = QLabel() # 텍스트는 retranslateUi에서 설정
        self.detail_name.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.detail_description = QLabel() # 텍스트는 retranslateUi에서 설정
        self.detail_description.setWordWrap(True)
        
        self.detail_layout.addWidget(self.detail_name)
        self.detail_layout.addWidget(self.detail_description)
        
        # 설치 옵션 그룹
        self.install_group = QGroupBox() # 텍스트는 retranslateUi에서 설정
        self.install_layout = QVBoxLayout(self.install_group)
        self.detail_layout.addWidget(self.install_group)
        
        # 환경 변수 그룹
        self.env_group = QGroupBox() # 텍스트는 retranslateUi에서 설정
        self.env_layout = QFormLayout(self.env_group)
        self.detail_layout.addWidget(self.env_group)
        
        # 인자 옵션 그룹
        self.args_group = QGroupBox() # 텍스트는 retranslateUi에서 설정
        self.args_layout = QFormLayout(self.args_group)
        self.detail_layout.addWidget(self.args_group)
        
        # 스크롤 영역에 상세 정보 컨텐츠 설정
        scroll_area.setWidget(self.detail_content)
        detail_layout.addWidget(scroll_area)
        
        # 스플리터에 위젯 추가
        splitter.addWidget(list_widget)
        splitter.addWidget(detail_widget)
        
        # 스플리터 비율 설정 (4:6)
        splitter.setSizes([400, 600])
        
        layout.addWidget(splitter)
    
    def _setup_my_mcp_tab(self):
        """내 MCP 탭 설정"""
        # 레이아웃 설정
        layout = QVBoxLayout(self.my_mcp_tab)
        
        # 현재 설정 파일 정보 영역
        config_info_layout = QHBoxLayout()
        
        self.config_label = QLabel() # 텍스트는 retranslateUi에서 설정
        self.config_path = QLabel() # 텍스트는 retranslateUi에서 설정
        config_info_layout.addWidget(self.config_label)
        config_info_layout.addWidget(self.config_path)
        config_info_layout.addStretch()
        
        self.change_config_path_button = QPushButton() # 텍스트는 retranslateUi에서 설정
        self.backup_button = QPushButton() # 텍스트는 retranslateUi에서 설정
        self.restore_button = QPushButton() # 텍스트는 retranslateUi에서 설정
        
        config_info_layout.addWidget(self.change_config_path_button)
        config_info_layout.addWidget(self.backup_button)
        config_info_layout.addWidget(self.restore_button)
        
        layout.addLayout(config_info_layout)
        
        # 내 MCP 목록 영역
        self.my_mcp_label = QLabel() # 텍스트는 retranslateUi에서 설정
        self.my_mcp_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(self.my_mcp_label)
        
        # 내 MCP 목록 위젯
        self.my_mcp_list = QListWidget()
        layout.addWidget(self.my_mcp_list)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        self.add_button = QPushButton() # 텍스트는 retranslateUi에서 설정
        self.edit_button = QPushButton() # 텍스트는 retranslateUi에서 설정
        self.delete_button = QPushButton() # 텍스트는 retranslateUi에서 설정
        self.move_up_button = QPushButton() # 텍스트는 retranslateUi에서 설정
        self.move_down_button = QPushButton() # 텍스트는 retranslateUi에서 설정
        self.save_button = QPushButton() # 텍스트는 retranslateUi에서 설정
        self.save_button.setStyleSheet("background-color: #4CAF50; color: white;")
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.move_up_button)
        button_layout.addWidget(self.move_down_button)
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
    
    def show_mcp_detail(self, mcp_info):
        """MCP 상세 정보 표시"""
        # 기본 정보 업데이트
        self.detail_name.setText(mcp_info.get('name', self.tr('Unknown MCP')))
        self.detail_description.setText(mcp_info.get('description', self.tr('No description available.')))
        
        # 설치 옵션 업데이트
        # 기존 위젯 제거
        while self.install_layout.count():
            item = self.install_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # 설치 옵션 추가
        install_options = mcp_info.get('installation_options', [])
        if install_options:
            for option in install_options:
                option_checkbox = QCheckBox(option)
                self.install_layout.addWidget(option_checkbox)
        else:
            self.install_layout.addWidget(QLabel(self.tr("No installation options info")))
        
        # 환경 변수 업데이트
        # 기존 위젯 제거
        while self.env_layout.count():
            item = self.env_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # 환경 변수 추가
        env_vars = mcp_info.get('env_vars', [])
        if env_vars:
            for env_var in env_vars:
                env_input = QLineEdit()
                env_input.setPlaceholderText(self.tr("Enter {0} value").format(env_var))
                self.env_layout.addRow(env_var, env_input)
        else:
            self.env_layout.addRow(QLabel(self.tr("No environment variable info")))
        
        # 인자 옵션 업데이트
        # 기존 위젯 제거
        while self.args_layout.count():
            item = self.args_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # 인자 옵션 추가
        args = mcp_info.get('args', [])
        if args:
            for arg in args:
                arg_input = QLineEdit()
                arg_input.setPlaceholderText(self.tr("Enter value"))
                self.args_layout.addRow(arg, arg_input)
        else:
            self.args_layout.addRow(QLabel(self.tr("No argument options info")))
    
    def populate_mcp_list(self, mcp_servers):
        """MCP 서버 목록 채우기"""
        # 목록 초기화
        self.mcp_list.clear()
        
        # MCP 서버 추가
        for server in mcp_servers:
            # 이름이 없는 경우 처리
            name = server.get('name', self.tr('Unnamed MCP Server')) 
            item = QListWidgetItem(name)
            item.setData(Qt.ItemDataRole.UserRole, server)
            self.mcp_list.addItem(item)
    
    def populate_my_mcp_list(self, my_mcp_servers):
        """내 MCP 서버 목록 채우기"""
        # 목록 초기화
        self.my_mcp_list.clear()
        
        # 내 MCP 서버 추가
        for server in my_mcp_servers:
             # 이름이 없는 경우 처리
            name = server.get('name', self.tr('Unnamed MCP Server'))
            item = QListWidgetItem(name)
            item.setData(Qt.ItemDataRole.UserRole, server)
            self.my_mcp_list.addItem(item)
    
    def set_config_path(self, path):
        """설정 파일 경로 설정"""
        # self.config_path QLabel에 경로 설정
        if hasattr(self, 'config_path') and isinstance(self.config_path, QLabel):
            self.config_path.setText(path if path else self.tr("Loading..."))
        else:
             print("Warning: config_path QLabel not found or not a QLabel")
    
    def show_error_message(self, title, message):
        """오류 메시지 표시"""
        QMessageBox.critical(self, title, message)
    
    def show_info_message(self, title, message):
        """정보 메시지 표시"""
        QMessageBox.information(self, title, message)
    
    def show_confirm_message(self, title, message):
        """확인 메시지 표시"""
        reply = QMessageBox.question(self, title, message,
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        return reply == QMessageBox.StandardButton.Yes

    def retranslateUi(self):
        """UI의 모든 텍스트를 현재 언어로 다시 번역합니다."""
        self.setWindowTitle(self.tr("MCP Config Manager"))
        self.tab_widget.setTabText(0, self.tr("Available MCPs"))
        self.tab_widget.setTabText(1, self.tr("My MCPs"))
        self.statusBar().showMessage(self.tr("Ready"))

        # 사용 가능한 MCP 탭
        self.search_label.setText(self.tr("Search:"))
        self.search_input.setPlaceholderText(self.tr("Enter MCP name or keyword"))
        self.category_label.setText(self.tr("Category:"))
        # QComboBox 아이템은 변경 시점에 다시 설정해야 할 수 있음
        # 임시 방편: 현재 아이템 유지 또는 필요 시 다시 채우기
        # self.category_filter.clear()
        # self.category_filter.addItems([self.tr("All"), self.tr("Search"), ...]) 
        self.install_label.setText(self.tr("Install Method:"))
        # self.install_filter.clear()
        # self.install_filter.addItems([self.tr("All"), "npm", "uvx", "docker"])
        self.search_button.setText(self.tr("Search"))
        self.list_label.setText(self.tr("MCP Server List"))
        self.select_all_button.setText(self.tr("Select All"))
        self.deselect_all_button.setText(self.tr("Deselect All"))
        self.apply_button.setText(self.tr("Apply"))
        self.detail_label.setText(self.tr("MCP Details"))
        # 상세 정보 초기 텍스트
        if not self.mcp_list.currentItem(): # 선택된 항목이 없을 때만 업데이트
             self.detail_name.setText(self.tr("No MCP Selected"))
             self.detail_description.setText(self.tr("Select an MCP to see details."))
        self.install_group.setTitle(self.tr("Installation Options"))
        self.env_group.setTitle(self.tr("Environment Variables"))
        self.args_group.setTitle(self.tr("Argument Options"))

        # 내 MCP 탭
        self.config_label.setText(self.tr("Current Config File:"))
        # self.config_path 레이블은 set_config_path에서 관리
        self.change_config_path_button.setText(self.tr("Change Path"))
        self.backup_button.setText(self.tr("Backup"))
        self.restore_button.setText(self.tr("Restore"))
        self.my_mcp_label.setText(self.tr("Installed MCP Servers"))
        self.add_button.setText(self.tr("Add"))
        self.edit_button.setText(self.tr("Edit"))
        self.delete_button.setText(self.tr("Delete"))
        self.move_up_button.setText(self.tr("Move Up"))
        self.move_down_button.setText(self.tr("Move Down"))
        self.save_button.setText(self.tr("Save"))

        # 메뉴바 텍스트 (필요 시)
        # self.menuBar().actions()[0].setText(self.tr("&Language"))
        # self.menuBar().actions()[0].menu().actions()[0].setText(self.tr("English"))
        # self.menuBar().actions()[0].menu().actions()[1].setText(self.tr("한국어"))
        # 참고: 메뉴 아이템은 생성 시 이미 tr()로 감싸져 있으므로 자동 갱신될 수 있음
