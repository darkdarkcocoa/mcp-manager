# MCP 설정 관리자 (MCP Config Manager) 개발 가이드

## 빌드 및 테스트 명령어
- 전체 테스트 실행: `python -m unittest discover tests`
- 단일 테스트 실행: `python -m unittest tests/test_file.py`
- 특정 테스트 함수 실행: `python tests/test_file.py`

## 코드 스타일 가이드라인
- **들여쓰기**: 4 스페이스 사용
- **최대 라인 길이**: 100자 이내
- **명명 규칙**:
  - 클래스: PascalCase (`ConfigManager`)
  - 함수/메서드: snake_case (`get_mcp_servers`)
  - 변수: snake_case (`config_path`)
  - 상수: UPPER_SNAKE_CASE (`DEFAULT_CONFIG`)
- **문서화**: 모든 모듈, 클래스, 함수에 독스트링 작성 (한글)
- **타입 힌트**: 모든 함수 인자와 반환값에 타입 힌트 추가
- **예외 처리**: 구체적인 예외를 사용하고 로깅 활용
- **가져오기 순서**: 표준 라이브러리 → 서드파티 → 프로젝트 모듈