#!/bin/bash
# SessionStart hook: prepares a Claude Code cloud session for MedLink PMG-2026
# (.NET 8 SDK, NuGet restore, Python deps for seed/report tooling). Idempotent, non-interactive.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

export DEBIAN_FRONTEND=noninteractive
export DOTNET_CLI_TELEMETRY_OPTOUT=1
export DOTNET_NOLOGO=1
export DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1

ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$ROOT"

# 1. .NET 8 SDK (Ubuntu 24.04 ships it in the main repo; builds.dotnet.microsoft.com is blocked by the proxy)
if ! dotnet --list-sdks 2>/dev/null | grep -q '^8\.'; then
  echo "[hook] Installing dotnet-sdk-8.0 via apt..."
  (sudo -n true 2>/dev/null && SUDO="sudo -n") || SUDO=""
  $SUDO apt-get update -qq
  $SUDO apt-get install -y -qq dotnet-sdk-8.0
fi
dotnet --list-sdks

# 2. NuGet restore for all projects (cached in container snapshot)
for proj in src/MedLink.Pmg.Module/MedLink.Pmg.Module.csproj src/MedLink.Pmg.Tests/MedLink.Pmg.Tests.csproj; do
  if [ -f "$proj" ]; then
    echo "[hook] dotnet restore $proj"
    dotnet restore "$proj" --verbosity quiet
  fi
done

# 3. Python tooling (seed builder, report inspection, TZ rendering)
python3 -m pip install -q --disable-pip-version-check openpyxl markdown requests 2>/dev/null || python3 -m pip install -q --break-system-packages openpyxl markdown requests

# 4. Session environment
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  {
    echo 'export DOTNET_CLI_TELEMETRY_OPTOUT=1'
    echo 'export DOTNET_NOLOGO=1'
    echo 'export PMG_API_URL="http://localhost:8085"'
  } >> "$CLAUDE_ENV_FILE"
fi

echo "[hook] MedLink PMG environment ready"
