---
name: pingpong-growth
description: Modular intelligent playbook for cross-platform follower growth. Auto-detects platform, searches real conversations, designs ping-pong hooks and fuses trends into platform-native structures. Supports X, Instagram, YouTube, Facebook, TikTok, Xiaohongshu, 视频号, 公众号, Bilibili, LinkedIn. CLI and MCP ready for Codex, Claude, OpenClaw and other agents. Update every 6 months. Triggers include 涨粉, 蹭热点, 乒乓钩子, cross-platform, 视频号, 公众号, grow followers.
---

# Social Media Growth Playbook

## Runtime

This skill ships with a real MCP server in `pingpong_growth/server.py`. Install it with `python -m pip install -e .`; use stdio for Codex and local clients, or Streamable HTTP at `/mcp` for ChatGPT Developer Mode. The server is deterministic and offline: pass conversation notes into `growth_search` instead of implying that it fetches social networks.

## Goal
Automate “蹭热点但不照抄”: search real ping-pong conversations → design platform-native hooks → output ready structures. Modular, low-entropy, CLI/MCP compatible.

## Core Workflow (4 steps, always follow)

1. **Detect**  
   Map user input to one or more platforms. Cross-platform = parallel generation.

2. **Search**  
   Use tools to pull last 7–30 days conversations. Extract:  
   - Common questions  
   - Typical objections / replies  
   - Emotional triggers  
   - Missing middle ground  

3. **Design**  
   Build ping-pong hooks + content templates per platform rules.  
   Never copy surface text. Always rebuild as dialogue flow.

4. **Output**  
   Structured result + #1 ranking signal reminder.  
   Offer performance refinement after 7–14 days.

## Cross-Platform Hook Pattern (universal)

```
[Trigger Question / Contradiction]
→ [Opposing View or Tension]
→ [Fused Insight as Resolution]
→ [Platform-Native CTA that invites next ping]
```

Adapt only the packaging (length, visual, CTA type). Core insight stays constant.

## Platform Algorithm Snapshot

Load full details from `references/platforms.md` when needed. Quick reference:

| Platform   | #1 Signal                  | Hook Focus                  |
|------------|----------------------------|-----------------------------|
| X          | First-30-min replies + threads | Question → counter → thread |
| Instagram  | Watch time (1.7–3s) + shares/saves | Visual tension in first 3s |
| YouTube    | CTR + watch time           | Title/thumbnail promise conflict |
| Facebook   | Meaningful comments/shares | Direct question / poll     |
| TikTok     | First 3s + completion      | Instant visual/verbal tension |
| 小红书     | Cover + first 3 lines      | Pain-point question first  |
| 视频号     | 前3秒 + 好友推荐 + ≥8字评论 | 3s tension + social seed   |
| 公众号     | 完读率 > 分享率            | Debate-style title + high-completion body |
| Bilibili   | Series + 弹幕              | Searchable + early 弹幕 trigger |
| LinkedIn   | Comment engagement         | Industry contradiction → insight |

## Modular Resources
- `references/platforms.md` — full ranking rules, limits, prompt fragments
- `references/hooks.md` — ping-pong patterns + cross-platform examples
- `references/hook-algorithm.md` — intelligent hook generation algorithm
- `scripts/` — CLI helpers (see below)

## CLI / MCP Interface (for Codex, Claude, OpenClaw, GitHub)

Expose as simple commands or MCP tools:

```
growth detect <text>          → return platform list
growth search <niche> [--days 14] → return conversation structures
growth design <platform> <structure> → return hooks + templates
growth cross <niche> <platforms...> → parallel designs
growth update-check           → remind half-year review
```

Implementation notes:
- Keep each function pure and under 50 lines.
- Input/output as JSON for easy agent chaining.
- Publish the whole skill directory to GitHub; other agents can load SKILL.md + references on demand.

## Agent Rules
- Search first unless user locks a topic and says “no search”.
- Label every design “融合自对话结构” so non-copy is visible.
- End with platform #1 signal.
- Every 6 months: re-validate signals in `references/platforms.md` and bump version.

## Entropy Rule
Main SKILL.md stays <150 lines.  
Platform details and examples live in references/.  
Scripts stay tiny and single-purpose.
