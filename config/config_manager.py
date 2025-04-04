"""
설정 파일 관리자 모듈

MCP 설정 관리자의 설정 파일 관리 기능을 제공합니다.
"""

import os
import json
import platform
import shutil
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('config_manager')

class ConfigManager:
    """설정 파일 관리자 클래스"""
    
    def __init__(self, config_path=None):
        """
        ConfigManager 초기화
        
        Args:
            config_path (str, optional): 설정 파일 경로. 기본값은 None으로, 
                                        이 경우 OS별 기본 경로를 사용합니다.
        """
        # 먼저 사용자 지정 파일로 직접 지정되었는지 확인
        try:
            # MCP 설정 관리자 설정 파일 경로
            config_dir = os.path.join(os.path.expanduser("~"), ".config", "mcp_manager")
            manager_config_path = os.path.join(config_dir, "config.json")
            
            logger.info(f"MCP 설정 관리자 설정 파일 경로: {manager_config_path}")
            
            if os.path.exists(manager_config_path):
                with open(manager_config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # 직접 설정 파일 경로를 지정한 경우
                if "claude_config_file" in config and os.path.exists(config["claude_config_file"]):
                    self.config_path = config["claude_config_file"]
                    logger.info(f"직접 지정된 설정 파일 사용: {self.config_path}")
                    
                    # 백업 디렉토리 설정
                    self.backup_dir = os.path.join(os.path.dirname(self.config_path), "backups")
                    os.makedirs(self.backup_dir, exist_ok=True)
                    
                    logger.info(f"설정 파일 경로: {self.config_path}")
                    logger.info(f"백업 디렉토리: {self.backup_dir}")
                    return
        except Exception as e:
            logger.error(f"직접 지정된 설정 파일 로드 오류: {e}")
            logger.exception("상세 오류 정보:")
        
        # 사용자 지정 클로드 설정 파일 경로 확인
        custom_path = self._get_custom_config_path()
        
        # 설정 파일 경로 설정
        if config_path:
            self.config_path = config_path
        elif custom_path:
            # 사용자가 직접 지정한 경로 사용
            self.config_path = os.path.join(custom_path, "claude_desktop_config.json")
            logger.info(f"사용자 지정 클로드 설정 경로를 사용합니다: {self.config_path}")
        else:
            # 기본 경로 사용
            self.config_path = self._get_default_config_path()
        
        # 백업 디렉토리 설정
        self.backup_dir = os.path.join(os.path.dirname(self.config_path), "backups")
        os.makedirs(self.backup_dir, exist_ok=True)
        
        logger.info(f"설정 파일 경로: {self.config_path}")
        logger.info(f"백업 디렉토리: {self.backup_dir}")
    
    def _get_custom_config_path(self):
        """
        사용자가 지정한 클로드 설정 파일 경로를 반환합니다.
        
        Returns:
            str: 사용자 지정 클로드 설정 파일 경로, 없으면 None
        """
        try:
            # MCP 설정 관리자 설정 파일 경로
            config_dir = os.path.join(os.path.expanduser("~"), ".config", "mcp_manager")
            config_path = os.path.join(config_dir, "config.json")
            
            logger.info(f"사용자 지정 설정 파일 경로: {config_path}")
            
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_content = f.read()
                    logger.info(f"설정 파일 내용: {config_content}")
                    config = json.loads(config_content)
                
                # 직접 설정 파일 경로를 지정한 경우
                if "claude_config_file" in config and os.path.exists(config["claude_config_file"]):
                    logger.info(f"직접 지정된 설정 파일 사용: {config['claude_config_file']}")
                    # 직접 설정 파일 경로를 반환
                    return os.path.dirname(config["claude_config_file"])
                # 설정 폴더 경로만 지정한 경우 (이전 버전 호환)
                elif "claude_config_path" in config:
                    logger.info(f"지정된 설정 폴더 사용: {config['claude_config_path']}")
                    return config.get("claude_config_path")
            
            logger.info("사용자 지정 설정 경로를 찾을 수 없음")
            return None
        except Exception as e:
            logger.error(f"사용자 지정 설정 파일 경로 로드 오류: {e}")
            logger.exception("상세 오류 정보:")
            return None
    
    def _get_default_config_path(self):
        """
        OS별 기본 설정 파일 경로를 반환합니다.
        
        Returns:
            str: 설정 파일 경로
        """
        system = platform.system()
        home_dir = os.path.expanduser("~")
        
        if system == "Windows":
            # Windows: %APPDATA%/Claude/claude_desktop_config.json
            config_dir = os.path.join(os.getenv('APPDATA'), "Claude")
        elif system == "Darwin":  # macOS
            # macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
            config_dir = os.path.join(home_dir, "Library", "Application Support", "Claude")
        else:  # Linux 및 기타
            # Linux: ~/.config/Claude/claude_desktop_config.json
            config_dir = os.path.join(home_dir, ".config", "Claude")
        
        # 디렉토리가 없으면 생성
        os.makedirs(config_dir, exist_ok=True)
        
        return os.path.join(config_dir, "claude_desktop_config.json")
    
    def load_config(self):
        """
        설정 파일을 로드합니다.
        
        Returns:
            dict: 설정 정보. 파일이 없거나 오류가 발생하면 기본 설정을 반환합니다.
        """
        try:
            if os.path.exists(self.config_path):
                logger.info(f"설정 파일 경로가 존재합니다: {self.config_path}")
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    logger.info(f"설정 파일 내용: {file_content}")
                    config = json.loads(file_content)
                logger.info(f"설정 파일을 로드했습니다. MCP 서버 수: {len(config.get('mcp_servers', []))}")
                return config
            else:
                logger.warning(f"설정 파일이 없습니다: {self.config_path}. 기본 설정을 사용합니다.")
                return self._get_default_config()
        except json.JSONDecodeError as e:
            logger.error(f"설정 파일 파싱 오류: {e}, 경로: {self.config_path}")
            # 오류가 있는 파일 백업
            self._backup_config(error=True)
            return self._get_default_config()
        except Exception as e:
            logger.error(f"설정 파일 로드 오류: {e}, 경로: {self.config_path}")
            return self._get_default_config()
    
    def save_config(self, config):
        """
        설정 정보를 파일에 저장합니다.
        
        Args:
            config (dict): 저장할 설정 정보
            
        Returns:
            bool: 저장 성공 여부
        """
        try:
            # 저장 전 설정 파일 검증
            if not self._validate_config(config):
                logger.error("설정 파일 검증 실패")
                return False
            
            # 저장 전 백업
            self._backup_config()
            
            # 설정 파일 저장
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            logger.info("설정 파일을 저장했습니다.")
            return True
        except Exception as e:
            logger.error(f"설정 파일 저장 오류: {e}")
            return False
    
    def _get_default_config(self):
        """
        기본 설정 정보를 반환합니다.
        
        Returns:
            dict: 기본 설정 정보
        """
        return {
            "mcp_servers": []
        }
    
    def _validate_config(self, config):
        """
        설정 정보를 검증합니다.
        
        Args:
            config (dict): 검증할 설정 정보
            
        Returns:
            bool: 검증 성공 여부
        """
        try:
            # 기본 구조 검증
            if not isinstance(config, dict):
                logger.error("설정 파일이 JSON 객체가 아닙니다.")
                return False
            
            # mcp_servers 필드 검증
            if "mcp_servers" not in config:
                logger.error("설정 파일에 mcp_servers 필드가 없습니다.")
                return False
            
            if not isinstance(config["mcp_servers"], list):
                logger.error("mcp_servers 필드가 배열이 아닙니다.")
                return False
            
            # 각 MCP 서버 항목 검증
            for i, server in enumerate(config["mcp_servers"]):
                if not isinstance(server, dict):
                    logger.error(f"mcp_servers[{i}]가 JSON 객체가 아닙니다.")
                    return False
                
                # 필수 필드 검증
                required_fields = ["name"]
                for field in required_fields:
                    if field not in server:
                        logger.error(f"mcp_servers[{i}]에 필수 필드 '{field}'가 없습니다.")
                        return False
            
            return True
        except Exception as e:
            logger.error(f"설정 파일 검증 오류: {e}")
            return False
    
    def _backup_config(self, error=False):
        """
        설정 파일을 백업합니다.
        
        Args:
            error (bool, optional): 오류로 인한 백업인지 여부. 기본값은 False입니다.
        """
        if not os.path.exists(self.config_path):
            logger.warning("백업할 설정 파일이 없습니다.")
            return
        
        try:
            # 백업 파일 이름 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"claude_desktop_config_{timestamp}"
            if error:
                backup_filename += "_error"
            backup_filename += ".json"
            
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            # 파일 복사
            shutil.copy2(self.config_path, backup_path)
            
            logger.info(f"설정 파일을 {backup_path}에 백업했습니다.")
            
            # 오래된 백업 파일 정리 (최대 10개 유지)
            self._cleanup_old_backups()
        except Exception as e:
            logger.error(f"설정 파일 백업 오류: {e}")
    
    def _cleanup_old_backups(self, max_backups=10):
        """
        오래된 백업 파일을 정리합니다.
        
        Args:
            max_backups (int, optional): 유지할 최대 백업 파일 수. 기본값은 10입니다.
        """
        try:
            # 백업 파일 목록 가져오기
            backup_files = [f for f in os.listdir(self.backup_dir) 
                           if f.startswith("claude_desktop_config_") and f.endswith(".json")]
            
            # 파일 수가 최대 개수를 초과하면 오래된 파일 삭제
            if len(backup_files) > max_backups:
                # 수정 시간 기준으로 정렬
                backup_files.sort(key=lambda f: os.path.getmtime(os.path.join(self.backup_dir, f)))
                
                # 오래된 파일 삭제
                for i in range(len(backup_files) - max_backups):
                    old_file = os.path.join(self.backup_dir, backup_files[i])
                    os.remove(old_file)
                    logger.info(f"오래된 백업 파일 {old_file}을 삭제했습니다.")
        except Exception as e:
            logger.error(f"백업 파일 정리 오류: {e}")
    
    def restore_backup(self, backup_file=None):
        """
        백업 파일에서 설정을 복원합니다.
        
        Args:
            backup_file (str, optional): 복원할 백업 파일 이름. 기본값은 None으로,
                                        이 경우 가장 최근 백업 파일을 사용합니다.
            
        Returns:
            bool: 복원 성공 여부
        """
        try:
            # 백업 파일 경로 결정
            if backup_file:
                backup_path = os.path.join(self.backup_dir, backup_file)
            else:
                # 가장 최근 백업 파일 찾기
                backup_files = [f for f in os.listdir(self.backup_dir) 
                               if f.startswith("claude_desktop_config_") and f.endswith(".json")]
                
                if not backup_files:
                    logger.error("복원할 백업 파일이 없습니다.")
                    return False
                
                # 수정 시간 기준으로 정렬 (최신 순)
                backup_files.sort(key=lambda f: os.path.getmtime(os.path.join(self.backup_dir, f)), reverse=True)
                
                backup_path = os.path.join(self.backup_dir, backup_files[0])
            
            # 백업 파일 존재 확인
            if not os.path.exists(backup_path):
                logger.error(f"백업 파일 {backup_path}이 존재하지 않습니다.")
                return False
            
            # 현재 설정 파일 백업
            current_backup = f"claude_desktop_config_before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            current_backup_path = os.path.join(self.backup_dir, current_backup)
            
            if os.path.exists(self.config_path):
                shutil.copy2(self.config_path, current_backup_path)
                logger.info(f"복원 전 현재 설정 파일을 {current_backup_path}에 백업했습니다.")
            
            # 백업 파일 복원
            shutil.copy2(backup_path, self.config_path)
            
            logger.info(f"설정 파일을 {backup_path}에서 복원했습니다.")
            return True
        except Exception as e:
            logger.error(f"설정 파일 복원 오류: {e}")
            return False
    
    def get_backup_list(self):
        """
        백업 파일 목록을 반환합니다.
        
        Returns:
            list: 백업 파일 정보 목록 (파일 이름, 날짜, 크기)
        """
        try:
            backup_files = [f for f in os.listdir(self.backup_dir) 
                           if f.startswith("claude_desktop_config_") and f.endswith(".json")]
            
            # 백업 파일 정보 수집
            backup_info = []
            for filename in backup_files:
                file_path = os.path.join(self.backup_dir, filename)
                mtime = os.path.getmtime(file_path)
                size = os.path.getsize(file_path)
                
                # 날짜 형식 변환
                date = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
                
                # 크기 형식 변환 (KB)
                size_kb = size / 1024
                
                backup_info.append({
                    "filename": filename,
                    "date": date,
                    "size": f"{size_kb:.1f} KB"
                })
            
            # 날짜 기준 정렬 (최신 순)
            backup_info.sort(key=lambda x: x["date"], reverse=True)
            
            return backup_info
        except Exception as e:
            logger.error(f"백업 파일 목록 가져오기 오류: {e}")
            return []
    
    def get_mcp_servers(self):
        """설정 파일에서 MCP 서버 목록을 가져옵니다."""
        config = self.load_config()
        
        # 실제 Claude 설정 파일 형식("mcpServers": {}) 처리
        if "mcpServers" in config and isinstance(config["mcpServers"], dict):
            logger.info("'mcpServers' 객체 형식 발견. 리스트 형식으로 변환합니다.")
            mcp_servers_list = []
            for server_name, server_config in config["mcpServers"].items():
                # server_config가 딕셔너리인지 확인
                if isinstance(server_config, dict):
                    new_server_entry = {
                        'name': server_name, 
                        # command, args, env 등 다른 키들을 안전하게 복사
                        'command': server_config.get('command'),
                        'args': server_config.get('args', []), # args가 없을 경우 빈 리스트
                        'env': server_config.get('env', {}),    # env가 없을 경우 빈 딕셔너리
                        # 필요에 따라 다른 필드도 추가 (예: description, category 등은 기본값 설정)
                        'description': server_config.get('description', "설명 없음"),
                        'category': server_config.get('category', "일반")
                        # enabled 상태 등 다른 정보는 필요시 추가/관리
                    }
                    mcp_servers_list.append(new_server_entry)
                    logger.debug(f"변환된 서버 정보: {new_server_entry}") # 변환된 정보 디버그 로깅
                else:
                     logger.warning(f"'{server_name}' 서버 설정이 올바른 형식이 아닙니다(객체여야 함): {server_config}")
            
            # 로그 추가: 변환 후 MCP 서버 목록 개수 출력
            logger.info(f"리스트로 변환된 MCP 서버 수: {len(mcp_servers_list)}")
            return mcp_servers_list
        # 이전 버전 또는 예상 형식 ("mcp_servers": []) 처리 (하위 호환성)
        elif "mcp_servers" in config and isinstance(config["mcp_servers"], list):
            logger.info("'mcp_servers' 리스트 형식 발견.")
            server_list = config.get("mcp_servers", [])
            logger.info(f"로드된 MCP 서버 수 (리스트 형식): {len(server_list)}")
            return server_list
        else:
            logger.warning("설정 파일에서 'mcpServers'(객체) 또는 'mcp_servers'(리스트) 키를 찾을 수 없거나 형식이 잘못되었습니다.")
            return []
    
    def save_mcp_servers(self, mcp_servers_list):
        """MCP 서버 목록을 설정 파일에 저장합니다."""
        config = self.load_config()
        
        # 내부적으로 사용하는 리스트 형식을 Claude가 사용하는 객체 형식으로 변환
        mcp_servers_object = {}
        for server in mcp_servers_list:
            server_name = server.get('name')
            if not server_name:
                 logger.warning("저장 중 이름 없는 서버 발견, 건너뛰었습니다: %s", server)
                 continue
            # 이름(name) 필드를 제외한 나머지 설정 복사
            server_config = {k: v for k, v in server.items() if k != 'name'}
            mcp_servers_object[server_name] = server_config
            
        config["mcpServers"] = mcp_servers_object
        # 이전 형식의 키가 있다면 제거 (선택적)
        if "mcp_servers" in config:
            del config["mcp_servers"]
            
        return self.save_config(config)
    
    def add_mcp_server(self, server_info):
        """MCP 서버를 설정 파일에 추가합니다."""
        my_mcp_servers = self.get_mcp_servers()
        
        # 중복 확인 (이름 기준)
        if any(s['name'] == server_info.get('name') for s in my_mcp_servers):
            logger.warning(f"이미 존재하는 서버입니다: {server_info.get('name')}")
            return False
        
        my_mcp_servers.append(server_info)
        return self.save_mcp_servers(my_mcp_servers)
    
    def delete_mcp_server(self, server_name):
        """MCP 서버를 설정 파일에서 삭제합니다."""
        my_mcp_servers = self.get_mcp_servers()
        original_length = len(my_mcp_servers)
        
        my_mcp_servers = [s for s in my_mcp_servers if s.get('name') != server_name]
        
        if len(my_mcp_servers) < original_length:
            return self.save_mcp_servers(my_mcp_servers)
        else:
             logger.warning(f"삭제할 서버를 찾지 못했습니다: {server_name}")
             return False
    
    def move_mcp_server(self, from_index, to_index):
        """MCP 서버의 순서를 변경합니다."""
        my_mcp_servers = self.get_mcp_servers()
        
        if 0 <= from_index < len(my_mcp_servers) and 0 <= to_index < len(my_mcp_servers):
            # 리스트 순서 변경
            server_to_move = my_mcp_servers.pop(from_index)
            my_mcp_servers.insert(to_index, server_to_move)
            return self.save_mcp_servers(my_mcp_servers)
        else:
            logger.error(f"잘못된 인덱스입니다: from={from_index}, to={to_index}")
            return False
