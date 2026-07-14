# padlet-mcp

[Padlet REST API](https://api.padlet.dev/v1)를 감싸는 MCP 서버. Claude Code가 Padlet 보드를 읽을 수 있게 해준다. 읽기 전용 — 글쓰기/수정/삭제 툴은 없다.

## 제공 툴

| 툴 | 설명 |
| --- | --- |
| `list_boards` | 현재 API 키로 접근 가능한 보드 목록 (id, 제목, URL) |
| `get_board` | 보드 하나의 섹션·게시물·댓글 전체 |

전형적인 사용 흐름: `list_boards`로 board_id 확인 → `get_board`로 내용 조회. padlet.com URL만 있고 board_id를 모를 때는 `list_boards`가 반환하는 `web_url`과 대조해서 찾으면 된다.

## 1. 설치

Python 3.10+ 만 있으면 된다 (uv 등 추가 도구 불필요):

```
pip install --user git+https://github.com/teamsparta-biz/padlet-mcp
```

새 버전이 올라온 뒤 갱신하려면:

```
pip install --user --upgrade git+https://github.com/teamsparta-biz/padlet-mcp
```

## 2. API 키 발급 및 설정

1. https://padlet.com/settings/api 접속 (로그인 필요) → API 키 발급 화면에서 새 키 생성 → 값 복사
   - 읽기 전용이라 작성자 attribution 문제는 없지만, 그래도 키는 각자 본인 계정으로 발급받을 것을 권장한다 — 그래야 특정 사람이 퇴사/키 유출 시 그 사람 키만 무효화하면 되고, `list_boards`도 본인이 실제 접근 권한 있는 보드만 정확히 보여준다.
2. 복사한 키를 아래 둘 중 하나로 저장 (파일 방식을 권장 — 터미널을 새로 열어도 유지됨):

   **방법 A: 파일에 저장 (권장)**

   Windows (PowerShell):
   ```powershell
   New-Item -ItemType Directory -Force -Path "$HOME\.secrets" | Out-Null
   Set-Content -Path "$HOME\.secrets\padlet_api_key.txt" -Value "<발급받은 키>" -NoNewline
   ```

   macOS / Linux:
   ```bash
   mkdir -p ~/.secrets
   printf '%s' '<발급받은 키>' > ~/.secrets/padlet_api_key.txt
   ```

   저장 경로를 바꾸고 싶으면 환경변수 `PADLET_API_KEY_FILE`로 다른 경로를 지정하면 된다.

   **방법 B: 환경변수로 직접 설정**

   Windows (PowerShell, 현재 세션에만 적용):
   ```powershell
   $env:PADLET_API_KEY = "<발급받은 키>"
   ```

   영구적으로 적용하려면 [시스템 환경 변수 편집]에 `PADLET_API_KEY`를 추가하거나, macOS/Linux는 `~/.bashrc`/`~/.zshrc`에 `export PADLET_API_KEY=...`를 추가.

키가 없으면 서버 실행 시 바로 에러가 나며 어디에 저장하면 되는지 메시지로 안내한다.

## 3. 설치 확인 (테스트)

Claude Code에 등록하기 전에, 키 설정이 맞는지 먼저 확인하자.

**가장 간단한 방법 — Padlet API를 직접 호출해서 실제 보드 목록이 나오는지 확인:**

```
python -c "from padlet_mcp.server import list_boards; import json; print(json.dumps(list_boards(), indent=2))"
```

에러 없이 본인 보드 목록(JSON)이 출력되면 키 설정이 정상이라는 뜻이다. (한글은 `\uXXXX`로 이스케이프되어 나오는 게 정상 — Windows 콘솔 인코딩 때문이며 실제 값은 깨지지 않는다.)

**MCP 프로토콜 그대로 테스트하고 싶다면** ([MCP Inspector](https://github.com/modelcontextprotocol/inspector) 사용, Node.js 필요):

```
npx @modelcontextprotocol/inspector python -m padlet_mcp
```

브라우저가 열리면 `list_boards`/`get_board` 툴을 직접 호출해볼 수 있다.

## 4. Claude Code에 등록

프로젝트 루트에서:

```
claude mcp add padlet --scope project -- python -m padlet_mcp
```

또는 `.mcp.json`에 직접 추가:

```json
{
  "mcpServers": {
    "padlet": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "padlet_mcp"],
      "env": {}
    }
  }
}
```

`claude mcp list`로 `padlet`이 떠 있는지, 도구가 정상 등록됐는지 확인.

## 5. 문제 해결

- **"Padlet API 키를 찾을 수 없습니다"** — 2단계의 환경변수/파일 설정이 안 된 것. 둘 중 하나를 다시 확인.
- **`pip install` 시 "script ... is not on PATH" 경고** — 무시해도 된다. `python -m padlet_mcp`로 실행하므로 Scripts 폴더가 PATH에 없어도 상관없다.
- **Claude Code에서 padlet 툴이 안 보임** — `.mcp.json` 등록 후 Claude Code를 재시작해야 반영된다.

## 로컬 개발 (기여자용)

이 저장소를 clone해서 직접 고칠 때는 [uv](https://docs.astral.sh/uv/)를 쓰면 편하다 (필수는 아님, `pip install -e .`로도 가능):

```
uv sync
uv run padlet-mcp
```
