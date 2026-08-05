# Install and run

## Local install

```bash
python -m venv .venv
. .venv/bin/activate          # Windows: .venv\\Scripts\\Activate.ps1
python -m pip install -e .
```

## Codex or another stdio MCP client

Register `mcp.json`, or run:

```bash
pingpong-growth
```

The server exposes `growth_detect`, `growth_search`, `growth_design`, `growth_cross`, and `growth_update_check`.

## ChatGPT Developer Mode

ChatGPT requires a reachable HTTPS MCP endpoint. Start the server:

```bash
python -m pingpong_growth.server --transport streamable-http --host 0.0.0.0 --port 8000
```

Expose port 8000 through an HTTPS tunnel or deploy it behind a stable HTTPS host, then add the URL ending in `/mcp` as a ChatGPT app in Developer Mode. The example shape is in `chatgpt-app.example.json`. Refresh the app after changing tool definitions.

The server is offline by design: `growth_search` structures supplied conversation notes and does not claim to fetch social-network data.
