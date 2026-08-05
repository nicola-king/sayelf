# Intelligent Ping-Pong Hook Generation Algorithm

## Input
- Niche / topic
- Raw conversation data (from search): questions, objections, emotional triggers, missing middle ground
- Target platform

## Algorithm Steps

1. **Extract Core Tension**
   - Identify the single strongest contradiction or repeated question in the data.
   - Score by frequency + emotional intensity.

2. **Build Dialogue Triple**
   - Q  = highest-frequency user question
   - O  = strongest opposing / common reply
   - M  = missing middle ground or under-served insight (this becomes the fused value)

3. **Generate Hook Skeleton**
   ```
   [Q as open] → [O as tension] → [M as resolution] → [Platform CTA]
   ```

4. **Platform Packaging Rules**
   - X / Twitter:        keep under 280 chars per tweet, prefer 3-tweet thread
   - Instagram Reels:    force first 3 seconds = Q + visual tension
   - YouTube Shorts:     first 1–2 seconds = Q, title = Q + promise of M
   - TikTok / 抖音:      first 3 seconds = Q, total 15–45s
   - 视频号:             first 3 seconds = Q, end with social seed CTA
   - 公众号:             title = Q or number+Q, body expands O→M with high completion structure
   - 小红书:             cover + first 3 lines = Q, body = practical M
   - Others:             map to nearest length / format constraint

5. **Originality Check**
   - Reject any sentence that appears verbatim in source data.
   - Force at least one re-phrased insight in the M section.

6. **Output**
   - 3–5 variations of the same skeleton
   - One fully written example ready to post
   - Explicit label: “融合自对话结构”

## Scoring for Best Hook
Priority order:
1. Early retention signal (first 1–3 seconds / first line)
2. Clear tension (Q vs O)
3. Unique fused value (M)
4. Platform-native CTA strength
