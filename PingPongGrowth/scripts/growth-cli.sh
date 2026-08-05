#!/usr/bin/env bash
# CLI adapter for the installable PingPongGrowth package.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."
exec python -m pingpong_growth.cli "$@"
