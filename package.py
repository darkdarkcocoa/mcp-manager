"""
MCP 설정 관리자 패키징 스크립트

PyInstaller를 사용하여 실행 파일을 생성합니다.
"""

import os
import sys
import platform

# PyInstaller 명령 생성
def create_pyinstaller_command():
    """PyInstaller 명령을 생성합니다."""
    system = platform.system()
    
    # 기본 명령
    cmd = [
        "python3 -m PyInstaller",
        "--name=MCP_Config_Manager",
        "--onefile",
        "--windowed",
        "--clean",
        "--add-data=LICENSE:.",
        "--icon=resources/icon.ico" if system == "Windows" else "--icon=resources/icon.icns" if system == "Darwin" else "",
    ]
    
    # 시스템별 추가 옵션
    if system == "Windows":
        cmd.append("--version-file=version_info.txt")
    elif system == "Darwin":
        cmd.append("--osx-bundle-identifier=com.mcp.configmanager")
    
    # 메인 스크립트 추가
    cmd.append("main.py")
    
    return " ".join(filter(None, cmd))

# 버전 정보 파일 생성 (Windows용)
def create_version_info():
    """버전 정보 파일을 생성합니다."""
    version_info = """
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [StringStruct(u'CompanyName', u'MCP'),
           StringStruct(u'FileDescription', u'MCP 설정 관리자'),
           StringStruct(u'FileVersion', u'1.0.0'),
           StringStruct(u'InternalName', u'MCP_Config_Manager'),
           StringStruct(u'LegalCopyright', u'Copyright (c) 2025'),
           StringStruct(u'OriginalFilename', u'MCP_Config_Manager.exe'),
           StringStruct(u'ProductName', u'MCP 설정 관리자'),
           StringStruct(u'ProductVersion', u'1.0.0')])
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    with open("version_info.txt", "w") as f:
        f.write(version_info)

# 리소스 디렉토리 생성
def create_resources():
    """리소스 디렉토리와 파일을 생성합니다."""
    os.makedirs("resources", exist_ok=True)
    
    # 간단한 아이콘 파일 생성 (실제로는 더 나은 아이콘을 사용해야 함)
    with open("resources/icon.ico", "w") as f:
        f.write("# 아이콘 파일 (실제로는 바이너리 파일이어야 함)")
    
    with open("resources/icon.icns", "w") as f:
        f.write("# 아이콘 파일 (실제로는 바이너리 파일이어야 함)")

# 라이센스 파일 생성
def create_license():
    """라이센스 파일을 생성합니다."""
    license_text = """
MIT License

Copyright (c) 2025 MCP Config Manager

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    with open("LICENSE", "w") as f:
        f.write(license_text)

# README 파일 생성
def create_readme():
    """README 파일을 생성합니다."""
    readme_text = """# MCP 설정 관리자 (MCP Config Manager)

MCP 설정 관리자는 Claude Desktop의 MCP(Model Context Protocol) 서버 설정을 관리하는 도구입니다.

## 기능

- GitHub에서 MCP 서버 목록 자동 크롤링
- 설치된 MCP 서버 관리
- 설정 파일 백업 및 복원
- 크로스 플랫폼 지원 (Windows, macOS, Linux)

## 설치 방법

### Windows

1. `MCP_Config_Manager_Setup.exe` 파일을 다운로드합니다.
2. 설치 프로그램을 실행하고 안내에 따라 설치합니다.

### macOS

1. `MCP_Config_Manager.dmg` 파일을 다운로드합니다.
2. DMG 파일을 열고 애플리케이션을 Applications 폴더로 드래그합니다.

### Linux

1. `MCP_Config_Manager.AppImage` 파일을 다운로드합니다.
2. 파일에 실행 권한을 부여합니다: `chmod +x MCP_Config_Manager.AppImage`
3. 애플리케이션을 실행합니다: `./MCP_Config_Manager.AppImage`

## 사용 방법

1. MCP 설정 관리자를 실행합니다.
2. "사용 가능한 MCP" 탭에서 원하는 MCP 서버를 선택합니다.
3. 필요한 설정을 입력하고 "적용" 버튼을 클릭합니다.
4. "내 MCP" 탭에서 설치된 MCP 서버를 관리합니다.
5. 변경 사항을 저장하면 Claude Desktop이 재시작됩니다.

## 개발자 정보

- 개발 언어: Python
- 사용 라이브러리: PyQt6, Requests, BeautifulSoup4, Markdown

## 라이센스

MIT License
"""
    with open("README.md", "w") as f:
        f.write(readme_text)

