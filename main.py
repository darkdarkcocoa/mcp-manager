"""
MCP 설정 관리자 메인 애플리케이션

크롤러, UI, 설정 파일 관리자를 통합하는 메인 애플리케이션 코드입니다.
"""

import os
import sys
import logging
import subprocess
import json
from PyQt6.QtWidgets import QApplication, QMessageBox, QListWidgetItem, QFileDialog
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTranslator, QLocale

from ui.main_window import MainWindow
from crawler.github_crawler import GitHubCrawler
from config.config_manager import ConfigManager
import utils

# 로깅 설정
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger('main')

class MCPLoaderThread(QThread):
    """MCP 서버 정보를 비동기적으로 로드하는 스레드"""
    
    # 시그널 정의
    finished = pyqtSignal(list)
    progress = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, force_refresh=False):
        """
        MCPLoaderThread 초기화
        
        Args:
            force_refresh (bool, optional): 캐시를 무시하고 강제로 새로고침할지 여부. 기본값은 False입니다.
        """
        super().__init__()
        self.force_refresh = force_refresh
    
    def run(self):
        """스레드 실행"""
        try:
            self.progress.emit("MCP 서버 목록을 가져오는 중...")
            
            # GitHub 크롤러 생성
            crawler = GitHubCrawler()
            
            # MCP 서버 목록 가져오기
            mcp_servers = crawler.get_mcp_servers(force_refresh=self.force_refresh)
            
            self.progress.emit(f"총 {len(mcp_servers)}개의 MCP 서버를 찾았습니다.")
            
            # 결과 전송
            self.finished.emit(mcp_servers)
        except Exception as e:
            logger.error(f"MCP 서버 로드 오류: {e}")
            self.error.emit(f"MCP 서버 로드 오류: {e}")

