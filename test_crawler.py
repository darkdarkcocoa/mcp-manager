"""
수정된 GitHub 크롤러 테스트 스크립트
"""

from crawler.github_crawler import GitHubCrawler

def test_crawler():
    """수정된 GitHub 크롤러를 테스트합니다."""
    print("수정된 GitHub 크롤러 테스트 시작...")
    
    # 크롤러 인스턴스 생성
    crawler = GitHubCrawler()
    
    # MCP 서버 목록 가져오기 (캐시 무시)
    servers = crawler.get_mcp_servers(force_refresh=True)
    
    # 결과 출력
    print(f"발견된 MCP 서버 수: {len(servers)}")
    print("\n첫 10개 서버:")
    for i, server in enumerate(servers[:10]):
        print(f"{i+1}. {server['name']} - {server['description'][:50]}...")
        print(f"   카테고리: {server['category']}")
        print(f"   설치 옵션: {', '.join(server['installation_options'])}")
        print(f"   타입: {server.get('type', 'unknown')}")
        print()
    
    print("수정된 GitHub 크롤러 테스트 완료!")
    
    return servers

if __name__ == "__main__":
    test_crawler()
