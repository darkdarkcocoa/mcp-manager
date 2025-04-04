"""
MCP 설정 관리자 테스트 스크립트

통합된 애플리케이션의 기능을 테스트합니다.
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# 상위 디렉토리를 모듈 검색 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawler.github_crawler import GitHubCrawler
from config.config_manager import ConfigManager
from main import MCPConfigManager, MCPLoaderThread

class TestMCPConfigManagerApp(unittest.TestCase):
    """MCP 설정 관리자 애플리케이션 테스트 클래스"""
    
    def setUp(self):
        """테스트 설정"""
        # 테스트용 디렉토리 설정
        self.test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_integration")
        os.makedirs(self.test_dir, exist_ok=True)
        
        # 테스트용 설정 파일 경로
        self.test_config_path = os.path.join(self.test_dir, "test_claude_desktop_config.json")
        
        # 기존 파일 삭제
        if os.path.exists(self.test_config_path):
            os.remove(self.test_config_path)
    
    def test_github_crawler_integration(self):
        """GitHub 크롤러 통합 테스트"""
        print("\n1. GitHub 크롤러 통합 테스트")
        
        # GitHub 크롤러 생성
        crawler = GitHubCrawler()
        
        # MCP 서버 목록 가져오기
        mcp_servers = crawler.get_mcp_servers()
        
        # 결과 확인
        self.assertIsNotNone(mcp_servers)
        self.assertIsInstance(mcp_servers, list)
        print(f"  - MCP 서버 목록 가져오기 성공: {len(mcp_servers)}개의 서버 발견")
        
        # 캐시 테스트
        cached_servers = crawler.get_mcp_servers()
        self.assertEqual(len(mcp_servers), len(cached_servers))
        print("  - 캐시 기능 정상 작동")
    
    def test_config_manager_integration(self):
        """설정 파일 관리자 통합 테스트"""
        print("\n2. 설정 파일 관리자 통합 테스트")
        
        # 설정 파일 관리자 생성
        config_manager = ConfigManager(config_path=self.test_config_path)
        
        # 기본 설정 로드
        config = config_manager.load_config()
        self.assertIsNotNone(config)
        self.assertIn("mcp_servers", config)
        print("  - 기본 설정 로드 성공")
        
        # MCP 서버 추가
        test_server = {
            "name": "테스트 서버",
            "description": "테스트용 MCP 서버",
            "installation_options": ["npm"],
            "env_vars": ["API_KEY"],
            "args": ["--port"],
            "category": "search",
            "enabled": True
        }
        
        result = config_manager.add_mcp_server(test_server)
        self.assertTrue(result)
        print("  - MCP 서버 추가 성공")
        
        # MCP 서버 목록 가져오기
        mcp_servers = config_manager.get_mcp_servers()
        self.assertEqual(len(mcp_servers), 1)
        self.assertEqual(mcp_servers[0]["name"], "테스트 서버")
        print("  - MCP 서버 목록 가져오기 성공")
        
        # 백업 테스트
        config_manager._backup_config()
        backup_list = config_manager.get_backup_list()
        self.assertGreater(len(backup_list), 0)
        print("  - 백업 기능 정상 작동")
    
    @patch('PyQt6.QtWidgets.QApplication')
    @patch('main.MainWindow')
    def test_ui_integration(self, mock_main_window, mock_app):
        """UI 통합 테스트 (모킹 사용)"""
        print("\n3. UI 통합 테스트 (모킹)")
        
        # 모의 객체 설정
        mock_main_window_instance = mock_main_window.return_value
        mock_main_window_instance.mcp_list = MagicMock()
        mock_main_window_instance.my_mcp_list = MagicMock()
        mock_main_window_instance.search_input = MagicMock()
        mock_main_window_instance.category_filter = MagicMock()
        mock_main_window_instance.install_filter = MagicMock()
        mock_main_window_instance.search_button = MagicMock()
        mock_main_window_instance.select_all_button = MagicMock()
        mock_main_window_instance.deselect_all_button = MagicMock()
        mock_main_window_instance.apply_button = MagicMock()
        mock_main_window_instance.add_button = MagicMock()
        mock_main_window_instance.edit_button = MagicMock()
        mock_main_window_instance.delete_button = MagicMock()
        mock_main_window_instance.move_up_button = MagicMock()
        mock_main_window_instance.move_down_button = MagicMock()
        mock_main_window_instance.save_button = MagicMock()
        mock_main_window_instance.backup_button = MagicMock()
        mock_main_window_instance.restore_button = MagicMock()
        mock_main_window_instance.statusBar = MagicMock()
        mock_main_window_instance.tab_widget = MagicMock()
        
        # ConfigManager 패치
        with patch('main.ConfigManager') as mock_config_manager:
            mock_config_manager_instance = mock_config_manager.return_value
            mock_config_manager_instance.config_path = self.test_config_path
            mock_config_manager_instance.get_mcp_servers.return_value = []
            
            # MCPConfigManager 생성
            manager = MCPConfigManager()
            
            # 이벤트 연결 확인
            self.assertTrue(mock_main_window_instance.mcp_list.itemClicked.connect.called)
            self.assertTrue(mock_main_window_instance.search_button.clicked.connect.called)
            self.assertTrue(mock_main_window_instance.apply_button.clicked.connect.called)
            print("  - UI 이벤트 연결 성공")
            
            # 초기화 확인
            self.assertTrue(mock_main_window_instance.set_config_path.called)
            self.assertTrue(mock_config_manager_instance.get_mcp_servers.called)
            print("  - UI 초기화 성공")
    
    def test_loader_thread(self):
        """로더 스레드 테스트"""
        print("\n4. 로더 스레드 테스트")
        
        # 시그널 모킹
        class MockSignal:
            def __init__(self):
                self.callbacks = []
            
            def connect(self, callback):
                self.callbacks.append(callback)
            
            def emit(self, *args):
                for callback in self.callbacks:
                    callback(*args)
        
        # MCPLoaderThread 패치
        with patch('main.MCPLoaderThread.finished', new_callable=MockSignal), \
             patch('main.MCPLoaderThread.progress', new_callable=MockSignal), \
             patch('main.MCPLoaderThread.error', new_callable=MockSignal), \
             patch('main.GitHubCrawler') as mock_crawler:
            
            # 모의 데이터 설정
            mock_crawler_instance = mock_crawler.return_value
            mock_servers = [
                {
                    "name": "테스트 서버 1",
                    "description": "테스트용 MCP 서버 1",
                    "installation_options": ["npm"],
                    "env_vars": ["API_KEY"],
                    "args": ["--port"],
                    "category": "search",
                    "enabled": True
                },
                {
                    "name": "테스트 서버 2",
                    "description": "테스트용 MCP 서버 2",
                    "installation_options": ["uvx"],
                    "env_vars": ["SECRET_KEY"],
                    "args": ["--debug"],
                    "category": "vision",
                    "enabled": False
                }
            ]
            mock_crawler_instance.get_mcp_servers.return_value = mock_servers
            
            # 로더 스레드 생성 및 실행
            loader = MCPLoaderThread()
            
            # 콜백 모킹
            finished_callback = MagicMock()
            progress_callback = MagicMock()
            error_callback = MagicMock()
            
            loader.finished.connect(finished_callback)
            loader.progress.connect(progress_callback)
            loader.error.connect(error_callback)
            
            # 스레드 실행
            loader.run()
            
            # 결과 확인
            mock_crawler_instance.get_mcp_servers.assert_called_once()
            finished_callback.assert_called_once_with(mock_servers)
            self.assertGreater(progress_callback.call_count, 0)
            error_callback.assert_not_called()
            print("  - 로더 스레드 정상 작동")
    
    def test_cross_platform_compatibility(self):
        """크로스 플랫폼 호환성 테스트"""
        print("\n5. 크로스 플랫폼 호환성 테스트")
        
        # 현재 플랫폼 확인
        import platform
        current_platform = platform.system()
        print(f"  - 현재 플랫폼: {current_platform}")
        
        # ConfigManager 생성 (OS별 설정 파일 위치 감지 테스트)
        config_manager = ConfigManager()
        
        # 설정 파일 경로 확인
        config_path = config_manager.config_path
        print(f"  - 감지된 설정 파일 경로: {config_path}")
        
        # 플랫폼별 경로 형식 확인
        if current_platform == "Windows":
            self.assertIn("AppData", config_path)
        elif current_platform == "Darwin":  # macOS
            self.assertIn("Library/Application Support", config_path)
        else:  # Linux 및 기타
            self.assertIn(".config", config_path)
        
        print("  - OS별 설정 파일 위치 감지 정상 작동")
    
    def tearDown(self):
        """테스트 정리"""
        # 테스트 파일 정리
        if os.path.exists(self.test_config_path):
            os.remove(self.test_config_path)

if __name__ == "__main__":
    unittest.main()
