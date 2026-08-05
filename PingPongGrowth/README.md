<div align="center">

# PingPongGrowth

**蹭热点不照抄 · 一键生成平台原生钩子**  
**Trend Fusion without Copying · Auto-generate Platform-Native Hooks**

</div>

---

### 中文简介
把「人们真正在聊什么」自动变成 X、Instagram、视频号、公众号、TikTok、小红书等平台的可直接发内容。  
核心算法：**乒乓对话钩子** = 提问 → 对立 → 融合解决 → 平台原生 CTA。

### English Intro
Automatically turns real conversations into ready-to-post content for X, Instagram, YouTube, TikTok, WeChat Channels, Official Accounts and more.  
Core algorithm: **Ping-Pong Hooks** = Question → Opposition → Fused Insight → Platform-Native CTA.

---

## 它解决什么 / What It Solves

| 痛点 | 解决方案 |
|------|----------|
| 追热点却同质化被限流 | 提取真实对话结构，重新融合设计 |
| 多平台内容重复造轮子 | 跨平台一键生成适配版本 |
| 不懂各平台算法信号 | 内置 2026 排名机制与钩子规则 |
| 人工效率低 | 智能搜索 + 自动钩子生成全流程 |

---

## 核心能力 / Core Capabilities

```
1. 智能平台识别        Auto platform detection (single / cross)
2. 实时对话挖掘        Real conversation mining (not surface trends)
3. 乒乓钩子生成算法    Intelligent ping-pong hook algorithm
4. 平台规则引擎        Built-in ranking signals & limits
5. MCP / CLI 就绪      Ready for Codex · Claude · OpenClaw
```

---

## 钩子生成算法 / Hook Generation Algorithm

```
Input:  niche + raw conversations + target platform
   ↓
1. Extract strongest tension (Q vs O)
2. Find missing middle ground (M)
3. Build skeleton:  Q → O → M → CTA
4. Package by platform rules (length / first-3s / title…)
5. Originality check (no verbatim copy)
   ↓
Output: 3–5 variations + 1 ready-to-post example
```

完整算法见 `references/hook-algorithm.md`

---

## 4步工作流 / 4-Step Workflow

```
检测平台  →  搜索真实对话  →  设计乒乓钩子  →  输出可发内容
Detect   →  Search Real Talk → Design Hooks → Ready Content
```

---

## 支持平台 / Supported Platforms

`X` · `Instagram` · `YouTube` · `Facebook` · `TikTok`  
`小红书` · `视频号` · `公众号` · `Bilibili` · `LinkedIn`

---

## MCP / CLI

```bash
./scripts/growth-cli.sh detect  "帮我做视频号涨粉"
./scripts/growth-cli.sh search  "美妆" --days 14
./scripts/growth-cli.sh design  视频号 <structure>
./scripts/growth-cli.sh cross   "职场" 视频号 公众号 Instagram
```

可作为 MCP 工具暴露：`growth_detect` · `growth_search` · `growth_design` · `growth_cross`

---

## 设计原则

- 主文件 <100 行（负熵）
- 算法与平台规则模块化
- 每半年只更新 `references/` 即可

---

<div align="center">

**PingPongGrowth**  
不抄热点，只融合对话  
Fuse the conversation, never copy the trend

</div>
