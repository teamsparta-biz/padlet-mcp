# padlet-mcp

[Padlet REST API](https://api.padlet.dev/v1)를 감싸는 MCP 서버. Claude Code가 Padlet 보드를 읽을 수 있게 해준다. 읽기 전용 — 글쓰기/수정/삭제는 안 됨.

## 1. 설치

Python 3.10+ 만 있으면 된다 (uv 등 추가 도구 불필요):

```
pip install --user git+https://github.com/teamsparta-biz/padlet-mcp
```

새 버전이 올라온 뒤 갱신하려면:

```
pip install --user --upgrade git+https://github.com/teamsparta-biz/padlet-mcp
```

## 2. API 키 받기

공용 biz 계정으로 로그인해서 https://padlet.com/settings/api 에서 키 값을 복사한다. 팀 전체가 공유하는 유일한 키이니 외부 공개 채널이나 커밋에는 올리지 말 것.

복사한 키는 Claude Code한테 그대로 던져주고 "이 키로 padlet-mcp 설정해줘"라고 하면 알아서 저장하고 연동까지 해준다.

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

- **"Padlet API 키를 찾을 수 없습니다"** — 2단계의 키 저장이 안 된 것. Claude Code한테 다시 키를 주고 설정해달라고 하면 된다.
- **`pip install` 시 "script ... is not on PATH" 경고** — 무시해도 된다. `python -m padlet_mcp`로 실행하므로 Scripts 폴더가 PATH에 없어도 상관없다.
- **Claude Code에서 padlet 툴이 안 보임** — `.mcp.json` 등록 후 Claude Code를 재시작해야 반영된다.

## 로컬 개발 (기여자용)

이 저장소를 clone해서 직접 고칠 때는 [uv](https://docs.astral.sh/uv/)를 쓰면 편하다 (필수는 아님, `pip install -e .`로도 가능):

```
uv sync
uv run padlet-mcp
```
