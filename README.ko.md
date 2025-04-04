# MCP 설정 관리자

*[English](README.md) 버전도 확인하세요*

MCP 설정 관리자는 Claude Desktop의 MCP(Model Context Protocol) 서버 설정을 관리하는 도구입니다.

## 기능

- GitHub에서 MCP 서버 목록 자동 크롤링
- 설치된 MCP 서버 관리
- 설정 파일 백업 및 복원
- 크로스 플랫폼 지원 (Windows, macOS, Linux)
- Claude Desktop 설정 파일 경로 직접 지정 가능

## 설치 방법

### 빌드된 패키지 설치

#### Windows

1. `MCP_Config_Manager_Setup.exe` 파일을 다운로드합니다.
2. 설치 프로그램을 실행하고 안내에 따라 설치합니다.

#### macOS

1. `MCP_Config_Manager.dmg` 파일을 다운로드합니다.
2. DMG 파일을 열고 애플리케이션을 Applications 폴더로 드래그합니다.
3. 참고: 첫 실행 시 "확인되지 않은 개발자" 경고가 표시될 수 있습니다. 이 경우 애플리케이션을 Control 키를 누른 상태에서 클릭하고 "열기"를 선택합니다.

#### Linux

1. `MCP_Config_Manager.AppImage` 파일을 다운로드합니다.
2. 파일에 실행 권한을 부여합니다: `chmod +x MCP_Config_Manager.AppImage`
3. 애플리케이션을 실행합니다: `./MCP_Config_Manager.AppImage`

### GitHub에서 소스코드로 실행

1. 저장소 클론:
   ```bash
   git clone https://github.com/darkdarkcocoa/mcp-manager.git
   cd mcp-manager
   ```

2. 가상 환경 설정 (선택 사항이지만 권장):
   ```bash
   python -m venv venv
   
   # Windows에서 활성화
   venv\Scripts\activate
   
   # macOS/Linux에서 활성화
   source venv/bin/activate
   ```

3. 필요한 라이브러리 설치:
   ```bash
   pip install -r requirements.txt
   ```

4. 애플리케이션 실행:
   ```bash
   python main.py
   ```

## 사용 방법

### 설정 파일 경로 설정

처음 실행 시 Claude Desktop 설정 파일 경로를 찾을 수 없으면 직접 Claude Desktop 설치 폴더를 지정할 수 있습니다.
* Windows: `%APPDATA%/Claude`
* macOS: `~/Library/Application Support/Claude`
* Linux: `~/.config/Claude`

이후에도 "내 MCP" 탭에서 "경로 변경" 버튼을 통해 설정 파일 경로를 변경할 수 있습니다.

### MCP 서버 관리

1. MCP 설정 관리자를 실행합니다.
2. "사용 가능한 MCP" 탭에서 원하는 MCP 서버를 선택합니다.
3. 필요한 설정을 입력하고 "적용" 버튼을 클릭합니다.
4. "내 MCP" 탭에서 설치된 MCP 서버를 관리합니다.
5. 변경 사항을 저장하면 Claude Desktop이 재시작됩니다.

## 개발자 정보

- 개발 언어: Python
- 사용 라이브러리: PyQt6, Requests, BeautifulSoup4, Markdown

## 개발 환경 설정

### 개발 의존성

프로젝트 개발에 필요한 패키지:
```
PyQt6>=6.0.0
requests>=2.25.0
beautifulsoup4>=4.9.0
markdown>=3.3.0
```

### 개발 및 기여

1. 이슈 및 기능 요청은 GitHub 이슈를 통해 제출해주세요.
2. 코드 기여는 Pull Request를 통해 제출해주세요.
3. 코드 작성 시 PEP 8 스타일 가이드를 따라주세요.

## 라이센스

MIT License
