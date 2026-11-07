# Purpose: check the policy files parse and keep their key safety settings.
# Book: Coding Agents in the Enterprise, Chapter 5
# Licence: MIT (see LICENSE)
import json
import tomllib
from pathlib import Path

import yaml

POLICIES = Path(__file__).resolve().parent.parent / "policies"


def test_claude_managed_settings():
    s = json.loads((POLICIES / "claude-code" / "managed-settings.json").read_text())
    assert s["permissions"]["disableBypassPermissionsMode"] == "disable"
    assert "Read(./.env)" in s["permissions"]["deny"]
    assert s["allowManagedPermissionRulesOnly"] is True
    assert s["allowManagedMcpServersOnly"] is True
    assert all("serverUrl" in e for e in s["allowedMcpServers"])   # never by name
    hooks = s["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
    assert hooks.endswith("block_secrets_and_destructive.py")


def test_codex_files():
    config = tomllib.loads((POLICIES / "codex" / "config.toml").read_text())
    assert config["sandbox_mode"] == "workspace-write"
    assert config["approval_policy"] == "on-request"
    assert config["sandbox_workspace_write"]["network_access"] is False
    req = tomllib.loads((POLICIES / "codex" / "requirements.toml").read_text())
    assert "danger-full-access" not in req["allowed_sandbox_modes"]
    assert "never" not in req["allowed_approval_policies"]
    assert all(r["decision"] in {"prompt", "forbidden"} for r in req["rules"]["prefix_rules"])


def test_copilot_setup_steps_job_name():
    wf = yaml.safe_load((POLICIES / "copilot" / "copilot-setup-steps.yml").read_text())
    assert list(wf["jobs"]) == ["copilot-setup-steps"]
    allowed = {"steps", "permissions", "runs-on", "services", "snapshot", "timeout-minutes"}
    assert set(wf["jobs"]["copilot-setup-steps"]) <= allowed
    assert wf["jobs"]["copilot-setup-steps"]["timeout-minutes"] <= 59


def test_cursor_hooks():
    h = json.loads((POLICIES / "cursor" / "hooks.json").read_text())
    assert h["version"] == 1
    assert h["hooks"]["beforeShellExecution"][0]["failClosed"] is True