# 사용자 매뉴얼 생성
def create_user_manual():
    """사용자 매뉴얼을 생성합니다."""
    manual_text = """# MCP 설정 관리자 사용자 매뉴얼

## 목차

1. [소개](#1-소개)
2. [설치 방법](#2-설치-방법)
3. [시작하기](#3-시작하기)
4. [MCP 서버 추가하기](#4-mcp-서버-추가하기)
5. [MCP 서버 관리하기](#5-mcp-서버-관리하기)
6. [설정 백업 및 복원](#6-설정-백업-및-복원)
7. [문제 해결](#7-문제-해결)
8. [자주 묻는 질문](#8-자주-묻는-질문)

## 1. 소개

MCP 설정 관리자는 Claude Desktop의 MCP(Model Context Protocol) 서버 설정을 쉽게 관리할 수 있는 도구입니다. 이 애플리케이션을 사용하면 GitHub에서 사용 가능한 MCP 서버 목록을 자동으로 가져오고, 원하는 서버를 선택하여 설정하고, 설정 파일을 백업 및 복원할 수 있습니다.

### 1.1 주요 기능

- GitHub에서 MCP 서버 목록 자동 크롤링
- 설치된 MCP 서버 관리
- 설정 파일 백업 및 복원
- 크로스 플랫폼 지원 (Windows, macOS, Linux)

## 2. 설치 방법

### 2.1 Windows

1. `MCP_Config_Manager_Setup.exe` 파일을 다운로드합니다.
2. 설치 프로그램을 실행하고 안내에 따라 설치합니다.
3. 설치가 완료되면 시작 메뉴 또는 바탕화면에서 MCP 설정 관리자를 실행할 수 있습니다.

### 2.2 macOS

1. `MCP_Config_Manager.dmg` 파일을 다운로드합니다.
2. DMG 파일을 열고 애플리케이션을 Applications 폴더로 드래그합니다.
3. Finder에서 Applications 폴더를 열고 MCP 설정 관리자를 실행합니다.

### 2.3 Linux

1. `MCP_Config_Manager.AppImage` 파일을 다운로드합니다.
2. 파일에 실행 권한을 부여합니다: `chmod +x MCP_Config_Manager.AppImage`
3. 애플리케이션을 실행합니다: `./MCP_Config_Manager.AppImage`

## 3. 시작하기

MCP 설정 관리자를 처음 실행하면 다음과 같은 화면이 표시됩니다:

1. **사용 가능한 MCP 탭**: GitHub에서 가져온 MCP 서버 목록이 표시됩니다.
2. **내 MCP 탭**: 현재 설치된 MCP 서버 목록이 표시됩니다.

애플리케이션이 시작되면 자동으로 GitHub에서 MCP 서버 목록을 가져옵니다. 이 과정은 인터넷 연결 상태에 따라 몇 초에서 몇 분이 소요될 수 있습니다.

## 4. MCP 서버 추가하기

### 4.1 서버 선택

1. "사용 가능한 MCP" 탭으로 이동합니다.
2. 목록에서 원하는 MCP 서버를 선택합니다. 여러 서버를 선택하려면 Ctrl 키(Windows/Linux) 또는 Command 키(macOS)를 누른 상태에서 클릭합니다.
3. 서버를 선택하면 오른쪽 패널에 상세 정보가 표시됩니다.

### 4.2 서버 설정

1. 선택한 서버의 상세 정보 패널에서 필요한 설정을 입력합니다:
   - 설치 옵션 선택 (npm, uvx, docker 등)
   - 환경 변수 입력 (API 키 등)
   - 인자 옵션 입력

2. 모든 설정을 완료한 후 "적용" 버튼을 클릭합니다.

## 5. MCP 서버 관리하기

### 5.1 서버 목록 보기

"내 MCP" 탭으로 이동하면 현재 설치된 MCP 서버 목록이 표시됩니다. 각 서버는 다음 정보를 포함합니다:
- 서버 이름
- 활성화 상태 (활성화된 서버는 검은색, 비활성화된 서버는 회색으로 표시)

### 5.2 서버 편집

1. 편집할 서버를 선택합니다.
2. "편집" 버튼을 클릭합니다.
3. 오른쪽 패널에서 서버 설정을 변경합니다.
4. 변경 사항을 저장하려면 "저장" 버튼을 클릭합니다.

### 5.3 서버 삭제

1. 삭제할 서버를 선택합니다.
2. "삭제" 버튼을 클릭합니다.
3. 확인 메시지가 표시되면 "예"를 클릭합니다.

### 5.4 서버 순서 변경

1. 이동할 서버를 선택합니다.
2. "위로" 또는 "아래로" 버튼을 클릭하여 서버 순서를 변경합니다.

### 5.5 변경 사항 적용

모든 변경 사항을 적용하려면 "저장" 버튼을 클릭합니다. 변경 사항을 적용하려면 Claude Desktop을 재시작해야 합니다. 재시작 확인 메시지가 표시되면 "예"를 클릭합니다.

## 6. 설정 백업 및 복원

### 6.1 설정 백업

1. "내 MCP" 탭에서 "백업" 버튼을 클릭합니다.
2. 현재 설정이 백업되고 확인 메시지가 표시됩니다.

### 6.2 설정 복원

1. "내 MCP" 탭에서 "복원" 버튼을 클릭합니다.
2. 가장 최근 백업에서 설정을 복원할지 확인하는 메시지가 표시됩니다.
3. "예"를 클릭하여 설정을 복원합니다.

## 7. 문제 해결

### 7.1 MCP 서버 목록을 가져올 수 없음

- 인터넷 연결을 확인하세요.
- GitHub 서버에 접속할 수 있는지 확인하세요.
- 애플리케이션을 재시작하세요.

### 7.2 설정 파일을 저장할 수 없음

- 설정 파일 경로에 쓰기 권한이 있는지 확인하세요.
- 다른 프로그램이 설정 파일을 사용 중인지 확인하세요.
- 관리자 권한으로 애플리케이션을 실행해 보세요.

### 7.3 Claude Desktop이 재시작되지 않음

- Claude Desktop이 실행 중인지 확인하세요.
- 수동으로 Claude Desktop을 재시작해 보세요.

## 8. 자주 묻는 질문

### 8.1 MCP 서버란 무엇인가요?

MCP(Model Context Protocol) 서버는 Claude AI와 외부 도구 및 서비스를 연결하는 서버입니다. 이를 통해 Claude가 웹 검색, 이미지 처리, 파일 작업 등 다양한 기능을 수행할 수 있습니다.

### 8.2 설정 파일은 어디에 저장되나요?

설정 파일은 운영체제에 따라 다음 위치에 저장됩니다:
- Windows: `%APPDATA%/Claude/claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

### 8.3 백업 파일은 어디에 저장되나요?

백업 파일은 설정 파일이 있는 디렉토리의 `backups` 폴더에 저장됩니다.

### 8.4 여러 컴퓨터 간에 설정을 공유할 수 있나요?

현재 버전에서는 설정 파일을 수동으로 복사하여 공유할 수 있습니다. 향후 버전에서는 설정 내보내기/가져오기 기능을 추가할 예정입니다.
"""
    with open("USER_MANUAL.md", "w") as f:
        f.write(manual_text)

