"""
GitHub 크롤러 모듈

MCP 서버 목록을 GitHub 저장소에서 크롤링하고 상세 정보를 수집하는 기능을 제공합니다.
"""

import os
import json
import time
import requests
import logging
import re
from bs4 import BeautifulSoup
import markdown

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('github_crawler')

class GitHubCrawler:
    """GitHub 저장소에서 MCP 서버 정보를 크롤링하는 클래스"""
    
    def __init__(self, cache_dir=None):
        """
        GitHubCrawler 초기화
        
        Args:
            cache_dir (str, optional): 캐시 디렉토리 경로. 기본값은 None으로, 
                                      이 경우 ~/.mcp_config_manager/cache를 사용합니다.
        """
        # 캐시 디렉토리 설정
        if cache_dir is None:
            home_dir = os.path.expanduser("~")
            self.cache_dir = os.path.join(home_dir, ".mcp_config_manager", "cache")
        else:
            self.cache_dir = cache_dir
            
        # 캐시 디렉토리가 없으면 생성
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # 캐시 파일 경로
        self.servers_cache_file = os.path.join(self.cache_dir, "mcp_servers.json")
        self.cache_expiry = 3600  # 캐시 유효 시간 (초)
        
        # README URL
        self.readme_url = "https://raw.githubusercontent.com/modelcontextprotocol/servers/main/README.md"
    
    def _is_cache_valid(self):
        """
        캐시가 유효한지 확인합니다.
        
        Returns:
            bool: 캐시가 유효하면 True, 그렇지 않으면 False
        """
        if not os.path.exists(self.servers_cache_file):
            return False
        
        # 캐시 파일의 수정 시간 확인
        mtime = os.path.getmtime(self.servers_cache_file)
        current_time = time.time()
        
        # 캐시 유효 시간이 지났는지 확인
        return (current_time - mtime) < self.cache_expiry
    
    def _load_cache(self):
        """
        캐시에서 MCP 서버 정보를 로드합니다.
        
        Returns:
            list: MCP 서버 정보 목록
        """
        try:
            with open(self.servers_cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(f"캐시 로드 실패: {e}")
            return None
    
    def _save_cache(self, data):
        """
        MCP 서버 정보를 캐시에 저장합니다.
        
        Args:
            data (list): 저장할 MCP 서버 정보 목록
        """
        try:
            with open(self.servers_cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"캐시 저장 성공: {self.servers_cache_file}")
        except Exception as e:
            logger.error(f"캐시 저장 실패: {e}")
    
    def get_mcp_servers(self, force_refresh=False):
        """
        MCP 서버 목록을 가져옵니다.
        
        Args:
            force_refresh (bool, optional): 캐시를 무시하고 강제로 새로고침할지 여부. 기본값은 False입니다.
            
        Returns:
            list: MCP 서버 정보 목록
        """
        # 캐시가 유효하고 강제 새로고침이 아니면 캐시에서 로드
        if not force_refresh and self._is_cache_valid():
            cached_data = self._load_cache()
            if cached_data:
                logger.info("캐시에서 MCP 서버 정보를 로드했습니다.")
                return cached_data
        
        logger.info("GitHub에서 MCP 서버 정보를 크롤링합니다...")
        
        # README.md 파일 다운로드
        readme_content = self._download_readme()
        
        if readme_content:
            # README.md 파일에서 MCP 서버 정보 파싱
            mcp_servers = self._parse_readme(readme_content)
            
            if mcp_servers:
                # 캐시에 저장
                self._save_cache(mcp_servers)
                logger.info(f"GitHub에서 {len(mcp_servers)}개의 MCP 서버를 찾았습니다.")
                return mcp_servers
        
        # 파싱 실패 시 하드코딩된 데이터 반환
        logger.warning("GitHub에서 MCP 서버 정보를 가져오지 못했습니다. 기본 데이터를 사용합니다.")
        mcp_servers = self._get_default_mcp_servers()
        
        # 캐시에 저장
        self._save_cache(mcp_servers)
        
        return mcp_servers
    
    def _download_readme(self):
        """
        README.md 파일을 다운로드합니다.
        
        Returns:
            str: README.md 파일 내용
        """
        try:
            logger.info(f"README.md 파일 다운로드 중: {self.readme_url}")
            
            headers = {
                'User-Agent': 'MCP-Config-Manager/1.0'
            }
            
            response = requests.get(self.readme_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            logger.info("README.md 파일 다운로드 성공")
            return response.text
        except Exception as e:
            logger.error(f"README.md 파일 다운로드 실패: {e}")
            return None
    
    def _parse_readme(self, readme_content):
        """
        README.md 파일에서 MCP 서버 정보를 파싱합니다.
        
        Args:
            readme_content (str): README.md 파일 내용
            
        Returns:
            list: MCP 서버 정보 목록
        """
        mcp_servers = []
        
        try:
            # 방법 1: 마크다운을 HTML로 변환 후 BeautifulSoup으로 파싱
            html = markdown.markdown(readme_content)
            soup = BeautifulSoup(html, 'html.parser')
            
            # Reference Servers와 Official Integrations 섹션 찾기
            headings = soup.find_all(['h1', 'h2', 'h3'])
            
            reference_section = None
            official_section = None
            
            for heading in headings:
                if "Reference Servers" in heading.text:
                    reference_section = heading
                elif "Official Integrations" in heading.text:
                    official_section = heading
            
            # Reference Servers 섹션 파싱
            if reference_section:
                logger.info("Reference Servers 섹션 발견")
                mcp_servers.extend(self._parse_section(reference_section, 'reference'))
            
            # Official Integrations 섹션 파싱
            if official_section:
                logger.info("Official Integrations 섹션 발견")
                mcp_servers.extend(self._parse_section(official_section, 'official'))
            
            # 방법 1로 파싱에 실패한 경우 방법 2 시도: 정규 표현식 사용
            if not mcp_servers:
                logger.info("BeautifulSoup 파싱 실패, 정규 표현식으로 시도")
                mcp_servers = self._parse_readme_with_regex(readme_content)
        
        except Exception as e:
            logger.error(f"README.md 파싱 실패: {e}")
            return []
        
        return mcp_servers if mcp_servers else []
    
    def _parse_section(self, heading, section_type):
        """
        섹션에서 MCP 서버 목록을 파싱합니다.
        
        Args:
            heading: 섹션 제목 요소
            section_type (str): 섹션 유형 ('reference' 또는 'official')
            
        Returns:
            list: MCP 서버 정보 목록
        """
        servers = []
        
        # 다음 ul 요소 찾기
        ul = None
        next_element = heading.next_sibling
        
        while next_element and not ul:
            if next_element.name == 'ul':
                ul = next_element
                break
            next_element = next_element.next_sibling
        
        if not ul:
            logger.warning(f"{section_type} 섹션에서 목록을 찾을 수 없습니다.")
            return []
        
        # 목록 항목 처리
        for li in ul.find_all('li'):
            try:
                # 링크 찾기
                a = li.find('a')
                if not a:
                    continue
                
                # 서버 이름과 설명 추출
                name = a.text.strip()
                description = li.text.replace(name, '', 1).strip()
                
                if description.startswith('-'):
                    description = description[1:].strip()
                elif description.startswith(':'):
                    description = description[1:].strip()
                
                # 카테고리 추정
                category = self._estimate_category(description)
                
                # 설치 옵션 설정
                installation_options = ['npm', 'pip'] if section_type == 'reference' else ['npm']
                
                # MCP 서버 정보 생성
                server_info = {
                    'name': name,
                    'description': description,
                    'installation_options': installation_options,
                    'config_sample': None,
                    'env_vars': [],
                    'args': [],
                    'category': category,
                    'type': section_type
                }
                
                servers.append(server_info)
                logger.info(f"{section_type} 서버 발견: {name}")
            
            except Exception as e:
                logger.error(f"목록 항목 파싱 실패: {e}")
        
        return servers
    
    def _parse_readme_with_regex(self, readme_content):
        """
        정규 표현식을 사용하여 README.md 파일에서 MCP 서버 정보를 파싱합니다.
        
        Args:
            readme_content (str): README.md 파일 내용
            
        Returns:
            list: MCP 서버 정보 목록
        """
        servers = []
        
        try:
            # Reference Servers 섹션 찾기
            reference_section_match = re.search(r'##\s+Reference\s+Servers\s+(.*?)(?=##|\Z)', readme_content, re.DOTALL)
            
            if reference_section_match:
                reference_section = reference_section_match.group(1)
                
                # 목록 항목 파싱
                list_items = re.findall(r'[-*]\s+\[([^]]+)\]\([^)]+\)([^\n]*)', reference_section)
                
                for name, description in list_items:
                    description = description.strip()
                    if description.startswith('-'):
                        description = description[1:].strip()
                    elif description.startswith(':'):
                        description = description[1:].strip()
                    
                    category = self._estimate_category(description)
                    
                    server_info = {
                        'name': name.strip(),
                        'description': description,
                        'installation_options': ['npm', 'pip'],
                        'config_sample': None,
                        'env_vars': [],
                        'args': [],
                        'category': category,
                        'type': 'reference'
                    }
                    
                    servers.append(server_info)
                    logger.info(f"Reference 서버 발견 (정규식): {name}")
            
            # Official Integrations 섹션 찾기
            official_section_match = re.search(r'##\s+Official\s+Integrations\s+(.*?)(?=##|\Z)', readme_content, re.DOTALL)
            
            if official_section_match:
                official_section = official_section_match.group(1)
                
                # 목록 항목 파싱
                list_items = re.findall(r'[-*]\s+\[([^]]+)\]\([^)]+\)([^\n]*)', official_section)
                
                for name, description in list_items:
                    description = description.strip()
                    if description.startswith('-'):
                        description = description[1:].strip()
                    elif description.startswith(':'):
                        description = description[1:].strip()
                    
                    category = self._estimate_category(description)
                    
                    server_info = {
                        'name': name.strip(),
                        'description': description,
                        'installation_options': ['npm'],
                        'config_sample': None,
                        'env_vars': [],
                        'args': [],
                        'category': category,
                        'type': 'official'
                    }
                    
                    servers.append(server_info)
                    logger.info(f"Official 서버 발견 (정규식): {name}")
        
        except Exception as e:
            logger.error(f"정규 표현식 파싱 실패: {e}")
        
        return servers
    
    def _estimate_category(self, description):
        """
        설명을 기반으로 서버 카테고리를 추정합니다.
        
        Args:
            description (str): 서버 설명
            
        Returns:
            str: 추정된 카테고리
        """
        if not description:
            return "general"
            
        description_lower = description.lower()
        
        if any(keyword in description_lower for keyword in ['search', '검색']):
            return 'search'
        elif any(keyword in description_lower for keyword in ['image', 'vision', '이미지', '비전', 'art', 'picture']):
            return 'vision'
        elif any(keyword in description_lower for keyword in ['audio', 'voice', 'speech', '오디오', '음성']):
            return 'audio'
        elif any(keyword in description_lower for keyword in ['file', 'document', '파일', '문서', 'filesystem']):
            return 'document'
        elif any(keyword in description_lower for keyword in ['database', 'sql', 'db', 'data', 'postgresql', 'sqlite']):
            return 'database'
        elif any(keyword in description_lower for keyword in ['web', 'browser', 'fetch', 'http']):
            return 'web'
        elif any(keyword in description_lower for keyword in ['git', 'github', 'gitlab']):
            return 'git'
        elif any(keyword in description_lower for keyword in ['time', 'date', 'timezone']):
            return 'time'
        elif any(keyword in description_lower for keyword in ['map', 'location', 'place', 'direction']):
            return 'map'
        elif any(keyword in description_lower for keyword in ['memory', 'thinking', 'thought']):
            return 'memory'
        elif any(keyword in description_lower for keyword in ['tool', 'utility', '도구', '유틸리티']):
            return 'utility'
        else:
            return 'general'
    
    def _get_default_mcp_servers(self):
        """
        기본 MCP 서버 목록을 반환합니다.
        
        Returns:
            list: 기본 MCP 서버 정보 목록
        """
        return [
            {
                'name': 'AWS KB Retrieval',
                'description': 'Retrieval from AWS Knowledge Base using Bedrock Agent Runtime',
                'installation_options': ['npm', 'pip'],
                'config_sample': None,
                'env_vars': ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION'],
                'args': ['--kb-id'],
                'category': 'search',
                'type': 'reference'
            },
            {
                'name': 'Brave Search',
                'description': 'Web and local search using Brave\'s Search API',
                'installation_options': ['npm', 'pip'],
                'config_sample': None,
                'env_vars': ['BRAVE_API_KEY'],
                'args': ['--count'],
                'category': 'search',
                'type': 'reference'
            },
            {
                'name': 'EverArt',
                'description': 'AI image generation using various models',
                'installation_options': ['npm', 'pip'],
                'config_sample': None,
                'env_vars': ['EVERART_API_KEY'],
                'args': ['--model', '--size'],
                'category': 'vision',
                'type': 'reference'
            },
            {
                'name': 'Filesystem',
                'description': 'Secure file operations with configurable access controls',
                'installation_options': ['npm', 'pip'],
                'config_sample': None,
                'env_vars': [],
                'args': ['--root', '--readonly'],
                'category': 'document',
                'type': 'reference'
            },
            {
                'name': 'GitHub',
                'description': 'Repository management, file operations, and GitHub API integration',
                'installation_options': ['npm', 'pip'],
                'config_sample': None,
                'env_vars': ['GITHUB_TOKEN'],
                'args': ['--repo', '--owner'],
                'category': 'git',
                'type': 'reference'
            },
            {
                'name': 'Aiven',
                'description': 'Navigate Aiven projects and interact with PostgreSQL, Kafka, ClickHouse and OpenSearch',
                'installation_options': ['npm'],
                'config_sample': None,
                'env_vars': ['AIVEN_TOKEN'],
                'args': ['--project'],
                'category': 'database',
                'type': 'official'
            },
            {
                'name': 'Apify',
                'description': 'Use 3,000+ pre-built cloud tools to extract data from websites',
                'installation_options': ['npm'],
                'config_sample': None,
                'env_vars': ['APIFY_API_KEY'],
                'args': [],
                'category': 'web',
                'type': 'official'
            },
            {
                'name': 'Cloudflare',
                'description': 'Deploy, configure & interrogate Cloudflare developer platform resources',
                'installation_options': ['npm'],
                'config_sample': None,
                'env_vars': ['CLOUDFLARE_API_TOKEN'],
                'args': [],
                'category': 'web',
                'type': 'official'
            },
            {
                'name': 'Stripe',
                'description': 'Interact with Stripe API',
                'installation_options': ['npm'],
                'config_sample': None,
                'env_vars': ['STRIPE_API_KEY'],
                'args': [],
                'category': 'database',
                'type': 'official'
            },
            {
                'name': 'Tavily',
                'description': 'Search engine for AI agents (search + extract)',
                'installation_options': ['npm'],
                'config_sample': None,
                'env_vars': ['TAVILY_API_KEY'],
                'args': ['--max-results'],
                'category': 'search',
                'type': 'official'
            }
        ]