class MCPConfigManager:
    """MCP 설정 관리자 메인 클래스"""
    
    def __init__(self):
        """MCPConfigManager 초기화"""
        # 애플리케이션 생성
        self.app = QApplication(sys.argv)
        
        # 번역기 설정
        self.translator = QTranslator()
        
        # 메인 윈도우 생성
        self.main_window = MainWindow()
        
        # 설정 파일 관리자 생성
        self.config_manager = ConfigManager()
        
        # 설정 파일 경로 검증
        self._validate_config_path()
        
        # 이벤트 연결
        self._connect_events()
        
        # 초기 설정
        self._initialize()

        # 기본 언어 설정 (예: 영어)
        self._load_language('en') 
    
    def _validate_config_path(self):
        """설정 파일 경로 검증"""
        # 설정 파일이 존재하는지 확인
        if not os.path.exists(self.config_manager.config_path):
            logger.warning(f"설정 파일을 찾을 수 없습니다: {self.config_manager.config_path}")
            
            reply = QMessageBox.question(
                self.main_window,
                "설정 파일 경로 선택",
                "Claude 설정 파일을 찾을 수 없습니다. 직접 Claude 설치 폴더를 지정하시겠습니까?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # 설정 파일 경로 선택
                self._select_claude_config_path()
    
    def _select_claude_config_path(self):
        """Claude 설정 파일 경로 선택"""
        # 파일을 직접 선택할 수 있는 옵션 제공
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window, 
            "Claude 설정 파일 선택", 
            "", 
            "JSON 파일 (*.json);;모든 파일 (*)"
        )
        
        if file_path:
            try:
                # 선택한 파일이 유효한 claude_desktop_config.json인지 확인
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        config_data = json.load(f)
                        # 기본 구조 확인
                        if not isinstance(config_data, dict):
                            raise ValueError("설정 파일이 JSON 객체가 아닙니다.")
                            
                        # mcp_servers 필드가 없어도 괜찮음 (새로 생성 가능)
                        if "mcp_servers" in config_data and not isinstance(config_data["mcp_servers"], list):
                            raise ValueError("mcp_servers 필드가 배열이 아닙니다.")
                            
                        logger.info(f"선택한 설정 파일 내용: {json.dumps(config_data, ensure_ascii=False)}")
                        
                    except json.JSONDecodeError:
                        raise ValueError("선택한 파일이 유효한 JSON 형식이 아닙니다.")
                        
                # MCP 설정 관리자 설정 파일 경로
                config_dir = os.path.join(os.path.expanduser("~"), ".config", "mcp_manager")
                os.makedirs(config_dir, exist_ok=True)
                
                config_path = os.path.join(config_dir, "config.json")
                
                # 설정 저장 (파일 경로 직접 저장)
                config = {"claude_config_path": os.path.dirname(file_path), "claude_config_file": file_path}
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                
                logger.info(f"Claude 설정 파일 경로 저장: {file_path}")
                
                # 애플리케이션 재시작
                QMessageBox.information(
                    self.main_window,
                    "설정 저장 완료",
                    f"Claude 설정 파일 경로가 설정되었습니다: {file_path}\n프로그램을 재시작합니다."
                )
                
                # 애플리케이션 재시작
                python = sys.executable
                os.execl(python, python, *sys.argv)
            except Exception as e:
                logger.error(f"설정 저장 오류: {e}")
                logger.exception("상세 오류 정보:")
                QMessageBox.critical(
                    self.main_window,
                    "오류",
                    f"설정 저장 중 오류가 발생했습니다: {e}"
                )
    
    def _connect_events(self):
        """이벤트 연결"""
        # MainWindow에서 언어 변경 시그널 연결
        self.main_window.language_changed.connect(self._on_language_changed)
        
        # 사용 가능한 MCP 탭 이벤트
        self.main_window.mcp_list.itemClicked.connect(self._on_mcp_selected)
        self.main_window.search_button.clicked.connect(self._on_search)
        self.main_window.select_all_button.clicked.connect(self._on_select_all)
        self.main_window.deselect_all_button.clicked.connect(self._on_deselect_all)
        self.main_window.apply_button.clicked.connect(self._on_apply)
        
        # 내 MCP 탭 이벤트
        self.main_window.my_mcp_list.itemClicked.connect(self._on_my_mcp_selected)
        self.main_window.add_button.clicked.connect(self._on_add)
        self.main_window.edit_button.clicked.connect(self._on_edit)
        self.main_window.delete_button.clicked.connect(self._on_delete)
        self.main_window.move_up_button.clicked.connect(self._on_move_up)
        self.main_window.move_down_button.clicked.connect(self._on_move_down)
        self.main_window.save_button.clicked.connect(self._on_save)
        
        # 백업/복원 이벤트
        self.main_window.backup_button.clicked.connect(self._on_backup)
        self.main_window.restore_button.clicked.connect(self._on_restore)
        
        # 설정 파일 경로 변경 버튼 추가
        self.main_window.change_config_path_button.clicked.connect(self._on_change_config_path)
    
    def _initialize(self):
        """초기 설정"""
        # 설정 파일 경로 표시
        self.main_window.set_config_path(self.config_manager.config_path)
        
        # 내 MCP 서버 목록 로드
        self._load_my_mcp_servers()
        
        # MCP 서버 목록 로드 (비동기, 강제 새로고침 추가)
        self._load_mcp_servers(force_refresh=True)
    
    def _load_mcp_servers(self, force_refresh=False):
        """
        MCP 서버 목록을 로드합니다.
        
        Args:
            force_refresh (bool, optional): 캐시를 무시하고 강제로 새로고침할지 여부. 기본값은 False입니다.
        """
        # 상태 표시줄 업데이트
        self.main_window.statusBar().showMessage("MCP 서버 목록을 가져오는 중...")
        
        # 로더 스레드 생성
        self.loader_thread = MCPLoaderThread(force_refresh=force_refresh)
        
        # 시그널 연결
        self.loader_thread.finished.connect(self._on_mcp_servers_loaded)
        self.loader_thread.progress.connect(lambda msg: self.main_window.statusBar().showMessage(msg))
        self.loader_thread.error.connect(lambda msg: self.main_window.show_error_message("오류", msg))
        
        # 스레드 시작
        self.loader_thread.start()
    
    def _load_my_mcp_servers(self):
        """내 MCP 서버 목록을 로드합니다."""
        try:
            # 로그 추가: 설정 파일 경로 출력
            logger.info(f"현재 설정 파일 경로: {self.config_manager.config_path}")
            logger.info(f"설정 파일 존재 여부: {os.path.exists(self.config_manager.config_path)}")
            
            # 설정 파일에서 MCP 서버 목록 가져오기
            my_mcp_servers = self.config_manager.get_mcp_servers()
            
            # 로그 추가: MCP 서버 목록 개수 및 정보 출력
            logger.info(f"로드된 MCP 서버 수: {len(my_mcp_servers)}")
            # 상세 서버 정보 로깅 (디버그 레벨)
            if my_mcp_servers: # 목록이 비어있지 않을 때만 로깅
                 logger.debug("로드된 서버 상세 정보:")
                 for i, server in enumerate(my_mcp_servers):
                     logger.debug(f"  Server {i+1}: {json.dumps(server, ensure_ascii=False)}")
            
            # 필수 필드가 없는 서버 항목 처리 (기존 로직 유지)
            processed_servers = []
            for server in my_mcp_servers:
                # name 필드가 없으면 로그 남기고 건너뛰거나 기본값 설정
                if 'name' not in server or not server['name']:
                    logger.warning(f"서버 항목에 'name' 필드가 없거나 비어있습니다. 건너뜁니다: {server}")
                    continue # 또는 server['name'] = "이름 없는 MCP 서버" 로 설정
                
                # description 필드가 없으면 기본값 설정
                if 'description' not in server:
                    server['description'] = "설명 없음"
                
                # 필요한 다른 필드 기본값 설정 (기존 로직 유지)
                if 'installation_options' not in server:
                    server['installation_options'] = []
                
                if 'env_vars' not in server:
                    server['env_vars'] = []
                
                if 'args' not in server:
                    server['args'] = []
                
                if 'category' not in server:
                    server['category'] = "일반"
                
                processed_servers.append(server)
            
            # 로그 추가: 처리 후 MCP 서버 목록 개수 출력
            logger.info(f"UI에 표시할 처리된 MCP 서버 수: {len(processed_servers)}")
            
            # 내 MCP 서버 목록 채우기
            self.main_window.populate_my_mcp_list(processed_servers)
            
            # 상태 표시줄 업데이트
            self.main_window.statusBar().showMessage(f"내 MCP 서버 {len(processed_servers)}개를 로드했습니다.")
        except Exception as e:
            logger.error(f"내 MCP 서버 로드 오류: {e}")
            logger.exception("상세 오류 정보:") # 예외 발생 시 스택 트레이스 포함
            self.main_window.show_error_message("오류", f"내 MCP 서버 로드 오류: {e}")
    
    def _on_mcp_servers_loaded(self, mcp_servers):
        """
        MCP 서버 목록 로드 완료 이벤트 핸들러
        
        Args:
            mcp_servers (list): MCP 서버 정보 목록
        """
        # MCP 서버 목록 채우기
        self.main_window.populate_mcp_list(mcp_servers)
        
        # 상태 표시줄 업데이트
        self.main_window.statusBar().showMessage(f"총 {len(mcp_servers)}개의 MCP 서버를 로드했습니다.")
    
    def _on_mcp_selected(self, item):
        """
        MCP 서버 선택 이벤트 핸들러
        
        Args:
            item (QListWidgetItem): 선택된 항목
        """
        # 선택된 MCP 서버 정보 가져오기
        mcp_info = item.data(Qt.ItemDataRole.UserRole)
        
        # MCP 상세 정보 표시
        self.main_window.show_mcp_detail(mcp_info)
    
    def _on_my_mcp_selected(self, item):
        """
        내 MCP 서버 선택 이벤트 핸들러
        
        Args:
            item (QListWidgetItem): 선택된 항목
        """
        # 선택된 MCP 서버 정보 가져오기
        mcp_info = item.data(Qt.ItemDataRole.UserRole)
        
        # MCP 상세 정보 표시
        self.main_window.show_mcp_detail(mcp_info)
    
    def _on_search(self):
        """검색 버튼 클릭 이벤트 핸들러"""
        # 검색어 가져오기
        search_text = self.main_window.search_input.text().lower()
        
        # 카테고리 필터 가져오기
        category = self.main_window.category_filter.currentText()
        if category == "전체":
            category = None
        
        # 설치 방법 필터 가져오기
        install_method = self.main_window.install_filter.currentText()
        if install_method == "전체":
            install_method = None
        
        # 모든 항목 가져오기
        for i in range(self.main_window.mcp_list.count()):
            item = self.main_window.mcp_list.item(i)
            mcp_info = item.data(Qt.ItemDataRole.UserRole)
            
            # 검색 조건에 맞는지 확인
            match = True
            
            # 검색어 확인
            if search_text and not (search_text in mcp_info['name'].lower() or search_text in mcp_info['description'].lower()):
                match = False
            
            # 카테고리 확인
            if category and mcp_info['category'] != category.lower():
                match = False
            
            # 설치 방법 확인
            if install_method and install_method.lower() not in mcp_info['installation_options']:
                match = False
            
            # 항목 표시 여부 설정
            item.setHidden(not match)
    
    def _on_select_all(self):
        """모두 선택 버튼 클릭 이벤트 핸들러"""
        # 모든 항목 선택
        for i in range(self.main_window.mcp_list.count()):
            item = self.main_window.mcp_list.item(i)
            if not item.isHidden():
                item.setSelected(True)
    
    def _on_deselect_all(self):
        """선택 해제 버튼 클릭 이벤트 핸들러"""
        # 모든 항목 선택 해제
        self.main_window.mcp_list.clearSelection()
    
    def _on_apply(self):
        """적용 버튼 클릭 이벤트 핸들러"""
        # 선택된 항목 가져오기
        selected_items = self.main_window.mcp_list.selectedItems()
        
        if not selected_items:
            self.main_window.show_info_message("알림", "선택된 MCP 서버가 없습니다.")
            return
        
        # 선택된 MCP 서버 정보 가져오기
        selected_servers = [item.data(Qt.ItemDataRole.UserRole) for item in selected_items]
        
        # 현재 내 MCP 서버 목록 가져오기
        my_mcp_servers = self.config_manager.get_mcp_servers()
        
        # 선택된 서버 추가
        for server in selected_servers:
            # 중복 확인
            if not any(my_server['name'] == server['name'] for my_server in my_mcp_servers):
                # 활성화 상태 추가
                server['enabled'] = True
                my_mcp_servers.append(server)
        
        # 설정 파일에 저장
        if self.config_manager.save_mcp_servers(my_mcp_servers):
            # 내 MCP 서버 목록 다시 로드
            self._load_my_mcp_servers()
            
            # 탭 전환
            self.main_window.tab_widget.setCurrentIndex(1)
            
            # 알림 표시
            self.main_window.show_info_message("알림", f"선택한 {len(selected_servers)}개의 MCP 서버를 추가했습니다.")
        else:
            self.main_window.show_error_message("오류", "MCP 서버 추가 실패")
    
    def _on_add(self):
        """추가 버튼 클릭 이벤트 핸들러"""
        # 탭 전환
        self.main_window.tab_widget.setCurrentIndex(0)
        
        # 알림 표시
        self.main_window.show_info_message("알림", "사용 가능한 MCP 탭에서 추가할 서버를 선택하세요.")
    
    def _on_edit(self):
        """편집 버튼 클릭 이벤트 핸들러"""
        # 선택된 항목 가져오기
        selected_items = self.main_window.my_mcp_list.selectedItems()
        
        if not selected_items:
            self.main_window.show_info_message("알림", "편집할 MCP 서버를 선택하세요.")
            return
        
        # 현재는 간단한 구현으로, 선택된 서버의 상세 정보만 표시
        selected_item = selected_items[0]
        mcp_info = selected_item.data(Qt.ItemDataRole.UserRole)
        
        # MCP 상세 정보 표시
        self.main_window.show_mcp_detail(mcp_info)
    
    def _on_delete(self):
        """삭제 버튼 클릭 이벤트 핸들러"""
        # 선택된 항목 가져오기
        selected_items = self.main_window.my_mcp_list.selectedItems()
        
        if not selected_items:
            self.main_window.show_info_message("알림", "삭제할 MCP 서버를 선택하세요.")
            return
        
        # 확인 메시지 표시
        if not self.main_window.show_confirm_message("확인", f"선택한 {len(selected_items)}개의 MCP 서버를 삭제하시겠습니까?"):
            return
        
        # 현재 내 MCP 서버 목록 가져오기
        my_mcp_servers = self.config_manager.get_mcp_servers()
        
        # 선택된 서버 삭제
        for item in selected_items:
            mcp_info = item.data(Qt.ItemDataRole.UserRole)
            my_mcp_servers = [server for server in my_mcp_servers if server['name'] != mcp_info['name']]
        
        # 설정 파일에 저장
        if self.config_manager.save_mcp_servers(my_mcp_servers):
            # 내 MCP 서버 목록 다시 로드
            self._load_my_mcp_servers()
            
            # 알림 표시
            self.main_window.show_info_message("알림", f"선택한 {len(selected_items)}개의 MCP 서버를 삭제했습니다.")
        else:
            self.main_window.show_error_message("오류", "MCP 서버 삭제 실패")
    
    def _on_move_up(self):
        """위로 버튼 클릭 이벤트 핸들러"""
        # 선택된 항목 가져오기
        selected_items = self.main_window.my_mcp_list.selectedItems()
        
        if not selected_items:
            self.main_window.show_info_message("알림", "이동할 MCP 서버를 선택하세요.")
            return
        
        # 현재 내 MCP 서버 목록 가져오기
        my_mcp_servers = self.config_manager.get_mcp_servers()
        
        # 선택된 서버 이동
        for item in selected_items:
            # 현재 인덱스 가져오기
            current_index = self.main_window.my_mcp_list.row(item)
            
            # 첫 번째 항목이면 이동 불가
            if current_index == 0:
                continue
            
            # 서버 이동
            if self.config_manager.move_mcp_server(current_index, current_index - 1):
                # 내 MCP 서버 목록 다시 로드
                self._load_my_mcp_servers()
                
                # 이동된 항목 선택
                self.main_window.my_mcp_list.item(current_index - 1).setSelected(True)
            else:
                self.main_window.show_error_message("오류", "MCP 서버 이동 실패")
    
    def _on_move_down(self):
        """아래로 버튼 클릭 이벤트 핸들러"""
        # 선택된 항목 가져오기
        selected_items = self.main_window.my_mcp_list.selectedItems()
        
        if not selected_items:
            self.main_window.show_info_message("알림", "이동할 MCP 서버를 선택하세요.")
            return
        
        # 현재 내 MCP 서버 목록 가져오기
        my_mcp_servers = self.config_manager.get_mcp_servers()
        
        # 선택된 서버 이동
        for item in selected_items:
            # 현재 인덱스 가져오기
            current_index = self.main_window.my_mcp_list.row(item)
            
            # 마지막 항목이면 이동 불가
            if current_index == len(my_mcp_servers) - 1:
                continue
            
            # 서버 이동
            if self.config_manager.move_mcp_server(current_index, current_index + 1):
                # 내 MCP 서버 목록 다시 로드
                self._load_my_mcp_servers()
                
                # 이동된 항목 선택
                self.main_window.my_mcp_list.item(current_index + 1).setSelected(True)
            else:
                self.main_window.show_error_message("오류", "MCP 서버 이동 실패")
    
    def _on_save(self):
        """저장 버튼 클릭 이벤트 핸들러"""
        # 현재 내 MCP 서버 목록 가져오기
        my_mcp_servers = self.config_manager.get_mcp_servers()
        
        # 설정 파일에 저장
        if self.config_manager.save_mcp_servers(my_mcp_servers):
            # 알림 표시
            self.main_window.show_info_message("알림", "설정을 저장했습니다.")
            
            # Claude Desktop 재시작 확인
            if self.main_window.show_confirm_message("확인", "변경 사항을 적용하려면 Claude Desktop을 재시작해야 합니다. 지금 재시작하시겠습니까?"):
                # Claude Desktop 재시작
                if utils.restart_claude_desktop():
                    self.main_window.show_info_message("알림", "Claude Desktop을 재시작했습니다.")
                else:
                    self.main_window.show_error_message("오류", "Claude Desktop 재시작 실패")
        else:
            self.main_window.show_error_message("오류", "설정 저장 실패")
    
    def _on_backup(self):
        """백업 버튼 클릭 이벤트 핸들러"""
        # 설정 파일 백업
        self.config_manager._backup_config()
        
        # 백업 목록 가져오기
        backup_list = self.config_manager.get_backup_list()
        
        # 알림 표시
        if backup_list:
            self.main_window.show_info_message("알림", f"설정 파일을 백업했습니다.\n최신 백업: {backup_list[0]['filename']}")
        else:
            self.main_window.show_info_message("알림", "설정 파일 백업 실패")
    
    def _on_restore(self):
        """복원 버튼 클릭 이벤트 핸들러"""
        # 백업 목록 가져오기
        backup_list = self.config_manager.get_backup_list()
        
        if not backup_list:
            self.main_window.show_info_message("알림", "복원할 백업 파일이 없습니다.")
            return
        
        # 확인 메시지 표시
        if not self.main_window.show_confirm_message("확인", f"최신 백업({backup_list[0]['filename']})에서 설정을 복원하시겠습니까?"):
            return
        
        # 설정 파일 복원
        if self.config_manager.restore_backup():
            # 내 MCP 서버 목록 다시 로드
            self._load_my_mcp_servers()
            
            # 알림 표시
            self.main_window.show_info_message("알림", "설정을 복원했습니다.")
        else:
            self.main_window.show_error_message("오류", "설정 복원 실패")
            
    def _on_change_config_path(self):
        """설정 파일 경로 변경 버튼 클릭 이벤트 핸들러"""
        # 확인 메시지 표시
        if not self.main_window.show_confirm_message("확인", "Claude 설치 폴더를 변경하시겠습니까? 프로그램이 재시작됩니다."):
            return
            
        # 설정 파일 경로 선택
        self._select_claude_config_path()
    
    def _on_language_changed(self, lang_code):
        """언어 변경 이벤트 처리"""
        self._load_language(lang_code)

    def _load_language(self, lang_code):
        """지정된 언어의 번역 파일을 로드하고 적용합니다."""
        # 기존 번역기 제거
        self.app.removeTranslator(self.translator)
        
        # 번역 파일 경로 설정 (예: translations/app_ko.qm)
        translation_path = os.path.join("translations", f"app_{lang_code}.qm")
        logger.info(f"Trying to load translation file: {translation_path}")

        if lang_code == 'en':
            # 영어는 기본 언어이므로 번역기 로드 불필요
            logger.info("Setting language to English (default).")
            # UI 갱신 호출
            self.main_window.retranslateUi()
        elif self.translator.load(translation_path):
            # 번역 파일 로드 성공 시 앱에 설치
            self.app.installTranslator(self.translator)
            logger.info(f"Successfully loaded and installed translation: {lang_code}")
            # UI 갱신 호출
            self.main_window.retranslateUi()
        else:
            logger.warning(f"Could not load translation file for language: {lang_code}. Path: {translation_path}")
            # 로드 실패 시 기본 언어(영어)로 유지하거나 오류 메시지 표시 가능
            # 여기서는 UI 갱신만 호출하여 영어로 표시되도록 함
            self.main_window.retranslateUi()

    def run(self):
        """애플리케이션 실행"""
        # 메인 윈도우 표시
        self.main_window.show()
        
        # 애플리케이션 실행
        return self.app.exec()

def main():
    """메인 함수"""
    # MCP 설정 관리자 생성 및 실행
    manager = MCPConfigManager()
    sys.exit(manager.run())

if __name__ == "__main__":
    main()