# 설치 스크립트 생성 (Windows용)
def create_windows_installer():
    """Windows용 설치 스크립트를 생성합니다."""
    inno_script = """
#define MyAppName "MCP 설정 관리자"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "MCP"
#define MyAppURL "https://github.com/modelcontextprotocol/servers"
#define MyAppExeName "MCP_Config_Manager.exe"

[Setup]
AppId={{8A9D3F7E-7C8D-4F8A-B8E7-6C9D3F7E7C8D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=dist
OutputBaseFilename=MCP_Config_Manager_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "korean"; MessagesFile: "compiler:Languages\\Korean.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "USER_MANUAL.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"
Name: "{group}\\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
"""
    with open("installer.iss", "w") as f:
        f.write(inno_script)

# 메인 함수
def main():
    """메인 함수"""
    print("MCP 설정 관리자 패키징을 시작합니다...")
    
    # 리소스 생성
    print("리소스 파일 생성 중...")
    create_resources()
    
    # 라이센스 파일 생성
    print("라이센스 파일 생성 중...")
    create_license()
    
    # README 파일 생성
    print("README 파일 생성 중...")
    create_readme()
    
    # 사용자 매뉴얼 생성
    print("사용자 매뉴얼 생성 중...")
    create_user_manual()
    
    # 버전 정보 파일 생성 (Windows용)
    if platform.system() == "Windows":
        print("버전 정보 파일 생성 중...")
        create_version_info()
    
    # PyInstaller 명령 생성
    pyinstaller_cmd = create_pyinstaller_command()
    print(f"PyInstaller 명령: {pyinstaller_cmd}")
    
    # Windows 설치 프로그램 스크립트 생성
    if platform.system() == "Windows":
        print("Windows 설치 프로그램 스크립트 생성 중...")
        create_windows_installer()
    
    print("MCP 설정 관리자 패키징이 완료되었습니다.")
    print("다음 명령을 실행하여 실행 파일을 생성하세요:")
    print(f"  {pyinstaller_cmd}")
    
    if platform.system() == "Windows":
        print("Windows 설치 프로그램을 생성하려면 Inno Setup을 설치하고 다음 명령을 실행하세요:")
        print("  iscc installer.iss")

if __name__ == "__main__":
    main()
