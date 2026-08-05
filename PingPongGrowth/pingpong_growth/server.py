"""MCP server for the PingPongGrowth playbook.

The server is deliberately deterministic and offline: it does not pretend to
search social networks. Callers may pass conversation material to `search`,
then use the returned structure with `design` or `cross`.
"""

from __future__ import annotations

import argparse
import re
from datetime import date
from typing import Any

from mcp.server.fastmcp import FastMCP


PLATFORMS = {
    "X": {"aliases": ("x", "twitter"), "signal": "replies and thread depth", "hook": "question → counterpoint → short thread"},
    "Instagram": {"aliases": ("instagram", "reels", "ig"), "signal": "watch time and shares/saves", "hook": "visual tension in the first 3 seconds"},
    "YouTube": {"aliases": ("youtube", "shorts"), "signal": "CTR and watch time", "hook": "title/thumbnail promise versus conflict"},
    "Facebook": {"aliases": ("facebook", "fb"), "signal": "meaningful comments and shares", "hook": "direct question or poll"},
    "TikTok": {"aliases": ("tiktok", "douyin"), "signal": "first 3 seconds and completion", "hook": "instant visual or verbal tension"},
    "Xiaohongshu": {"aliases": ("xiaohongshu", "小红书", "rednote"), "signal": "cover and first 3 lines", "hook": "pain-point question first"},
    "WeChatChannels": {"aliases": ("视频号", "wechat channels", "channels"), "signal": "first 3 seconds and social recommendations", "hook": "3-second tension plus a social seed"},
    "OfficialAccount": {"aliases": ("公众号", "official account", "wechat article"), "signal": "completion and sharing", "hook": "debate-style title with a high-completion body"},
    "Bilibili": {"aliases": ("bilibili", "哔哩哔哩"), "signal": "series discovery and comments", "hook": "searchable title plus early comment trigger"},
    "LinkedIn": {"aliases": ("linkedin",), "signal": "comment engagement", "hook": "industry contradiction → insight"},
}


def _clean(value: str | None) -> str:
    return re.sub(r"\s+", " ", (value or "").strip())


def _platform_matches(text: str) -> list[str]:
    lowered = text.lower()
    matches = []
    for name, info in PLATFORMS.items():
        if any(alias.lower() in lowered for alias in info["aliases"]):
            matches.append(name)
    return matches


def _fallback_platforms(text: str) -> list[str]:
    return _platform_matches(text) or ["X", "Instagram", "YouTube", "TikTok"]


def _conversation_parts(conversations: str) -> dict[str, str]:
    lines = [_clean(line.lstrip("-•0123456789. ")) for line in conversations.splitlines() if _clean(line)]
    question = next((line for line in lines if "?" in line or "？" in line), lines[0] if lines else "大家真正想解决的是什么？")
    opposition = next((line for line in lines if line != question), "有人认为应该追热点，另一方认为应该只做长期价值")
    middle = "把真实分歧重写成可验证、可行动的共同解法"
    return {"question": question, "opposition": opposition, "middle_ground": middle}


def _hook(platform: str, parts: dict[str, str], cta: str | None = None) -> dict[str, str]:
    info = PLATFORMS[platform]
    call_to_action = _clean(cta) or "你站哪一边？把你的经历补充进下一轮对话。"
    return {
        "platform": platform,
        "question": parts["question"],
        "opposition": parts["opposition"],
        "fused_insight": parts["middle_ground"],
        "hook": f"{parts['question']} {parts['opposition']} 但真正可行的解法是：{parts['middle_ground']}。",
        "cta": call_to_action,
        "number_one_signal": info["signal"],
        "packaging": info["hook"],
        "originality_label": "融合自对话结构",
    }


def create_server(host: str = "127.0.0.1", port: int = 8000) -> FastMCP:
    mcp = FastMCP(
        "pingpong-growth",
        instructions="Use this when turning supplied conversation material into original, platform-native social hooks. The server is offline and does not fetch social networks.",
        host=host,
        port=port,
        streamable_http_path="/mcp",
        stateless_http=True,
    )

    @mcp.tool()
    def growth_detect(text: str) -> dict[str, Any]:
        """Use this when you need to identify target platforms from a topic or brief."""
        platforms = _platform_matches(_clean(text))
        return {"platforms": platforms or _fallback_platforms(text), "matched_explicitly": bool(platforms)}

    @mcp.tool()
    def growth_search(niche: str, conversations: str = "", days: int = 14) -> dict[str, Any]:
        """Use this when you have conversation notes and need a structured Q/O/M input for hook design."""
        if not 1 <= days <= 90:
            raise ValueError("days must be between 1 and 90")
        source = _clean(conversations)
        parts = _conversation_parts(source or niche)
        return {"niche": _clean(niche), "days": days, "source_mode": "supplied_conversations" if source else "seeded_structure", "structure": parts, "next_step": "Pass structure fields to growth_design or growth_cross."}

    @mcp.tool()
    def growth_design(platform: str, question: str, opposition: str, middle_ground: str, cta: str = "") -> dict[str, Any]:
        """Use this when you need one original platform-native hook from a Q/O/M structure."""
        canonical = next((name for name in PLATFORMS if name.lower() == platform.lower()), None)
        if not canonical:
            raise ValueError(f"Unsupported platform: {platform}. Use growth_detect first.")
        parts = {"question": _clean(question), "opposition": _clean(opposition), "middle_ground": _clean(middle_ground)}
        if not all(parts.values()):
            raise ValueError("question, opposition, and middle_ground are required")
        return _hook(canonical, parts, cta)

    @mcp.tool()
    def growth_cross(niche: str, platforms: list[str], conversations: str = "") -> dict[str, Any]:
        """Use this when you need the same conversation insight packaged for several platforms."""
        parts = _conversation_parts(_clean(conversations) or _clean(niche))
        unknown = [item for item in platforms if not any(name.lower() == item.lower() for name in PLATFORMS)]
        if unknown:
            raise ValueError(f"Unsupported platforms: {', '.join(unknown)}")
        results = [_hook(next(name for name in PLATFORMS if name.lower() == item.lower()), parts) for item in platforms]
        return {"niche": _clean(niche), "structure": parts, "results": results}

    @mcp.tool()
    def growth_update_check() -> dict[str, str]:
        """Use this when you need the scheduled reminder to review platform signals."""
        return {"recommended_review": "6 months after the last platforms.md update", "checked_on": date.today().isoformat()}

    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the PingPongGrowth MCP server")
    parser.add_argument("--transport", choices=("stdio", "streamable-http"), default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    create_server(args.host, args.port).run(transport=args.transport)


if __name__ == "__main__":
    main()
