"""Command-line adapter over the same functions exposed by the MCP server."""

from __future__ import annotations

import argparse
import json

from .server import _conversation_parts, _fallback_platforms, _hook, _platform_matches, PLATFORMS


def main() -> None:
    parser = argparse.ArgumentParser(prog="pingpong-growth")
    commands = parser.add_subparsers(dest="command", required=True)

    detect = commands.add_parser("detect")
    detect.add_argument("text", nargs="+")

    search = commands.add_parser("search")
    search.add_argument("niche")
    search.add_argument("--conversations", default="")
    search.add_argument("--days", type=int, default=14)

    design = commands.add_parser("design")
    design.add_argument("platform")
    design.add_argument("question")
    design.add_argument("opposition")
    design.add_argument("middle_ground")
    design.add_argument("--cta", default="")

    cross = commands.add_parser("cross")
    cross.add_argument("niche")
    cross.add_argument("platforms", nargs="+")
    cross.add_argument("--conversations", default="")

    commands.add_parser("update-check")
    args = parser.parse_args()

    if args.command == "detect":
        explicit = _platform_matches(" ".join(args.text))
        result = {"platforms": explicit or _fallback_platforms(" ".join(args.text)), "matched_explicitly": bool(explicit)}
    elif args.command == "search":
        if not 1 <= args.days <= 90:
            parser.error("--days must be between 1 and 90")
        source = args.conversations.strip()
        result = {"niche": args.niche.strip(), "days": args.days, "source_mode": "supplied_conversations" if source else "seeded_structure", "structure": _conversation_parts(source or args.niche), "next_step": "Pass structure fields to design or cross."}
    elif args.command == "design":
        canonical = next((name for name in PLATFORMS if name.lower() == args.platform.lower()), None)
        if not canonical:
            parser.error(f"unsupported platform: {args.platform}")
        result = _hook(canonical, {"question": args.question.strip(), "opposition": args.opposition.strip(), "middle_ground": args.middle_ground.strip()}, args.cta)
    elif args.command == "cross":
        unknown = [item for item in args.platforms if not any(name.lower() == item.lower() for name in PLATFORMS)]
        if unknown:
            parser.error(f"unsupported platforms: {', '.join(unknown)}")
        parts = _conversation_parts(args.conversations.strip() or args.niche)
        result = {"niche": args.niche.strip(), "structure": parts, "results": [_hook(next(name for name in PLATFORMS if name.lower() == item.lower()), parts) for item in args.platforms]}
    else:
        from datetime import date
        result = {"recommended_review": "6 months after the last platforms.md update", "checked_on": date.today().isoformat()}

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
