"""
GitHub 크롤러 테스트 스크립트

MCP 서버 목록을 크롤링하는 기능을 테스트합니다.
"""

import os
import sys
import json

# 상위 디렉토리를 모듈 검색 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawler.github_crawler import GitHubCrawler

def test_github_crawler():
    """GitHub 크롤러 테스트 함수"""
    print("GitHub 크롤러 테스트를 시작합니다...")
    
    # 테스트용 캐시 디렉토리 설정
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_cache")
    os.makedirs(cache_dir, exist_ok=True)
    
    # GitHubCrawler 인스턴스 생성
    crawler = GitHubCrawler(cache_dir=cache_dir)
    
    # MCP 서버 목록 가져오기
    print("MCP 서버 목록을 가져오는 중...")
    servers = crawler.get_mcp_servers()
    
    # 결과 출력
    if servers:
        print(f"총 {len(servers)}개의 MCP 서버를 찾았습니다.")
        print("\n서버 목록:")
        for i, server in enumerate(servers, 1):
            print(f"{i}. {server['name']} - {server['description'][:50]}...")
            print(f"   카테고리: {server['category']}")
            print(f"   설치 옵션: {', '.join(server['installation_options']) if server['installation_options'] else '정보 없음'}")
            print(f"   환경 변수: {', '.join(server['env_vars']) if server['env_vars'] else '정보 없음'}")
            print(f"   인자 옵션: {', '.join(server['args'][:3]) if server['args'] else '정보 없음'}")
            if len(server['args']) > 3:
                print(f"      ... 외 {len(server['args']) - 3}개")
            print()
        
        # 첫 번째 서버의 상세 정보를 파일로 저장
        if servers:
            first_server = servers[0]
            server_name = first_server['name']
            file_path = os.path.join(cache_dir, f"{server_name}_details.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(first_server, f, ensure_ascii=False, indent=2)
            print(f"첫 번째 서버({server_name})의 상세 정보를 {file_path}에 저장했습니다.")
    else:
        print("MCP 서버를 찾을 수 없습니다.")
    
    # 캐시 테스트
    print("\n캐시 테스트를 시작합니다...")
    print("캐시에서 MCP 서버 목록을 가져오는 중...")
    cached_servers = crawler.get_mcp_servers()
    if cached_servers:
        print(f"캐시에서 총 {len(cached_servers)}개의 MCP 서버를 찾았습니다.")
    else:
        print("캐시에서 MCP 서버를 찾을 수 없습니다.")
    
    print("\nGitHub 크롤러 테스트를 완료했습니다.")

if __name__ == "__main__":
    test_github_crawler()
