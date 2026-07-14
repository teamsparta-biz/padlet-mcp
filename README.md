# padlet-mcp

[Padlet REST API](https://api.padlet.dev/v1)를 감싸는 MCP 서버. Claude Code가 Padlet 보드를 읽고 쓸 수 있게 해준다.

## 제공 툴

| 툴 | 설명 |
| --- | --- |
| `list_boards` | 현재 API 키로 접근 가능한 보드 목록 (id, 제목, URL) |
| `get_board` | 보드 하나의 섹션·게시물·댓글 전체 |
| `create_post` | 보드에 새 게시물 작성 |

전형적인 사용 흐름: `list_boards`로 board_id 확인 → `get_board`로 내용 조회 → (필요하면) `create_post`로 작성. padlet.com URL만 있고 board_id를 모를 때는 `list_boards`가 반환하는 `web_url`과 대조해서 찾으면 된다.

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

1. [Padlet 개발자 설정](https://padlet.com/settings/api)에서 본인 명의 API 키 발급 (공유 키 사용 금지 — 게시물 작성자가 본인 계정으로 찍힘)
2. 아래 둘 중 하나로 설정:
   - 환경변수 `PADLET_API_KEY`
   - `~/.secrets/padlet_api_key.txt` 파일에 키 값만 저장 (경로를 바꾸고 싶으면 `PADLET_API_KEY_FILE` 환경변수 사용)

키가 없으면 서버 실행 시 바로 에러가 나며 어디에 저장하면 되는지 메시지로 안내한다.

## 3. Claude Code에 등록

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

## 4. 문제 해결

- **"Padlet API 키를 찾을 수 없습니다"** — 2단계의 환경변수/파일 설정이 안 된 것. 둘 중 하나를 다시 확인.
- **`pip install` 시 "script ... is not on PATH" 경고** — 무시해도 된다. `python -m padlet_mcp`로 실행하므로 Scripts 폴더가 PATH에 없어도 상관없다.
- **Claude Code에서 padlet 툴이 안 보임** — `.mcp.json` 등록 후 Claude Code를 재시작해야 반영된다.

## 로컬 개발 (기여자용)

이 저장소를 clone해서 직접 고칠 때는 [uv](https://docs.astral.sh/uv/)를 쓰면 편하다 (필수는 아님, `pip install -e .`로도 가능):

```
uv sync
uv run padlet-mcp
```
