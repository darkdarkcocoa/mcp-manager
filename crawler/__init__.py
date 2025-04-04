"""
MCP 설정 관리자의 크롤러 패키지

GitHub에서 MCP 서버 정보를 크롤링하는 기능을 제공합니다.
"""

from .github_crawler import GitHubCrawler

__all__ = ['GitHubCrawler']
