import logging
import os
from pathlib import Path

import httpx
from mcp.server.fastmcp import FastMCP

logging.getLogger("httpx").setLevel(logging.WARNING)

API_BASE = "https://api.padlet.dev/v1"
DEFAULT_KEY_FILE = Path.home() / ".secrets" / "padlet_api_key.txt"


def _load_api_key() -> str:
    key = os.environ.get("PADLET_API_KEY")
    if key:
        return key.strip()
    key_file = Path(os.environ.get("PADLET_API_KEY_FILE", DEFAULT_KEY_FILE))
    if key_file.exists():
        return key_file.read_text(encoding="utf-8").strip()
    raise RuntimeError(
        f"Padlet API 키를 찾을 수 없습니다. PADLET_API_KEY 환경변수를 설정하거나 "
        f"{key_file} 파일에 키를 저장하세요."
    )


API_KEY = _load_api_key()

mcp = FastMCP("padlet")


def _get(path: str, params: dict | None = None) -> dict:
    resp = httpx.get(
        f"{API_BASE}{path}",
        headers={"x-api-key": API_KEY},
        params=params,
        timeout=30,
    )
    if resp.status_code >= 400:
        raise RuntimeError(f"Padlet API 오류 {resp.status_code}: {resp.text}")
    return resp.json()


def _index_included(included: list[dict] | None) -> dict:
    return {(item["type"], item["id"]): item for item in included or []}


@mcp.tool()
def list_boards() -> list[dict]:
    """현재 API 키로 접근 가능한 보드(Padlet) 목록을 반환한다.

    각 보드의 id(get_board에 쓰는 16자리 식별자), 제목, 공개 URL을 담는다.
    padlet.com URL만 알고 있을 때는 이 목록에서 web_url을 비교해 board_id를 찾는다.
    """
    data = _get("/me", params={"include": "boards"})
    index = _index_included(data.get("included"))
    boards = []
    for ref in data["data"]["relationships"].get("boards", {}).get("data", []):
        board = index.get(("board", ref["id"]))
        if not board:
            continue
        attrs = board.get("attributes", {})
        boards.append(
            {
                "id": board["id"],
                "title": attrs.get("title"),
                "description": attrs.get("description"),
                "web_url": (attrs.get("webUrl") or {}).get("live"),
            }
        )
    return boards


@mcp.tool()
def get_board(board_id: str) -> dict:
    """보드 하나의 섹션·게시물·댓글을 모두 가져와 정리된 형태로 반환한다.

    board_id는 list_boards로 얻은 16자리 보드 ID다 (padlet.com URL의 슬러그가 아님).
    """
    data = _get(f"/boards/{board_id}", params={"include": "posts,sections,comments"})
    index = _index_included(data.get("included"))
    board = data["data"]
    attrs = board.get("attributes", {})

    def resolve(ref):
        return index.get((ref["type"], ref["id"])) if ref else None

    section_titles = {}
    for ref in board["relationships"].get("sections", {}).get("data", []):
        section = resolve(ref)
        if section:
            section_titles[section["id"]] = section["attributes"].get("title")

    posts = []
    for ref in board["relationships"].get("posts", {}).get("data", []):
        post = resolve(ref)
        if not post:
            continue
        pattrs = post["attributes"]
        content = pattrs.get("content", {})
        section_ref = post.get("relationships", {}).get("section", {}).get("data")
        posts.append(
            {
                "id": post["id"],
                "author": (pattrs.get("author") or {}).get("fullName"),
                "section": section_titles.get(section_ref["id"]) if section_ref else None,
                "subject": content.get("subject"),
                "body_html": content.get("bodyHtml"),
                "attachment_url": (content.get("attachment") or {}).get("url"),
                "created_at": pattrs.get("createdAt"),
            }
        )

    comments = []
    for ref in board["relationships"].get("comments", {}).get("data", []):
        comment = resolve(ref)
        if comment:
            comments.append(comment["attributes"])

    return {
        "id": board["id"],
        "title": attrs.get("title"),
        "description": attrs.get("description"),
        "sections": list(section_titles.values()),
        "posts": posts,
        "comments": comments,
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
