# padlet-mcp

Padlet REST API(`https://api.padlet.dev/v1`)를 감싸는 MCP 서버. `list_boards`, `get_board`, `create_post` 세 가지 툴을 제공한다.

## 요구사항

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (설치: `pip install uv` 또는 공식 인스톨러)
- 본인 명의의 Padlet API 키 ([Padlet 개발자 설정](https://padlet.com/settings/api)에서 발급)

## API 키 설정

둘 중 하나:

1. 환경변수 `PADLET_API_KEY`
2. `~/.secrets/padlet_api_key.txt` 파일에 키만 저장 (경로는 `PADLET_API_KEY_FILE` 환경변수로 바꿀 수 있음)

## Claude Code에 등록

프로젝트 루트에서:

```
claude mcp add padlet --scope project -- uvx --from git+https://github.com/<org>/padlet-mcp padlet-mcp
```

`uvx`가 매번 이 저장소에서 패키지를 받아 실행하므로 로컬에 clone하거나 경로를 맞출 필요가 없다. 각자 자기 Padlet API 키만 위 방법으로 설정하면 된다.

## 로컬 개발

```
uv sync
uv run padlet-mcp
```
